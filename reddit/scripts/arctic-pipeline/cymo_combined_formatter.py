import pandas as pd
import argparse
import os

def merge_csv(file1, file2, output_file=None):
    # Read the CSV files into DataFrames
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    print(df2.head())
    print(df1.head())

    # Concatenate the two DataFrames
    merged_df = pd.concat([df1, df2])

    # Shuffle the merged DataFrame
    shuffled_df = merged_df.sample(frac=1).reset_index(drop=True)

    if output_file:
        # Save the shuffled DataFrame to a new CSV file if output file is provided
        shuffled_df.to_csv(output_file, index=False)
        print(f"Merged and shuffled data saved to {output_file}")
    else:
        # Print the first few rows of the shuffled DataFrame
        print(shuffled_df.head())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Merge and shuffle two CSV files with the same headers.')
    parser.add_argument('condition_dir', type=str, help='Path to the first CSV file')

    args = parser.parse_args()
    base_name = os.path.basename(args.condition_dir.strip('/'))
    extracted_part = base_name.split('_')[0]
    merge_csv(f'{args.condition_dir}/diagnosed/diagnosed-data.cymo.csv', 
              f'{args.condition_dir}/control/control-data.cymo.csv',
              f'{args.condition_dir}/{extracted_part}-combined.csv')
