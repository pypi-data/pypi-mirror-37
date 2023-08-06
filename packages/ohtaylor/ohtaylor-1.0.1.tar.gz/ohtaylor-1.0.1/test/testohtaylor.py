
import unittest

from testnum import TestNumericalTaylor  # noqa
from testsym import TestSymbolicTaylor   # noqa
from testutils import TestTaylorUtils    # noqa
from testdiffcalc import TestDiffCalc    # noqa


def main():
    unittest.main()


if __name__ == "__main__":
    main()
