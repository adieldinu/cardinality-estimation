from hll import HyperLogLog
import numpy as np
import matplotlib.pyplot as plt
import random
import randomhash
import math
def generate_zipfian_data(alpha, n, N):
    """
    Generates a Zipfian-distributed dataset.

    Parameters:
    - alpha: The Zipfian distribution parameter (alpha >= 0).
    - n: The number of distinct elements.
    - N: The total number of elements in the stream.

    Returns:
    - A list containing N elements, distributed according to the Zipfian law.
    """
    # Generate probabilities for each element
    ranks = np.arange(1, n + 1)  # Ranks from 1 to n
    probabilities = 1.0 / (ranks ** alpha)  # Zipfian probabilities
    probabilities /= probabilities.sum()  # Normalize to make it a proper probability distribution

    # Generate data stream of size N based on the probabilities
    data = np.random.choice(ranks, size=N, p=probabilities)

    # Map ranks back to unique strings (e.g., element_1, element_2, ...)
    data_stream = [f"element_{i}" for i in data]
    return data_stream

def plot_cardinality_estimation(n_values, alpha=1.0, N=1000, error_rate=0.01):
    estimated_cardinalities = []
    # Explicitly create the RandomHashFamily and pass it to HyperLogLog
    hash_family = randomhash.RandomHashFamily(count=1)
    
    for n in n_values:
        zipfian_data = generate_zipfian_data(alpha, n, N)
        hll = HyperLogLog(error_rate=error_rate, hash_family=hash_family)  # Pass hash_family to HyperLogLog
        for item in zipfian_data:
            hll.add(item)
        estimated_cardinality = hll.card()
        estimated_cardinalities.append(estimated_cardinality)

    plt.figure(figsize=(10, 6))
    plt.plot(n_values, estimated_cardinalities, label="Estimated Cardinality", marker="o")
    plt.plot(n_values, n_values, color="r", linestyle="--", label="True Cardinality")
    plt.xlabel("Number of Unique Elements (n)")
    plt.ylabel("Cardinality")
    plt.title("Effect of n on Cardinality Estimation with HyperLogLog")
    plt.legend()
    plt.grid()
    plt.show()

# Function to plot cardinality estimation for different N values
def plot_cardinality_estimation_N(N_values, n, alpha, error_rate=0.01):
    estimated_cardinalities = []
    # Explicitly create the RandomHashFamily and pass it to HyperLogLog
    hash_family = randomhash.RandomHashFamily(count=1)
    
    for N in N_values:
        zipfian_data = generate_zipfian_data(alpha, n, N)
        hll = HyperLogLog(error_rate=error_rate, hash_family=hash_family)  # Pass hash_family to HyperLogLog
        for item in zipfian_data:
            hll.add(item)
        estimated_cardinality = hll.card()
        estimated_cardinalities.append(estimated_cardinality)

    plt.figure(figsize=(10, 6))
    plt.plot(N_values, estimated_cardinalities, label=f"Estimated Cardinality (alpha={alpha})", marker="o")
    plt.plot(N_values, [n] * len(N_values), color="r", linestyle="--", label="True Cardinality")
    plt.xlabel("Total Number of Elements (N)")
    plt.ylabel("Cardinality (Distinct Elements)")
    plt.title(f"Effect of N on Cardinality Estimation with HyperLogLog (alpha={alpha})")
    plt.legend()
    plt.grid()
    plt.show()

def plot_cardinality_estimation_alpha(alpha_values, N=1000, n=100, error_rate=0.01):
    estimated_cardinalities = []
    
    for alpha in alpha_values:
        zipfian_data = generate_zipfian_data(alpha, n, N)
        hash_family = randomhash.RandomHashFamily(count=1)  # Explicitly create the RandomHashFamily
        
        hll = HyperLogLog(error_rate=error_rate, hash_family=hash_family)  # Pass hash_family to HyperLogLog
        for item in zipfian_data:
            hll.add(item)
        
        estimated_cardinality = hll.card()
        estimated_cardinalities.append(estimated_cardinality)

    plt.figure(figsize=(10, 6))
    plt.plot(alpha_values, estimated_cardinalities, label=f"Estimated Cardinality", marker="o")
    plt.plot(alpha_values, [n] * len(alpha_values), color="r", linestyle="--", label="True Cardinality")
    plt.xlabel("Alpha Value")
    plt.ylabel("Cardinality (Distinct Elements)")
    plt.title(f"Effect of Alpha on Cardinality Estimation with HyperLogLog")
    plt.legend()
    plt.grid()
    plt.show()

def main():
    n_values = [50, 100, 150, 200, 300, 400, 500, 700, 900, 1000]
  # Example n values
    alpha_values = [1.0, 1.05, 1.1, 1.15, 1.2]  # Example alpha values
    N_values = [2000, 2500, 2750, 3000, 3250, 3500, 3750, 4000]
    n = 100
    N=1000
    alpha = 2
    #n_b = [N, int(N * math.log(N)), N**2]
    #plot_cardinality_estimation(n_b)
    plot_cardinality_estimation_N(N_values, n, alpha)
    #plot_cardinality_estimation_alpha(alpha_values)
if __name__ == "__main__":
    main()
