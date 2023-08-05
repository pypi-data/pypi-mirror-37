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

import copy
import netaddr

from oslo_log import log as logging

from octavia.common import constants
from octavia.common import data_models as common_dm
from octavia.common import utils as common_utils
from octavia.api.drivers import data_models as provider_dm
from octavia.api.drivers import driver_lib
from octavia.api.drivers import utils

LOG = logging.getLogger(__name__)

PROPERTY_DEFAULTS = {constants.TYPE: 'none',
                     'cookie_name': 'none',
                     constants.URL_PATH: '/',
                     constants.HTTP_METHOD: 'GET',
                     constants.EXPECTED_CODES: '200',
                     'subnet': '255.255.255.255',
                     'mask': '255.255.255.255',
                     'gw': '255.255.255.255'}

LOADBALANCER_PROPERTIES = ['vip_address', 'admin_state_up']
LISTENER_PROPERTIES = ['listener_id', 'protocol_port', 'protocol',
                       'connection_limit', 'admin_state_up']
DEFAULT_CERT_PROPERTIES = ['id', 'certificate', 'intermediates',
                           'private_key', 'passphrase', 'primary_cn']
SNI_CERT_PROPERTIES = DEFAULT_CERT_PROPERTIES + ['position']
L7_RULE_PROPERTIES = ['l7rule_id', 'type', 'compare_type',
                      'key', 'value', 'admin_state_up']
L7_POLICY_PROPERTIES = ['l7policy_id', 'action', 'redirect_pool_id',
                        'redirect_url', 'position', 'admin_state_up']
DEFAULT_POOL_PROPERTIES = ['id']
POOL_PROPERTIES = ['pool_id', 'protocol', 'lb_algorithm', 'admin_state_up']
MEMBER_PROPERTIES = ['member_id', 'address', 'protocol_port', 'weight',
                     'admin_state_up', 'mask', 'gw']
SESSION_PERSISTENCY_PROPERTIES = ['type', 'cookie_name',
                                  'persistence_timeout', 'persistence_granularity']
HEALTH_MONITOR_PROPERTIES = ['healthmonitor_id','type', 'delay', 'timeout',
                             'max_retries', 'max_retries_down',
                             'admin_state_up', 'url_path','http_method',
                             'expected_codes']


def get_pdm_id(pdm):
    if isinstance(pdm, provider_dm.LoadBalancer):
        return pdm.loadbalancer_id
    elif isinstance(pdm, provider_dm.Listener):
        return pdm.listener_id
    elif isinstance(pdm, provider_dm.Pool):
        return pdm.pool_id
    elif isinstance(pdm, provider_dm.Member):
        return pdm.member_id
    elif isinstance(pdm, provider_dm.HealthMonitor):
        return pdm.healthmonitor_id
    elif isinstance(pdm, provider_dm.L7Policy):
        return pdm.l7policy_id
    elif isinstance(pdm, provider_dm.L7Rule):
        return pdm.l7rule_id


def _get_pdm_lb_id(dl, pdm):
    if isinstance(pdm, provider_dm.LoadBalancer):
        return pdm.loadbalancer_id
    elif isinstance(pdm, (provider_dm.Listener, provider_dm.Pool)):
        return pdm.loadbalancer_id
    elif isinstance(pdm, (provider_dm.Member, provider_dm.HealthMonitor)):
        pool = dl.pool_repo.get(dl.db_session, id=pdm.pool_id)
        return pool.load_balancer_id
    elif isinstance(pdm, provider_dm.L7Policy):
        listener = dl.listener_repo.get(dl.db_session, id=pdm.listener_id)
        return listener.load_balancer_id
    elif isinstance(pdm, provider_dm.L7Rule):
        l7policy = dl.l7policy_repo.get(dl.db_session, id=pdm.l7policy_id)
        return l7policy.listener.load_balancer_id


def _get_pdm_lb(dl, pdm, create):
    lb_id = _get_pdm_lb_id(dl, pdm)
    if isinstance(pdm, provider_dm.LoadBalancer) and create:
        return pdm
    else:
        # This manual operation is performed as a result of Octavia bug.
        # https://review.openstack.org/#/c/605376
        lb_cdm = dl.loadbalancer_repo.get(dl.db_session, **{'id': lb_id})
        lb_pdm = provider_dm.LoadBalancer(
            admin_state_up=lb_cdm.enabled, loadbalancer_id=lb_cdm.id,
            project_id=lb_cdm.project_id, vip_address=lb_cdm.vip.ip_address,
            vip_network_id=lb_cdm.vip.network_id, vip_port_id=lb_cdm.vip.port_id,
            vip_subnet_id=lb_cdm.vip.subnet_id)
        if isinstance(pdm, provider_dm.LoadBalancer):
            lb_pdm.admin_state_up = pdm.admin_state_up
        return lb_pdm


