from shamir_share import share, reconstruct
from numpy.random import randint, choice

message_space = 100
message = randint(message_space, size = 5)
print "messages are: "
print message

res = [share(m, 3, 7) for m in message]
shares, p = zip(*res)

print "NOW TESTING FOR SUCCESS"
for i in range(5):
    print "Now testing message {}".format(i+1)
    print "Message share is {} with prime {}".format(shares[i], p[i])
    idx = choice(7, 3, replace=False)
    sample = [shares[i][j] for j in idx]
    res = int(reconstruct(sample, p[i]))
    print "Original message is {}".format(message[i])
    print "Reconstructed message is {}".format(res)
    if res == message[i]:
        print "Message successfully retrieved"
    else:
        print "Reconstruction failed"
    print ""

print "NOW TESTING FOR FAILURE"
for i in range(5):
    print "Now testing message {}".format(i+1)
    print "Message share is {} with prime {}".format(shares[i], p[i])
    idx = choice(7, 2, replace=False)
    sample = [shares[i][j] for j in idx]
    res = int(reconstruct(sample, p[i]))
    print "Original message is {}".format(message[i])
    print "Reconstructed message is {}".format(res)
    if res == message[i]:
        print "Message successfully retrieved"
    else:
        print "Reconstruction failed"
    print ""
