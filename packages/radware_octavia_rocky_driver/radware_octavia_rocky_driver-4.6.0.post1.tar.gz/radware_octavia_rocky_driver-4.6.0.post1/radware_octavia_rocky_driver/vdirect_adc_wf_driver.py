# Copyright 2018 Radware LTD. All rights reserved
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

import copy

import config as rad_config
import vdirect_client


# Alteon strict application type port numbers
# with automatic protocol selection
ALTEON_STRICT_APPLICATION_TYPE_PORTS_LIST_AUTO_PROTOCOL = [
    20, 21, 22, 23, 25, 43, 69, 79,
    109, 110, 161, 179, 194, 554, 1985
]

# Alteon strict application type port numbers
# with possible (tcp/udp/stateless) protocol selection
ALTEON_STRICT_APPLICATION_TYPE_PORTS_LIST_VARIOUS_PROTOCOL = [
    37, 42, 53, 119, 123, 143, 144, 162,
    389, 520, 1812, 1813, 5060
]

# Alteon strict application type port numbers
ALTEON_STRICT_APPLICATION_PORTS_LIST = \
    ALTEON_STRICT_APPLICATION_TYPE_PORTS_LIST_AUTO_PROTOCOL + \
    ALTEON_STRICT_APPLICATION_TYPE_PORTS_LIST_VARIOUS_PROTOCOL

# Alteon encrypted application type (https/ssl)
# with automatic protocol selection
ALTEON_HTTP_PORT = 80

# Alteon encrypted application type (https/ssl)
# with automatic protocol selection
ALTEON_ENCRYPTED_PORT = 443

WORKFLOW_TEMPLATE_RUNNABLE_TYPE = 'WorkflowTemplate'
WORKFLOW_RUNNABLE_TYPE = 'Workflow'
CREATE_WORKFLOW_ACTION = 'createWorkflow'
DELETE_WORKFLOW_ACTION = 'deleteWorkflow'


class VDirectADCWorkflowDriverException(Exception):
    def __init__(self, message):
        self.message = message


class ConfigurationMissing(VDirectADCWorkflowDriverException):
    def __init__(self):
        message = "Driver configuration missing. "
        super(ConfigurationMissing, self).__init__(message)


class ConfigurationSectionMissing(VDirectADCWorkflowDriverException):
    def __init__(self, section):
        self.section = section
        message = 'Driver configuration section ' + repr(section) + ' is missing.'
        super(ConfigurationSectionMissing, self).__init__(message)


class ConfigurationReadFailure(VDirectADCWorkflowDriverException):
    def __init__(self, reason):
        self.reason = reason
        message = 'Failed to read driver configuration. Reason:' + repr(reason)
        super(ConfigurationReadFailure, self).__init__(message)


class WorkflowTemplateMissing(VDirectADCWorkflowDriverException):
    def __init__(self, template_name):
        self.template_name = template_name
        message = "vDirect Workflow template %s is missing " \
                  "on vDirect server. Upload missing workflow."\
                  % template_name

        super(WorkflowTemplateMissing, self).__init__(message)


class ConfigurationConflict(VDirectADCWorkflowDriverException):
    def __init__(self, conflict_description):
        self.conflict_description = conflict_description
        message = "Unable to satisfy the request " \
                  "due to load balancer configuration conflict. " \
                  "Conflict description: %s."\
                  % conflict_description

        super(ConfigurationConflict, self).__init__(message)


class RESTRequestFailure(VDirectADCWorkflowDriverException):
    def __init__(self, status, reason, description, success_codes=None):
        self.status = status
        self.reason = reason
        self.description = description
        self.success_codes = success_codes
        message = "REST request failed with status %(status)s. " \
                  "Reason: %(reason)s, Description: %(description)s. " \
                  "Success status codes are %(success_codes)s"\
                  % (status, reason, description, success_codes)

        super(RESTRequestFailure, self).__init__(message)


