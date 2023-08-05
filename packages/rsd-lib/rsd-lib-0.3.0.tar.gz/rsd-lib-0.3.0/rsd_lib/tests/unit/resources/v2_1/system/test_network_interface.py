# Copyright 2018 99cloud, Inc.
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

import json
import mock
import testtools

from rsd_lib.resources.v2_1.system import network_interface


class NetworkInterfaceTestCase(testtools.TestCase):

    def setUp(self):
        super(NetworkInterfaceTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_1/'
                  'system_network_interface.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.network_interface_inst = network_interface.NetworkInterface(
            self.conn, '/redfish/v1/Systems/System1/EthernetInterfaces/LAN1',
            redfish_version='1.1.0')

    def test__parse_attributes(self):
        self.network_interface_inst._parse_attributes()
        self.assertEqual('Ethernet Interface',
                         self.network_interface_inst.name)
        self.assertEqual('LAN1', self.network_interface_inst.identity)
        self.assertEqual('System NIC 1',
                         self.network_interface_inst.description)
        self.assertEqual('Enabled', self.network_interface_inst.status.state)
        self.assertEqual('OK', self.network_interface_inst.status.health)
        self.assertEqual('OK',
                         self.network_interface_inst.status.health_rollup)
        self.assertEqual(True, self.network_interface_inst.interface_enabled)
        self.assertEqual('AA:BB:CC:DD:EE:FF',
                         self.network_interface_inst.permanent_mac_address)
        self.assertEqual('AA:BB:CC:DD:EE:FF',
                         self.network_interface_inst.mac_address)
        self.assertEqual(100, self.network_interface_inst.speed_mbps)
        self.assertEqual(True, self.network_interface_inst.auto_neg)
        self.assertEqual(True, self.network_interface_inst.full_duplex)
        self.assertEqual(1500, self.network_interface_inst.mtu_size)
        self.assertEqual('web483', self.network_interface_inst.host_name)
        self.assertEqual('web483.redfishspecification.org',
                         self.network_interface_inst.fqdn)
        self.assertEqual('fe80::3ed9:2bff:fe34:600',
                         self.network_interface_inst.ipv6_default_gateway)
        self.assertEqual(None,
                         self.network_interface_inst.max_ipv6_static_addresses)
        self.assertEqual(['names.redfishspecification.org'],
                         self.network_interface_inst.name_servers)
        self.assertEqual('192.168.0.10',
                         self.network_interface_inst.ipv4_addresses[0].address)
        self.assertEqual('255.255.252.0',
                         self.network_interface_inst.ipv4_addresses[0].
                         subnet_mask)
        self.assertEqual('192.168.0.1',
                         self.network_interface_inst.ipv4_addresses[0].gateway)
        self.assertEqual('fe80::1ec1:deff:fe6f:1e24',
                         self.network_interface_inst.ipv6_addresses[0].address)
        self.assertEqual(64,
                         self.network_interface_inst.ipv6_addresses[0].
                         prefix_length)
        self.assertEqual('Static',
                         self.network_interface_inst.ipv6_addresses[0].
                         address_origin)
        self.assertEqual('Preferred',
                         self.network_interface_inst.ipv6_addresses[0].
                         address_state)
        self.assertEqual([], self.network_interface_inst.ipv6_static_addresses)
        self.assertEqual(None, self.network_interface_inst.vlan)


class NetworkInterfaceCollectionTestCase(testtools.TestCase):

    def setUp(self):
        super(NetworkInterfaceCollectionTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_1/'
                  'system_network_interface_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.network_interface_col = network_interface.\
            NetworkInterfaceCollection(
                self.conn,
                '/redfish/v1/Systems/System1/EthernetInterfaces',
                redfish_version='1.1.0')

    def test__parse_attributes(self):
        self.network_interface_col._parse_attributes()
        self.assertEqual('1.1.0', self.network_interface_col.redfish_version)
        self.assertEqual(
            ('/redfish/v1/Systems/System1/EthernetInterfaces/LAN1',),
            self.network_interface_col.members_identities)

    @mock.patch.object(network_interface, 'NetworkInterface', autospec=True)
    def test_get_member(self, mock_network_interface):
        self.network_interface_col.get_member(
            '/redfish/v1/Systems/System1/EthernetInterfaces/LAN1')
        mock_network_interface.assert_called_once_with(
            self.network_interface_col._conn,
            '/redfish/v1/Systems/System1/EthernetInterfaces/LAN1',
            redfish_version=self.network_interface_col.redfish_version)

    @mock.patch.object(network_interface, 'NetworkInterface', autospec=True)
    def test_get_members(self, mock_network_interface):
        members = self.network_interface_col.get_members()
        calls = [
            mock.call(self.network_interface_col._conn,
                      '/redfish/v1/Systems/System1/EthernetInterfaces/LAN1',
                      redfish_version=self.network_interface_col.
                      redfish_version)
        ]
        mock_network_interface.assert_has_calls(calls)
        self.assertIsInstance(members, list)
        self.assertEqual(1, len(members))
