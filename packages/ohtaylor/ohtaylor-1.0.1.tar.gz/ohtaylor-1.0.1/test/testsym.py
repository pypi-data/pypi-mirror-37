
import unittest
import sympy
import math

from sympy.abc import x, y, z

from ohtaylor import taylor


# Check the symbolic evaluation of Taylor series
class TestSymbolicTaylor(unittest.TestCase):

    # Test the calculation of Taylor series for e^x
    def test_exp_single_var(self):
        # Given exp(x), the Taylor series for n=1 at x0=0 is 1 + 1(1-dx)
        x = sympy.symbols('x')
        f = sympy.functions.elementary.exponential.exp(x)
        x0 = 0
        px = taylor(f, x0, 1)
        self.assertTrue(px == x + 1)
        # Evaluate the function at some points and check values are correct
        self.assertAlmostEqual(1.1, px.evalf(subs={x: 0.1}))

        # When n=2, we have P(x) = 1 + x + x^2/2
        px = taylor(f, x0, 2)
        self.assertTrue(px == 1 + x + x**2/2)
        # Evaluate the function at a point
        self.assertAlmostEqual(1.105, px.evalf(subs={x: 0.1}))

        # Evaluate the value of exp(x) at 1 to calculate the value of e
        px = taylor(f, x0, 20)
        self.assertAlmostEqual(2.718281828459045, px.evalf(subs={x: 1}))

    # Test tje calculation of Taylor series for sin(x)
    def test_sine_single_var(self):
        # Evaluate the Taylor series of sin(x)
        f = sympy.functions.elementary.trigonometric.sin(x)
        x0 = 0
        px = taylor(f, x0, 1)
        self.assertTrue(px == x)
        px = taylor(f, x0, 2)
        self.assertTrue(px == x)
        px = taylor(f, x0, 3)
        self.assertTrue(px == x - x**3/6)

        # Evaluate sin(x) at 45 degrees with x0 at 0 and 1
        sin_pi_4 = math.sin(math.pi/4)
        self.assertAlmostEqual(sin_pi_4, taylor(f, 0, 10)
                               .evalf(subs={x: math.pi/4}))
        self.assertAlmostEqual(sin_pi_4, taylor(f, 1, 10)
                               .evalf(subs={x: math.pi/4}))

    # Test the calculation of Taylor series for [e^x e^x] at [0,1]
    def test_exp_1toM(self):
        # Evaluate the Taylor series of [e^x e^x]
        # which is just e^x repeated twice in a list
        f = [sympy.exp(x), sympy.exp(x)]
        x0 = [0, 1]
        px = taylor(f, x0, 2)
        self.assertTrue(px[0] == 1 + x + x ** 2 / 2)
        e_ = sympy.functions.elementary.exponential.exp(1)
        self.assertTrue(px[1] == e_ + e_*(x-1) + e_*(x - 1) ** 2 / 2)

    # Check the error handling of the taylor function when
    # the input is bad and when we mix expressions with numbers
    def test_bad_input(self):
        # Check that a number is just returned back
        self.assertEqual(1, taylor(1, 2, 3))
        self.assertEqual([1, 2.1], taylor([1, 2.1], [1, 2], 3))
        with self.assertRaises(RuntimeError):
            taylor([1, 2], 2, 3)
        with self.assertRaises(RuntimeError):
            taylor([1, x], 2, 3)
        with self.assertRaises(RuntimeError):
            taylor([[x], [x]], 2, 3)
        self.assertEqual([1, taylor(x**2, 1, 3)],
                         taylor([1, sympy.symbols('x')**2], [2, 1], 3))

    # Test the calculation of Taylor series for exp(xy)
    def test_exp_multi_var(self):
        f = sympy.functions.elementary.exponential.exp(x**2 + y)
        x0 = [0, 0]
        px = taylor(f, x0, 3)
        self.assertEqual(1 + y + x**2 + y**2/2 + x**2*y + y**3/6, px)

        # Check if this still works when we evaluate at exp((1,1))
        # and match to exp(2)
        px = taylor(f, x0, 10)
        self.assertAlmostEqual(math.exp(.2),
                               px.subs([(x, math.sqrt(.1)), (y, .1)]).evalf())

    def test_sin_multi_var(self):
        f = sympy.functions.elementary.trigonometric.sin(x + y)
        x0 = [0, 0]
        px = taylor(f, x0, 10)

        # Evaluate the value when x + y = 45 degrees (pi/4)
        # and then see if the value matches
        sin_pi_4 = math.sin(math.pi/4)
        sv = zip((x, y), (math.pi/8, math.pi/8))
        self.assertAlmostEqual(sin_pi_4, px.subs(sv).evalf())
        sv = zip((x, y), (3*math.pi / 4, -math.pi / 2))
        self.assertAlmostEqual(sin_pi_4, px.subs(sv).evalf())

    # Make a multi-variable sin(x+y) and check that output value is correct
    # when we plug in values

    # Check that calculating the Taylor series of a polynomial
    # is a polynomial itself
    def test_poly_multi_var(self):
        f = x**3 + 2*y - y**3 - 3*x
        x0 = [0, 0]
        px = taylor(f, x0, 10)
        self.assertTrue(px == f)

    # Function with three input variables and one output variable
    def test_multi_var_with_3_inputs(self):
        f = x ** 3 * y * z
        x0 = [1, 3, -2]
        px = taylor(f, x0, 5)
        xval = [(x, 1/2), (y, 2/3), (z, 1/2)]
        self.assertAlmostEqual(f.subs(xval), px.subs(xval))

    # Example from http://www.math.ubc.ca/~feldman/m226/taylor2d.pdf
    def test_sqrt_multi_var(self):
        f = sympy.sqrt(1 + y**2 + 4*x**2)
        x0 = [1, 2]
        # Send the values as a list of tuples
        # so that we know which part is x and y
        px = taylor(f, list(zip([x, y], x0)), 2)
        epx = 3 + sympy.Rational(4, 3)*(x-1) \
            + sympy.Rational(2, 3)*(y-2) \
            + sympy.Rational(10, 27)*(x-1)**2 \
            - sympy.Rational(8, 27)*(x-1)*(y-2) \
            + sympy.Rational(5, 54)*(y-2)**2
        self.assertTrue(sympy.expand(px) == sympy.expand(epx))

    # Test alternate symbols and give x0 as a list of tuples
    # that makes the points unambiguous
    def test_different_symbols_multi_var(self):
        pi = sympy.symbols('pi')
        theta = sympy.symbols('theta')
        kappa = sympy.symbols('kappa')
        f = sympy.sin(kappa) + sympy.cos(theta) + sympy.sin(3*pi)
        x0 = [2*math.pi/3, math.pi/3, 2*math.pi/3]
        px = taylor(f, list(zip([pi, theta, kappa], x0)), 13)

        xeval = [(pi, math.pi/2), (theta, math.pi/3), (kappa, math.pi/4)]
        self.assertAlmostEqual(f.subs(xeval).evalf(), px.subs(xeval).evalf())

    # Test R^N->R^M
    def test_rn_to_rm(self):
        f1 = sympy.functions.elementary.exponential.exp(x+y)
        f2 = sympy.functions.elementary.trigonometric.cos(x**2 + y + z)
        f = (f1, f2)
        x0 = [0, 0]
        x1 = (0, 0, 1)
        p = taylor(f, (x0, x1), 2)

        # Check that the components match up
        self.assertEqual(taylor(f1, x0, 2), p[0])
        self.assertEqual(taylor(f1, x0, 2), p[0])
        self.assertEqual(taylor(f2, x1, 2), p[1])

        # Check that the list notation also works
        p = taylor([f1, f2], [x0, x1], 2)
        self.assertEqual(taylor(f1, x0, 2), p[0])
        self.assertEqual(taylor(f2, x1, 2), p[1])

        f3 = sympy.functions.elementary.trigonometric.sin(y)
        x3 = (0,)
        p = taylor((f1, f2, f3), (x0, x1, x3), 2)
        self.assertEqual(taylor(f1, x0, 2), p[0])
        self.assertEqual(taylor(f2, x1, 2), p[1])
        self.assertEqual(taylor(f3, x3, 2), p[2])
