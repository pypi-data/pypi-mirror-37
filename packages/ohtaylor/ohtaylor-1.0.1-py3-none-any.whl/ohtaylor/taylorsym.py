
import sympy
import numbers

from ohtaylor.taylorutils import ktuples_nsum, factorial_tuple, \
    create_symbol_point_list
from ohtaylor.diffcalc import DiffCalcCached


# Find the Taylor series when f:R^1 -> R^1
def taylorsym_1_1(x, f, x0, n):
    # If the input is given as a list or tuple of one variable,
    # change it to be a number
    if isinstance(x0, list) or isinstance(x0, tuple):
        x0 = x0[0]

    px = f.subs(x, x0)
    fi_1x = f

    for i in range(1, n+1):
        fix = sympy.diff(fi_1x, x)
        fi_1x = fix
        px += fix.subs(x, x0) / sympy.factorial(i) * (x - x0)**i
    return px


# Find the Taylor series for f:R^N -> R
def taylorsym_N_1(x, f, x0, n):
    # Number of input variables
    k = len(x)
    vars = create_symbol_point_list(x, x0)
    d = DiffCalcCached()
    syms, ivs = zip(*vars)

    # Generate the Taylor series
    px = 0
    for i in range(0, n+1):
        tuples = ktuples_nsum(k, i)
        for t in tuples:
            fix = d.diff(f, syms, t)
            fix = fix.subs(vars)
            for j in range(0, k):
                fix *= (syms[j] - ivs[j])**t[j]
            px += fix / factorial_tuple(t)
    return px


# Send to R^1 or R^n
def taylorsym_d(f, x0, n):
    if isinstance(f, numbers.Number):
        return f

    # Get the independent variables
    symbols = f.free_symbols

    # Dispatch to the right place
    if len(symbols) == 1:
        [x] = symbols
        return taylorsym_1_1(x, f, x0, n)
    else:
        return taylorsym_N_1(symbols, f, x0, n)


# Send each of the dimensions of R^M output to be evaluated independently
def taylorsym_l(f, x0, n):
    px = [None]*len(f)
    for i in range(0, len(f)):
        px[i] = taylorsym_d(f[i], x0[i], n)
    return px


# Figure out the dimensions and dispatch to the right Taylor series evaluation
# Check that the inputs are valid and match up
def taylorsym(f, x0, n):
    if isinstance(f, list) or isinstance(f, tuple):
        return taylorsym_l(f, x0, n)
    else:
        return taylorsym_d(f, x0, n)
