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

from abc import ABCMeta
from abc import abstractmethod
import copy
import ConfigParser
import io
import os.path

import exceptions as ex

TYPE = 0
DEFAULT_VALUE = 1
VALUE = 2


def bull(str):
    return str.lower() == 'true'


CONFIG_TEMPLATE = {
    'vdirect_ip': ['str', None, None],
    'vdirect_secondary_ip': ['str', None, None],
    'vdirect_user': ['str', 'vDirect', None],
    'vdirect_password': ['str', 'radware', None],
    'vdirect_http_port': ['int', 2188, None],
    'vdirect_https_port': ['int', 2189, None],
    'use_https': ['bool', True, None],
    'ssl_verify_context': ['bool', True, None],
    'timeout': ['int', 5000, None],
    'base_uri': ['str', '', None],

    'service_adc_type': ['str', 'VA', None],
    'service_adc_version': ['str', '', None],
    'service_ha_pair': ['bool', False, None],
    'configure_allowed_address_pairs': ['bool', False, None],
    'force_one_leg': ['bool', True, None],
    'service_throughput': ['int', 100, None],
    'service_ssl_throughput': ['int', 100, None],
    'service_compression_throughput': ['int', 100, None],
    'service_cache': ['int', 20, None],
    'service_resource_pool_ids': ['list', [], None],
    'service_isl_vlan': ['int', -1, None],
    'service_session_mirroring_enabled': ['bool', False, None],

    'workflow_template_names': ['list',
                                ['openstack_LBaaS', 'manage_l3', ],
                                None],
    'lb_workflow_template_name': ['str', 'openstack_LBaaS', None],
    'lb_create_payload': ['dict', {"twoleg_enabled": "_REPLACE_",
                         "ha_network_name": "HA-Network",
                         "ha_ip_pool_name": "default",
                         "allocate_ha_vrrp": True,
                         "allocate_ha_ips": True,
                         "data_port": 1,
                         "data_ip_address": "192.168.200.99",
                         "data_ip_mask": "255.255.255.0",
                         "gateway": "192.168.200.1",
                         "ha_port": 2}, None],
    'configure_action_name': ['str', 'apply', None],
    'stats_action_name': ['str', 'stats', None],
    'status_action_name': ['str', 'status', None],
    'enable_monitoring': ['bool', False, None],
    'monitoring_interval': ['int', 600, None],
}


class RadwareConfig (object):
    __metaclass__ = ABCMeta

    def __init__(self, service_provider):
        self.service_provider = service_provider
        self.CONFIG = copy.deepcopy(CONFIG_TEMPLATE)
        self.load()

    def __getattr__(self, key):
        if not self.missing():
            return self.CONFIG[key][VALUE]
        return None

    def missing(self):
        return self.CONFIG['vdirect_ip'][VALUE] == \
               self.CONFIG['vdirect_ip'][DEFAULT_VALUE]

    def load(self):
        kv = self.get_dict()
        for k, v in self.CONFIG.iteritems():
            if k in kv:
                self.CONFIG[k][VALUE] = kv.get(k)
            else:
                self.CONFIG[k][VALUE] = self.CONFIG[k][DEFAULT_VALUE]

    @abstractmethod
    def get_dict(self):
        pass


class RadwareConfFileConfig (RadwareConfig):
    types = {
        'str': str,
        'int': int,
        'bool': bull,
        'list': list,
        'dict': dict}

    def __init__(self, filename, service_provider=None):
        self.filename = filename
        super(RadwareConfFileConfig, self).__init__(service_provider)

    @staticmethod
    def convert (value, type):
        return RadwareConfFileConfig.types[type](value)

    def get_dict(self):
        if not os.path.isfile(self.filename):
            raise ex.ConfigurationMissing()

        try:
            with open(self.filename) as f:
                sample_config = f.read()

            config = ConfigParser.RawConfigParser(allow_no_value=True)
            config.readfp(io.BytesIO(sample_config))

            kv = {}
            for k, v in config.items('DEFAULT'):
                kv[k] = RadwareConfFileConfig.convert(v, self.CONFIG[k][TYPE])

            return kv
        except Exception as e:
            raise ex.ConfigurationReadFailure(e.message)
