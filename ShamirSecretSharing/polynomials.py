import numpy as np
import random
from scipy.interpolate import lagrange

"""
Gets the coefficients for a random polynomial of degree t-1
Parameters:
    t: threshold of reconstruction
    p: the prime to be used as the field size
Returns:
    coefs: random sample of (t-1) integers to be used as coefficients
"""

def get_random_coefs(t, p):
    return random.sample(xrange(p), t - 1)

"""
Produces n shares by evaluating the polynomial determined by the coefficients
Parameters:
    coefs: list of coefficients of the polynomial, with coefs[0] being the message
    n:     number of shares to be produced
    p:     the prime to be used as the field size
Returns:
    shares: list of tuples (i, s) where
        i is the x value of the share in the polynomial
        s is the y value of the share
"""

def produce_shares(coefs, n, p):
    t = len(coefs)
    arr = np.zeros((n, t), dtype=int)
    x_range = range(1, n + 1)
    for i in x_range:
        for j in range(t):
            arr[i-1][j] = pow(i, j)
    raw_shares = np.dot(arr, coefs)
    modular_shares = map(lambda x: x % p, raw_shares)
    return zip(x_range, modular_shares)

"""
Interpolates the k-1 degree polynomial produced by k shares
Parameters:
    shares: see produce_shares
    p:      the prime used as the field size
Returns:
    m: f(0), where f is the polynomial interpolated
        should reconstruct the message if the number of shares given is correct
"""

def interpolate(shares, p):
    x, y = zip(*shares)
    lag = lagrange(x, y)
    return lag(0) % p
