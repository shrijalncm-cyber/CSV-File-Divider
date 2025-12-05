# CSV Product Converter

A modern GUI application to filter and transform product CSV files for import.

## Features

✨ **Modern UI** - Clean, dark mode interface with intuitive controls  
🔍 **Smart Filtering** - Automatically filters out unwanted rows  
📊 **Column Mapping** - Transforms source CSV to target format  
⚙️ **Configurable** - Set default values for quantity, weight, MOQ, and units  
📁 **Easy Output** - Generates ready-to-import CSV files

## Filtering Rules

The application automatically applies these filters:

- ✅ **Includes**: Only rows where `variant_index = 0`
- ✅ **Includes**: Only rows where `available = TRUE`
- ❌ **Skips**: All other rows

## Input CSV Requirements

Your input CSV must have these columns:
- `product_title` - Product name
- `price` - Selling price
- `crossed_price` - Original/crossed price
- `variant_index` - Variant identifier (only 0 will be included)
- `available` - Availability status (TRUE/FALSE)
- `image_1` - First product image URL
- `image_2` - Second product image URL (optional)
- `image_3` - Third product image URL (optional)

## Output CSV Format

The output CSV will have these columns:

| Column | Source | Notes |
|--------|--------|-------|
| productName | product_title | From input CSV |
| productSku | - | Empty |
| sellingPrice | price | From input CSV |
| crossed_price | crossed_price | From input CSV |
| quantity | User input | Applied to all rows |
| weight | User input | Applied to all rows |
| productDescription | - | Empty |
| moq | User input | Applied to all rows |
| sellingUnit | User dropdown | Applied to all rows |
| image | image_1 | From input CSV |
| image.1 | image_2 | From input CSV |
| image.2 | image_3 | From input CSV |

## How to Use

1. **Launch the application**
   ```bash
   python csv_converter.py
   ```

2. **Select your CSV file**
   - Click "Browse CSV File"
   - Choose your product CSV

3. **Configure default values**
   - Set default quantity (e.g., 100)
   - Set default weight (e.g., 1)
   - Set MOQ - Minimum Order Quantity (e.g., 1)
   - Choose selling unit from dropdown

4. **Convert**
   - Click "⚡ Convert CSV"
   - Wait for processing
   - Output file will be saved as `[filename]_converted.csv`

## Example

**Input CSV** (7 rows):
- Row 1: variant_index=0, available=TRUE ✅ Included
- Row 2: variant_index=1, available=TRUE ❌ Skipped (variant_index ≠ 0)
- Row 3: variant_index=0, available=TRUE ✅ Included
- Row 4: variant_index=0, available=FALSE ❌ Skipped (not available)
- Row 5: variant_index=0, available=TRUE ✅ Included
- Row 6: variant_index=2, available=TRUE ❌ Skipped (variant_index ≠ 0)
- Row 7: variant_index=0, available=TRUE ✅ Included

**Output CSV**: 4 rows (Rows 1, 3, 5, 7 only)

## Requirements

- Python 3.8+
- customtkinter >= 5.2.0
- pandas >= 2.0.0

Install dependencies:
```bash
pip install -r requirements.txt
```

## Selling Unit Options

- Piece
- Kilogram
- Gram
- Litre
- Millilitre
- Meter
- Centimeter
- Inch
- Foot
- Dozen
- Pair
- Bundle
- Set
- Sheet
- Roll
- Tube

---

**Made with ❤️ for easy product CSV management**
