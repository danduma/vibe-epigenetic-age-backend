from biolearn.data_library import DataLibrary
import pandas as pd
import os

def main():
    # Create output directory if it doesn't exist
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    
    # Load the GSE41169 blood DNAm data
    print("Loading GSE41169 dataset...")
    data_source = DataLibrary().get("GSE41169")
    data = data_source.load()
    data = data.dnam
    
    # Extract first column
    first_column = data.iloc[:, 0]
    
    # Save to CSV
    output_path = os.path.join(output_dir, "gse41169_first_column.csv")
    first_column.to_csv(output_path)
    print(f"First column has been saved to: {output_path}")
    print(f"Number of rows saved: {len(first_column)}")

if __name__ == "__main__":
    main() 