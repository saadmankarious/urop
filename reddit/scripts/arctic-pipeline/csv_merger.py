import pandas as pd
import argparse

def merge_csv(file1, file2, output_file=None):
    # Read the CSV files into DataFrames
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Concatenate the two DataFrames
    merged_df = pd.concat([df1, df2])

    # Optionally, you can reset the index if you want a continuous index
    merged_df.reset_index(drop=True, inplace=True)

    if output_file:
        # Save the merged DataFrame to a new CSV file if output file is provided
        merged_df.to_csv(output_file, index=False)
        print(f"Merged data saved to {output_file}")
    else:
        # Print the first few rows of the merged DataFrame
        print(merged_df.head())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Merge two CSV files with the same headers.')
    parser.add_argument('file1', type=str, help='Path to the first CSV file')
    parser.add_argument('file2', type=str, help='Path to the second CSV file')
    parser.add_argument('--output', type=str, help='Path to the output CSV file (optional)', default=None)

    args = parser.parse_args()

    merge_csv(args.file1, args.file2, args.output)
