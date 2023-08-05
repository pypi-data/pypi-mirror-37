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

from oslo_log import log as logging

from octavia.api.drivers import driver_lib
from octavia.common import constants

LOG = logging.getLogger(__name__)


def _report_status(status):
    LOG.debug("Updating statuses:" + repr(status))
    driver_lib.DriverLibrary().update_loadbalancer_status(status)


def post_lb_create(**kwargs):
    result = kwargs.get('result')
    lb_id = kwargs.get('lb_id')
    status_dict = {constants.LOADBALANCERS: [{'id': lb_id}]}

    if result[3]['success']:
        status_dict[constants.LOADBALANCERS][0][constants.PROVISIONING_STATUS] = constants.ACTIVE
        status_dict[constants.LOADBALANCERS][0][constants.OPERATING_STATUS] = constants.ONLINE
    else:
        status_dict[constants.LOADBALANCERS][0][constants.PROVISIONING_STATUS] = constants.ERROR
        status_dict[constants.LOADBALANCERS][0][constants.OPERATING_STATUS] = constants.ERROR
    _report_status(status_dict)


def post_lb_configure(**kwargs):
    deleted_id = kwargs.get('deleted_id')
    status_dict = kwargs.get('statuses')
    result = kwargs.get('result')
    success = result[3]['success']

    for type, objects in status_dict.items():
        for object in objects:
            if success:
                if deleted_id and object['id'] == deleted_id:
                    object[constants.PROVISIONING_STATUS] = constants.DELETED
                else:
                    object[constants.PROVISIONING_STATUS] = constants.ACTIVE
                    object[constants.OPERATING_STATUS] = constants.ONLINE
            else:
                object[constants.PROVISIONING_STATUS] = constants.ERROR
                object[constants.OPERATING_STATUS] = constants.ERROR
    _report_status(status_dict)


def post_lb_delete(**kwargs):
    result = kwargs.get('result')
    lb_id = kwargs.get('lb_id')

    status_dict = {constants.LOADBALANCERS: [{'id': lb_id}]}

    if result[3]['success']:
        status_dict[constants.LOADBALANCERS][0][constants.PROVISIONING_STATUS] = constants.DELETED
    else:
        status_dict[constants.LOADBALANCERS][0][constants.PROVISIONING_STATUS] = constants.ERROR
        status_dict[constants.LOADBALANCERS][0][constants.OPERATING_STATUS] = constants.ERROR
    _report_status(status_dict)


def update_operating_status(**kwargs):
    #TODO
    pass

def update_statistics(**kwargs):
    #TODO
    pass
