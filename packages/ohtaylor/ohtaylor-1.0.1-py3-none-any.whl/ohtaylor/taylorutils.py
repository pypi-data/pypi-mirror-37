
import sympy


# Generator of tuples of size k that sum up to n using recursion
def ktuples_nsum(k, n):
    if k == 0 and n == 0:
        yield tuple()
        return
    if k == 1:
        yield (n,)
        return
    if n == 0:
        yield (0,)*k
        return

    for start in range(n, -1, -1):
        for qu in ktuples_nsum(k-1, n-start):
            yield (start,)+qu


# Calculate the number of tuples of size k that sum to n
# (number of tuples the above function calculates)
def nkparts(k, n):
    if k == 1:
        return 1
    if k == 2:
        return n + 1

    sum = 0
    for i in range(0, n+1):
        sum += nkparts(k-1, n-i)
    return sum


# For each of the integer in the tuple, calculate the factorial
# and multiply them together
def factorial_tuple(t):
    if isinstance(t, tuple):
        v = 1
        for i in range(0, len(t)):
            v *= sympy.factorial(t[i])
        return v
    else:
        raise RuntimeError("Input to the function must be a tuple")


# Sort the symbols by their
def sort_symbols(symbols):
    return sorted(symbols, key=lambda k: k.name)


# Create a list of tuples of symbols and values.
# If the input is already in that format,
# do nothing
def create_symbol_point_list(symbols, x0):
    # Check that the dimensions of symbols and x0 match up
    if len(symbols) != len(x0):
        emsg = "Dimension of x_0 doesn't match the number of symbols." \
               + "Symbols %d, x0: %d" \
               % (len(symbols),  len(x0))
        raise RuntimeError(emsg)

    # Check if x0 is already in the right format
    if all(type(x) is tuple and len(x) == 2 for x in x0):
        return x0

    vals = sort_symbols(symbols)
    return list(zip(vals, x0))
