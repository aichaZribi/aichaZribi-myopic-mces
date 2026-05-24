import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import re

# ---------------------------------------------------
# Load files
# ---------------------------------------------------

files = glob.glob(r"C:\Users\HP\Desktop\thesis\script\example\filter_mass_diff_and_size\filtered_pairs_800_1000_Highs_thread_*.csv")


dfs = []

for file in files:
    threads = int(re.search(r"thread_(\d+)", os.path.basename(file)).group(1))
    df = pd.read_csv(file)
    df["threads"] = threads
    dfs.append(df)

data = pd.concat(dfs, ignore_index=True)

# ---------------------------------------------------
# Keep only rows where solver was called
# ---------------------------------------------------

solver_data = data[data["ilp_solver"] == 1].copy()

# ---------------------------------------------------
# Runtime summary: mean, median, sum
# ---------------------------------------------------

runtime_summary = solver_data.groupby("threads").agg(
    number_of_solver_calls=("runtime_sec", "count"),
    mean_runtime=("runtime_sec", "mean"),
    median_runtime=("runtime_sec", "median"),
    total_runtime=("runtime_sec", "sum"),
    min_runtime=("runtime_sec", "min"),
    max_runtime=("runtime_sec", "max")
).reset_index()

runtime_summary = runtime_summary.sort_values("threads")

# Runtime decrease compared to 1 thread
baseline_runtime = runtime_summary.loc[
    runtime_summary["threads"] == runtime_summary["threads"].min(),
    "mean_runtime"
].iloc[0]

runtime_summary["mean_runtime_decrease_%"] = (
    (baseline_runtime - runtime_summary["mean_runtime"])
    / baseline_runtime
) * 100

print("\n=== Runtime Summary: Solver Called Only ===")
print(runtime_summary)

# ---------------------------------------------------
# Skipped lines summary
# ---------------------------------------------------

skipped_summary = data.groupby("threads").agg(
    total_lines=("threads", "count"),
    skipped_lines=("skipped", "sum"),
    not_skipped_lines=("skipped", lambda x: (x == 0).sum())
).reset_index()

skipped_summary = skipped_summary.sort_values("threads")

print("\n=== Skipped Lines Summary ===")
print(skipped_summary)

# ---------------------------------------------------
# Plot mean, median, and total runtime
# ---------------------------------------------------

plt.figure(figsize=(9, 5))

plt.plot(
    runtime_summary["threads"],
    runtime_summary["mean_runtime"],
    marker="o",
    label="Mean runtime"
)

plt.plot(
    runtime_summary["threads"],
    runtime_summary["median_runtime"],
    marker="o",
    label="Median runtime"
)

plt.xlabel("Number of Threads")
plt.ylabel("Runtime (seconds)")
plt.title("Mean and Median Runtime vs Threads\nSolver Called Only")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(9, 5))

plt.plot(
    runtime_summary["threads"],
    runtime_summary["total_runtime"],
    marker="o"
)

plt.xlabel("Number of Threads")
plt.ylabel("Total Runtime (seconds)")
plt.title("Total Runtime vs Threads\nSolver Called Only")
plt.grid(True)
plt.tight_layout()
plt.show()

# ---------------------------------------------------
# Bar plot: total skipped pairs per thread
# ---------------------------------------------------

skipped_summary = data.groupby("threads").agg(
    total_pairs=("skipped", "count"),
    skipped_pairs=("skipped", "sum"),
    not_skipped_pairs=("skipped", lambda x: (x == 0).sum())
).reset_index()

skipped_summary = skipped_summary.sort_values("threads")

print("\n=== Skipped Pairs Summary ===")
print(skipped_summary)

plt.figure(figsize=(8, 5))

plt.bar(
    skipped_summary["threads"].astype(str),
    skipped_summary["skipped_pairs"]
)

plt.xlabel("Number of Threads")
plt.ylabel("Number of Skipped Pairs")
plt.title("Total Skipped Pairs per Thread")
plt.tight_layout()
plt.show()

# ---------------------------------------------------
# Check if skipped lines were solved with more threads
# ---------------------------------------------------

if "pair_id" in data.columns:

    pivot = data.pivot_table(
        index="pair_id",
        columns="threads",
        values="skipped",
        aggfunc="first"
    )

    lowest_thread = min(data["threads"].unique())

    higher_threads = [
        t for t in sorted(data["threads"].unique())
        if t > lowest_thread
    ]

    solved_later = pivot[
        (pivot[lowest_thread] == 1) &
        (pivot[higher_threads] == 0).any(axis=1)
    ]

    print("\n=== Lines skipped with lowest thread count but solved with more threads ===")
    print(solved_later)

    print("\nNumber of skipped lines solved after increasing threads:")
    print(len(solved_later))

# ---------------------------------------------------
# Find IDs solved with 1 thread but skipped with 24
# ---------------------------------------------------

# Create pivot table:
# rows = pair_id
# columns = thread count
# values = skipped status

pivot = data.pivot_table(
    index="pair_id",
    columns="threads",
    values="skipped",
    aggfunc="first"
)

# Condition:
# thread 1 -> solved (skipped == 0)
# thread 24 -> skipped (skipped == 1)

solved_1_skipped_24 = pivot[
    (pivot[1] == 0) &
    (pivot[24] == 1)
]

print("\n=== IDs solved with 1 thread but skipped with 24 ===")
print(solved_1_skipped_24.index.tolist())

print("\nCount:")
print(len(solved_1_skipped_24))