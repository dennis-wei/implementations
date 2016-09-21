"""
robin_hash_test.py

This program just tests that the basic functionalities of the RobinHash hash
map are working. Maybe I'll implement unit tests later.
"""

from __future__ import division
from robin_hash import RobinHash
import random
import string

# Initialization
print "Initializing Hash Map"
rh = RobinHash(10)

# set and get
print "Inserting first entry"
assert rh.set('one', 1) == True
assert rh.get('one') == 1
assert rh.load() == 0.1

# another set and get
print "Inserting second entry"
assert rh.set('two', 2) == True
assert rh.get('two') == 2
assert rh.load() == 0.2

# override a key: value pair, test multiple data types
print "Overriding first entry"
assert rh.set('one', 'one') == True
assert rh.get('one') == 'one'

# deletion
print "Deleting first entry"
assert rh.delete('one') == 'one'
assert rh.load() == 0.1
print "Deleting second entry"
assert rh.delete('two') == 2
assert rh.load() == 0

print "Inserting to fill map"
hash_function = lambda _: 8
for i in range(10):
    assert rh.set(str(i), i) == True
    assert rh.load() == (i + 1) / 10
assert rh.set('11', 11) == False
assert rh.set('7', 'seven') == True

# Run a bunch of sort of random functions to hopefully catch any bugs, edge
#   cases, or obscure failures

def _get_random_string():
    valid_chars = string.ascii_letters + string.digits
    r_str = ""
    length = random.randint(1, 20)
    for i in range(length):
        r_str += random.choice(valid_chars)
    return r_str

print "\nRunning randomized experiments\n"
rh = RobinHash(512)
random_keys = []
for i in range(1000):
    key = _get_random_string()
    value = _get_random_string()
    assert rh.set(key, value) or rh.load() == 1
    if random.random() < 0.3 and rh.load() != 1:
        random_keys.append(key)
    if random.random() < 0.05:
        for key in random_keys:
            assert rh.get(key)
            if random.random() < 0.5:
                assert rh.set(key, _get_random_string())
                assert rh.get(key)
            else:
                rh.delete(key)
                assert not rh.get(key)
        random_keys = []
    if random.random() < .05:
        rh.get(_get_random_string())
    if random.random() < 0.1:
        new_key = _get_random_string()
        rh.delete(new_key)
        if new_key in random_keys:
            random_keys.remove(new_key)
print "After experiments, load is: ", rh.load()
print "Max Probe Distance is: ", rh.max_probe


print "All tests successful!"
