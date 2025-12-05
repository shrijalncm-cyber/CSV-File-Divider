"""
Automated test script for CSV Breaker application
"""
import pandas as pd
import os
from pathlib import Path

def test_csv_processing():
    """Test the CSV processing logic"""
    
    # Test parameters
    input_file = "sample_data.csv"
    rows_per_file = 5
    header_row_num = 0  # 0-indexed (row 1 in UI)
    output_folder = "test_output"
    
    print("🧪 Testing CSV Breaker Logic...")
    print(f"Input file: {input_file}")
    print(f"Rows per file: {rows_per_file}")
    print(f"Header row: {header_row_num + 1}")
    print(f"Output folder: {output_folder}")
    print("-" * 50)
    
    # Read CSV
    df = pd.read_csv(input_file, header=None)
    print(f"✓ Read CSV: {len(df)} rows total")
    
    # Extract header
    header = df.iloc[header_row_num]
    print(f"✓ Header extracted: {list(header)}")
    
    # Remove header from data
    data_rows = df[df.index != header_row_num]
    print(f"✓ Data rows (excluding header): {len(data_rows)}")
    
    # Create output directory
    output_dir = Path(output_folder)
    output_dir.mkdir(exist_ok=True)
    print(f"✓ Created output directory: {output_dir}")
    
    # Calculate splits
    num_files = (len(data_rows) + rows_per_file - 1) // rows_per_file
    print(f"✓ Will create {num_files} files")
    print("-" * 50)
    
    # Process files
    for i in range(num_files):
        start_idx = i * rows_per_file
        end_idx = min((i + 1) * rows_per_file, len(data_rows))
        
        chunk = data_rows.iloc[start_idx:end_idx]
        output_df = pd.concat([pd.DataFrame([header]), chunk], ignore_index=True)
        
        output_file = output_dir / f"Bulk upload {i + 1}.csv"
        output_df.to_csv(output_file, index=False, header=False)
        
        print(f"✓ Created: {output_file.name} ({len(chunk)} data rows + header)")
    
    print("-" * 50)
    print(f"✅ SUCCESS! Created {num_files} files in '{output_folder}' folder")
    print("\nFile details:")
    for file in sorted(output_dir.glob("*.csv")):
        file_df = pd.read_csv(file, header=None)
        print(f"  - {file.name}: {len(file_df)} total rows")

if __name__ == "__main__":
    test_csv_processing()
