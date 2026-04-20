import pandas as pd
from rdkit import Chem

INPUT_FILE = r"C:\Users\HP\Desktop\thesis\script\example\filtered_pairs.csv"
REPORT_FILE = r"C:\Users\HP\Desktop\thesis\script\example\filtered_pairs_inspection_report.csv"
CLEAN_OUTPUT_FILE = r"C:\Users\HP\Desktop\thesis\script\example\filtered_pairs_clean.csv"

# Read file
df = pd.read_csv(INPUT_FILE)

# Adjust these if your column names are different
SMILES1_COL = "1"
SMILES2_COL = "2"

if SMILES1_COL not in df.columns or SMILES2_COL not in df.columns:
    raise ValueError(
        f"Expected SMILES columns '{SMILES1_COL}' and '{SMILES2_COL}' not found. "
        f"Available columns: {list(df.columns)}"
    )

report_rows = []
valid_row_indices = []

for idx, row in df.iterrows():
    smiles1 = "" if pd.isna(row[SMILES1_COL]) else str(row[SMILES1_COL]).strip()
    smiles2 = "" if pd.isna(row[SMILES2_COL]) else str(row[SMILES2_COL]).strip()

    status1 = "valid"
    status2 = "valid"

    if smiles1 == "":
        status1 = "empty"
        mol1 = None
    else:
        mol1 = Chem.MolFromSmiles(smiles1)
        if mol1 is None:
            status1 = "invalid"

    if smiles2 == "":
        status2 = "empty"
        mol2 = None
    else:
        mol2 = Chem.MolFromSmiles(smiles2)
        if mol2 is None:
            status2 = "invalid"

    row_status = "valid_pair" if status1 == "valid" and status2 == "valid" else "invalid_pair"

    report_rows.append({
        "original_row": idx,
        "smiles1": smiles1,
        "smiles2": smiles2,
        "smiles1_status": status1,
        "smiles2_status": status2,
        "row_status": row_status
    })

    if row_status == "valid_pair":
        valid_row_indices.append(idx)

# Save inspection report
report_df = pd.DataFrame(report_rows)
report_df.to_csv(REPORT_FILE, index=False)

print(f"Inspection report saved to: {REPORT_FILE}")
print(report_df["row_status"].value_counts(dropna=False))
print("\nSMILES1 status counts:")
print(report_df["smiles1_status"].value_counts(dropna=False))
print("\nSMILES2 status counts:")
print(report_df["smiles2_status"].value_counts(dropna=False))

# Keep only valid rows
clean_df = df.loc[valid_row_indices].copy()

# Save cleaned filtered file
clean_df.to_csv(CLEAN_OUTPUT_FILE, index=False)

print(f"\nClean filtered file saved to: {CLEAN_OUTPUT_FILE}")
print(f"Number of valid rows kept: {len(clean_df)}")