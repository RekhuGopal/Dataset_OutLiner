import pandas as pd
import os
import random
import argparse

# Define headers
HEADERS = ["Stock-ID", "Timestamp", "Price"]

# function to Extracts exactly 30 consecutive data points from a CSV file starting from a random timestamp.
def extract_data_points(file_path, num_points=30):
    try:
        df = pd.read_csv(file_path, header=None, names=HEADERS)
        
        # Check if the DataFrame is empty or does not have enough data points
        if df.empty or len(df) < num_points:
            raise ValueError("Not enough data points in file.")
        
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%d-%m-%Y')
        df.sort_values('Timestamp', inplace=True)
        
        # Randomly select a start index ensuring it doesn't exceed the available data minus the number of points
        start_index = random.randint(0, len(df) - num_points)
        sampled_df = df.iloc[start_index:start_index + num_points]
        
        return sampled_df
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None

# Function to Detects outliers based on the mean and standard deviation of the 30 sampled data points.
def detect_outliers(data_frame):
    try:
        mean_price = data_frame['Price'].mean()
        std_dev = data_frame['Price'].std()
        threshold = 2 * std_dev
        
        # Identify outliers
        outliers = data_frame[(data_frame['Price'] > mean_price + threshold) | 
                              (data_frame['Price'] < mean_price - threshold)].copy()

        # If there are outliers, calculate additional columns for the output
        if not outliers.empty:
            outliers.loc[:, 'Mean'] = mean_price
            outliers.loc[:, 'Deviation'] = outliers['Price'] - mean_price
            outliers.loc[:, 'Percent_Deviation'] = (outliers['Deviation'] / mean_price) * 100
        
        # Ensure the output DataFrame has all necessary columns
        outliers = outliers[['Stock-ID', 'Timestamp', 'Price', 'Mean', 'Deviation', 'Percent_Deviation']] if not outliers.empty else pd.DataFrame(columns=['Stock-ID', 'Timestamp', 'Price', 'Mean', 'Deviation', 'Percent_Deviation'])
        
        return outliers
    except Exception as e:
        print(f"Error detecting outliers: {e}")
        return None

# Function to Processes stock price files in each exchange directory, extracts data points, detects outliers, and generates reports.
def process_files(input_dir, output_dir, num_files=1):
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        exchanges = [d for d in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, d))]

        for exchange in exchanges:
            exchange_path = os.path.join(input_dir, exchange)
            files = [f for f in os.listdir(exchange_path) if f.endswith('.csv')]
            files = files[:num_files]

            if not files:
                print(f"No CSV files found in the directory {exchange_path}.")
                continue
            
            for file in files:
                file_path = os.path.join(exchange_path, file)
                output_path = os.path.join(output_dir, f'{exchange}_outliers_{file}')
                
                data = extract_data_points(file_path)
                if data is not None:
                    outliers = detect_outliers(data)
                    if outliers is not None:
                        outliers.to_csv(output_path, index=False)
                        print(f"Outliers for file {file} in {exchange} saved to {output_path}")
                    else:
                        print(f"No outliers detected for file {file} in {exchange}")
                else:
                    print(f"Failed to process file {file} in {exchange}")
    except Exception as e:
        print(f"Error processing files: {e}")

# Main function for Orchestration 
def main():
    parser = argparse.ArgumentParser(description='Stock Price Outlier Detection')
    parser.add_argument('input_dir', type=str, help='Directory containing input CSV files grouped by exchange.')
    parser.add_argument('output_dir', type=str, help='Directory to save output CSV files.')
    parser.add_argument('--num_files', type=int, default=1, help='Number of files to process from each exchange directory.')

    args = parser.parse_args()
    process_files(args.input_dir, args.output_dir, args.num_files)

if __name__ == '__main__':
    main()
