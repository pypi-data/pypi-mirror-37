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

import os
import unittest
import time
from itertools import product
from string import ascii_lowercase
from distutils import version
from cassandra import util
from datetime import datetime, timedelta
import gc
import objgraph

from biggraphite import accessor as bg_accessor
from biggraphite import metric as bg_metric
from biggraphite.drivers import cassandra as bg_cassandra
from tests.drivers.base_test_metadata import BaseTestAccessorMetadata
from tests.test_utils_cassandra import HAS_CASSANDRA
from tests import test_utils as bg_test_utils

PAGESIZE = os.sysconf('SC_PAGESIZE')

@unittest.skipUnless(HAS_CASSANDRA, "CASSANDRA_HOME must be set to a >=3.5 install")
class TestAccessorWithCassandraData(bg_test_utils.TestCaseWithAccessor):
    def test_fetch(self):
        metricsp2 = [''.join(i) for i in product(ascii_lowercase, repeat = 3)]
        metrics = []

        d = datetime.today() - timedelta(days=5)
        for m in metricsp2:
            metric = bg_test_utils.make_metric("test.metric."+ m)
            metric.updated_on = d
            self.accessor.create_metric(metric)
            metrics.append(metric)

        del metricsp2
        gc.collect()

        objgraph.show_growth(limit=10)

        gc_count = 0
        for i in range(5):
            for m in metrics:
                self.accessor.touch_metric(m)
                m.updated_on = d
                if gc_count > 1000:
                    gc.collect()
                    gc_count = 0
                else:
                    gc_count = gc_count + 1
            objgraph.show_growth()

        gc.collect()

        print("{} total".format(len(metrics)))

if __name__ == "__main__":
    unittest.main()
