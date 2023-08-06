
import unittest

from ohtaylor.diffcalc import DiffCalc, DiffCalcCached
from sympy.abc import x, y, z


class TestDiffCalc (unittest.TestCase):

    # Test that unzipping works
    def test_unzipping(self):
        vars = zip([x, y, z], [1, 2, 3])
        vars, x0 = zip(*vars)
        self.assertEqual((x, y, z), vars)
        self.assertEqual((1, 2, 3), x0)

    # Check that the basic diff calculating works
    def test_basic_diff(self):
        d = DiffCalc()
        f = x**2 * y**2 * z**2
        df = d.diff(f, (x, y, z), (1, 1, 1))
        self.assertEqual(8*x*y*z, df)

    # Check that getting the smaller tuple value works
    def test_get_smaller_tuple(self):
        zt = DiffCalcCached.get_smaller_tuple((0, 0, 0))
        self.assertEqual((-1, (0, 0, 0)), zt)

        t2 = (1, 2, 3)
        t2r = DiffCalcCached.get_smaller_tuple(t2)
        self.assertEqual((0, (0, 2, 3)), t2r)

        t3 = (0, 3, 2)
        t3r = DiffCalcCached.get_smaller_tuple(t3)
        self.assertEqual((1, (0, 2, 2)), t3r)

    # Test the cached diff method
    def test_cached_diff(self):
        d = DiffCalcCached()
        f = x**2 * y**2 * z**2
        symbs = (x, y, z)
        f1 = d.diff(f, symbs, (0, 0, 0))
        self.assertEqual(f, f1)
        f1 = d.diff(f, symbs, (1, 0, 0))
        self.assertEqual(2*x * y**2 * z**2, f1)
        t = (2, 0, 0)
        i1, t1 = DiffCalcCached.get_smaller_tuple(t)
        self.assertTrue(t1 in d.diff_cache)
        self.assertEqual(0, i1)
        f1 = d.diff(f, symbs, (2, 0, 0))
        self.assertEqual(2 * y ** 2 * z ** 2, f1)
        f1 = d.diff(f, symbs, (0, 0, 2))
        self.assertEqual(2 * y ** 2 * x ** 2, f1)
