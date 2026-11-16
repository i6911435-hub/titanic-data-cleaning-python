import os
import sys
import pandas as pd
import numpy as np


def run_data_cleansing(input_csv="cleaned_titanic.csv", output_dir="Output"):
  if not os.path.exists(input_csv):
    print(f"Error: Input file '{input_csv}' not found.")
    sys.exit(1)

  os.makedirs(output_dir, exist_ok=True)
  report = []
  report.append("TITANIC DATA CLEANSING - EXECUTION REPORT")
  report.append("=" * 64)

  # 5.1 Data Loading and Inspection
  df = pd.read_csv(input_csv)
  orig_rows, orig_cols = df.shape
  orig_dups = int(df.duplicated().sum())
  orig_missing_series = df.isna().sum()
  orig_missing_total = int(orig_missing_series.sum())

  report.append(f"Original shape: {orig_rows} rows x {orig_cols} columns")
  report.append(f"Exact duplicate rows before cleaning: {orig_dups}")
  report.append("\nMissing values before cleaning:")
  report.append(orig_missing_series.to_string())
  report.append("")

  # 5.2 Text Standardization (Whitespace removal)
  text_cols = df.select_dtypes(include=["object", "string"]).columns.tolist()
  for col in text_cols:
    df[col] = df[col].astype(str).str.strip()
  report.append("Step 1 - Text whitespace cleaned.")

  # 5.3 Duplicate Removal
  dups_removed = int(df.duplicated().sum())
  df = df.drop_duplicates().reset_index(drop=True)
  report.append(f"Step 2 - Duplicate rows removed: {dups_removed}")

  # 5.4 Data Type Correction
  for col in ["PassengerId", "Survived", "Pclass", "SibSp", "Parch"]:
    if col in df.columns:
      df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
  for col in ["Age", "Fare"]:
    if col in df.columns:
      df[col] = pd.to_numeric(df[col], errors="coerce")
  report.append("Step 3 - Numeric columns converted to appropriate numeric types.")

  # 5.5 Handling Invalid Values (Negative Age / Fare check)
  neg_age = int((df["Age"] < 0).sum()) if "Age" in df.columns else 0
  neg_fare = int((df["Fare"] < 0).sum()) if "Fare" in df.columns else 0
  if "Age" in df.columns:
    df.loc[df["Age"] < 0, "Age"] = np.nan
  if "Fare" in df.columns:
    df.loc[df["Fare"] < 0, "Fare"] = np.nan
  report.append(
      f"Step 4 - Invalid negative Age values corrected: {neg_age}; negative Fare"
      f" values corrected: {neg_fare}."
  )

  # 5.6 Handling Missing Values (Group Median & Mode)
  if "Age" in df.columns:
    if {"Pclass", "Sex"}.issubset(df.columns):
      df["Age"] = df.groupby(["Pclass", "Sex"], dropna=False)["Age"].transform(
          lambda s: s.fillna(s.median())
      )
    df["Age"] = df["Age"].fillna(df["Age"].median())

  if "Embarked" in df.columns:
    df["Embarked"] = df["Embarked"].replace(
        {"nan": np.nan, "NaN": np.nan, "None": np.nan, "": np.nan}
    )
    if df["Embarked"].isna().any():
      df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])

  if "Cabin" in df.columns:
    df["CabinKnown"] = df["Cabin"].notna().astype(int)
    df = df.drop(columns=["Cabin"])

  for col in df.select_dtypes(include=[np.number]).columns:
    if df[col].isna().any():
      df[col] = df[col].fillna(df[col].median())
  for col in df.select_dtypes(include=["object", "string"]).columns:
    if df[col].isna().any():
      df[col] = df[col].fillna(df[col].mode()[0])

  final_missing_total = int(df.isna().sum().sum())
  report.append(
      f"Step 5 - Missing cells before: {orig_missing_total}; after:"
      f" {final_missing_total}."
  )

  # 5.7 Handling Inconsistent Data (Case Normalization)
  if "Sex" in df.columns:
    df["Sex"] = df["Sex"].str.strip().str.lower()
  if "Embarked" in df.columns:
    df["Embarked"] = df["Embarked"].str.strip().str.upper()
  report.append(
      "Step 6 - Categorical text values standardized (Sex lowercase; Embarked"
      " uppercase)."
  )

  # 5.8 Outlier Detection (IQR Rule - Flagged, not deleted)
  report.append(
      "Step 7 - Outliers detected with the IQR rule and flagged, not deleted."
  )
  for col in ["Age", "Fare", "SibSp", "Parch"]:
    if col in df.columns:
      q1 = df[col].quantile(0.25)
      q3 = df[col].quantile(0.75)
      iqr = q3 - q1
      lower = q1 - 1.5 * iqr
      upper = q3 + 1.5 * iqr
      flag_col = f"{col}_OutlierFlag"
      df[flag_col] = ((df[col] < lower) | (df[col] > upper)).astype(int)
      report.append(f"  {col}: {int(df[flag_col].sum())} potential outlier(s)")

  # 5.9 Data Validation
  val_dups = int(df.duplicated().sum()) == 0
  val_miss = int(df.isna().sum().sum()) == 0
  val_age = bool((df["Age"] >= 0).all()) if "Age" in df.columns else True
  val_fare = bool((df["Fare"] >= 0).all()) if "Fare" in df.columns else True
  val_surv = (
      bool(df["Survived"].isin([0, 1]).all()) if "Survived" in df.columns else True
  )

  report.append("\nStep 8 - Data validation:")
  report.append(f"  No duplicate rows: {'PASS' if val_dups else 'FAIL'}")
  report.append(f"  No missing cells: {'PASS' if val_miss else 'FAIL'}")
  report.append(f"  Age non-negative: {'PASS' if val_age else 'FAIL'}")
  report.append(f"  Fare non-negative: {'PASS' if val_fare else 'FAIL'}")
  report.append(f"  Survived values are 0/1: {'PASS' if val_surv else 'FAIL'}")

  # 5.10 Exporting the Cleaned Dataset
  out_csv = os.path.join(output_dir, "final_cleaned_titanic.csv")
  out_txt = os.path.join(output_dir, "cleaning_execution_report.txt")
  df.to_csv(out_csv, index=False)

  report.append(f"\nCleaned dataset saved to: {os.path.abspath(out_csv)}")
  report.append(f"Final shape: {df.shape[0]} rows x {df.shape[1]} columns")
  report.append("\nMissing values after cleaning:")
  report.append(df.isna().sum().to_string())

  full_report = "\n".join(report)
  with open(out_txt, "w", encoding="utf-8") as f:
    f.write(full_report)

  print(full_report)
  print(
      "\nSUCCESS: Cleaned CSV and execution report saved in"
      f" {output_dir} folder."
  )


if __name__ == "__main__":
  run_data_cleansing("cleaned_titanic.csv")