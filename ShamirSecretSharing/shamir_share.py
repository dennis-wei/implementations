from prime import get_larger_prime
from polynomials import get_random_coefs, produce_shares, interpolate

def share(message, t, n):
    if n < t:
        print "n < t"
        return None

    p = get_larger_prime(message)

    coefs = [message] + get_random_coefs(t, p)
    shares = produce_shares(coefs, n, p)
    return shares, p

def reconstruct(shares, p):
    message_number = interpolate(shares, p)
    return message_number
