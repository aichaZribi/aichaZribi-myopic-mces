import pandas as pd
import matplotlib.pyplot as plt

# =========================
# PATHS
# =========================
paths = [
    r"C:\Users\HP\Desktop\thesis\script\example\filter_mass_diff_and_size\filtered_pairs_0_200.csv",
    r"C:\Users\HP\Desktop\thesis\script\example\filter_mass_diff_and_size\filtered_pairs_200_300.csv",
    r"C:\Users\HP\Desktop\thesis\script\example\filter_mass_diff_and_size\filtered_pairs_300_500.csv",
    r"C:\Users\HP\Desktop\thesis\script\example\filter_mass_diff_and_size\filtered_pairs_500_800.csv",
    r"C:\Users\HP\Desktop\thesis\script\example\filter_mass_diff_and_size\filtered_pairs_800_1000.csv"
]

# =========================
# LOAD + PREPARE
# =========================
dfs = []
for p in paths:
    df = pd.read_csv(p)
    df["source"] = p.split("\\")[-1]
    dfs.append(df)

df_all = pd.concat(dfs, ignore_index=True)

# keep only non-skipped rows
df_all = df_all[df_all["skipped"] == 0].copy()

# average mass
df_all["avg_mass"] = (df_all["mass1"] + df_all["mass2"]) / 2

# =========================
# BEST PLOT
# Runtime vs average mass, colored by solver usage
# =========================
plt.figure(figsize=(8, 6))

df0 = df_all[df_all["solverCalled"] == 0]
df1 = df_all[df_all["solverCalled"] == 1]

plt.scatter(df0["avg_mass"], df0["runtime_sec"], label="solverCalled = 0", alpha=0.7)
plt.scatter(df1["avg_mass"], df1["runtime_sec"], label="solverCalled = 1", alpha=0.7)

plt.xlabel("Average Mass")
plt.ylabel("Runtime (sec)")
plt.title("Runtime vs Average Mass, Colored by Solver Usage")
plt.legend()
plt.tight_layout()
plt.show()