def _get_lb_listeners(dl, lb_id, create, new_pdm, deleted_id):
    pdms = _get_pdms(
        dl.db_session, dl.listener_repo,
        {'load_balancer_id': lb_id},
        utils.db_listeners_to_provider_listeners)

    pdms = [l for l in pdms if l.listener_id != deleted_id]
    if create:
        pdms.append(new_pdm)
    elif new_pdm:
        pdms = [pdm for pdm in pdms if pdm.listener_id != new_pdm.listener_id]
        pdms.append(new_pdm)
    return pdms


def _get_lb_pools(dl, lb_id, create, new_pdm, deleted_id):
    pdms = _get_pdms(
        dl.db_session, dl.pool_repo,
        {'load_balancer_id': lb_id},
        utils.db_pools_to_provider_pools)

    pdms = [l for l in pdms if l.pool_id != deleted_id]
    if create:
        pdms.append(new_pdm)
    elif new_pdm:
        pdms = [pdm for pdm in pdms if pdm.pool_id != new_pdm.pool_id]
        pdms.append(new_pdm)
    return pdms


def _get_pool_members(dl, pool_id, create, new_pdm, deleted_id):
    pdms = _get_pdms(
        dl.db_session, dl.member_repo,
        {'pool_id': pool_id},
        utils.db_members_to_provider_members)

    pdms = [l for l in pdms if l.member_id != deleted_id]
    if create:
        pdms.append(new_pdm)
    elif new_pdm:
        pdms = [pdm for pdm in pdms if pdm.member_id != new_pdm.member_id]
        pdms.append(new_pdm)
    return pdms


def _get_pool(dl, pool_id):
    return _get_pdm(
        dl.db_session, dl.pool_repo, {'id': pool_id},
        utils.db_pool_to_provider_pool)


def _get_healthmonitor(dl, healthmonitor_id):
        return _get_pdm(
        dl.db_session, dl.health_mon_repo, {'id': healthmonitor_id},
        utils.db_HM_to_provider_HM)


def _get_listener_l7policies(dl, listener_id, create, new_pdm, deleted_id):
    pdms = _get_pdms(
        dl.db_session, dl.l7policy_repo,
        {'listener_id': listener_id},
        utils.db_l7policies_to_provider_l7policies)

    pdms = [l for l in pdms if l.l7policy_id != deleted_id]
    if create:
        pdms.append(new_pdm)
    elif new_pdm:
        pdms = [pdm for pdm in pdms if pdm.l7policy_id != new_pdm.l7policy_id]
        pdms.append(new_pdm)
    return pdms


def _get_l7policy_rules(dl, l7policy_id, create, new_pdm, deleted_id):
    pdms = _get_pdms(
        dl.db_session, dl.l7rule_repo,
        {'l7policy_id': l7policy_id},
        utils.db_l7rules_to_provider_l7rules)

    pdms = [l for l in pdms if l.l7rule_id != deleted_id]
    if create:
        pdms.append(new_pdm)
    elif new_pdm:
        pdms = [pdm for pdm in pdms if pdm.l7rule_id != new_pdm.l7rule_id]
        pdms.append(new_pdm)
    return pdms


def _get_pdm(session, repo, filters, converter):
    return converter(repo.get(session, **filters))


def _get_pdms(session, repo, filters, converter):
    return converter(repo.get_all(session, **filters)[0])


