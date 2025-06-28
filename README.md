# Credit Card Transactions Analysis

## Dataset Creation Process

This dataset was created using a modified version of the [Sparkov Data Generation](https://github.com/lcabrp/Sparkov_Data_Generation) tool, which generates synthetic credit card transaction data for fraud detection research and testing.

### Key Improvements in Forked Repository

The forked repository includes specific enhancements to the original Sparkov implementation:
- **Optimized transaction data format** by removing redundant customer information from transaction files
- **Transaction files now only include SSN** as customer identifier instead of duplicating all customer details
- **Added utility script** (`cleanup_empty_csvs.py`) to remove empty transaction files generated during parallel processing
- **More normalized data structure** with customer data separated from transaction data

### Step-by-Step Generation Process

#### 1. Data Generation
Generated synthetic transaction data using the modified Sparkov tool:

```bash
python datagen.py -n 1010 -o output_folder 01/01/2020 06/25/2025
```

**Parameters:**
- `-n 1010`: Generate data for 1,010 customers
- `-o output_folder`: Output directory for generated files
- `01/01/2020 06/25/2025`: Date range spanning 5+ years (January 1, 2020 to June 25, 2025)

#### 2. Data Cleanup
Removed empty CSV files created during the parallel generation process:

```bash
python cleanup_empty_csvs.py -d '|' output_folder
```

**Parameters:**
- `-d '|'`: Specify pipe delimiter as field separator
- `output_folder`: Directory to clean up

#### 3. Data Organization
Copied the remaining CSV files to the `data/` folder for analysis and version control.

### Dataset Overview

The generation process produced a comprehensive dataset with:
- **Multiple CSV files** containing transaction data organized by demographic profiles
- **1,010 customers** across 12 different demographic segments
- **5+ years of transaction history** (2020-2025)
- **Realistic fraud patterns** integrated into the data
- **Geographic distribution** across the United States
- **Modern transaction categories** including traditional and contemporary spending patterns

### File Structure

```
data/
├── customers.csv                           # Customer demographics and profile assignments
├── adults_2550_female_urban_0000-0201.csv  # Transaction files organized by:
├── adults_2550_male_urban_0404-0605.csv    #   - Demographic profile
├── adults_50up_female_rural_0202-0403.csv  #   - Data chunks
├── young_adults_male_urban_0606-0807.csv   #   - Time periods
└── ...                                     # Additional transaction files
```

### Source Repository

**Modified Sparkov Data Generation Tool:** https://github.com/lcabrp/Sparkov_Data_Generation

This fork provides enhanced data generation capabilities with improved normalization and modern transaction patterns compared to the original implementation.

## Data Dictionary

### Customer Data (customers.csv)

- **ssn**: Social Security Number - Unique customer identifier
- **cc_num**: Credit Card Number - Customer's credit card number
- **first**: First Name - Customer's first name
- **last**: Last Name - Customer's last name
- **gender**: Gender - Customer's gender (M/F)
- **street**: Street Address - Customer's street address
- **city**: City - Customer's city of residence
- **state**: State - Customer's state of residence
- **zip**: ZIP Code - Customer's postal code
- **lat**: Latitude - Geographic latitude of customer address
- **long**: Longitude - Geographic longitude of customer address
- **city_pop**: City Population - Population of customer's city
- **job**: Job Title - Customer's occupation
- **dob**: Date of Birth - Customer's birth date
- **acct_num**: Account Number - Customer's account number
- **profile**: Customer Profile - Demographic profile assignment

### Transaction Data (54 transaction files)

- **ssn**: Social Security Number - Links to customer data
- **trans_num**: Transaction Number - Unique transaction identifier
- **trans_date**: Transaction Date - Date of transaction
- **trans_time**: Transaction Time - Time of transaction
- **category**: Transaction Category - Type of purchase/transaction
- **amt**: Amount - Transaction amount in USD
- **is_fraud**: Fraud Flag - Binary indicator (0=legitimate, 1=fraudulent)
- **merchant**: Merchant Name - Name of the merchant/business
- **merch_lat**: Merchant Latitude - Geographic latitude of merchant
- **merch_long**: Merchant Longitude - Geographic longitude of merchant

## Data Summary

- **Total Customers**: 1,010
- **Total Transaction Files**: 53
- **Total Transactions**: 4,740,009
- **Date Range**: 2020-2025 (5+ years of data)
- **Geographic Coverage**: Nationwide (United States)
- **Fraud Rate**: ~1% (realistic fraud detection scenario)
- **Data Quality**: No missing values detected
- **File Format**: CSV with pipe (|) delimiter
- **Total Dataset Size**: ~639 MB

## Project Structure

```
card_transactions_analysis/
├── data/                           # Generated transaction data
├── data_generation_analysis.md     # Analysis of data generation logic
├── data_dictionary_and_summary.ipynb  # EDA notebook for project plan
├── README.md                       # This file
├── requirements.txt                # Python dependencies
└── ...                            # Additional analysis notebooks (to be added)
```

## Setup Instructions

### Option 1: Using UV (Recommended - Faster)

**First, install UV if you don't have it:**
```bash
pip install uv
```

```bash
# Clone the repository
git clone https://github.com/lcabrp/card_transactions_analysis.git
cd card_transactions_analysis

# Install dependencies (uses pyproject.toml and uv.lock)
uv sync

# Start Jupyter notebook
jupyter notebook
```

### Option 2: Using pip (Traditional)

```bash
# Clone the repository
git clone https://github.com/lcabrp/card_transactions_analysis.git
cd card_transactions_analysis

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Start Jupyter notebook
jupyter notebook
```

### Dependencies

- pandas - Data manipulation and analysis
- numpy - Numerical computing
- matplotlib - Basic plotting and visualization
- seaborn - Statistical data visualization
- jupyter - Interactive notebook environment

## Suggested Next Steps

- [ ] Exploratory Data Analysis (EDA) using Python
- [ ] Data visualization and insights
- [ ] Fraud detection modeling
- [ ] Customer segmentation analysis
- [ ] Time series analysis of transaction patterns
