
import unittest
import math
import sympy

from sympy.abc import x, y, z

from ohtaylor.taylorutils import nkparts, \
    ktuples_nsum, factorial_tuple, create_symbol_point_list, sort_symbols


# Test the utility function that calculates the tuples of partitions
class TestTaylorUtils(unittest.TestCase):

    # Test that tuples sum works the way we want it to
    def test_tuples_sum(self):
        data = list(ktuples_nsum(0, 0))
        self.assertEqual((), data[0])

        # Singleton should only create a single value
        data = list(ktuples_nsum(1, 1))
        self.assertEqual(1, len(data))
        self.assertEqual((1,), data[0])
        self.assertEqual(1, nkparts(1, 1))

        # Check that all the permutations are generated
        data = list(ktuples_nsum(2, 2))
        self.assertEqual(3, len(data))
        self.assertTrue((2, 0) in data)
        self.assertTrue((0, 2) in data)
        self.assertTrue((1, 1) in data)
        self.assertEqual(3, nkparts(2, 2))

        self.assertEqual(2, nkparts(2, 1))
        data = list(ktuples_nsum(3, 2))
        self.assertEqual(len(data), nkparts(3, 2))

        data = list(ktuples_nsum(4, 12))
        self.assertTrue((3, 3, 3, 3) in data)
        self.assertTrue((0, 0, 12, 0) in data)
        self.assertEqual(len(data), nkparts(4, 12))
        # Check that there are no duplicates
        self.assertEqual(len(data), len(set(data)))

    # Test taking the factorial of a tuple
    def test_factorial_tuple(self):
        t = (1, 2, 3)
        v = math.factorial(1) * math.factorial(2) * math.factorial(3)
        self.assertEqual(v, factorial_tuple(t))

        t = (3, 2, 1, 5, 7)
        v = math.factorial(3) * math.factorial(2) * \
            math.factorial(5) * math.factorial(7)
        self.assertEqual(v, factorial_tuple(t))

    # Sort symbol list and check we have symbols that are sorted by
    # their string representation
    def test_symbols_sort(self):
        f = z + y + x
        sl = list(f.free_symbols)
        sl = sort_symbols(sl)
        self.assertEqual([x, y, z], sl)
        self.assertEqual([x, y, z], sort_symbols([z, y, x]))

        pi = sympy.symbols('pi')
        theta = sympy.symbols('theta')
        kappa = sympy.symbols('kappa')
        sl = sort_symbols([kappa, theta, pi])
        self.assertEqual([kappa, pi, theta], sl)

    # Check that the symbol-point list is created correctly
    def test_create_symbol_point_list(self):
        f = z + y + x
        x0 = [1, 2, 3]
        self.assertEqual([(x, 1), (y, 2), (z, 3)],
                         create_symbol_point_list(f.free_symbols, x0))

        l1 = [(z, 3), (y, 2), (x, 1)]
        self.assertEqual(l1, create_symbol_point_list(f.free_symbols, l1))