def get_lb_and_graph(pdm, create=False, delete=False):

    statuses = {
        constants.LOADBALANCERS: [],
        constants.LISTENERS: [],
        constants.POOLS: [],
        constants.MEMBERS: [],
        constants.HEALTHMONITORS: [],
        constants.L7POLICIES: [],
        constants.L7RULES: []}

    pdm_id = get_pdm_id(pdm)
    dl = driver_lib.DriverLibrary()
    lb_pdm = _get_pdm_lb(dl, pdm, create)
    lb_id = lb_pdm.loadbalancer_id

    statuses[constants.LOADBALANCERS].append({'id': lb_id})
    if isinstance(pdm, provider_dm.Listener):
        statuses[constants.LISTENERS].append({'id': pdm.listener_id})
    if isinstance(pdm, provider_dm.Pool):
        statuses[constants.POOLS].append({'id': pdm.pool_id})
        if pdm.listener_id:
            statuses[constants.LISTENERS].append({'id': pdm.listener_id})
    if isinstance(pdm, provider_dm.Member):
        statuses[constants.MEMBERS].append({'id': pdm.member_id})
        statuses[constants.POOLS].append({'id': pdm.pool_id})
    if isinstance(pdm, provider_dm.HealthMonitor):
        statuses[constants.HEALTHMONITORS].append({'id': pdm.healthmonitor_id})
        statuses[constants.POOLS].append({'id': pdm.pool_id})
    if isinstance(pdm, provider_dm.L7Policy):
        statuses[constants.L7POLICIES].append({'id': pdm.l7policy_id})
        statuses[constants.LISTENERS].append({'id': pdm.listener_id})
    if isinstance(pdm, provider_dm.L7Rule):
        statuses[constants.L7RULES].append({'id': pdm.l7rule_id})
        statuses[constants.L7POLICIES].append({'id': pdm.l7policy_id})

    graph = {}

    for prop in LOADBALANCER_PROPERTIES:
        graph[prop] = getattr(lb_pdm, prop, PROPERTY_DEFAULTS.get(prop))
    graph['pip_address'] = graph['vip_address']

    graph['listeners'] = []
    listeners = _get_lb_listeners(
        dl, lb_id,
        True if create and isinstance(pdm, provider_dm.Listener)
                and pdm.loadbalancer_id == lb_id else False,
        pdm if isinstance(pdm, provider_dm.Listener)
               and pdm.loadbalancer_id == lb_id and not delete else None,
        pdm_id if delete else None)
    for l in listeners:
        l_dict = {}
        if l.default_pool_id and delete and l.default_pool_id == pdm_id:
            continue
        default_pool = None
        if isinstance(pdm, provider_dm.Pool) and pdm.listener_id == l.listener_id:
            default_pool = pdm
        elif l.default_pool_id:
            default_pool = _get_pool(dl, l.default_pool_id)

        if not default_pool:
            continue

        default_pool_members = _get_pool_members(
            dl, default_pool.pool_id,
            True if create and isinstance(pdm, provider_dm.Member) else False,
            pdm if isinstance(pdm, provider_dm.Member) and not delete else None,
            pdm_id if delete else None)
        if not default_pool_members:
            continue

        for prop in LISTENER_PROPERTIES:
            l_dict[prop] = getattr(
                l, prop, PROPERTY_DEFAULTS.get(prop))
        l_dict['id'] = l_dict.pop('listener_id')

        def_pool_dict = {'id': default_pool.pool_id}
        if default_pool.session_persistence:
            sp_dict = {}
            for prop in SESSION_PERSISTENCY_PROPERTIES:
                sp_dict[prop] = \
                    default_pool.session_persistence.get(
                        prop,PROPERTY_DEFAULTS.get(prop))
            if sp_dict['persistence_timeout']:
                sp_dict['persistence_timeout'] = str(int(sp_dict.pop('persistence_timeout')) / 60)
            def_pool_dict['sessionpersistence'] = sp_dict
        l_dict['default_pool'] = def_pool_dict

        if l.default_tls_container_ref and delete and l.default_tls_container_ref == pdm_id:
            l_dict['default_tls_certificate'] = l.default_tls_container_data
        if l.sni_container_refs:
            l_dict['sni_tls_certificates'] = l.sni_container_data

        l7policies = _get_listener_l7policies(
            dl, l.listener_id,
            True if create and isinstance(pdm, provider_dm.L7Policy)
                    and pdm.listener_id == l.listener_id else False,
            pdm if isinstance(pdm, provider_dm.L7Policy)
                   and pdm.listener_id == l.listener_id and not delete else None,
            pdm_id if delete else None)

        l_dict['l7_policies'] = []
        for p in l7policies:

            if isinstance(pdm, provider_dm.L7Rule) \
                    and statuses[constants.L7POLICIES][0]['id'] == p.l7policy_id:
                statuses[constants.LISTENERS].append({'id': p.listener_id})

            p_dict = {}
            for prop in L7_POLICY_PROPERTIES:
                p_dict[prop] = getattr(
                    p, prop, PROPERTY_DEFAULTS.get(prop))
            p_dict['id'] = p_dict.pop('l7policy_id')

            p_dict['rules'] = []
            l7rules = _get_l7policy_rules(
                dl, p.l7policy_id,
                True if create and isinstance(pdm, provider_dm.L7Rule)
                        and pdm.l7policy_id == p.l7policy_id else False,
                pdm if isinstance(pdm, provider_dm.L7Rule)
                       and pdm.l7policy_id == p.l7policy_id and not delete else None,
                pdm_id if delete else None)

            for r in l7rules:
                r_dict = {}
                for prop in L7_RULE_PROPERTIES:
                    r_dict[prop] = getattr(
                        r, prop, PROPERTY_DEFAULTS.get(prop))
                r_dict['id'] = r_dict.pop('l7rule_id')
                p_dict['rules'].append(r_dict)
            if p_dict['rules']:
                l_dict['l7_policies'].append(p_dict)
        graph['listeners'].append(l_dict)

    graph['pools'] = []
    pools = _get_lb_pools(
        dl, lb_id,
        True if create and isinstance(pdm, provider_dm.Pool)
                and pdm.loadbalancer_id == lb_id else False,
        pdm if isinstance(pdm, provider_dm.Pool)
               and pdm.loadbalancer_id == lb_id and not delete else None,
        pdm_id if delete else None)
    for p in pools:

        if (isinstance(pdm, provider_dm.Member)
            or isinstance(pdm, provider_dm.HealthMonitor))\
                and statuses[constants.POOLS][0]['id'] == p.pool_id\
                and p.listener_id:
            statuses[constants.LISTENERS].append({'id': p.listener_id})

        p_dict = {}
        for prop in POOL_PROPERTIES:
            p_dict[prop] = getattr(
                p, prop,
                PROPERTY_DEFAULTS.get(prop))
        p_dict['id'] = p_dict.pop('pool_id')

        hm = None
        if isinstance(pdm, provider_dm.HealthMonitor) and pdm.pool_id == p.pool_id:
            if not delete:
                hm = pdm
        elif p.healthmonitor:
            hm = _get_healthmonitor(dl, p.healthmonitor.healthmonitor_id)

        if hm:
            hm_dict = {}
            for prop in HEALTH_MONITOR_PROPERTIES:
                hm_dict[prop] = getattr(
                    hm, prop,
                    PROPERTY_DEFAULTS.get(prop))
            hm_dict['id'] = hm_dict.pop('healthmonitor_id')
            p_dict['healthmonitor'] = hm_dict

        members = _get_pool_members(
            dl, p.pool_id,
            True if create and isinstance(pdm, provider_dm.Member)
                    and pdm.pool_id == p.pool_id else False,
            pdm if isinstance(pdm, provider_dm.Member)
                   and pdm.pool_id == p.pool_id and not delete else None,
            pdm_id if delete else None)

        p_dict['members'] = []
        for member in members:
            m_dict = {}
            for prop in MEMBER_PROPERTIES:
                m_dict[prop] = getattr(
                    member, prop,
                    PROPERTY_DEFAULTS.get(prop))
            m_dict['id'] = m_dict.pop('member_id')
            _accomplish_member_static_route_data(member, lb_pdm, m_dict)
            p_dict['members'].append(m_dict)
        graph['pools'].append(p_dict)

    return lb_pdm, statuses, graph


def _accomplish_member_static_route_data(member, lb_pdm, m_dict):
    n_driver = common_utils.get_network_driver()
    vip_subnet = n_driver.get_subnet(lb_pdm.vip_subnet_id)

    if netaddr.IPAddress(member.address) in netaddr.IPNetwork(vip_subnet.cidr):
        return

    member_ports = n_driver._get_resources_by_filters(
        'port', unique_item=False,
        ip_address=member.address, tenant_id=lb_pdm.project_id)
    if len(member_ports) == 1:
        member_port = member_ports[0]
        member_port_ip_data = member_port.fixed_ips[0]
        member_subnet = n_driver.get_subnet(member_port_ip_data.subnet_id)
        member_network = netaddr.IPNetwork(member_subnet.cidr)
        m_dict['subnet'] = str(member_network.network)
        m_dict['mask'] = str(member_network.netmask)
    else:
        m_dict['subnet'] = m_dict['address']
    m_dict['gw'] = vip_subnet.gateway_ip


def merge_updated(old, new):
    merged = copy.deepcopy(old)
    for attr in (a for a in dir(new)
                 if not a.startswith('__')
                    and not isinstance(getattr(new, a), provider_dm.UnsetType)):
        setattr(merged, attr, getattr(new, attr))
    return merged
