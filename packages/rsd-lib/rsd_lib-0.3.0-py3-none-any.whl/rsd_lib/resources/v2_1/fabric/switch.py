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

import logging

from sushy.resources import base

from rsd_lib import utils as rsd_lib_utils

LOG = logging.getLogger(__name__)


class StatusField(base.CompositeField):
    state = base.Field('State')
    health = base.Field('Health')
    health_rollup = base.Field('HealthRollUp')


class PortsField(base.CompositeField):
    identity = base.Field('@odata.id')


class Switch(base.ResourceBase):

    identity = base.Field('Id')
    """The switch identity"""

    name = base.Field('Name')
    """The switch name"""

    description = base.Field('Description')
    """The switch description"""

    switch_type = base.Field('SwitchType')
    """The switch type"""

    status = StatusField('Status')
    """The switch status"""

    manufacturer = base.Field('Manufacturer')
    """The switch manufacturer name"""

    model = base.Field('Model')
    """The switch model"""

    sku = base.Field("SKU")
    """The switch SKU"""

    serial_number = base.Field('SerialNumber')
    """The switch serial number"""

    part_number = base.Field('PartNumber')
    """The switch part number"""

    asset_tag = base.Field('AssetTag')
    """The switch custom asset tag"""

    domain_id = base.Field('DomainID')
    """The switch domain id"""

    is_managed = base.Field('IsManaged')
    """The switch managed state"""

    total_switch_width = base.Field('TotalSwitchWidth',
                                    adapter=rsd_lib_utils.int_or_none)
    """The switch total switch width"""

    indicator_led = base.Field('IndicatorLED')
    """The switch indicator led"""

    power_state = base.Field('PowerState')
    """The switch power state"""

    ports = PortsField('Ports')

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a Switch

        :param connector: A Connector instance
        :param identity: The identity of the Switch resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(Switch, self).__init__(connector, identity,
                                     redfish_version)


class SwitchCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return Switch

    def __init__(self, connector, path, redfish_version=None):
        """A class representing an Endpoint

        :param connector: A Connector instance
        :param path: The canonical path to the Switch collection resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(SwitchCollection, self).__init__(connector, path,
                                               redfish_version)
