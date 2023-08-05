# Copyright 2018, Radware LTD. All rights reserved
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from threading import Thread

from oslo_log import log as logging

from octavia.api.drivers import exceptions
from octavia.api.drivers import provider_base as driver_base

import config
import dm_utils
import feedback
import radware_provider_exceptions
import vdirect_adc_wf_driver

LOG = logging.getLogger(__name__)

AGENT_PROCESS_STARTED = False

def exception_transformator(f):
    def transformator(*args, **kwargs):
        try:
            r = f(*args, **kwargs)
        except vdirect_adc_wf_driver.VDirectADCWorkflowDriverException as e:
            if isinstance(e, vdirect_adc_wf_driver.ConfigurationConflict):
                raise radware_provider_exceptions.ConfigurationConflict(
                conflict_description=e.conflict_description)
            elif isinstance(e, vdirect_adc_wf_driver.RESTRequestFailure):
                raise radware_provider_exceptions.RESTRequestFailure(
                    status=e.status, reason=e.reason,
                    description=e.description, success_codes=e.success_codes)
            elif isinstance(e, vdirect_adc_wf_driver.WorkflowTemplateMissing):
                raise radware_provider_exceptions.WorkflowTemplateMissing(
                    workflow_template=e.template_name)
        return r
    return transformator


class RadwareOctaviaProviderDriver(driver_base.ProviderDriver):
    @exception_transformator
    def __init__(self, **kwargs):

        super(RadwareOctaviaProviderDriver, self).__init__()

        self.service_consumer = 'Octavia'
        self.config = config.RadwareConfFileConfig(
            '/etc/radware/octavia_driver.conf',
            kwargs.get('name'))

        self.wf_driver = vdirect_adc_wf_driver.VDirectADCWorkflowDriver(
            self.service_consumer, self.config)

        #if self.config.monitor_lb_status:
         #   self._start_monitoring_process ()

    def create_vip_port(self, loadbalancer_id, project_id, vip_dictionary):
        raise exceptions.NotImplementedError()

    def _start_monitoring_process (self):
        global AGENT_PROCESS_STARTED
        if not AGENT_PROCESS_STARTED:
            RadwareOctaviaProviderDriver._start_monitoring_process(self.wf_driver)
            AGENT_PROCESS_STARTED = True

    @exception_transformator
    def _create_lb(self, lb):
        params = {'network_id': lb.vip.network_id}

        result = self.wf_driver.create_lb_workflow(lb.id, params, lb.project_id)
        t = Thread(target=feedback.post_lb_create, kwargs=dict(lb_id=lb.id, result=result))
        t.start()

    @exception_transformator
    def _configure_lb(self, dm, create=False, delete=False):
        lb_cdm, statuses, payload = dm_utils.get_lb_and_graph(dm, create=create, delete=delete)

        if not self.wf_driver.lb_workflow_exists(lb_cdm.id):
            self._create_lb(lb_cdm)

        deleted_id = None if not delete else dm_utils.get_pdm_id(dm)
        params = payload

        result = self.wf_driver.apply_lb_workflow(lb_cdm.id, params)
        t = Thread(target=feedback.post_lb_configure,
                   kwargs=dict(deleted_id=deleted_id, statuses=statuses, result=result))
        t.start()

    def loadbalancer_create(self, lb_provider_dm):
        lb_cdm, statuses, payload = dm_utils.get_lb_and_graph(lb_provider_dm, create=True)
        self._create_lb(lb_cdm)

    def loadbalancer_update(self, old_loadbalancer_provider_dm,
                            loadbalancer_provider_dm):
        raise exceptions.UnsupportedOptionError(
            user_fault_string='Loadbalancer update operation'
                              'is not supported as for now as a result of Octavia bug.'
                              '(https://review.openstack.org/#/c/605376)',
            operator_fault_string='Loadbalancer update operation'
                              'is not supported as for now because the following '
                                  'https://review.openstack.org/#/c/605376.')

        merged = dm_utils.merge_updated(old_loadbalancer_provider_dm, loadbalancer_provider_dm)
        self._configure_lb(merged)

    def loadbalancer_delete(self, lb_provider_dm, cascade):
        result = self.wf_driver.remove_lb_workflow(lb_provider_dm.loadbalancer_id)
        t = Thread(target=feedback.post_lb_delete,
                   kwargs=dict(lb_id=lb_provider_dm.loadbalancer_id, result=result))
        t.start()

    def loadbalancer_failover(self, loadbalancer_id):
        raise exceptions.NotImplementedError()

    @exception_transformator
    def listener_create(self, listener_provider_dm):
        self.wf_driver.validate_listener(
            listener_provider_dm.protocol,
            listener_provider_dm.protocol_port)
        self._configure_lb(listener_provider_dm, create=True)

    def listener_update(self, old_listener_provider_dm,
                        listener_provider_dm):
        merged = dm_utils.merge_updated(old_listener_provider_dm, listener_provider_dm)
        self._configure_lb(merged)

    def listener_delete(self, listener_provider_dm):
        self._configure_lb(listener_provider_dm, delete=True)

    def pool_create(self, pool_provider_dm):
        self._configure_lb(pool_provider_dm, create=True)

    def pool_update(self, old_pool_provider_dm,
                    pool_provider_dm):
        merged = dm_utils.merge_updated(old_pool_provider_dm, pool_provider_dm)
        self._configure_lb(merged)

    def pool_delete(self, pool_provider_dm):
        self._configure_lb(pool_provider_dm, delete=True)

    def member_create(self, member_provider_dm):
        self._configure_lb(member_provider_dm, create=True)

    def member_update(self, old_member_provider_dm,
                      member_provider_dm):
        merged = dm_utils.merge_updated(old_member_provider_dm, member_provider_dm)
        self._configure_lb(merged)

    def member_delete(self, member_provider_dm):
        self._configure_lb(member_provider_dm, delete=True)

    def member_batch_update(self, members):
        raise exceptions.NotImplementedError()

    def health_monitor_create(self, hm_provider_dm):
        self._configure_lb(hm_provider_dm, create=True)

    def health_monitor_update(self, old_hm_provider_dm,
                              hm_provider_dm):
        merged = dm_utils.merge_updated(old_hm_provider_dm, hm_provider_dm)
        self._configure_lb(merged)

    def health_monitor_delete(self, hm_provider_dm):
        self._configure_lb(hm_provider_dm, delete=True)

    def l7policy_create(self, l7policy_provider_dm):
        self._configure_lb(l7policy_provider_dm, create=True)

    def l7policy_update(self, old_l7policy_provider_dm,
                        l7policy_provider_dm):
        merged = dm_utils.merge_updated(old_l7policy_provider_dm, l7policy_provider_dm)
        self._configure_lb(merged)

    def l7policy_delete(self, l7policy_provider_dm):
        self._configure_lb(l7policy_provider_dm, delete=True)

    def l7rule_create(self, l7rule_provider_dm):
        self._configure_lb(l7rule_provider_dm, create=True)

    def l7rule_update(self, old_l7rule_provider_dm,
                      l7rule_provider_dm):
        merged = dm_utils.merge_updated(old_l7rule_provider_dm, l7rule_provider_dm)
        self._configure_lb(merged)

    def l7rule_delete(self, l7rule_provider_dm):
        self._configure_lb(l7rule_provider_dm, delete=True)
