# Copyright 2014 Mirantis Inc.
# All Rights Reserved.
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

from oslo_log import log
import six
from tempest import config
import testtools
from testtools import testcase as tc

from manila_tempest_tests.tests.api import base

CONF = config.CONF
LOG = log.getLogger(__name__)


class SecurityServiceListMixin(object):

    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_list_security_services(self):
        listed = self.shares_client.list_security_services()
        self.assertTrue(any(self.ss_ldap['id'] == ss['id'] for ss in listed))
        self.assertTrue(any(self.ss_kerberos['id'] == ss['id']
                            for ss in listed))

        # verify keys
        keys = ["name", "id", "status", "type", ]
        [self.assertIn(key, s_s.keys()) for s_s in listed for key in keys]

    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_list_security_services_with_detail(self):
        listed = self.shares_client.list_security_services(detailed=True)
        self.assertTrue(any(self.ss_ldap['id'] == ss['id'] for ss in listed))
        self.assertTrue(any(self.ss_kerberos['id'] == ss['id']
                            for ss in listed))

        # verify keys
        keys = [
            "name", "id", "status", "description",
            "domain", "server", "dns_ip", "user", "password", "type",
            "created_at", "updated_at", "project_id",
        ]
        [self.assertIn(key, s_s.keys()) for s_s in listed for key in keys]

    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    @testtools.skipIf(
        not CONF.share.multitenancy_enabled, "Only for multitenancy.")
    def test_list_security_services_filter_by_share_network(self):
        sn = self.shares_client.get_share_network(
            self.shares_client.share_network_id)
        fresh_sn = []
        for i in range(2):
            sn = self.create_share_network(
                neutron_net_id=sn["neutron_net_id"],
                neutron_subnet_id=sn["neutron_subnet_id"])
            fresh_sn.append(sn)

        self.shares_client.add_sec_service_to_share_network(
            fresh_sn[0]["id"], self.ss_ldap["id"])
        self.shares_client.add_sec_service_to_share_network(
            fresh_sn[1]["id"], self.ss_kerberos["id"])

        listed = self.shares_client.list_security_services(
            params={'share_network_id': fresh_sn[0]['id']})
        self.assertEqual(1, len(listed))
        self.assertEqual(self.ss_ldap['id'], listed[0]['id'])

        keys = ["name", "id", "status", "type", ]
        [self.assertIn(key, s_s.keys()) for s_s in listed for key in keys]

    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_list_security_services_detailed_filter_by_ss_attributes(self):
        search_opts = {
            'name': 'ss_ldap',
            'type': 'ldap',
            'user': 'fake_user',
            'server': 'fake_server_1',
            'dns_ip': '1.1.1.1',
            'domain': 'fake_domain_1',
        }
        listed = self.shares_client.list_security_services(
            detailed=True,
            params=search_opts)
        self.assertTrue(any(self.ss_ldap['id'] == ss['id'] for ss in listed))
        for ss in listed:
            self.assertTrue(all(ss[key] == value for key, value
                                in search_opts.items()))


class SecurityServicesTest(base.BaseSharesMixedTest,
                           SecurityServiceListMixin):

    @classmethod
    def resource_setup(cls):
        super(SecurityServicesTest, cls).resource_setup()
        # create share type
        cls.share_type = cls._create_share_type()
        cls.share_type_id = cls.share_type['id']

    def setUp(self):
        super(SecurityServicesTest, self).setUp()
        ss_ldap_data = {
            'name': 'ss_ldap',
            'dns_ip': '1.1.1.1',
            'server': 'fake_server_1',
            'domain': 'fake_domain_1',
            'user': 'fake_user',
            'password': 'pass',
        }
        ss_kerberos_data = {
            'name': 'ss_kerberos',
            'dns_ip': '2.2.2.2',
            'server': 'fake_server_2',
            'domain': 'fake_domain_2',
            'user': 'test_user',
            'password': 'word',
        }
        self.ss_ldap = self.create_security_service('ldap', **ss_ldap_data)
        self.ss_kerberos = self.create_security_service(
            'kerberos', **ss_kerberos_data)

    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_create_delete_security_service(self):
        data = self.generate_security_service_data()
        self.service_names = ["ldap", "kerberos", "active_directory"]
        for ss_name in self.service_names:
            ss = self.create_security_service(ss_name, **data)
            self.assertDictContainsSubset(data, ss)
            self.assertEqual(ss_name, ss["type"])
            self.shares_client.delete_security_service(ss["id"])

    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_get_security_service(self):
        data = self.generate_security_service_data()
        ss = self.create_security_service(**data)
        self.assertDictContainsSubset(data, ss)

        get = self.shares_client.get_security_service(ss["id"])
        self.assertDictContainsSubset(data, get)

    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_update_security_service(self):
        data = self.generate_security_service_data()
        ss = self.create_security_service(**data)
        self.assertDictContainsSubset(data, ss)

        upd_data = self.generate_security_service_data()
        updated = self.shares_client.update_security_service(
            ss["id"], **upd_data)

        get = self.shares_client.get_security_service(ss["id"])
        self.assertDictContainsSubset(upd_data, updated)
        self.assertDictContainsSubset(upd_data, get)

    @tc.attr(base.TAG_POSITIVE, base.TAG_API_WITH_BACKEND)
    @testtools.skipIf(
        not CONF.share.multitenancy_enabled, "Only for multitenancy.")
    def test_try_update_valid_keys_sh_server_exists(self):
        ss_data = self.generate_security_service_data()
        ss = self.create_security_service(**ss_data)

        sn = self.shares_client.get_share_network(
            self.shares_client.share_network_id)
        fresh_sn = self.create_share_network(
            neutron_net_id=sn["neutron_net_id"],
            neutron_subnet_id=sn["neutron_subnet_id"])

        self.shares_client.add_sec_service_to_share_network(
            fresh_sn["id"], ss["id"])

        # Security service with fake data is used, so if we use backend driver
        # that fails on wrong data, we expect error here.
        # We require any share that uses our share-network.
        try:
            self.create_share(share_type_id=self.share_type_id,
                              share_network_id=fresh_sn["id"],
                              cleanup_in_class=False)
        except Exception as e:
            # we do wait for either 'error' or 'available' status because
            # it is the only available statuses for proper deletion.
            LOG.warning("Caught exception. It is expected in case backend "
                        "fails having security-service with improper data "
                        "that leads to share-server creation error. "
                        "%s" % six.text_type(e))

        update_data = {
            "name": "name",
            "description": "new_description",
        }
        updated = self.shares_client.update_security_service(
            ss["id"], **update_data)
        self.assertDictContainsSubset(update_data, updated)

    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_list_security_services_filter_by_invalid_opt(self):
        listed = self.shares_client.list_security_services(
            params={'fake_opt': 'some_value'})
        self.assertTrue(any(self.ss_ldap['id'] == ss['id'] for ss in listed))
        self.assertTrue(any(self.ss_kerberos['id'] == ss['id']
                            for ss in listed))

    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_try_list_security_services_all_tenants(self):
        listed = self.shares_client.list_security_services(
            params={'all_tenants': 1})
        self.assertTrue(any(self.ss_ldap['id'] == ss['id'] for ss in listed))
        self.assertTrue(any(self.ss_kerberos['id'] == ss['id']
                            for ss in listed))
