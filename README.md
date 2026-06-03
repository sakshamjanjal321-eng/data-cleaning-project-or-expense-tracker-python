# Expense Tracker & Data Cleaning Pipeline

A python-based personal finance manager (Expense Tracker) paired with an automated, robust Pandas data-cleaning pipeline.

## Project Structure

```text
expense-tracker/
│
├── data/
│   ├── expenses.csv           # Raw database of recorded expenses
│   └── clean_data.csv         # Cleaned output from the pipeline
│
├── src/
│   ├── expense_tracker.py     # Command-line interface for expense tracking
│   └── data_cleaning.py       # Automated data-cleaning pipeline
│
├── tests/
│   └── test_expense_tracker.py # Pytest unit test suite
│
├── README.md                  # Project documentation
├── requirements.txt           # Python package dependencies
└── .gitignore                 # Files excluded from git tracking
```

---

## Getting Started

### Prerequisites

Ensure you have Python 3.8+ installed on your system.

### Installation

1. Clone the repository:
   ```bash
   git clone <your-repository-url>
   cd expense-tracker
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### 1. Expense Tracker
An interactive CLI tool to log your daily expenses across categories (food, transport, utilities, entertainment, and other), view summary statistics, and filter entries by specific months.

Run the tracker with:
```bash
python src/expense_tracker.py
```

**Features:**
*   **Add Expense**: Automatically timestamped inputs.
*   **View Summary**: Total spending, categorized breakdown, and percentage distribution.
*   **List Recent**: View details of recent logs.
*   **Filter by Month**: Interactively select any month present in the database to see custom breakdowns.

---

### 2. Data Cleaning Pipeline
An automated Pandas pipeline designed to clean messy dataset inputs (such as null fields, wrong formats, inconsistent text casings, and statistical outliers).

Run the pipeline with:
```bash
python src/data_cleaning.py
```

**Clean-up Steps Performed:**
1.  **Standardize Column Names**: Strips whitespace and normalizes names to `snake_case`.
2.  **Remove Duplicates**: Drops exact duplicate rows.
3.  **Handle Missing Values**: Drops missing key identifiers; fills numeric nulls with column median, and text nulls with `"Unknown"`.
4.  **Fix Data Types**: Standardizes date formats and converts columns to numeric representations.
5.  **Standardize Text**: Trims spaces and formats strings to Title Case.
6.  **Remove Outliers**: Caps extreme outliers mathematically using the Interquartile Range (IQR) method.

---

## Running Tests

Unit tests are written using `pytest`. Run the test suite from the root of the project:

```bash
pytest
```
