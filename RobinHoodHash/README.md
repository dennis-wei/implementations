# Robin Hood Hash Map

This is a Hash Map I implemented for the KPCB Fellows application, Fall 2016.
The code can additionally be found on Github [here](https://github.com/dennis-wei/implementations/tree/master/RobinHoodHash).

### Background
Taking inspiration from the Rust Language, I decided to use a Robin Hood implementation. This implementation retains many of the benefits of simple linear probing (very low search, insertion, and deletion time given a good enough hashing algorithm) while improving on the actually time spent probing. The algorithm achieves this by greedily swapping elements during an insertion if the linear offset from an entry's original hash value is larger than that of the entry corresponding to the current index. What this accomplishes is very low mean probe length (indices iterated through to find an empty bucket), as inherited from traditional linear probing, as well as low variance on probe length due to the greedy swapping.

Additionally, I also implemented a backward shift deletion algorithm which essentially makes the table as if a key was never inserted. This outperforms traditional linear probing techniques because over time, multiple deletions can add significants amount of compute time due to the numerous tombstones that are created. By removing them from the table altogether, probing becomes considerably faster for tables with many deletions.

The references I used for the implementation of this algorithm are:  
_The original paper_ [[1]](https://cs.uwaterloo.ca/research/tr/1986/CS-86-14.pdf)  
_Emmanuel Goossaert's articles on the topic_ [[2]](http://codecapsule.com/2013/11/11/robin-hood-hashing/) [[3]](http://codecapsule.com/2013/11/17/robin-hood-hashing-backward-shift-deletion/)

### Included Files
`robin_hash.py` contains the entirety of the implementation, including the `RobinHash` class, a class for it's entries `RobinEntry`, and a hash function `hash_function` that can be overwritten.

`robin_hash_test` contains some generalized tests for the module. The first couple of portions simply test the basic functions (get, set, delete, load) in a small, contained hash map. The map is then filled to test for bugs at high load.  
The next portion runs a relatively highly randomized series of tests on a larger hash map in order to test for any edge cases or obscure bugs I may have missed.

### Using the HashMap
To use the hash map, simply treat it as a standard Python module. A simple sample of how to use it can be found below, and more detailed usage cases are in the test file.

At the moment, the hash map does not support resizing. However, this is definitely something that could easily be implemented in the future.

Additionally, although the hash map was only designed for string keys in mind, the hash function does support other data types, and any hash function should be compatible with the structure.

### Example
Run this in a standard python shell

```
from robin_hash import RobinHash

rh = RobinHash(size = 512)
rh.set('one', 1)
x = rh.get('one')
load_factor = rh.load()
y = rh.delete('one')

```

To run the test file from the command line, use the command  
`python robin_hash_test.py`

### Moving Forward
There are definitely still ways to improve on this. As mentioned above, resizing has not been implemented, and would not be incredibly hard to do given Python's incredibly lenient implementation of arrays. Additionally, I may look into either some timing tests, perhaps comparing to Python's primative dictionary type, or some statistical analysis on probe length mean, varience, etc. for various data sets.
