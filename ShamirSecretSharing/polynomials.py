import numpy as np
import random
from scipy.interpolate import lagrange

def get_random_coefs(t, p):
    return random.sample(xrange(p), t - 1)

def produce_shares(coefs, n, p):
    t = len(coefs)
    shares = []
    arr = np.zeros((n, t), dtype=int)
    for i in range(1, n + 1):
        for j in range(t):
            arr[i-1][j] = pow(i, j)
    res = np.dot(arr, coefs)
    res = map(lambda x: x % p, res)
    return zip(range(1, n + 1), res)

def interpolate(shares, p):
    x, y = zip(*shares)
    lag = lagrange(x, y)
    return lag(0) % p
