import os
import pandas as pd
import time  # Import the time module
from hll import HyperLogLog  # Assuming HyperLogLog is in hll.py
from recordinality import Recordinality  # Assuming Recordinality is implemented elsewhere

# Define the dataset folder path
folder_path = 'datasets/'  # Update this to 'dataset/' or specify the correct path if needed

# Check if the folder exists
if not os.path.exists(folder_path):
    print(f"Error: The folder '{folder_path}' does not exist!")
else:
    # Continue with the logic to test the comparison on the books
    def generate_comparison_table(folder_path, k, error_rate):
        """
        Generate a comparison table with HyperLogLog and Recordinality.
        """
        # List all .txt files (books) in the dataset folder
        book_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.txt')]
        
        # Initialize an empty list to store results
        comparison_results = []

        # Loop through the books and test
        for book_path in book_files:
            result = test_comparison_on_book(book_path, k, error_rate)
            comparison_results.append(result)

        # Convert the results to a pandas DataFrame
        df = pd.DataFrame(comparison_results, columns=["Book", "True Cardinality", "HLL Estimate", "HLL Time", "Recordinality Estimate", "Recordinality Time"])
        return df

    def test_comparison_on_book(book_path, k, error_rate):
        """
        Test the comparison of HLL and Recordinality on a single book.
        """
        # Read the book (text file) content
        with open(book_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Assuming you have a function `process_text` to extract unique words
        unique_words = set(content.split())

        true_cardinality = len(unique_words)

        # --- HyperLogLog Estimation ---
        # Measure time for HLL
        start_time = time.time()

        try:
            # HyperLogLog uses error_rate for precision internally
            hll = HyperLogLog(error_rate=error_rate)  # Using error_rate (b)
        except TypeError as e:
            print(f"Error while initializing HyperLogLog: {e}")
            return [os.path.basename(book_path), true_cardinality, None, None, None, None]  # Return None if error occurs

        for word in unique_words:
            hll.add(word)

        hll_estimate = hll.card()  # Use the 'card' method to get the estimate
        hll_time = time.time() - start_time  # Time taken for HyperLogLog

        # --- Recordinality Estimation ---
        # Measure time for Recordinality
        start_time = time.time()

        recordinality = Recordinality(k=k)  # Adjust according to your Recordinality constructor
        for word in unique_words:
            recordinality.add(word)

        recordinality_estimate = recordinality.estimate_cardinality()
        recordinality_time = time.time() - start_time  # Time taken for Recordinality

        # Return results including computation times
        return [os.path.basename(book_path), true_cardinality, hll_estimate, hll_time, recordinality_estimate, recordinality_time]

    # Example values for k and error_rate (you can adjust based on your needs)
    k = 128
    error_rate = 0.01  # Example error rate for HLL (between 0 and 1)

    # Generate the comparison table
    df = generate_comparison_table(folder_path, k, error_rate)

    # Print the comparison table
    print(df)
