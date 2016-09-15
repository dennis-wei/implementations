from __future__ import division
from shamir_share import share, reconstruct
from numpy.random import randint, choice
from termcolor import colored

# Maximum message
message_space = 10000
# Number of messages to be created
num_samples = 3
# threshold
t = 2
# total shares
n = 5

# Create random messages
message = randint(message_space, size = num_samples)

print "MESSAGES ARE: {}".format(message)
print ""

# Produce shares for each message
res = [share(m, t, n) for m in message]
# Unpacks list(shares), list(primes) values into a list of (share, prime) tuples
shares, p = zip(*res)

print colored("NOW TESTING FOR SUCCESS", "cyan")
count = 0
for i in range(num_samples):
    print colored("Now testing message {}: {}".format(i+1, message[i]), "magenta")
    print "Message share is {} with prime {}".format(shares[i], p[i])

    # Get random sample of three shares
    idx = choice(n, t, replace=False)
    sample = [shares[i][j] for j in idx]

    print "Sample shares are {}".format(sample)
    res = int(reconstruct(sample, p[i]))
    print "Original message is {}".format(message[i])
    print "Reconstructed message is {}".format(res)

    if res == message[i]:
        print colored("Message successfully retrieved", "green")
    else:
        print colored("Reconstruction failed", "red")
    print ""


print colored("NOW TESTING FOR FAILURE", "cyan")
for i in range(num_samples):
    print colored("Now testing message {}: {}".format(i+1, message[i]), "magenta")
    print "Message shares are {} with prime {}".format(shares[i], p[i])

    # Get random unqualified share set
    idx = choice(n, t-1, replace=False)
    sample = [shares[i][j] for j in idx]

    print "Sample shares are {}".format(sample)
    res = int(reconstruct(sample, p[i]))
    print "Original message is {}".format(message[i])
    print "Reconstructed message is {}".format(res)

    if res == message[i]:
        print colored("Message retrieved by luck", "red")
    else:
        print colored("Yay, reconstruction failed!", "green")
    print ""
