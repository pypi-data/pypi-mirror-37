.. image:: http://www.radappliances.com/images/radware-logo.gif

=============================================
Radware provider driver for Openstack Octavia
=============================================

This driver is the Octavia provider driver for openstack ROCKY release.


***********
Disclaimer:
***********

- Radware provider driver is currently not supporting following:

	- UDP type pools are partially supported
	- Members batch update is not supported.
	- TERMINATED_HTTPS listeners are not supported.


**************************************************
Activate and configure Radware's Octavia provider:
**************************************************

- Install the radware_octavia_rocky_driver package by executing the following command (use sudo if needed):

	.. code-block:: python

		pip install radware_octavia_rocky_driver

- Open the Octavia configuration file named octavia.conf. Under *[api_settings]* section, add Radware provider to *enabled_provider_drivers* list.
	You may also want to set the default provider to Radware by setting the *default_provider_driver* option.


- The provider configuation for Radware driver should be defined in a proprietary configuration file under "/etc/radware" folder.
	The name of the file is "octavia_driver.conf".

	**Note:Pay attention to the configuration file permissions and owner, the file should have read permissions for neutron user.**

	The name of the section should be [DEFAULT].
	Add driver's parameters under the DEFAULT section, for a reference:

	.. code-block:: python

		[DEFAULT]
		vdirect_ip = 192.168.10.20

	See all possible parameters description in this README.rst file


- Restart the Octavia service
	
*********************************
Using Radware's Octavia provider:
*********************************

For LB creation with Radware provider specify the radware provider in loadbalancer create CLI command.
For example, if the name of the radware provider is **radware**, provider configuration
CLI command will be:

.. code-block:: python

	openstack loadbalancer create --provider radware ...


************************************************
Driver's configuration parameters specification:
************************************************

Following is a list of all driver configuration parameters.
The only mandatory parameter is vdirect_address. Other parameters have default values

* *vdirect_ip: The primary / standalone vDirect server IP address. **This parameter is mandatory**.
* *vdirect_secondary_address*:  The secondary vDirect server IP address when vDirect HA pair is used.
* *vdirect_user*: The vDirect server user name, the default is root.
* *vdirect_password*: The vDirect server user password, the default is radware.
* *vdirect_http_port*: The vDirect server HTTP port. The default is the default vDirect server HTTP port 2188.
* *vdirect_https_port*: The vDirect server HTTPS port. The default is the default vDirect server HTTPS port 2189.
* *use_https*: Use HTTPS for vDirect server connections, the default is True. If False is set, HTTP connections will be used.
* *ssl_verify_context*: Verify SSL certificates on HTTPS connections. the default is True. 
* *timeout*: vDirect server HTTP[S] connection timeout, the default is 5000 milliseconds.
* *base_uri*: vDirect server REST API base uri, the default is ''.
* *service_adc_type*: ADC service type. Options are: VA or VX, the default is VA.
* *service_ha_pair*: Enables or disables ADC service HA-pair, the default is False.
* *configure_allowed_address_pairs*: configure specific allowed address pairs on VIP and PIP ports, in addition to a general CIDR allowed address pair configuration, the default is False.
* *service_throughput*: Service throughput, the default is 1000.
* *service_ssl_throughput*: Service SSL throughput, the default is 100.
* *service_compression_throughput*: Service compression throughput, the default is 100.
* *service_cache*: The size of ADC service cache, the default is 20.
* *service_resource_pool_ids*: The list of vDirect server's resource pools to use for ADC service provissioning, the default is empty.
* *service_isl_vlan*: A required VLAN for the interswitch link to use, the default is -1.
* *service_session_mirroring_enabled*: Enable or disable Alteon interswitch link for stateful session failover the default is False.
