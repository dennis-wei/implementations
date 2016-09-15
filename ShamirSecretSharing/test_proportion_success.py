from __future__ import division
from shamir_share import share, reconstruct
from numpy.random import randint, choice
from termcolor import colored
import itertools
import matplotlib.pyplot as plt
import numpy as np

print colored("Now testing message sizes.", "red")
message_sizes = [10**n for n in range(2, 8)]
print colored("All message size: {}".format(message_sizes), "cyan")
NUM_SAMPLES = 1000
t = 3
n = 5
NUM_PROPORTIONS = 10
mean_proportions = []
for message_size in message_sizes:
    props = []
    for i in range(NUM_PROPORTIONS):
        # Generate random messages
        message = randint(message_size, size = NUM_SAMPLES)
        res = [share(m, t, n) for m in message]
        shares, p = zip(*res)

        # calculate proportion of correctly reconstructed messages
        count = 0
        for i in range(NUM_SAMPLES):
            idx = choice(n, t, replace=False)
            sample = [shares[i][j] for j in idx]

            res = int(reconstruct(sample, p[i]))
            if res == message[i]:
                count += 1

        props.append(count / NUM_SAMPLES)

    # Take the average of the proportions
    mean_prop = np.mean(props)
    mean_proportions.append(mean_prop)
    print "Results for message_size = {}: {}".format(message_size, mean_prop)

print colored("Total proportion mean: {}".format(np.mean(mean_proportions)), "green")
print colored("Total proportion variance: {}".format(np.var(mean_proportions)), "green")

print ""

print colored("Now calculating proportions.", "red")
# Maximum message
MESSAGE_SPACE = 10000
# Number of messages to be created
NUM_SAMPLES = 1000
# threshold range
T_RANGE = (2, 10)
# Number of times to run each (t, n) pair. Final y value is the average of these trials
NUM_PROPORTIONS = 5
# Upper range for n. Guarantee minimum 20 - t_range[1] points for each line
N_MAX = 20

# Iterate through (t, n) pairs
for t in range(*T_RANGE):

    # Keep track of points to plot
    x_points = []
    y_points = []

    for n in range(t, N_MAX):

        # Keep track of proportions to average
        props = []
        for i in range(NUM_PROPORTIONS):
            # Generate random messages
            message = randint(MESSAGE_SPACE, size = NUM_SAMPLES)
            # Get shares for each message
            res = [share(m, t, n) for m in message]
            shares, p = zip(*res)

            # calculate proportion of correctly reconstructed messages
            count = 0
            for i in range(NUM_SAMPLES):
                idx = choice(n, t, replace=False)
                sample = [shares[i][j] for j in idx]

                res = int(reconstruct(sample, p[i]))
                if res == message[i]:
                    count += 1

            props.append(count / NUM_SAMPLES)

        # Take the average of the proportions
        mean_prop = np.mean(props)
        print "Results for t = {} and n = {}: {}".format(t, n, mean_prop)
        x_points.append(n)
        y_points.append(mean_prop)

    # Add line for t to plot
    plt.plot(x_points, y_points, linewidth=2.0, \
                linestyle = "--", label="t = {}".format(t))

# Plot
print colored("Now Plotting.", "red")
plt.xlabel('n')
plt.ylabel('p')
plt.title('Reconstruction Sucess Rate')
plt.legend()
plt.show()
