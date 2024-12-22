Dinu Eduard-Adiel
# README - How to Run `test.py`

## Prerequisites

Before running the `test.py` script, ensure you have the following installed:

1. **Python** (version 3.6 or above).
2. **Required Python Libraries**:
   - `matplotlib`
   - `pandas`
   - `randomhash`
   - `numpy`
   - `time`
   - `os`

If you don't have these libraries installed, you can install them using `pip`:

```bash
pip install matplotlib pandas randomhash numpy
```

## Folder Structure

Ensure your folder structure looks something like this:

```
/your_project_folder
    /datasets  (contains your datasets .txt files)
    /test.py  (the script you will run)
    /hll.py   (contains the HyperLogLog implementation)
    /recordinality.py  (contains the Recordinality implementation)
    README.txt  (this file)
```

## Running the Test

1. **Prepare your Dataset**:
   - Place your `.txt` files (such as book texts or datasets) inside the `datasets/` folder.

2. **Open a terminal or command prompt** in your project directory.

3. **Run the Script**:
   Run the following command to execute the `test.py` script:

   ```bash
   python test.py
   ```

   This will execute the test and generate output, including comparison results between HyperLogLog and Recordinality algorithms.

4. **Output**:
   The script will compute the cardinality estimates for the datasets using both algorithms and generate comparison tables and plots.

## Customizing the Test

You can adjust the values for the parameters like `k` (for Recordinality) and `error_rate` (for HyperLogLog) in the script `test.py`:

- **Adjust `k`** for Recordinality:
   Change the value of `k` in the script to control the accuracy and speed of the Recordinality algorithm.

- **Adjust `error_rate`** for HyperLogLog:
   Set the desired error rate in the script to control the precision of the HyperLogLog algorithm.