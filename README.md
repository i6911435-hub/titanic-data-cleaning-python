# Titanic Dataset — Data Cleaning with Python

## Dataset
**Name:** Titanic: Machine Learning from Disaster (training data, `train.csv`)  
**Source:** Kaggle  
**Dataset page:** https://www.kaggle.com/c/titanic/data

Download `train.csv` from Kaggle and place it at `data/train.csv`. Kaggle may ask you to sign in and accept the competition rules.

## Run the project
```bash
pip install pandas matplotlib
python data_cleaning.py
```

The script creates:
- `data/cleaned_titanic.csv`
- `screenshots/01_before_processing.png`
- `screenshots/02_missing_values.png`
- `screenshots/03_after_cleaning.png`
- `screenshots/04_validation.png`

## Cleaning methods
- Inspect shape, first rows, data types and missing-value counts.
- Check exact duplicate rows and remove them if present.
- Trim leading/trailing whitespace from text fields.
- Drop `Cabin` because the training dataset has very extensive missingness in this field.
- Fill missing `Age` values using the median.
- Fill missing `Embarked` values using the mode.
- Recheck missing values and duplicates; export the cleaned CSV.

## GitHub
Create a new public repository on GitHub (for example `titanic-data-cleaning-python`), upload this folder, and then copy the repository URL into your assignment submission. This project package is not automatically published to GitHub.
