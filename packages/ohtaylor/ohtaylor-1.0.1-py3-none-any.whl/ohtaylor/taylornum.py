
import math

from ohtaylor.taylorutils import nkparts, ktuples_nsum, factorial_tuple


def taylornum_R1_R1(fvals, dt):
    px = 0
    for i in range(0, len(fvals)):
        px += fvals[i] / math.factorial(i) * math.pow(dt, i)
    return px


# Check that the input dictionary in R^N->R is valid
def check_taylornum_RN_R(fvals):
    # Check that all the entries are tuples to floats
    if not all(isinstance(key, tuple) for key in fvals.keys()):
        return False, 'Entries not tuples'

    # Estimate n from the first tuple entry and check that all the tuples
    # have that length
    N = len(list(fvals.keys())[0])
    if not all(len(key) == N for key in fvals.keys()):
        return False, 'Tuple lengths not the same'

    # Check that the size of the dictionary is correct and that the right
    # number of partials are present
    K = 0
    sumk = 0
    # First get the length of the dictionary
    nentries = len(fvals)
    while sumk < nentries:
        sumk += nkparts(N, K)
        K += 1
    if sumk != nentries:
        return False, 'Number of entries are not consistent'

    # Check that all the partial derivatives are present for the given n
    for k in range(0, K):
        dtuples = ktuples_nsum(N, k)
        if not all(dtuple in fvals for dtuple in dtuples):
            return False, 'Missing derivative'

    return True, (N, K)


# Handle the case of going to one output dimension
def taylornum_RN_R(fvals, dt):
    # Check the we have good values in the dictionary
    f, v = check_taylornum_RN_R(fvals)
    if not f:
        raise RuntimeError(v)

    # Create the polynomial to evaluate the Taylor series
    N, K = v
    fdt = 0
    for k in range(0, K):
        tuples = ktuples_nsum(N, k)
        for t in tuples:
            fix = fvals[t]/factorial_tuple(t)
            for j in range(0, N):
                fix *= dt[j] ** t[j]
            fdt += fix

    return fdt


# Handle the case of RM multiple outputs
def taylornum_RN_RM(fvals, dt):
    if len(fvals) != len(dt):
        raise RuntimeError("Dimensions of f and dt do not agree")

    pdt = []
    for i in range(0, len(fvals)):
        if isinstance(fvals[i], dict):
            pdt.append(taylornum_RN_R(fvals[i], dt[i]))
        else:
            pdt.append(taylornum_R1_R1(fvals[i], dt[i]))
    return pdt


def taylornum(fvals, dt):
    if isinstance(fvals, dict):
        return taylornum_RN_R(fvals, dt)

    # List or tuple means that output is R^M. Dict means that input is also R^N
    if all(isinstance(fivals, (list, tuple, dict)) for fivals in fvals):
        return taylornum_RN_RM(fvals, dt)

    # This is a R->R function
    [pdt] = taylornum_RN_RM((fvals,), (dt,))
    return pdt
