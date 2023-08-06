
import sympy


# Calculate the derivatives using diff and indices in the tuple
class DiffCalc:
    # Take the derivative of the function f according to the tuple t
    # with the order given in x
    @staticmethod
    def diff(f, x, t):
        k = len(x)
        fix = f

        for j in range(0, k):
            fix = sympy.diff(fix, x[j], t[j])

        return fix


# Calculate the derivatives but try to cache previous derivatives
class DiffCalcCached:
    # Find a tuple that is one smaller in sum. It will go from left to right
    # to reduce the sum. If a value is 0, it will move to the right one step
    @staticmethod
    def get_smaller_tuple(t):
        val = sum(t)

        # If the sum is zero, then we cannot find a smaller tuple
        if val == 0:
            return -1, t

        for i in range(0, len(t)):
            if t[i] > 0:
                return i, t[:i] + (t[i] - 1,) + t[i+1:]

    def __init__(self):
        # Cached values of previous diffs from tuples of lower sum
        self.diff_cache = {}
        # Last expression that we used to calculate the derivative
        self.last_expr = None

    def diff(self, f, x, t):
        # If the expression f changes, we clear the cache
        if f != self.last_expr:
            self.diff_cache.clear()
            self.last_expr = f

        # Nothing to take derivative of. Add f to the diff cache
        if sum(t) == 0:
            self.diff_cache[t] = f
            return f

        # Look up the cache to find a previously calculated derivative that we
        # just have to do one more diff of to get the derivative we want
        # If it is not found, just calculate the entire derivative
        # and add to cache
        i, st = DiffCalcCached.get_smaller_tuple(t)
        if st in self.diff_cache:
            dfi = self.diff_cache[st]
            df = sympy.diff(dfi, x[i])
        else:
            df = DiffCalc.diff(f, x, t)

        # Add the calculated derivative to the cache
        self.diff_cache[t] = df
        return df
