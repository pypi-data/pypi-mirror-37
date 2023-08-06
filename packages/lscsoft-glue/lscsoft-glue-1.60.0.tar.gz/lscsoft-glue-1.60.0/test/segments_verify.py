#!/usr/bin/env python

import sys
import unittest
import warnings


class TestSegmentsWarning(unittest.TestCase):
    def test_warning(self):
        with warnings.catch_warnings(record=True) as ctx:
            warnings.simplefilter('always')
            from glue import segments
        self.assertIn('ligo.segments', str(ctx[0].message))


class TestSegments(unittest.TestCase):
    def test_sanity(self):
        with warnings.catch_warnings() as ctx:
            warnings.filterwarnings('ignore', category=DeprecationWarning)
            from glue import segments
        a = segments.segment(1, 2)
        b = segments.segment(3, 4)
        l = segments.segmentlist([a, b])
        d = segments.segmentlistdict()
        d['a'] = segments.segmentlist([a])
        d['b'] = segments.segmentlist([b])
        self.assertEqual(d['a'], l[:1])
        self.assertEqual(d['b'], l[1:])


# run the tests
if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSegmentsWarning))
    suite.addTest(unittest.makeSuite(TestSegments))

    if not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful():
        sys.exit(1)
