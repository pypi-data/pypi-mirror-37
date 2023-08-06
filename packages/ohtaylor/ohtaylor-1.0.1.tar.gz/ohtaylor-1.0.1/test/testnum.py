
import unittest
import sympy
from sympy.abc import x, y, z

from ohtaylor import taylor
from ohtaylor.taylornum import check_taylornum_RN_R
from ohtaylor.taylorutils import ktuples_nsum
from ohtaylor.diffcalc import DiffCalcCached


# return value has a string if false and just true when
def get_flag(val):
    if isinstance(val, tuple):
        return val[0]
    else:
        return val


# Test the numerical Taylor series calculation
class TestNumericalTaylor(unittest.TestCase):

    # Test the single variable exponential function
    def test_exp_single_var(self):
        # Linear approximation of e^x at 0.
        # Should be e^0 + e^0*dt
        f = [1, 1]
        dt = 0.1
        self.assertAlmostEqual(1.1, taylor(f, dt))

        # Quadratic approximation of e^x at 0
        # Should be e^0 + e^0*dt + e^0*dt^2
        f = [1, 1, 1]
        dt = 0.1
        self.assertAlmostEqual(1.105, taylor(f, dt))

    # Test the single variable sine Taylor series expansion
    def test_sine_single_var(self):
        # Linear approximation of sin(x) at 0
        # Should be sin(0) + cos(0)*dt
        f = [0, 1]
        dt = 0.1
        self.assertAlmostEqual(0.1, taylor(f, dt))

        # Quadratic approximation of sin(x) at 0
        # Should be sin(0) + cos(0)*dt + sin(0)*dt^2
        f = [0, 1, 0]
        dt = 0.1
        self.assertAlmostEqual(0.1, taylor(f, dt))

    # Test when we have multiple R->R^M.
    # The input data for f is a list, then we  know it has
    # multi-dimensional output
    def test_R_to_R2(self):
        f1 = (1, 1, 1)
        dt1 = 0.1
        f2 = (0, 1)
        dt2 = 0.1
        solution = (1.105, 0.1)
        self.assertAlmostEqual(solution[0], taylor((f1, f2), (dt1, dt2))[0])
        self.assertAlmostEqual(solution[1], taylor((f1, f2), (dt1, dt2))[1])

    # Check that the checker for the dictionary input works
    # and that it fails on bad input
    def test_rn_r_dict_check(self):
        # Check dictionary without tuple
        fn = {}
        fn[0] = 1
        self.assertFalse(check_taylornum_RN_R(fn)[0])

        # Check not all are tuples
        fn.clear()
        fn[(0,)] = 1
        fn[0] = 1
        self.assertFalse(check_taylornum_RN_R(fn)[0])

        # Check different size tuples
        fn.clear()
        fn[(0,)] = 1
        fn[(0, 1)] = 1
        self.assertFalse(check_taylornum_RN_R(fn)[0])

        # Check that all the partial derivatives are present
        fn.clear()
        fn[(0, 0, 0)] = 1
        fn[(0, 1, 0)] = 1
        fn[(0, 0, 1)] = 1
        self.assertFalse(check_taylornum_RN_R(fn)[0])

        # Check that we are missing some of the partial derivatives
        fn.clear()
        fn[(0,)] = 1
        fn[(2,)] = 1
        self.assertFalse(check_taylornum_RN_R(fn)[0])

        # Check a good one that is R->R
        fn.clear()
        fn[(0,)] = 1
        fn[(1,)] = 1
        fn[(2,)] = 1
        self.assertTrue(check_taylornum_RN_R(fn)[0])

    # When the first variable is a dictionary, then we assume
    # that all the derivatives are given as tuples in the dictionary
    def test_rn_tor(self):
        # Simple single variable case
        fn = {}
        fn[(0,)] = 1
        fn[(1,)] = 1
        fn[(2,)] = 1
        dt = (0.1,)

        val = taylor(fn, dt)
        self.assertAlmostEqual(1.105, val)

        # This is from the function exp(x+y) and we want it to close to exp
        fn.clear()
        fn[(0, 0)] = 1
        fn[(1, 0)] = 1
        fn[(0, 1)] = 1
        fn[(2, 0)] = 1
        fn[(1, 1)] = 1
        fn[(0, 2)] = 1
        dt = (0.05, 0.05)
        val = taylor(fn, dt)
        self.assertAlmostEqual(1.105, val)
        dt = (0.01, 0.09)
        self.assertAlmostEqual(1.105, taylor(fn, dt))

    # Sending symbols rather than dt.
    # Technically (x - x0) = (x0 + dt - x0) = dt
    def test_dt_as_sym(self):
        # Simple single variable case
        fn = dict()
        fn[(0,)] = 1
        fn[(1,)] = 1
        fn[(2,)] = 1

        val = taylor(fn, (x,))
        px = taylor(sympy.exp(x), n=2, x0=0)
        self.assertEqual(val, px)

    # Function to compute all the derivatives of a function at a given point
    # and given n Return a dictionary of the values of the derivatives for
    # the corresponding tuples
    @staticmethod
    def compute_derivative(f, n, x0):
        # Dictionary where we will store the values
        fvals = {}
        # Derivative calculator
        d = DiffCalcCached()

        # Unzip the values
        syms, _ = zip(*x0)

        for i in range(0, n+1):
            # Create the list for tuples for this derivative
            tuples = ktuples_nsum(len(syms), i)
            for t in tuples:
                # Calculate the derivatives and add it to the dictionary
                fi = d.diff(f, syms, t)
                fix = (fi.subs(x0)).evalf()
                fvals[t] = fix
        return fvals

    # Test that the compute derivatives symbolically to compute the dictionary
    # works correctly.
    def test_compute_derivatives(self):
        # Check that all the derivatives of exp(x) are 1
        f = sympy.exp(x)
        d = self.compute_derivative(f, 3, tuple(zip((x,), (0,))))
        self.assertEqual(4, len(d))
        self.assertAlmostEqual(1.0, d[(0,)])
        self.assertAlmostEqual(1.0, d[(1,)])
        self.assertAlmostEqual(1.0, d[(2,)])
        self.assertAlmostEqual(1.0, d[(3,)])

        # Check that derivatives of higher dimensions are calculated correctly
        f = sympy.exp(x*y)
        d = self.compute_derivative(f, 2, tuple(zip((x, y), (0, 0))))
        self.assertEqual(6, len(d))
        self.assertAlmostEqual(1.0, d[(1, 1)])

    # Make sure that the sym and num produce the same results
    # for the given polynomials
    def test_num_with_sym(self):
        # Function that we will like to test out to
        f1 = sympy.exp(x + y)
        f2 = sympy.cos(x ** 2 + y + z)
        x0 = (0, 0)
        x1 = (0, 0, 1)

        # Create the numerical values for the partial derivatives from what
        # was calculated and check if they match up
        n = 6
        syms = (x, y)
        fvals1 = self.compute_derivative(f1, n, tuple(zip(syms, x0)))
        dt1 = (0.1, 0.1)
        pxn1 = taylor(fvals1, dt1)
        vals = tuple(map(lambda x, y: x+y, x0, dt1))
        self.assertAlmostEqual(f1.subs(tuple(zip(syms, vals))), pxn1)

        # Check the two dimensional values
        n = 7
        syms = (x, y, z)
        fvals2 = self.compute_derivative(f2, n, tuple(zip(syms, x1)))

        # Use the calculated values for Taylor series numerical approximation
        dt2 = (0.1, 0.1, 0.1)
        x1dt = tuple(map(lambda x, y: x+y, x1, dt2))
        px = f2.subs(tuple(zip(syms, x1dt))).evalf()
        pxn2 = taylor(fvals2, dt2)
        self.assertAlmostEqual(px, pxn2)

        # f is R^3->R^2
        f = (fvals1, fvals2)
        px = taylor(f, (dt1, dt2))
        self.assertAlmostEqual(pxn1, px[0])
