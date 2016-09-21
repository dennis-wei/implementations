"""
robin_hash.py

This module primarily contains a class for a Robin Hood hash map implementation
The details behind the design can be found at the following references:
    https://cs.uwaterloo.ca/research/tr/1986/CS-86-14.pdf
    http://codecapsule.com/2013/11/17/robin-hood-hashing-backward-shift-deletion/

At a high level, the implementation uses a slightly modified version of linear
probing to handle collisions. Instead of simply looking for the next available
bin, the hash map minimizes the variance of probe distance by greedily
swapping with another entry if it is closer to it's ideal location.

In addition, rather than having tombstones to handle deletion, the hash map
uses a backwards shift deletion method which essentially modifies the hash map
to be as if that key had never been inserted in the first place
"""

def hash_function(string):
    """
    robin_hash.hash_function

    Hashing function for the hash map
    By default uses Python's built in hash function
    However, can be overwritten for testing purposes

    Parameters:
        string (string): string to be hashed
    Returns:
        (int) hashed value
    """
    return hash(string)

# Entry into the hash map
class RobinEntry():
    """
    robin_hash.RobinEntry

    Entries of the hash map
    """

    def __init__(self, key, value):
        """
        CONSTRUCTOR

        Parameters:
            key (string): dictionary key
            value (AnyType): dictionary value
        Variables:
            key (string): dictionary key
            value (AnyType): dictionary value
            bin_dist (int):
                The offset between where the bin in which an entry should have been
                inserted had there been no collision and where it actually is
                This value doesn't actually need to be initialized, it's just
                here for clarity
        """

        self.key = key
        self.value = value
        self.bin_dist = -1

class RobinHash():
    """
    robin_hash.RobinHash

    Main HashMap class
    Uses Robin Hood Linear Probing Open Addressing to handle collisions
    """

    def __init__(self, size = 128):
        """
        CONSTRUCTOR

        Parameters:
            size: size of the hash map
        Variables:
            bins (list): array corresponding to the hash table
                technically not fixed size, so Python will allocate some extra
                memory to account for appends that won't happen
                fixed size array would require numpy
            num_bins (int): number of bins in the hash table/hash map size
            used_bins (int): number of bins currently in use
            max_probe (int):
                keeps track of the max extra probing distiance required by the
                linear probing
                slightly optimizes searches and deletions
        """
        self.bins = [None] * size
        self.num_bins = size
        self.used_bins = 0
        self.max_probe = 0

    def get(self, key):
        """
        RobinHash.get

        Gets the value associated with a key in the hash map

        Parameters:
            key (string): the key to be searched for in the map
        Returns:
            (AnyType)
                Value associated with the key if the pair has been inserted
                None otherwise

        Calls the function that gets both the hash index and the value, but
        only returns the value
        """
        return self.__get_idx_and_value(key)[1]

    def set(self, key, value):
        """
        RobinHash.set
        Inserts a key: value pair into the hash map

        Parameters:
            key (string): the key of the pair to be inserted
            value (AnyType): the value of the pair to be inserted
        Returns:
            (Bool)
                True if the set is successful
                False if the set is not successful
                    This should only occur if the hash map is full
        """
        # First search for the key and override it if it is found
        idx = self.__get_idx_and_value(key)[0]
        if idx != None:
            self.bins[idx].value = value
            return True

        # If map is full, return False
        if self.used_bins == self.num_bins:
            return False

        # Increment number of bins in use
        self.used_bins += 1

        # Hash key and get a RobinEntry to be inserted
        hash_value = hash_function(key)
        entry = RobinEntry(key, value)

        # Get the non-collision index, initialize probe distance for entry swaps
        init_idx = hash_value % self.num_bins
        probe_dist = 0

        # Linear probe search
        for i in range(self.num_bins):
            # Linear probe hashing collision
            curr_idx = (init_idx + i) % self.num_bins
            curr_bin = self.bins[curr_idx]

            # Empty bin found -> insert here
            if not curr_bin:
                # Store the offset from the non-collision ideal index
                entry.bin_dist = probe_dist
                self.bins[curr_idx] = entry
                # Keep track of the maximum probing distance
                self.max_probe = max(probe_dist, self.max_probe)
                return True
            # Current probe distance longer than that of the current entry
            # Swap the two entries, now trying to insert the entry that was
            #   there before while keeping track of the new probing distance
            elif probe_dist > curr_bin.bin_dist:
                old_entry = curr_bin
                entry.bin_dist = probe_dist
                self.max_probe = max(probe_dist, self.max_probe)
                self.bins[curr_idx] = entry

                entry = old_entry
                probe_dist = entry.bin_dist
            # Increment probing distance before going to next index
            probe_dist += 1
        # Should never run since an empty spot should always be found if the map
        #   isn't full
        return False

    def delete(self, key):
        """
        RobinHash.delete
        Deletes a key: value pair in the map and backshifts affected entries

        Parameters:
            key (string): Key of the pair to delete
        Returns:
            (AnyType)
                The value of the deleted pair if it is in the map
                None if the value is not in the map
        """

        # Search for the key and get it's hash index and value
        idx, val = self.__get_idx_and_value(key)

        # Return None if the key is not found in the map
        if idx == None:
            return None

        # initialize indices
        curr_idx = idx
        next_idx = (idx + 1) % self.num_bins

        # Backwards shift algorithm
        # Shift entries back one until either an entry is in it's correct spot
        #   or an empty bin is found
        # Intuitively, make it as if the key was never inserted
        while self.bins[next_idx] and self.bins[next_idx].bin_dist != 0:
            # Shift entry backwards
            self.bins[idx] = self.bins[next_idx]
            # Decrement relative distance if it was not an empty bin
            self.bins[idx].bin_dist -= 1
            idx = next_idx
            next_idx = (idx + 1) % self.num_bins
        # Return the value of the original key: value pair
        self.bins[idx] = None
        self.used_bins -= 1
        return val

    def load(self):
        """
        RobinHash.load
        Returns the load factor of the map

        Returns:
            (float) load factor of hash map
        """

        return float(self.used_bins) / self.num_bins

    def __get_idx_and_value(self, key):
        """
        RobinHash.__get_idx_and_value
        Internal function to search for a key and return both the hash index
            and the value associated with the key

        Parameters:
            key (string): The key to search for
        Returns:
            (int, AnyType)
                tuple corresponding to the array index of the entry
                and the value corresponding to the key
        """
        # Hash and get ideal no-collision bin
        hash_value = hash_function(key)
        init_idx = hash_value % self.num_bins
        # Linear probing
        #   Search until an empty bin, a bin where the entry would have been
        #   inserted, or until the max probing distance of the table is
        #   exceeded
        for i in range(self.max_probe + 1):
            curr_idx = (init_idx + i) % self.num_bins
            curr_bin = self.bins[curr_idx]
            # Key cannot be in map -> return (None, None)
            if not curr_bin or i > curr_bin.bin_dist:
                return (None, None)
            # Key found -> return (index, value)
            elif curr_bin.key == key:
                return (curr_idx, curr_bin.value)
        # Max probe distance exceeded -> return (None, None)
        return (None, None)
