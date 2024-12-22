import math
from randomhash import RandomHashFamily


def bit_length(w):
    return w.bit_length()


def get_alpha(p):
    if not (4 <= p <= 16):
        raise ValueError("p=%d should be in range [4 : 16]" % p)

    if p == 4:
        return 0.673

    if p == 5:
        return 0.697

    if p == 6:
        return 0.709

    return 0.7213 / (1.0 + 1.079 / (1 << p))


def get_rho(w, max_width):
    rho = max_width - bit_length(w) + 1

    if rho <= 0:
        raise ValueError('w overflow')

    return rho


class HyperLogLog:
    """
    HyperLogLog cardinality counter using `randomhash`.
    """

    def __init__(self, error_rate, hash_family=None):
        """
        Initializes a HyperLogLog.

        :param error_rate: Absolute error / cardinality.
        :param hash_family: An instance of RandomHashFamily. If None, defaults to one with a single hash function.
        """
        if not (0 < error_rate < 1):
            raise ValueError("Error_Rate must be between 0 and 1.")

        # Determine precision p and initialize registers
        p = int(math.ceil(math.log((1.04 / error_rate) ** 2, 2)))

        self.alpha = get_alpha(p)
        self.p = p
        self.m = 1 << p
        self.M = [0 for _ in range(self.m)]

        # Use provided hash family or create one
        self.hash_family = hash_family or RandomHashFamily(count=1)
        self.hash_func = self.hash_family.hashes  # Default hash function from the family

    def add(self, value):
        """
        Adds an item to the HyperLogLog.
        """
        if not isinstance(value, str):
            value = str(value)

        # Use the hash function to get the hashed value
        x = self.hash_func(value)[0]  # Get the first hash value from the family
        j = x & (self.m - 1)  # Extract the first p bits
        w = x >> self.p  # Remaining bits
        self.M[j] = max(self.M[j], get_rho(w, 64 - self.p))

    def update(self, *others):
        """
        Merges other HyperLogLog counters into this one.
        """
        for item in others:
            if self.m != item.m:
                raise ValueError('Counters precisions should be equal')

        self.M = [max(*items) for items in zip(*([item.M for item in others] + [self.M]))]

    def __len__(self):
        return round(self.card())

    def _Ep(self):
        """
        Internal function to calculate the estimate.
        """
        E = self.alpha * float(self.m ** 2) / sum(math.pow(2.0, -x) for x in self.M)
        return E  # Removed bias correction for simplicity unless provided

    def card(self):
        """
        Returns the estimate of the cardinality.
        """
        V = self.M.count(0)

        if V > 0:
            H = self.m * math.log(self.m / float(V))
            return H if H <= 5 * self.m else self._Ep()
        else:
            return self._Ep()

