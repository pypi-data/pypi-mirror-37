#    Copyright 2010 OpenStack LLC
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

from manila import test
from manila.tests import utils as test_utils


class TestUtilsTestCase(test.TestCase):
    def test_get_test_admin_context(self):
        """get_test_admin_context's return value behaves like admin context."""
        ctxt = test_utils.get_test_admin_context()

        # TODO(soren): This should verify the full interface context
        # objects expose.
        self.assertTrue(ctxt.is_admin)
