import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

# =========================
# PATHS
# =========================
INPUT_PATH = r"C:\Users\HP\Desktop\thesis\script\example\example_compound_data.csv"
OUTPUT_PATH = r"C:\Users\HP\Desktop\thesis\script\example\filtered_pairs.csv"

# Columns (based on your example)
SMILES1_COL = 1
SMILES2_COL = 2

MASS_TOLERANCE = 1.0
USE_EXACT_MASS = False

# =========================
# FUNCTION
# =========================
def compute_mass(smiles):
    if pd.isna(smiles):
        return None

    smiles = str(smiles).strip()
    if not smiles:
        return None

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None

    return Descriptors.ExactMolWt(mol) if USE_EXACT_MASS else Descriptors.MolWt(mol)

# =========================
# MAIN
# =========================
print("Loading data...")
df = pd.read_csv(INPUT_PATH, header=None)

print("Computing masses...")
df["mass1"] = df.iloc[:, SMILES1_COL].apply(compute_mass)
df["mass2"] = df.iloc[:, SMILES2_COL].apply(compute_mass)

# Remove invalid rows
invalid = df["mass1"].isna() | df["mass2"].isna()
invalid_count = invalid.sum()
df = df[~invalid].reset_index(drop=True)

print(f"Invalid rows removed: {invalid_count}")

# Compute mass difference
df["mass_diff"] = (df["mass1"] - df["mass2"]).abs()

# Filter
filtered_df = df[df["mass_diff"] <= MASS_TOLERANCE].copy()

print(f"Rows before filtering: {len(df)}")
print(f"Rows after filtering: {len(filtered_df)}")

# Save (keep original + new columns)
filtered_df.to_csv(OUTPUT_PATH, index=False)

print("Done ✅")
print(f"Saved to: {OUTPUT_PATH}")