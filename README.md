# Credit Card Transactions Analysis

A comprehensive analysis of synthetic credit card transaction data to identify fraud patterns and customer spending behaviors. This project analyzes 4.74 million transactions across 1,010 customers spanning 5+ years (2020-2025).

## Project Summary

### Problem Statement
Credit card fraud costs billions annually and affects millions of consumers. Understanding transaction patterns and identifying characteristics that distinguish fraudulent from legitimate transactions is crucial for financial institutions to protect customers and minimize losses.

### Key Findings
Our analysis of 4.74 million transactions revealed several important patterns:

**Fraud Detection Insights:**
- Fraud rates vary significantly by time of day, with certain hours showing higher risk
- Analysis of customer-merchant distances shows no significant correlation with fraud occurrence
- Specific transaction categories exhibit higher fraud rates than others
- Weekend vs. weekday patterns show distinct fraud characteristics

**Customer Behavior Patterns:**
- Transaction volumes peak during specific hours and days
- Customer demographics (age group, location) correlate with spending patterns
- Average transaction amounts vary significantly across merchant categories

**Geographic Insights:**
- Customer distribution spans all US states with concentration in major metropolitan areas
- Geographic distance analysis reveals fraud occurs equally across all distance ranges (0.199%-0.207%)
- Urban vs. rural customers show different spending behaviors

### Data Limitations
- **Synthetic Data**: This analysis uses computer-generated data that simulates real patterns but may not capture all real-world complexities
- **Time Period**: Data spans 2020-2025, including some future dates that represent projected patterns
- **Sample Size**: While large (4.7M transactions), this represents a subset of real-world transaction volumes
- **Geographic Scope**: Limited to US-based transactions and customers

### Business Impact
These findings can help financial institutions improve fraud detection systems by incorporating time-based, geographic, and category-specific risk factors into their monitoring algorithms.

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
uv sync or python -m uv sync
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
```

### Dependencies

- **pandas** - Data manipulation and analysis of transaction datasets
- **numpy** - Numerical computing for statistical calculations and feature engineering
- **matplotlib** - Basic plotting and visualization framework
- **seaborn** - Statistical data visualization for enhanced plot aesthetics
- **plotly** - Interactive geographic visualizations and mapping
- **sqlite3** - Database operations for data storage and SQL joins
- **ipykernel** - Jupyter kernel for notebook environments

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

### Source Repository

**Modified Sparkov Data Generation Tool:** https://github.com/lcabrp/Sparkov_Data_Generation

This fork provides enhanced data generation capabilities with improved normalization and modern transaction patterns compared to the original implementation.

## Project Objective

### Credit Card Transaction Insights and Fraud Pattern Analysis

**Main Problem to Solve:**
Analyze credit card transaction data to uncover key spending patterns and identify characteristics that distinguish fraudulent from legitimate transactions.

**Core Research Questions:**

1. **Customer Spending Patterns**
   - How do average transaction amounts vary across customer demographic profiles?
   - Which customer segments generate the highest transaction volumes?

2. **Transaction Timing Analysis**
   - What are the peak transaction hours and days of the week?
   - Are there temporal patterns that correlate with fraud occurrence?

3. **Fraud vs. Legitimate Transaction Characteristics**
   - How do transaction amounts and merchant distances differ between fraudulent and legitimate transactions?
   - What geographic patterns exist in fraudulent transactions?

4. **Transaction Category and Geographic Analysis**
   - Which transaction categories are most common across different regions?
   - How does customer location relate to merchant location patterns?

**Expected Deliverables:**
- Comprehensive data analysis with multiple visualizations
- Data-driven insights about customer behavior and fraud patterns
- Recommendations for transaction monitoring based on findings

**Why This Approach:**
This objective leverages the dataset's rich demographic and transaction data while focusing on exploratory data analysis and business insights.

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

### Transaction Data (53 transaction files)

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
- **Fraud Rate**: ~0.2% (realistic fraud detection scenario)
- **Data Quality**: No missing values detected
- **File Format**: CSV with pipe (|) delimiter
- **Total Dataset Size**: ~639 MB

## Project Structure

```
card_transactions_analysis/
├── data/                               # Generated transaction data (53 CSV files)
│   ├── customers.csv                   # Customer demographics and profiles
│   └── *.csv                          # Transaction files by demographic groups
├── 01_data_transf.ipynb               # Data transformation and database creation
├── 02_analysis.ipynb                  # Main analysis with visualizations and insights
├── data_dictionary_and_summary.ipynb  # Initial EDA and project planning
├── useful_functions.py                # Custom functions for data processing
├── fraud_detection.db                 # SQLite database with cleaned data
├── README.md                          # Project documentation
├── requirements.txt                   # Python dependencies (pip)
└── pyproject.toml                     # UV dependencies (modern package management)
```

## Analysis Completed

This project includes comprehensive analysis of credit card transaction patterns and fraud detection insights:

### Data Processing & Engineering
- **Data Cleaning**: Processed 4.7M+ transactions across 53 CSV files with proper data type optimization
- **Feature Engineering**: Created time-based features (hour, day_of_week) and geographic features (distance between customer and merchant)
- **Database Integration**: Stored cleaned data in SQLite database with proper primary/foreign keys and indexes

### Key Findings
- **Fraud Patterns**: Fraud rate varies by time of day and transaction category, with certain merchant categories showing higher risk
- **Geographic Insights**: Distance analysis shows fraud rates remain consistent (0.199%-0.207%) across all customer-merchant distance ranges
- **Customer Demographics**: Analysis reveals spending patterns across different population groups and locations
- **Temporal Patterns**: Clear patterns in transaction volume and fraud rates by hour and day of week

### Technical Implementation
- **SQL Joins**: Used INNER JOIN between customers and transactions tables to retrieve analysis data
- **Custom Functions**: Implemented 10 reusable functions with proper type hints and documentation
- **Visualizations**: Created multiple plot types (bar charts, scatter plots, line plots, stacked charts) with consistent styling

## Future Analysis Opportunities

- Machine learning fraud detection models
- Customer lifetime value analysis
- Seasonal transaction pattern analysis
- Geographic fraud hotspot identification
