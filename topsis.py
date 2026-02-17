import sys
import pandas as pd
import numpy as np
import os

def load_file(input_file):
    if not os.path.exists(input_file):
        print("Error: File not found.")
        sys.exit(1)

    try:
        if input_file.endswith(".csv"):
            return pd.read_csv(input_file)
        elif input_file.endswith(".xlsx"):
            return pd.read_excel(input_file)
        else:
            print("Error: Unsupported file format. Use .csv or .xlsx.")
            sys.exit(1)
    except Exception:
        print("Error: Unable to read input file.")
        sys.exit(1)

def validate_numeric_columns(df):
    numeric_data = df.iloc[:, 1:]

    if numeric_data.shape[1] < 2:
        print("Error: Input file must contain at least three columns.")
        sys.exit(1)

    try:
        numeric_data = numeric_data.apply(pd.to_numeric)
    except Exception:
        print("Error: All columns except the first must contain numeric values.")
        sys.exit(1)

    return numeric_data.astype(float)


def validate_weights_impacts(weights, impacts, num_columns):
    weights = weights.split(',')
    impacts = impacts.split(',')

    if len(weights) != len(impacts) or len(weights) != num_columns:
        print("Error: Number of weights, impacts, and numeric columns must be equal.")
        sys.exit(1)

    for impact in impacts:
        if impact not in ['+', '-']:
            print("Error: Impacts must be either '+' or '-'.")
            sys.exit(1)

    try:
        weights = np.array(weights, dtype=float)
    except ValueError:
        print("Error: Weights must be numeric values.")
        sys.exit(1)

    return weights, impacts


def topsis(input_file, weights, impacts, output_file):
    data = load_file(input_file)

    if data.shape[1] < 3:
        print("Error: Input file must contain three or more columns.")
        sys.exit(1)

    numeric_data = validate_numeric_columns(data)
    weights, impacts = validate_weights_impacts(weights, impacts, numeric_data.shape[1])
    normalization_factor = np.sqrt((numeric_data ** 2).sum())
    normalized_matrix = numeric_data / normalization_factor
    weighted_matrix = normalized_matrix * weights

    ideal_best = []
    ideal_worst = []

    for i in range(len(impacts)):
        if impacts[i] == '+':
            ideal_best.append(weighted_matrix.iloc[:, i].max())
            ideal_worst.append(weighted_matrix.iloc[:, i].min())
        else:
            ideal_best.append(weighted_matrix.iloc[:, i].min())
            ideal_worst.append(weighted_matrix.iloc[:, i].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)
    distance_best = np.sqrt(((weighted_matrix - ideal_best) ** 2).sum(axis=1))
    distance_worst = np.sqrt(((weighted_matrix - ideal_worst) ** 2).sum(axis=1))
    score = distance_worst / (distance_best + distance_worst)

    data["Topsis Score"] = score
    data["Rank"] = score.rank(method='max', ascending=False).astype(int)
    data.to_csv(output_file, index=False)

    print("TOPSIS calculation completed successfully.")

def main():
    import sys
    if len(sys.argv) != 5:
        print("Usage: topsis <input_file> <weights> <impacts> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    weights = sys.argv[2]
    impacts = sys.argv[3]
    output_file = sys.argv[4]

    # Call your TOPSIS function here
    # Example:
    topsis(input_file, weights, impacts, output_file)


if __name__ == "__main__":
    main()

