# Dataset_OutLiner
# Stock Price Outlier Detection

## Overview

This project includes a Python script for detecting outliers in stock price data. The script processes CSV files containing stock price data, extracts a set of consecutive data points, and identifies any outliers based on statistical analysis.

## Setup

## Directory Structure

Ensure your directory structure looks like this:
/DATASET_OUTLINER
├── data
│ ├── LSE
│ ├── NASDAQ
│ └── NYSE
├── output
└── stock_price_outlier_detection.py



- **data/**: Contains subdirectories for each stock exchange (e.g., LSE, NASDAQ, NYSE). Each subdirectory should contain CSV files with stock price data.
- **output/**: The directory where output files will be saved.
- **stock_price_outlier_detection.py**: The Python script for detecting outliers.

## Requirements

- Python 3.x
- `pandas`
- `numpy`

You can install the required packages using pip:

```bash
pip install pandas numpy

```
## Usage
python stock_price_outlier_detection.py <input_dir> <output_dir> [--num_files <num_files>]
Example : python stock_price_outlier_detection.py data output --num_files 2  

## Example
Example out are kept in "output" folder


## Dockerfile
To create a Docker image for the stock_price_outlier_detection.py script , Docker file is kept in folder