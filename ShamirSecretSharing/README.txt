~~~ shamir_share.py ~~~
This module serves to implement a Shamir Secret Sharing Scheme.
It uses Mersenne primes to construct a field based on the message space.
It uses scipy's lagrange interpolation to reconstruct the message.
USAGE:
    To construct shares, run shamir_share.py's share function
        share(message, t, n)
    To reconstruct the message, run shamir_share.py's reconstruct function
        reconstruct(shares, p) where shares is a list of exactly t shares and
        p is the first Mersenne prime larger than the message
The program currently only supports integer messages, so to encode, for example,
a string message, one would have to convert the string to an integer somehow,
while keeping mindful of Python's 64-bit limit on integers.

~~~ polynomials.py ~~~
This module does the polynomial work behind the algorithm, such as
generating the random polynomial, evaluating the polynomial to produce shares,
and interpolating the shares into a polynomial

~~~ prime.py ~~~
This module essentially contains a list of Mersenne primes and finds the first
one larger than the message

~~~ test_drive.py ~~~
This program randomly constructs and shares messages before testing that
the reconstruction succeeds with t shares and fails with t-1 shares.
At the moment, reconstruction is rather unreliable. See test_proportion_success.py
for statistical tests on reconstruction success rate.

~~~ test_proportion_success ~~~
The first portion of the test_proportion_success program serves to demonstrate that
the proportion of correctly reconstructed messages is independent of the message size.

10 iterations of 1000 messages are created. The outputted result for each message
size is the mean proportion of the proportion from each iteration. For each
message, a 3-out-of-5 sharing scheme is created.

The low variance of these proportions seems to suggest that the message size
does not affect the reconstruction success rate.


The purpose of the second segment of the program is to determine the relationship
between (t, n) pairs and reconstruction success rate.

Eight values of t are tested, with n ranging from t to 20 for each t.
This time, for each (t, n) pair, 5 iteration of 1000 messages each are drawn.
The outputted proportion for each (t, n) pair is the mean of these iteration proportions.

In general, as t and n increase, the reconstruction success rate goes down,
seemingly in exponential fashion. This is likely due to scipy's lagrange
implementation being numerically unstable as the number of points being
interpolated on increases
