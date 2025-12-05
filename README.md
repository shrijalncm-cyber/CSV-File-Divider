# CSV Breaker

A modern, user-friendly GUI application to split large CSV files into smaller chunks.

## Features

✨ **Modern UI** - Sleek dark mode interface with CustomTkinter  
📊 **Smart CSV Splitting** - Divide large files into manageable chunks  
📋 **Header Preservation** - Automatically include header rows in each file  
⚡ **Fast Processing** - Efficient pandas-based CSV handling  
📁 **Organized Output** - Files saved with sequential naming (Bulk upload 1, 2, 3...)  
🎯 **User-Friendly** - Simple configuration with clear visual feedback

## Quick Start

### Option 1: Run the Executable (Recommended)
1. Download `CSV_Breaker.exe` from the `dist_minimal` folder
2. Double-click to run - no installation needed!

### Option 2: Run from Source
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python csv_breaker.py
```

## How to Use

1. **Select CSV File** - Click "Browse File" to choose your CSV
2. **Configure Settings**:
   - **Rows per file**: Number of data rows in each output file
   - **Header row number**: Which row contains your headers (1-indexed)
   - **Output folder name**: Name for the folder to store split files
3. **Process** - Click "⚡ Process CSV" and wait for completion
4. **Done** - Find your files in the output folder!

## Example

If you have a CSV with 1000 rows and set "Rows per file" to 200:
- You'll get 5 files: `Bulk upload 1.csv` through `Bulk upload 5.csv`
- Each file will have the header row plus up to 200 data rows
- All files saved in your specified output folder

## Output File Naming

Files are named sequentially:
- `Bulk upload 1.csv`
- `Bulk upload 2.csv`
- `Bulk upload 3.csv`
- ... and so on

## Executable Details

- **File**: `dist_minimal/CSV_Breaker.exe`
- **Size**: ~82 MB
- **Platform**: Windows
- **Requirements**: None (standalone executable)

## Building from Source

To create your own executable:

```bash
# Install PyInstaller
pip install pyinstaller

# Build (minimal size)
build_minimal.bat

# Or build with spec file
pyinstaller csv_breaker.spec --clean
```

## Technical Details

- **GUI Framework**: CustomTkinter (Modern Tkinter alternative)
- **CSV Processing**: pandas
- **Packaging**: PyInstaller with size optimizations

## Requirements (for running from source)

- Python 3.8+
- customtkinter >= 5.2.0
- pandas >= 2.0.0

## License

Free to use and modify.

---

**Made with ❤️ for easy CSV management**
