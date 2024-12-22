import matplotlib.pyplot as plt
import numpy as np
from recordinality import Recordinality
import randomhash

# Function to generate Zipfian-distributed data
def generate_zipfian_data(alpha, n, N):
    ranks = np.arange(1, n + 1)  # Ranks from 1 to n
    probabilities = 1.0 / (ranks ** alpha)  # Zipfian probabilities
    probabilities /= probabilities.sum()  # Normalize to make it a proper probability distribution

    # Generate data stream of size N based on the probabilities
    data = np.random.choice(ranks, size=N, p=probabilities)
    data_stream = [f"element_{i}" for i in data]
    return data_stream

# Function to test Recordinality with different ks
def test_recordinality_for_multiple_ks(alpha, n, N, k_values):
    true_cardinality = n  # True cardinality is just n (number of distinct elements in the dataset)
    results = []

    for k in k_values:
        # Generate Zipfian data
        data_stream = generate_zipfian_data(alpha, n, N)

        # Create Recordinality estimator with sample size k
        estimator = Recordinality(k=k)

        # Add elements to the estimator
        for item in data_stream:
            estimator.add(item)

        # Estimate cardinality
        estimated_cardinality = estimator.estimate_cardinality()

        # Store results (including k and the estimated cardinality)
        results.append((k, estimated_cardinality))

    return results, true_cardinality

# Function to plot the results
def plot_recordinality_estimations(results, true_cardinality):
    ks, estimated_cardinalities = zip(*results)

    plt.figure(figsize=(10, 6))
    plt.plot(ks, estimated_cardinalities, marker='o', label="Estimated Cardinality")
    plt.axhline(y=true_cardinality, color='r', linestyle='--', label="True Cardinality")
    plt.xlabel("Sample Size (k)")
    plt.ylabel("Estimated Cardinality")
    plt.title("Recordinality Estimation vs True Cardinality for Various k")
    plt.legend()
    plt.grid(True)
    plt.show()

# Main function to run the test
def main():
    alpha = 1.0  # Zipfian distribution parameter
    n = 1000  # Number of distinct elements
    N = 5000  # Total number of elements in the stream
    k_values = [16, 32, 64, 128, 256, 512]  # Different sample sizes k to test

    results, true_cardinality = test_recordinality_for_multiple_ks(alpha, n, N, k_values)
    plot_recordinality_estimations(results, true_cardinality)

if __name__ == "__main__":
    main()
