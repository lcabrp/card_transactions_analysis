# Credit Card Transactions Analysis — Copilot Instructions

This repo analyzes **synthetic credit card transaction data** for fraud detection and customer behavior patterns. Primary focus: fraud rate analysis, geographic patterns, time-based trends, and customer segmentation using 4.74M transactions.

**Data Source:** Synthetic credit card transactions (2020-2025)  
**Database:** SQLite (fraud_detection.db)  
**Tech Stack:** Python 3.13, pandas, numpy, matplotlib, seaborn, plotly, Jupyter notebooks  
**Optional:** RAPIDS cuDF for GPU acceleration

---

## Project Structure

```
card_transactions_analysis/
├── 01_data_transf.ipynb           # Data transformation & feature engineering
├── 02_analysis.ipynb              # Fraud analysis & visualizations
├── data_dictionary_and_summary.ipynb  # Data exploration & schema
├── useful_functions.py            # Reusable utilities
├── fraud_detection.db             # SQLite database
├── data/                          # Source CSV files
├── docs/                          # Documentation
├── gpu_test.py                    # RAPIDS/CUDA validation
└── pyproject.toml                 # Dependencies
```

---

## Python/Notebook Conventions

### GPU Acceleration Pattern (Optional)

Both main notebooks use **cudf.pandas** accelerator for GPU acceleration when available:

```python
# At notebook top (comment out if no CUDA GPU)
%load_ext cudf.pandas

# Convert GPU DataFrames to CPU pandas before plotting
from useful_functions import to_plain_pandas

# ✓ CORRECT - Convert before plotting
plot_df = to_plain_pandas(df, ['column1', 'column2'])
sns.scatterplot(data=plot_df, x='column1', y='column2')

# ✗ WRONG - Direct GPU DataFrame to plotting libraries
sns.scatterplot(data=df, x='column1', y='column2')  # Type errors!
```

**Why this matters:**
- `cudf.pandas` accelerates pandas operations on GPU with zero code changes
- Plotting libraries (seaborn, matplotlib, plotly) expect CPU pandas/NumPy arrays
- Always convert to plain pandas right before plotting to avoid type errors

**To disable GPU acceleration:**
- Comment out or remove `%load_ext cudf.pandas` at notebook top
- Everything runs on CPU with standard pandas

### Data Type Optimization

Use memory-efficient dtypes for large datasets:

```python
from useful_functions import optimize_df_types

# Optimize DataFrame memory usage
df = optimize_df_types(df)  # Downcasts int64→int32/int16, etc.
```

### Helper Functions (useful_functions.py)

**Key utilities:**

```python
from useful_functions import (
    to_plain_pandas,      # GPU→CPU DataFrame conversion
    get_files_dir,        # Get all files matching pattern
    show_df_info,         # Display DataFrame summary
    optimize_df_types     # Optimize memory usage
)

# Get all CSV files in directory
csv_files = get_files_dir('data/', '*.csv')

# Display comprehensive DataFrame info
show_df_info(df)
```

### pandas Style Preferences

```python
# Prefer explicit column selection
df[['trans_date_trans_time', 'amt', 'is_fraud', 'category']]

# Use descriptive variable names
fraud_df, customer_stats, geo_patterns

# Round metrics consistently
.round(2)  # percentages, rates, amounts
.round(0)  # counts

# Date handling
df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])
```

---

## Database Conventions

### SQLite Usage

**Connection pattern:**

```python
import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect('fraud_detection.db')

# Read query into DataFrame
query = """
SELECT 
    category,
    COUNT(*) as transaction_count,
    SUM(is_fraud) as fraud_count,
    AVG(amt) as avg_amount
FROM transactions
WHERE trans_date_trans_time >= '2024-01-01'
GROUP BY category
"""
df = pd.read_sql_query(query, conn)

# Always close connection
conn.close()
```

**SQL style:**
- Use uppercase for SQL keywords: `SELECT`, `FROM`, `WHERE`, `GROUP BY`
- Indent multi-line queries for readability
- Add descriptive aliases: `COUNT(*) as transaction_count`

---

## Analysis Patterns

### Fraud Detection Metrics

**Key metrics:**
- **Fraud Rate:** `SUM(is_fraud) / COUNT(*)` by various dimensions
- **Time-based patterns:** Hourly/daily/weekend fraud rates
- **Category analysis:** Fraud rates by merchant category
- **Geographic patterns:** Distance analysis, state-level fraud rates

```python
# Calculate fraud rate by category
fraud_by_category = df.groupby('category').agg({
    'is_fraud': ['sum', 'count', 'mean']
}).round(4)
fraud_by_category.columns = ['fraud_count', 'total_txns', 'fraud_rate']
```

