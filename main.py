import heapq
import randomhash
import math
import numpy as np


def generate_zipfian_data(alpha, n, N):
    """
    Generate a data stream following the Zipfian distribution.

    Parameters:
        alpha (float): Parameter for Zipfian distribution (must be > 1).
        n (int): Number of distinct elements.
        N (int): Total number of elements in the stream.

    Returns:
        list: Synthetic data stream.
    """
    if alpha <= 1:
        raise ValueError("Parameter 'alpha' must be greater than 1 for the Zipfian distribution.")
    
    data = np.random.zipf(alpha, N)
    data = np.clip(data, 1, n)  # Ensure values are within [1, n]
    return data



