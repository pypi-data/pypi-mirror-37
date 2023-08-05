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

from sushy.resources import base

from rsd_lib import utils as rsd_lib_utils


class StatusField(base.CompositeField):
    state = base.Field('State')
    health = base.Field('Health')
    health_rollup = base.Field('HealthRollup')


class IPv4AddressesField(base.ListField):
    address = base.Field('Address')
    subnet_mask = base.Field('SubnetMask')
    address_origin = base.Field('AddressOrigin')
    gateway = base.Field('Gateway')


class IPv6AddressesField(base.ListField):
    address = base.Field('Address')
    prefix_length = base.Field('PrefixLength')
    address_origin = base.Field('AddressOrigin')
    address_state = base.Field('AddressState')


class IPv6StaticAddressesField(base.ListField):
    address = base.Field('Address')
    prefix_length = base.Field('PrefixLength')


class VLANField(base.CompositeField):
    vlan_enable = base.Field('VLANEnable', adapter=bool)
    vlan_id = base.Field('VLANId',
                         adapter=rsd_lib_utils.int_or_none)


class NetworkInterface(base.ResourceBase):

    name = base.Field('Name')
    """The network interface name"""

    identity = base.Field('Id')
    """The network interface identity"""

    description = base.Field('Description')
    """The network interface description"""

    status = StatusField('Status')
    """The network interface status"""

    interface_enabled = base.Field('InterfaceEnabled', adapter=bool)
    """The boolean indicate this network interface is enabled or not"""

    permanent_mac_address = base.Field('PermanentMACAddress')
    """The network interface permanent mac address"""

    mac_address = base.Field('MACAddress')
    """The network interface mac address"""

    speed_mbps = base.Field('SpeedMbps')
    """The network interface speed"""

    auto_neg = base.Field('AutoNeg', adapter=bool)
    """Indicates if the speed and duplex is automatically configured
    by the NIC
    """

    full_duplex = base.Field('FullDuplex', adapter=bool)
    """Indicates if the NIC is in Full Duplex mode or not"""

    mtu_size = base.Field('MTUSize',
                          adapter=rsd_lib_utils.int_or_none)
    """The network interface mtu size"""

    host_name = base.Field('HostName')
    """The network interface host name"""

    fqdn = base.Field('FQDN')
    """Fully qualified domain name obtained by DNS for this interface"""

    ipv6_default_gateway = base.Field('IPv6DefaultGateway')
    """Default gateway address that is currently in use on this interface"""

    max_ipv6_static_addresses = base.Field('MaxIPv6StaticAddresses',
                                           adapter=rsd_lib_utils.int_or_none)
    """Indicates the maximum number of Static IPv6 addresses that can be
    configured on this interface
    """

    name_servers = base.Field('NameServers')
    """The network interface nameserver"""

    ipv4_addresses = IPv4AddressesField('IPv4Addresses')
    """The network interface ipv4 address"""

    ipv6_addresses = IPv6AddressesField('IPv6Addresses')
    """The network interface ipv6 address"""

    ipv6_static_addresses = IPv6StaticAddressesField('IPv6StaticAddresses')
    """The network interface ipv6 static address"""

    vlan = VLANField('VLAN')
    """The network interface vlan collection"""

    oem = base.Field('oem')
    """The network interface oem field"""

    links = base.Field('links')
    """The network interface links field"""

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a Network Interface

        :param connector: A Connector instance
        :param identity: The identity of the Network Interface
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(NetworkInterface, self).__init__(connector,
                                               identity,
                                               redfish_version)


class NetworkInterfaceCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return NetworkInterface

    def __init__(self, connector, path, redfish_version=None):
        """A class representing a NetworkInterfaceCollection

        :param connector: A Connector instance
        :param path: The canonical path to the network interface collection
            resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(NetworkInterfaceCollection, self).__init__(connector,
                                                         path,
                                                         redfish_version)