def exception_transformator(f):
    def transformator(*args, **kwargs):
        try:
            r = f(*args, **kwargs)
        except vdirect_client.RestClientException as e:
            raise RESTRequestFailure(
                e.status_code, e.failure_reason, e.failure_msg)
        except Exception as e:
            raise RESTRequestFailure(
                None, None, e.failure_msg)
        return r
    return transformator


class VDirectADCWorkflowDriver():
    def __init__(self, service_consumer, config):

        if not config or not isinstance(config, rad_config.RadwareConfig):
            raise ConfigurationMissing()

        self.service_consumer = service_consumer
        self.config = config

        self.service = {
            "name": "_REPLACE_",
            "haPair": self.config.service_ha_pair,
            "sessionMirroringEnabled": self.config.service_session_mirroring_enabled,
            "primary": {
                "capacity": {
                    "throughput": self.config.service_throughput,
                    "sslThroughput": self.config.service_ssl_throughput,
                    "compressionThroughput":
                    self.config.service_compression_throughput,
                    "cache": self.config.service_cache
                },
                "network": {
                    "type": "portgroup",
                    "portgroups": '_REPLACE_'
                },
                "adcType": self.config.service_adc_type,
                "acceptableAdc": "Exact"
            }
        }
        if self.config.service_resource_pool_ids:
            ids = self.config.service_resource_pool_ids
            self.service['resourcePoolIds'] = [
                {'id': id} for id in ids
            ]
        else:
            self.service['resourcePoolIds'] = []

        if self.config.service_isl_vlan:
            self.service['islVlan'] = self.config.service_isl_vlan
        self.lb_create_payload = self.config.lb_create_payload
        self.configure_action_name = self.config.configure_action_name

        self.vdirect_client = vdirect_client.RestClient(
            self.config.vdirect_ip,
            self.config.vdirect_user,
            self.config.vdirect_password,
            secondary_vdirect_ip=self.config.vdirect_secondary_ip,
            https_port=self.config.vdirect_https_port,
            http_port=self.config.vdirect_http_port,
            timeout=self.config.timeout,
            https=self.config.use_https,
            verify=self.config.ssl_verify_context)

        self._verify_workflow_templates()

    @exception_transformator
    def _verify_workflow_templates(self):
        if not self.config.workflow_template_names:
            pass
        response = self.vdirect_client.runnable.get_runnable_objects(WORKFLOW_TEMPLATE_RUNNABLE_TYPE)
        if 'names' not in response[vdirect_client.RESP_DATA]:
            raise WorkflowTemplateMissing(self.config.workflow_template_names[0])

        template_names = response[vdirect_client.RESP_DATA]['names']
        for required_template in self.config.workflow_template_names:
            if required_template not in template_names:
                raise WorkflowTemplateMissing(required_template)

    def _lb_wf_name(self, lb_id):
        return self._consumer_wf_prefix() + lb_id

    def _consumer_wf_prefix(self):
        return self.service_consumer + '_LB-'

    def _wf_lb_id(self, wf_name):
        return wf_name.split(self.service_consumer + '_LB-')[1]

    @exception_transformator
    def get_existing_lb_workflows(self):
        response = self.vdirect_client.runnable.get_runnable_objects('Workflow')

        names_list = []
        prefix = self._consumer_wf_prefix()
        if 'names' not in response[vdirect_client.RESP_DATA]:
            return names_list
        for name in response[vdirect_client.RESP_DATA]['names']:
            if name.startswith(prefix):
                names_list.append(name)
        return names_list

    @exception_transformator
    def lb_workflow_exists(self, lb_id):
        response = self.vdirect_client.runnable.get_runnable_objects(WORKFLOW_RUNNABLE_TYPE)
        if 'names' not in response[vdirect_client.RESP_DATA]:
            return False
        workflow_names = response[vdirect_client.RESP_DATA]['names']
        return self._lb_wf_name(lb_id) in workflow_names

    @exception_transformator
    def create_lb_workflow(self, lb_id, params, tenant_id=None, feedback=None, feedback_kwargs=None):

        if tenant_id:
            self.vdirect_client.tenant.create(
                {'name': tenant_id,
                 'description': 'Openstack tenant. Created by Openstack Octavia driver.'})

        network_id = params.pop('network_id')
        wf_name = self._lb_wf_name(lb_id)
        service = copy.deepcopy(self.service)
        service['name'] = 'srv_' + network_id
        if tenant_id:
            service['tenantId'] = tenant_id

        if self.config.force_one_leg:
            self.lb_create_payload["twoleg_enabled"] = False
            service['primary']['network']['portgroups'] = [network_id]

        tenants = [tenant_id] if tenant_id else []
        parameters = dict(self.lb_create_payload, service_params=service,
                          workflowName=wf_name,
                          __tenants=tenants)

        result = self.vdirect_client.runnable.run(
            parameters, WORKFLOW_TEMPLATE_RUNNABLE_TYPE,
            self.config.lb_workflow_template_name,
            CREATE_WORKFLOW_ACTION)
        if feedback:
            if feedback_kwargs:
                feedback(**dict(feedback_kwargs, result=result))
            else:
                feedback(**dict(result=result))
        return result

    @exception_transformator
    def apply_lb_workflow(self, lb_id, params, feedback=None, feedback_kwargs=None):
        wf_name = self._lb_wf_name(lb_id)

        result = self.vdirect_client.runnable.run(
            params, WORKFLOW_RUNNABLE_TYPE,
            wf_name, self.config.configure_action_name)
        if feedback:
            if feedback_kwargs:
                feedback(**dict(feedback_kwargs, result=result))
            else:
                feedback(**dict(result=result))
        return result

    @exception_transformator
    def remove_lb_workflow(self, lb_id, feedback=None, feedback_kwargs=None):
        wf_name = self._lb_wf_name(lb_id)

        if not self.lb_workflow_exists(lb_id):
            return None

        result = self.vdirect_client.runnable.run(
                {}, WORKFLOW_RUNNABLE_TYPE,
                wf_name, DELETE_WORKFLOW_ACTION)
        if feedback:
            if feedback_kwargs:
                feedback(**dict(feedback_kwargs, result=result))
            else:
                feedback(**dict(result=result))
        return result

    @exception_transformator
    def get_lb_operational_status (self, lb_id):
        pass

    @staticmethod
    def validate_listener(listener_protocol, listener_protocol_port):
        if listener_protocol not in ('TCP', 'UDP')\
                and listener_protocol_port in ALTEON_STRICT_APPLICATION_PORTS_LIST:
                raise ConfigurationConflict(
                    'Listener with %(protocol)s '
                    'protocol may not use '
                    'port %(port)s. This port is reserved for certain '
                    'application type and only may use '
                    'TCP or UDP protocols. '
                    'Following is a list of ports allowed for using '
                    'with TCP or UDP protocols only %(ports_list)s' %
                    {'protocol': listener_protocol,
                        'port': listener_protocol_port,
                        'ports_list': ALTEON_STRICT_APPLICATION_PORTS_LIST})

        if listener_protocol not in ('HTTPS', 'TCP', 'TERMINATED_HTTPS')\
                and listener_protocol_port == ALTEON_ENCRYPTED_PORT:
            raise ConfigurationConflict(
                'Listener with %(protocol)s '
                'protocol may not use '
                'port number %(port)s. This port number is reserved '
                'for TCP, HTTPS or TERMINATED_HTTPS protocols.' %
                {'protocol': listener_protocol, 'port': ALTEON_ENCRYPTED_PORT})

        if listener_protocol not in ('HTTP', 'TCP')\
                and listener_protocol_port == ALTEON_HTTP_PORT:
            raise ConfigurationConflict(
                'Listener with %(protocol)s '
                'protocol may not use '
                'port number %(port)s. This port number is reserved '
                'for TCP or HTTP  protocols.' %
                {'protocol': listener_protocol, 'port': ALTEON_HTTP_PORT})
