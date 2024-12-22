import os
import time
import pandas as pd
from recordinality import Recordinality
import randomhash

# Function to read the content of a book file
def read_book(book_path):
    with open(book_path, 'r', encoding='utf-8') as file:
        return file.read().split()

# Function to test Recordinality on a book dataset
def test_recordinality_on_book(book_path, k):
    # Read book content and create the data stream
    data_stream = read_book(book_path)
    
    # True cardinality (unique words in the book)
    true_cardinality = len(set(data_stream))
    
    # Recordinality estimation
    estimator = Recordinality(k=k)
    start_time = time.time()
    for item in data_stream:
        estimator.add(item)
    estimated_cardinality = estimator.estimate_cardinality()
    computation_time = time.time() - start_time
    
    return true_cardinality, estimated_cardinality, computation_time

# Function to generate a table of results for all books in the dataset
def generate_cardinality_table(folder_path, k):
    results = []
    
    # Iterate over all text files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):  # Ensure it's a text file
            book_path = os.path.join(folder_path, filename)
            
            # Test the Recordinality on the book dataset
            true_cardinality, estimated_cardinality, computation_time = test_recordinality_on_book(book_path, k)
            
            # Add the results to the list
            results.append({
                'Book': filename,
                'True Cardinality': true_cardinality,
                'Estimated Cardinality': estimated_cardinality,
                'Computation Time (s)': computation_time
            })
    
    # Create a DataFrame from the results
    df = pd.DataFrame(results)
    return df

# Function to display the table
def display_table_in_window(df):
    import tkinter as tk
    from tkinter import ttk
    
    # Create the main window
    window = tk.Tk()
    window.title("Recordinality Results")

    # Create a Treeview widget to display the table
    tree = ttk.Treeview(window, columns=list(df.columns), show="headings")

    # Define the columns
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    # Insert rows into the table
    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    tree.pack(expand=True, fill="both")
    
    # Run the GUI window
    window.mainloop()

# Main function to test Recordinality on all datasets
def main():
    folder_path = 'datasets'  # Path to the folder containing the book datasets
    k = 20  # Sample size for Recordinality
    
    # Generate the cardinality table
    df = generate_cardinality_table(folder_path, k)
    
    # Display the table in a window
    display_table_in_window(df)

if __name__ == "__main__":
    main()
