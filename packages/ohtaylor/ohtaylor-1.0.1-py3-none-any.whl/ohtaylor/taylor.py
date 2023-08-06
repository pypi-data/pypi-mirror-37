
import sympy
import numbers

from .taylornum import taylornum
from .taylorsym import taylorsym


# Calculate the taylor series.
# This is the main routing function that determines symbolic or
# numerical Taylor series and where to send the data to
def taylor(f, x0, n=None):
    # If n is None, then we know that this is a numeric
    if n is None:
        return taylornum(f, x0)

    # Symbolic. Check that everytfalsehing is a symbol
    if isinstance(f, list) or isinstance(f, tuple):
            if all(isinstance(fi, tuple(sympy.core.all_classes))
                   or isinstance(fi, numbers.Number) for fi in f):
                if isinstance(x0, list) or isinstance(x0, tuple):
                    if len(f) == len(x0):
                        return taylorsym(f, x0, n)
                    else:
                        error_msg = 'ERROR: Size of f and x0 do not match'
                        raise RuntimeError(error_msg)
                else:
                    error_msg = 'x0 is not the same size as f'
                    raise RuntimeError(error_msg)
            else:
                emsg = 'ERROR: Expected list to be all symbolic expressions.'
                raise RuntimeError(emsg)
    elif isinstance(f, tuple(sympy.core.all_classes)) \
            or isinstance(f, numbers.Number):
        return taylorsym(f, x0, n)
    else:
        raise RuntimeError('ERROR: Expected symbolic expressions.')
