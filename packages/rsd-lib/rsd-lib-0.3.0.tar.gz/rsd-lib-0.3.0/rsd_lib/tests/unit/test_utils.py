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

import testtools

from rsd_lib import utils as rsd_lib_utils


class UtilsTestCase(testtools.TestCase):

    def test_get_resource_identity(self):
        self.assertIsNone(rsd_lib_utils.get_resource_identity(None))
        self.assertIsNone(rsd_lib_utils.get_resource_identity({}))
        self.assertEqual(
            '/redfish/v1/Systems/437XR1138R2/BIOS',
            rsd_lib_utils.get_resource_identity({
                "@odata.id": "/redfish/v1/Systems/437XR1138R2/BIOS"}))

    def test_int_or_none(self):
        self.assertIsNone(rsd_lib_utils.int_or_none(None))
        self.assertEqual(0, rsd_lib_utils.int_or_none('0'))
        self.assertEqual(1, rsd_lib_utils.int_or_none('1'))
