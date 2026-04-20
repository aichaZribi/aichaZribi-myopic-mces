import pandas as pd
import random

INPUT_FILE = r"C:\Users\HP\Desktop\thesis\script\example\compound_data.csv"
OUTPUT_FILE = r"C:\Users\HP\Desktop\thesis\script\example\example_compound_data.csv"

df = pd.read_csv(INPUT_FILE)

smiles = (
    df["smiles"]
    .dropna()
    .astype(str)
    .str.strip()
)

smiles = smiles[smiles != ""].tolist()

if len(smiles) < 2:
    raise ValueError("Not enough valid SMILES to create example-style pairs.")

random.seed(42)
random.shuffle(smiles)

if len(smiles) % 2 != 0:
    smiles = smiles[:-1]

rows = []
for i in range(0, len(smiles), 2):
    idx = i // 2
    smiles1 = smiles[i]
    smiles2 = smiles[i + 1]
    rows.append([idx, smiles1, smiles2])

out_df = pd.DataFrame(rows)
out_df.to_csv(OUTPUT_FILE, index=False, header=False)

print(f"Created {OUTPUT_FILE} with {len(out_df)} rows.")