### Geographic Analysis

**Distance calculation:**
```python
# Customer-merchant distance (already in source data)
# 'distance' column contains haversine distance in km
```

**State-level aggregations:**
```python
# Aggregate by state
state_stats = df.groupby('state').agg({
    'amt': ['sum', 'mean', 'count'],
    'is_fraud': ['sum', 'mean']
}).round(2)
```

### Time Series Analysis

**Extract time components:**
```python
# Extract hour, day of week, is_weekend
df['hour'] = df['trans_date_trans_time'].dt.hour
df['day_of_week'] = df['trans_date_trans_time'].dt.dayofweek
df['is_weekend'] = df['day_of_week'].isin([5, 6])
```

**Time-based aggregations:**
```python
# Fraud rate by hour
hourly_fraud = df.groupby('hour')['is_fraud'].agg(['sum', 'count', 'mean'])
```

---

## Visualization Conventions

### Plotting Library Selection

- **Matplotlib/Seaborn:** Statistical plots, distributions, categorical comparisons
- **Plotly:** Interactive maps, geographic visualizations

### Standard Plot Patterns

```python
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Seaborn style
sns.set_style('whitegrid')

# Figure sizing
plt.figure(figsize=(12, 6))

# For GPU-accelerated data, always convert first
plot_df = to_plain_pandas(df, ['x_col', 'y_col', 'hue_col'])
sns.scatterplot(data=plot_df, x='x_col', y='y_col', hue='hue_col')

# Plotly geographic
fig = px.scatter_geo(
    df, 
    lat='lat', 
    lon='long',
    color='is_fraud',
    hover_name='city',
    scope='usa'
)
fig.show()
```

---

## Data Characteristics & Limitations

### Synthetic Data

**Important:** This is **computer-generated data** simulating real patterns:
- Transaction patterns are modeled, not actual historical data
- Fraud patterns are programmatically generated
- May not capture all real-world complexities

### Time Period

- Data spans **2020-2025** (includes some future dates as projections)
- 4.74 million transactions
- 1,010 unique customers

### Geographic Scope

- US-based transactions only
- Customer and merchant locations within United States
- Distance calculations use haversine formula

---

## Common Workflows

### Initial Data Exploration

1. **Load data:** Read CSVs or query SQLite
2. **Check quality:** `show_df_info(df)` for schema and memory
3. **Optimize types:** `df = optimize_df_types(df)`
4. **Explore fraud rates:** Basic aggregations by key dimensions

### Fraud Pattern Analysis

1. **Time patterns:** Hourly/daily/weekend fraud rates
2. **Category analysis:** Fraud rates by merchant category
3. **Geographic patterns:** State-level and distance analysis
4. **Customer behavior:** Segmentation by age/location

### Visualization Pipeline

1. **Prepare data:** Filter and aggregate as needed
2. **Convert GPU data:** Use `to_plain_pandas()` if using cudf.pandas
3. **Create plots:** Seaborn for statistical, Plotly for geographic
4. **Save outputs:** Export plots and summary tables

---

## Setup & Dependencies

### Standard Installation (uv)

```bash
uv sync  # Install dependencies from pyproject.toml
```

### Traditional pip

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### GPU Acceleration (Optional)

**RAPIDS cuDF** on WSL2 + Conda:

```bash
conda create -n rapids-25.08 -c rapidsai -c conda-forge -c nvidia \
    rapids=25.08 python=3.13 cuda-version=12.5
conda activate rapids-25.08
```

**Windows/macOS:**
- RAPIDS not officially supported
- Comment out `%load_ext cudf.pandas` in notebooks
- Runs on CPU with standard pandas

---

## Performance Considerations

### Memory Optimization

- Use `optimize_df_types()` to reduce memory footprint
- Filter data early: `df = df[df['trans_date_trans_time'] >= '2024-01-01']`
- Drop unnecessary columns before operations

### GPU vs CPU

- **GPU (cudf.pandas):** 2-10× speedup on large operations
- **CPU (pandas):** Works everywhere, simpler setup
- **Hybrid:** GPU compute, CPU for plotting

### SQLite Performance

- Index frequently queried columns
- Use `WHERE` clauses to limit rows early
- Close connections when done

---

## Documentation

- **README.md:** Project overview, setup instructions, key findings
- **docs/:** Additional analysis documentation
- **Notebooks:** Self-documenting with markdown cells

---

## References

- **Data Source:** Synthetic credit card transactions
- **Database Schema:** See `data_dictionary_and_summary.ipynb`
- **RAPIDS cuDF:** https://rapids.ai/
- **Fraud Detection Metrics:** See `02_analysis.ipynb`
