from prime import get_larger_prime
from polynomials import get_random_coefs, produce_shares, interpolate

"""
Produces the shares in a t-out-of-n shamir sharing scheme of a message
Parameters:
    message: The message to be encoded and shared. Must be an integer.
    t:       The threshold of reconstruction
    n:       The number of shares to produce
Returns:
    tuple (shares, p) where
        shares is a list of (x, y) coordinates
        p is the prime associated with the field those shares were produced in
"""

def share(message, t, n):
    if n < t:
        print "n < t"
        return None

    p = get_larger_prime(message)

    coefs = [message] + get_random_coefs(t, p)
    shares = produce_shares(coefs, n, p)
    return shares, p

"""
Reconstructs the message from a list of shares
Parameters:
    shares: list of (x, y) coordinates corresponding to shares
    p: the prime associated with the sharing scheme
Returns:
    message: the message
"""

def reconstruct(shares, p):
    message = interpolate(shares, p)
    return message
