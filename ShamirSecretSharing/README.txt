The first portion of the program serves to demonstrate that the proportion of
correctly reconstructed messages is independent of the message size.

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
