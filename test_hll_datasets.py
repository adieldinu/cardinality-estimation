import os
import randomhash
import math
import time
from hll import HyperLogLog
import pandas as pd
import tkinter as tk
from tkinter import ttk

# Load data from a .txt file
def load_txt_file(filepath):
    """
    Loads a .txt file where each line contains one word and returns a list of words.
    """
    words = []
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            word = line.strip()
            if word:  # Only add non-empty words
                words.append(word)
    return words


# Process a book to measure time for distinct words counting

def process_book_with_hll(book_path, error_rate=0.01):
    """
    Estimates cardinality for a given book using the HyperLogLog algorithm.
    """
    # Load words from the book's .txt file
    words = load_txt_file(book_path)
    
    # Create the RandomHashFamily for the HyperLogLog
    hash_family = randomhash.RandomHashFamily(count=1)
    
    # Initialize the HyperLogLog with the error rate and hash family
    hll = HyperLogLog(error_rate=error_rate, hash_family=hash_family)
    
    # Start measuring time
    start_time = time.time()
    
    # Add each word to the HyperLogLog estimator
    for word in words:
        hll.add(word)
    
    # Estimate the cardinality (number of unique words)
    estimated_cardinality = hll.card()
    
    # Calculate the true cardinality (the number of unique words in the dataset)
    true_cardinality = len(set(words))
    
    # Measure the time taken to process
    computation_time = time.time() - start_time
    
    # Return results
    return len(words), estimated_cardinality, true_cardinality, computation_time

# Function to process all books in a folder and create a table with cardinality comparison for each
def generate_cardinality_table(folder_path, error_rate=0.01):
    """
    Processes all .txt books in the folder and generates a table with cardinality comparison for each.
    """
    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    
    # Prepare a list to hold the results (book name, total words, true cardinality, estimated cardinality, absolute difference, computation time)
    results = []
    
    # Process each book and collect the results
    for txt_file in txt_files:
        book_path = os.path.join(folder_path, txt_file)  # Get the full path of the book
        total_words, estimated_cardinality, true_cardinality, computation_time = process_book_with_hll(book_path, error_rate)
        
        # Calculate the absolute difference between true and estimated cardinalities
        abs_difference = abs(true_cardinality - estimated_cardinality)
        
        # Add the results to the list
        results.append({
            'Book': txt_file,
            'Total Words': total_words,
            'True Cardinality': true_cardinality,
            'Estimated Cardinality': estimated_cardinality,
            'Absolute Difference': abs_difference,
            'Computation Time (s)': computation_time
        })
    
    # Create a pandas DataFrame to display the results in a table format
    df = pd.DataFrame(results)
    
    # Display the table in a new Tkinter window
    display_table_in_window(df)

# Function to display the DataFrame in a new Tkinter window
def display_table_in_window(df):
    """
    Display a pandas DataFrame in a new Tkinter window using a Treeview widget.
    """
    # Create the Tkinter window
    root = tk.Tk()
    root.title("Cardinality Estimation Results")
    
    # Ensure all column names are strings (strip any unnecessary whitespace)
    columns = [str(col).strip() for col in df.columns]
    
    # Create a Treeview widget to display the DataFrame
    tree = ttk.Treeview(root, columns=columns, show="headings")
    
    # Define columns in Treeview
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor='center')
    
    # Insert rows into the Treeview
    for index, row in df.iterrows():
        tree.insert("", "end", values=row.tolist())
    
    # Place the Treeview widget in the window
    tree.pack(expand=True, fill="both")
    
    # Add a scrollbar
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    
    # Start the Tkinter event loop
    root.mainloop()

# Example usage - generate the cardinality table for all books in the 'datasets' folder
folder_path = 'datasets'  # Replace with the path to your datasets folder
generate_cardinality_table(folder_path)
