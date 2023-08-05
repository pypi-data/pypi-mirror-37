#!/usr/bin/env python
# Copyright (c) 2018 Radware LTD. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# THIS FILE IS MANAGED BY THE GLOBAL REQUIREMENTS REPO - DO NOT EDIT
from distutils import log
from distutils.core import Command

import os
from setuptools import setup
from setuptools.command.install import install
import ConfigParser


OCTAVIA_CONFIG_FILE_FQN = os.path.join(os.sep, 'etc', 'octavia', 'octavia.conf')
RADWARE_CONFIG_FILE_PATH = os.path.join(os.sep, 'etc', 'radware')
RADWARE_CONFIG_FILE_FQN = os.path.join(RADWARE_CONFIG_FILE_PATH, 'octavia_driver.conf')

OCTAVIA_PROVIDER_DRIVER_CONFIG = 'amphora: The Octavia Amphora driver.'
RADWARE_PROVIDER_DRIVER_NAME = 'radware'
RADWARE_PROVIDER_DRIVER_DESCRIPTION = 'The Radware provider.'
RADWARE_PROVIDER_DRIVER_CONFIG = ', ' + RADWARE_PROVIDER_DRIVER_NAME\
                                 + ': ' + RADWARE_PROVIDER_DRIVER_DESCRIPTION

VDIRECT_IP_OPTION = 'vdirect_ip'

DEFAULTS = {
    'vdirect_ip': None,
    'vdirect_secondary_ip': None,
    'vdirect_user': 'vDirect',
    'vdirect_password': 'radware',
    'vdirect_http_port': 2188,
    'vdirect_https_port': 2189,
    'use_https': True,
    'ssl_verify_context': True,
    'timeout': 5000,
    'base_uri': None,
    'service_adc_type': 'VA',
    'service_ha_pair': False,
    'configure_allowed_address_pairs': False,
    'force_one_leg': True,
    'service_throughput': 100,
    'service_ssl_throughput': 100,
    'service_compression_throughput': 100,
    'service_cache': 20,
    'service_resource_pool_ids': [],
    'service_isl_vlan': -1,
    'service_session_mirroring_enabled': False,
    'workflow_template_names': ['openstack_LBaaS', 'manage_l3', ],
    'lb_workflow_template_name': 'openstack_LBaaS',
    'lb_create_payload': {'twoleg_enabled': '_REPLACE_',
                         'ha_network_name': 'HA-Network',
                         'ha_ip_pool_name': 'default',
                         'allocate_ha_vrrp': True,
                         'allocate_ha_ips': True,
                         'data_port': 1,
                         'data_ip_address': '192.168.200.99',
                         'data_ip_mask': '255.255.255.0',
                         'gateway': '192.168.200.1',
                         'ha_port': 2},
    'configure_action_name': 'apply',
    'stats_action_name': 'stats',
    'stats_action_name': 'status',
    'enable_monitoring': False,
    'monitoring_interval': 600
}

DEFAULT_CONFIG = '\
[DEFAULT]\n\
vdirect_ip = \n\
#vdirect_secondary_ip = \n\
#vdirect_user = vDirect\n\
#vdirect_password = \n\
#vdirect_http_port = 2188\n\
#vdirect_https_port = 2189\n\
#use_https = true\n\
#ssl_verify_context = true\n\
#timeout = 5000\n\
#base_uri = \n\
#service_adc_type = VA\n\
#service_ha_pair = false\n\
#configure_allowed_address_pairs = false\n\
#force_one_leg = true\n\
#service_throughput = 100\n\
#service_ssl_throughput = 100\n\
#service_compression_throughput = 100\n\
#service_cache = 20\n\
#service_resource_pool_ids = \n\
#service_isl_vlan = -1\n\
#service_session_mirroring_enabled = false\n\
#workflow_template_names = [openstack_LBaaS, manage_l3, ]\n\
#lb_workflow_template_name = openstack_LBaaS\n\
#lb_create_payload = {\"twoleg_enabled\": \"_REPLACE_\",\n\
#                         \"ha_network_name\": \"HA-Network\",\n\
#                         \"ha_ip_pool_name\": \"default\",\n\
#                         \"allocate_ha_vrrp\": True,\n\
#                         \"allocate_ha_ips\": True,\n\
#                         \"data_port\": 1,\n\
#                         \"data_ip_address\": \"192.168.200.99\",\n\
#                         \"data_ip_mask\": \"255.255.255.0\",\n\
#                         \"gateway\": \"192.168.200.1\",\n\
#                         \"ha_port\": 2}\n\
#configure_action_name = apply\n\
#stats_action_name = stats\n\
#stats_action_name = status\n\
#enable_monitoring = false\n\
#monitoring_interval = 600\n\
'


