#!/usr/bin/env python
# Copyright 2018 Criteo
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import print_function

from tests import test_utils as bg_test_utils  # noqa

bg_test_utils.prepare_graphite_imports()  # noqa

import unittest

from carbon import database
from carbon import conf as carbon_conf

from biggraphite import metric as bg_metric
from biggraphite.plugins import carbon as bg_carbon
import objgraph
import time
from biggraphite import accessor as bg_accessor
from biggraphite.drivers import cassandra as bg_cassandra
from tests.drivers.base_test_metadata import BaseTestAccessorMetadata
from tests.test_utils_cassandra import HAS_CASSANDRA
from tests import test_utils as bg_test_utils



_TEST_METRIC = "a.b.c"


@unittest.skipUnless(HAS_CASSANDRA, "CASSANDRA_HOME must be set to a >=3.5 install")
class TestAccessorWithCassandraData(bg_test_utils.TestCaseWithAccessor):
    def test_carbon_flow(self):
        self._plugin = bg_carbon.BigGraphiteDatabase(carbon_conf.Settings())
        self._plugin._accessor = self.accessor

        objgraph.show_growth(limit=1000)

        points = [(1, 42)]

        self._plugin.exists(_TEST_METRIC)
        self._plugin.create(_TEST_METRIC, retentions=[(1, 60)], xfilesfactor=0.5, aggregation_method="sum")
        metric_before_write = self._plugin._cache.get_metric(_TEST_METRIC)
        self._plugin.write(_TEST_METRIC, points)
        self._plugin._createOneMetric()
        metric_after_write = self._plugin._cache.get_metric(_TEST_METRIC)

        objgraph.show_growth(limit=1000)
        objgraph.show_refs([metric_after_write], filename='am.png')
        objgraph.show_refs([metric_before_write], filename='bm.png')
        objgraph.show_backrefs([metric_after_write], filename='abm.png')
        objgraph.show_backrefs([metric_before_write], filename='bbm.png')

if __name__ == "__main__":
    unittest.main()
