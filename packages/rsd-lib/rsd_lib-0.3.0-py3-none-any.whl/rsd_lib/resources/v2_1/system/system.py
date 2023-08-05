# Copyright 2018 Intel, Inc.
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

from sushy import exceptions
from sushy.resources.system import system

from rsd_lib.resources.v2_1.system import memory
from rsd_lib.resources.v2_1.system import network_interface
from rsd_lib.resources.v2_1.system import storage_subsystem
from rsd_lib import utils


class System(system.System):

    _memory = None  # ref to System memory collection instance
    _storage_subsystem = None  # ref to storage subsystem collection instance
    _network_interface = None  # ref to network interface collection instance

    def _get_memory_collection_path(self):
        """Helper function to find the memory path"""
        system_col = self.json.get('Memory')
        if not system_col:
            raise exceptions.MissingAttributeError(attribute='Memory',
                                                   resource=self._path)
        return utils.get_resource_identity(system_col)

    @property
    def memory(self):
        """Property to provide reference to `Metrics` instance

        It is calculated once the first time it is queried. On refresh,
        this property is reset.
        """
        if self._memory is None:
            self._memory = memory.MemoryCollection(
                self._conn, self._get_memory_collection_path(),
                redfish_version=self.redfish_version)

        return self._memory

    def _get_storage_subsystem_collection_path(self):
        """Helper function to find the storage subsystem path"""
        storage_subsystem_col = self.json.get('Storage')
        if not storage_subsystem_col:
            raise exceptions.MissingAttributeError(
                attribute='StorageSubsystem',
                resource=self._path)
        return utils.get_resource_identity(storage_subsystem_col)

    @property
    def storage_subsystem(self):
        """Property to provide reference to `StorageSubsystem` instance

        It is calculated once the first time it is queried. On refresh,
        this property is reset.
        """
        if self._storage_subsystem is None:
            self._storage_subsystem = storage_subsystem.\
                StorageSubsystemCollection(
                    self._conn, self._get_storage_subsystem_collection_path(),
                    redfish_version=self.redfish_version)
        return self._storage_subsystem

    def _get_network_interface_collection_path(self):
        """Helper function to find the network interface path"""
        network_interface_col = self.json.get('EthernetInterfaces')
        if not network_interface_col:
            raise exceptions.MissingAttributeError(
                attribute='NetworkInterface',
                resource=self._path
            )
        return utils.get_resource_identity(network_interface_col)

    @property
    def network_interface(self):
        """Property to provide reference to `NetworkInterface` instance

        It is calculated once the first time it is queried. On refresh,
        this property is reset.
        """
        if self._network_interface is None:
            self._network_interface = network_interface.\
                NetworkInterfaceCollection(
                    self._conn, self._get_network_interface_collection_path(),
                    redfish_version=self.redfish_version
                )
        return self._network_interface

    def refresh(self):
        super(System, self).refresh()
        self._memory = None
        self._storage_subsystem = None
        self._network_interface = None


class SystemCollection(system.SystemCollection):

    @property
    def _resource_type(self):
        return System