class RadwareOctaviaDriverConfiguration(Command):
    description = "Sets the vDirect IP address in driver configuration file." \
                  "Adds the driver to enabled_provider_drivers list in" \
                  "octavia configuration file as \"radware\"." \
                  "Optionally, sets the \"radware\" provider as a default" \
                  "provider driver."
    user_options = [
        ('vdirect-ip-address=', None, 'Specify the vDirect server IP address.'),
        ('default=', None, 'Set the radware driver as a default Octavia provider driver.'),
    ]

    def initialize_options(self):
        self.vdirect_ip_address = None
        self.default = False

    def finalize_options(self):
        pass

    def run(self):
        self._set_vdirect_ip()
        #self._add_provider_driver()
        #install.run(self)

    def _add_provider_driver(self):
        config = ConfigParser.ConfigParser()
        config.read(OCTAVIA_CONFIG_FILE_FQN)
        if not config.has_section('api_settings'):
            log.warn("Octavia configuration file %s "
                     "does not contain [api_settings] section. "
                     "Unable to add \"radware\" provider."
                     % OCTAVIA_CONFIG_FILE_FQN)
            return

        if config.has_option('api_settings', 'enabled_provider_drivers'):
            drivers = config.get(
                'api_settings', 'enabled_provider_drivers')\
                      + RADWARE_PROVIDER_DRIVER_CONFIG
        else:
            drivers = OCTAVIA_PROVIDER_DRIVER_CONFIG\
                      + RADWARE_PROVIDER_DRIVER_CONFIG

        config.set('api_settings', 'enabled_provider_drivers', drivers)
        if self.default:
            config.set('api_settings', 'default_provider_driver',
                       RADWARE_PROVIDER_DRIVER_NAME)

        octavia_conf_file = open(OCTAVIA_CONFIG_FILE_FQN, 'w')
        config.write(octavia_conf_file)
        octavia_conf_file.close()

    def _set_vdirect_ip(self):
        config = ConfigParser.ConfigParser()
        config.read(RADWARE_CONFIG_FILE_FQN)
        ip = config.get(ConfigParser.DEFAULTSECT, VDIRECT_IP_OPTION)
        if ip and ip is not None:
            log.warn("Octavia driver configuration file already "
                     "has vDirect ip address set to " + ip
                     + ". Overriden with provided IP address")
        config.set(ConfigParser.DEFAULTSECT, VDIRECT_IP_OPTION, self.vdirect_ip_address)

        radware_conf_file = open(RADWARE_CONFIG_FILE_FQN, 'w')
        config.write(radware_conf_file)
        radware_conf_file.close()


class OverrideInstall(install):
    file_mode = 0o644
    folder_mode = 0o755

    def _write_default_config_file(self):
        file_mode = 0o644
        folder_mode = 0o755

        log.info("Changing the package folder permissions to %s" % (oct(folder_mode)))
        dirname = os.path.dirname(self.get_outputs()[0])
        os.chmod(dirname, folder_mode)

        log.info("Changing files permissions to %s" % (oct(file_mode)))
        for filepath in self.get_outputs():
            os.chmod(filepath, file_mode)

        log.info("Creating %s folder" % RADWARE_CONFIG_FILE_PATH)
        if not os.path.exists(RADWARE_CONFIG_FILE_PATH):
            os.mkdir(RADWARE_CONFIG_FILE_PATH, folder_mode)
            log.info("Changing permissions for %s folder"
                     % RADWARE_CONFIG_FILE_PATH)
            os.chmod(RADWARE_CONFIG_FILE_PATH, folder_mode)
        if not os.path.exists(RADWARE_CONFIG_FILE_FQN):
            '''
            log.info("Writing default configuration file.")
            config = ConfigParser.ConfigParser(defaults=DEFAULTS)
            radware_conf_file = open(RADWARE_CONFIG_FILE_FQN, 'w')
            config.write(radware_conf_file)
            radware_conf_file.close()
            '''
            log.info("Writing default configuration file")
            cf = os.open(RADWARE_CONFIG_FILE_FQN, os.O_CREAT | os.O_RDWR, 0o755)
            os.write(cf, DEFAULT_CONFIG)
            os.chmod(RADWARE_CONFIG_FILE_FQN, file_mode)
            os.close(cf)
        else:
            log.info("Preserving existing configuration file")

    def run(self):
        install.run(self)
        self._write_default_config_file()


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='radware_octavia_rocky_driver',
      version='4.6.0-1',
      description='Octavia Radware driver for Openstack Rocky',
      long_description = readme(),
      classifiers=[
          'Environment :: OpenStack',
          'Intended Audience :: Information Technology',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 2.7'
      ],
      keywords=['radware', 'vdirect', 'lbaas', 'ADC', 'octavia'],
      url='https://pypi.python.org/pypi/radware_octavia_rocky_driver',
      author='Evgeny Fedoruk, Radware',
      author_email='evgenyf@radware.com',
      packages=['radware_octavia_rocky_driver'],
      zip_safe=False,
      cmdclass={'install': OverrideInstall,
                'configure': RadwareOctaviaDriverConfiguration},
      entry_points={
          'octavia.api.drivers': [
              'radware = radware_octavia_rocky_driver.octavia_provider_driver:RadwareOctaviaProviderDriver',
          ]})
