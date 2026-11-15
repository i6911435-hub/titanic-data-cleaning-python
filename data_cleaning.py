"""
Titanic Dataset Data Cleaning Project
1) Download train.csv from the Kaggle page linked in README.md.
2) Put train.csv inside the data/ folder.
3) Run: pip install pandas matplotlib
4) Run: python data_cleaning.py

The script creates cleaned_titanic.csv and genuine screenshots from the downloaded file.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "train.csv"
OUT = ROOT / "data" / "cleaned_titanic.csv"
SHOTS = ROOT / "screenshots"
SHOTS.mkdir(exist_ok=True)

if not DATA.exists():
    raise FileNotFoundError(
        "Missing data/train.csv. Download train.csv from the Kaggle Titanic page "
        "and place it in the project's data folder."
    )

df = pd.read_csv(DATA)
print("BEFORE PROCESSING")
print("Shape:", df.shape)
print(df.head().to_string(index=False))
print("\\nMissing values by column:\\n", df.isna().sum())
print("\\nDuplicate rows:", df.duplicated().sum())

# Screenshot 1: original dataset preview
fig, ax = plt.subplots(figsize=(13, 3.2))
ax.axis("off")
ax.set_title(f"Before Processing — first 8 rows | shape={df.shape}", weight="bold")
tbl = ax.table(cellText=df.head(8).fillna("MISSING").astype(str).values,
               colLabels=df.columns, loc="center", cellLoc="left")
tbl.auto_set_font_size(False); tbl.set_fontsize(6); tbl.scale(1, 1.35)
plt.tight_layout(); plt.savefig(SHOTS / "01_before_processing.png", dpi=180); plt.close()

# Screenshot 2: missing values discovery
missing = df.isna().sum()
fig, ax = plt.subplots(figsize=(9, 4))
ax.axis("off")
ax.set_title("Missing Values Found — df.isna().sum()", weight="bold")
lines = [f"{col:<15} {count}" for col, count in missing.items()]
ax.text(0.05, 0.92, "Column          Missing count\\n" + "\\n".join(lines),
        va="top", family="monospace", fontsize=11)
ax.text(0.05, 0.08, f"Duplicate rows detected: {df.duplicated().sum()}",
        va="bottom", fontsize=11)
plt.tight_layout(); plt.savefig(SHOTS / "02_missing_values.png", dpi=180); plt.close()

# Cleaning operations
clean = df.copy()
# Remove fully duplicated records, if any.
clean = clean.drop_duplicates()
# Remove leading/trailing whitespace from text columns.
for col in clean.select_dtypes(include="object").columns:
    clean[col] = clean[col].str.strip()

# Cabin is missing for most records; retaining it would add little reliable information.
if "Cabin" in clean.columns:
    clean = clean.drop(columns=["Cabin"])

# Median is robust to extreme values; use it for numeric Age.
if "Age" in clean.columns:
    clean["Age"] = clean["Age"].fillna(clean["Age"].median())

# Mode is suitable for the small number of missing categorical Embarked values.
if "Embarked" in clean.columns and clean["Embarked"].isna().any():
    clean["Embarked"] = clean["Embarked"].fillna(clean["Embarked"].mode()[0])

# Save cleaned dataset and validation report.
clean.to_csv(OUT, index=False)
print("\\nAFTER CLEANING")
print("Shape:", clean.shape)
print(clean.head().to_string(index=False))
print("\\nMissing values after cleaning:\\n", clean.isna().sum())
print("Duplicate rows after cleaning:", clean.duplicated().sum())

# Screenshot 3: cleaned dataset preview
fig, ax = plt.subplots(figsize=(13, 3.2))
ax.axis("off")
ax.set_title(f"After Cleaning — first 8 rows | shape={clean.shape}", weight="bold")
tbl = ax.table(cellText=clean.head(8).astype(str).values,
               colLabels=clean.columns, loc="center", cellLoc="left")
tbl.auto_set_font_size(False); tbl.set_fontsize(6); tbl.scale(1, 1.35)
plt.tight_layout(); plt.savefig(SHOTS / "03_after_cleaning.png", dpi=180); plt.close()

# Screenshot 4: validation
after_missing = int(clean.isna().sum().sum())
after_duplicates = int(clean.duplicated().sum())
fig, ax = plt.subplots(figsize=(8, 2.8)); ax.axis("off")
ax.set_title("Final Data Quality Validation", weight="bold")
ax.text(0.08, 0.65, f"Total missing cells: {after_missing}\\nDuplicate rows: {after_duplicates}\\nOutput: {OUT.name}",
        fontsize=13, family="monospace", va="center")
plt.tight_layout(); plt.savefig(SHOTS / "04_validation.png", dpi=180); plt.close()

print(f"\\nScreenshots saved in: {SHOTS}")
print(f"Cleaned CSV saved at: {OUT}")
