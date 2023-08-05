# Copyright 2018 Radware LTD.
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

from octavia.i18n import _
from octavia.api.drivers import exceptions as driver_exceptions


class RadwareDriverException(driver_exceptions.DriverError):
    def __init__(self, user_message, operator_message):
        super(RadwareDriverException, self).__init__(
            user_fault_string=user_message,
            operator_fault_string=operator_message)

    def __str__(self):
        return self.operator_fault_string


class ConfigurationMissing(RadwareDriverException):

    def __init__(self, **kwargs):
        user_fault_string = _(
            "Unable to satisfy the request "
            "due to missing service provider configuration.")

        operator_fault_string = _(
            "Driver configuration missing. "
            "Specify driver configuration under %(module_name)s section "
            "in octavia configuration file or under DEFAULT section either "
            "in /etc/radware/%(module_name)s.conf file or "
            "/etc/octavia/%(module_name)s.conf")

        super(ConfigurationMissing, self).__init__(
            user_fault_string % kwargs, operator_fault_string % kwargs)


class WorkflowTemplateMissing(RadwareDriverException):
    def __init__(self, **kwargs):
        user_fault_string = _(
            "Unable to satisfy the request "
            "due to service provider internal deployment failure.")

        operator_fault_string = _(
            "vDirect Workflow template %(workflow_template)s is missing "
            "on vDirect server. Upload missing workflow")

        super(WorkflowTemplateMissing, self).__init__(
            user_fault_string % kwargs, operator_fault_string % kwargs)


class ConfigurationConflict(RadwareDriverException):
    def __init__(self, **kwargs):
        user_fault_string = _(
            "Unable to satisfy the request "
            "due to load balancer configuration conflict. "
            "Conflict description: %(conflict_description)s.")

        operator_fault_string = _(
            "Loadbalancer configuration conflict found."
            "%(conflict_description)s")

        super(ConfigurationConflict, self).__init__(
            user_fault_string % kwargs, operator_fault_string  % kwargs)


class RESTRequestFailure(RadwareDriverException):
    def __init__(self, **kwargs):
        self.status = kwargs.get('status')
        self.reason = kwargs.get('reason')
        self.description = kwargs.get('description')
        self.success_codes = kwargs.get('success_codes')

        user_fault_string = _(
            "Unable to satisfy the request "
            "due to internal service provider failure. "
            "See log messages for detailed failure description.")

        operator_fault_string = _(
            "REST request failed with status %(status)s. "
            "Reason: %(reason)s, Description: %(description)s. "
            "Success status codes are %(success_codes)s")

        super(RESTRequestFailure, self).__init__(
            user_fault_string % kwargs, operator_fault_string % kwargs)
