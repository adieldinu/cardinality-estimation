import randomhash
import heapq

class Recordinality:
    def __init__(self, k):
        """
        Initialize the Recordinality data structure.

        Parameters:
            k (int): The fixed size of the sample.
        """
        self.k = k
        self.sample = []  # Max-heap to store the k smallest hash values (negated for min-heap behavior)
        self.hash_family = randomhash.RandomHashFamily(count=1)

    def _hash(self, value):
        """
        Hash a value using RandomHashFamily.

        Parameters:
            value (str): The value to hash.

        Returns:
            int: The hash value.
        """
        return self.hash_family.hashes(value)[0]

    def add(self, value):
        """
        Add a value to the Recordinality sample.

        Parameters:
            value (str): The value to add.
        """
        hash_value = self._hash(value)
        if len(self.sample) < self.k:
            heapq.heappush(self.sample, -hash_value)  # Negate to simulate max-heap
        elif -hash_value > self.sample[0]:  # If the new hash value is smaller
            heapq.heapreplace(self.sample, -hash_value)  # Replace the largest

    def estimate_cardinality(self):
        """
        Estimate the cardinality of the data stream.

        Returns:
            float: The estimated cardinality.
        """
        if len(self.sample) < self.k:
            return 0  # Not enough data to estimate
        R_k = -self.sample[0]  # Largest hash value in the sample
        return self.k / (R_k / (2 ** 32))  # Scale based on 32-bit hash space


