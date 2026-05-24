import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# -----------------------------
# Load data
# -----------------------------
BASE_DIR = Path(__file__).resolve().parents[2]
cbc = pd.read_csv(
    BASE_DIR / "example" / "filter_mass_diff_and_size"/"filtered_pairs_800_1000_PULP_CBC.csv"
)

highs = pd.read_csv(
    BASE_DIR / "example" / "filter_mass_diff_and_size"/"filtered_pairs_800_1000_Highs.csv"
)

# -----------------------------
# Rename columns
# -----------------------------
cbc = cbc.rename(columns={
    "distance": "distance_CBC",
    "runtime_inside_mces": "runtime_CBC",
    "runtime_sec": "total_runtime_CBC",
    "solverCalled": "solverCalled_CBC",
    "compute_mode": "compute_mode_CBC",
})

highs = highs.rename(columns={
    "distance": "distance_HiGHS",
    "runtime_inside_mces": "runtime_HiGHS",
    "runtime_sec": "total_runtime_HiGHS",
    "solverCalled": "solverCalled_HiGHS",
    "compute_mode": "compute_mode_HiGHS",
    "error_message": "error_HiGHS",
})

# -----------------------------
# Merge CBC and HiGHS results
# -----------------------------
df = pd.merge(
    cbc,
    highs[[
        "pair_id",
        "distance_HiGHS",
        "runtime_HiGHS",
        "total_runtime_HiGHS",
        "solverCalled_HiGHS",
        "compute_mode_HiGHS",
        "error_HiGHS"
    ]],
    on="pair_id",
    how="inner"
)

# Keep only pairs where HiGHS ILP solver was called
df = df[df["solverCalled_HiGHS"] == 1].copy()

# -----------------------------
# Cases where both solvers called ILP
# -----------------------------
both_called = df[
    (df["solverCalled_CBC"] == 1) &
    (df["solverCalled_HiGHS"] == 1)
].copy()

both_called = both_called.dropna(subset=[
    "distance_CBC",
    "distance_HiGHS",
    "runtime_CBC",
    "runtime_HiGHS"
])

both_called["same_distance"] = np.isclose(
    both_called["distance_CBC"],
    both_called["distance_HiGHS"],
    atol=1e-6
)

both_called["runtime_difference"] = (
    both_called["runtime_CBC"] -
    both_called["runtime_HiGHS"]
)

both_called["speedup_CBC_over_HiGHS"] = (
    both_called["runtime_CBC"] /
    both_called["runtime_HiGHS"]
)

both_called["faster_solver"] = np.where(
    both_called["runtime_HiGHS"] < both_called["runtime_CBC"],
    "HiGHS",
    "CBC"
)

# -----------------------------
# Fair comparison: same distance only
# -----------------------------
fair = both_called[both_called["same_distance"]].copy()

print("\n===== GENERAL SOLVER COMPARISON =====")
print("Pairs where both solvers called ILP:", len(both_called))
print("Pairs with same distance:", len(fair))
print("Pairs with different distance:", len(both_called) - len(fair))

print("\n===== SAME-DISTANCE RUNTIME COMPARISON =====")
print("Fair comparison pairs:", len(fair))

if len(fair) > 0:
    print("Mean CBC runtime:", fair["runtime_CBC"].mean())
    print("Mean HiGHS runtime:", fair["runtime_HiGHS"].mean())
    print("Median CBC runtime:", fair["runtime_CBC"].median())
    print("Median HiGHS runtime:", fair["runtime_HiGHS"].median())
    print("Mean speedup CBC/HiGHS:", fair["speedup_CBC_over_HiGHS"].mean())

    print("\nFaster solver counts:")
    print(fair["faster_solver"].value_counts())

# -----------------------------
# Plot 1: Boxplot
# -----------------------------
if len(fair) > 0:
    plt.figure(figsize=(7, 5))

    plt.boxplot(
        [
            fair["runtime_CBC"],
            fair["runtime_HiGHS"]
        ],
        tick_labels=["CBC", "HiGHS"]
    )

    plt.ylabel("Runtime inside MCES (seconds)")
    plt.title("Runtime distribution on same-distance pairs")
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(
        "01_runtime_boxplot_same_distance.png",
        dpi=300
    )

    plt.show()

# -----------------------------
# Plot 2: Runtime per pair ID
# -----------------------------
if len(fair) > 0:
    plot_df = fair.sort_values("runtime_CBC").copy()

    x = np.arange(len(plot_df))
    width = 0.4

    plt.figure(figsize=(14, 6))

    plt.bar(
        x - width / 2,
        plot_df["runtime_CBC"],
        width,
        label="CBC"
    )

    plt.bar(
        x + width / 2,
        plot_df["runtime_HiGHS"],
        width,
        label="HiGHS"
    )

    plt.xlabel("Pair ID")
    plt.ylabel("Runtime inside MCES (seconds)")
    plt.title("Runtime per pair on same-distance pairs")

    plt.xticks(
        x,
        plot_df["pair_id"],
        rotation=90,
        fontsize=7
    )

    plt.legend()
    plt.tight_layout()

    plt.savefig(
        "02_runtime_per_pair_same_distance.png",
        dpi=300
    )

    plt.show()

# -----------------------------
# Export same-distance analysis
# -----------------------------
same_distance_columns = [
    "pair_id",
    "distance_CBC",
    "distance_HiGHS",
    "runtime_CBC",
    "runtime_HiGHS",
    "runtime_difference",
    "speedup_CBC_over_HiGHS",
    "faster_solver",
    "compute_mode_CBC",
    "compute_mode_HiGHS",
    "smiles1",
    "smiles2"
]

fair[same_distance_columns].to_csv(
    "same_distance_pairs_analysis.csv",
    index=False
)

# ====================================================
# CBC SKIPPED ANALYSIS
# ====================================================

cbc_skipped = df[
    (df["solverCalled_CBC"] == 0) &
    (df["solverCalled_HiGHS"] == 1)
].copy()

print("\n===== CBC-SKIPPED PAIRS ANALYSIS =====")
print("Pairs skipped by CBC but solved/attempted by HiGHS:", len(cbc_skipped))

cbc_skipped["highs_distance_calculated"] = (
    cbc_skipped["distance_HiGHS"].notna()
)

print("\nDid HiGHS calculate a distance?")
print(cbc_skipped["highs_distance_calculated"].value_counts())

successful_highs = cbc_skipped[
    cbc_skipped["highs_distance_calculated"]
].copy()

failed_highs = cbc_skipped[
    ~cbc_skipped["highs_distance_calculated"]
].copy()

print("\nHiGHS successful cases:", len(successful_highs))
print("HiGHS failed/no-distance cases:", len(failed_highs))

if len(successful_highs) > 0:
    print("\n===== HiGHS DISTANCE STATISTICS FOR CBC-SKIPPED PAIRS =====")
    print("Mean distance:", successful_highs["distance_HiGHS"].mean())
    print("Median distance:", successful_highs["distance_HiGHS"].median())
    print("Minimum distance:", successful_highs["distance_HiGHS"].min())
    print("Maximum distance:", successful_highs["distance_HiGHS"].max())

    print("\n===== HiGHS RUNTIME STATISTICS FOR CBC-SKIPPED PAIRS =====")
    print("Mean runtime:", successful_highs["runtime_HiGHS"].mean())
    print("Median runtime:", successful_highs["runtime_HiGHS"].median())
    print("Minimum runtime:", successful_highs["runtime_HiGHS"].min())
    print("Maximum runtime:", successful_highs["runtime_HiGHS"].max())

print("\n===== HiGHS COMPUTE MODES FOR CBC-SKIPPED PAIRS =====")
print(cbc_skipped["compute_mode_HiGHS"].value_counts(dropna=False))

print("\n===== HiGHS ERRORS FOR CBC-SKIPPED PAIRS =====")
print(cbc_skipped["error_HiGHS"].value_counts(dropna=False))

cbc_skipped_columns = [
    "pair_id",
    "distance_HiGHS",
    "runtime_HiGHS",
    "total_runtime_HiGHS",
    "compute_mode_HiGHS",
    "error_HiGHS",
    "highs_distance_calculated",
    "smiles1",
    "smiles2"
]

cbc_skipped[cbc_skipped_columns].to_csv(
    "cbc_skipped_pairs_analysis.csv",
    index=False
)

# ====================================================
# DIFFERENT-DISTANCE ANALYSIS
# ====================================================

different = both_called[
    ~both_called["same_distance"]
].copy()

print("\n===== DIFFERENT-DISTANCE PAIRS ANALYSIS =====")
print("Number of different-distance pairs:", len(different))

if len(different) > 0:
    different["distance_difference"] = (
        different["distance_CBC"] -
        different["distance_HiGHS"]
    )

    different["absolute_distance_difference"] = (
        different["distance_difference"].abs()
    )

    different["relative_distance_difference_percent"] = (
        different["absolute_distance_difference"] /
        (
            (
                different["distance_CBC"].abs() +
                different["distance_HiGHS"].abs()
            ) / 2
        )
    ) * 100

    different["smaller_distance_solver"] = np.where(
        different["distance_HiGHS"] < different["distance_CBC"],
        "HiGHS",
        "CBC"
    )

    different["runtime_ratio_CBC_over_HiGHS"] = (
        different["runtime_CBC"] /
        different["runtime_HiGHS"]
    )

    different["faster_solver"] = np.where(
        different["runtime_HiGHS"] < different["runtime_CBC"],
        "HiGHS",
        "CBC"
    )

    different = different.sort_values(
        "absolute_distance_difference",
        ascending=False
    )

    print("\nAverage absolute distance difference:")
    print(different["absolute_distance_difference"].mean())

    print("\nMaximum absolute distance difference:")
    print(different["absolute_distance_difference"].max())

    print("\nAverage relative difference (%):")
    print(different["relative_distance_difference_percent"].mean())

    print("\nSolver producing smaller distance:")
    print(different["smaller_distance_solver"].value_counts())

    print("\nFaster solver among different-distance pairs:")
    print(different["faster_solver"].value_counts())

    different_columns = [
        "pair_id",
        "distance_CBC",
        "distance_HiGHS",
        "distance_difference",
        "absolute_distance_difference",
        "relative_distance_difference_percent",
        "runtime_CBC",
        "runtime_HiGHS",
        "runtime_ratio_CBC_over_HiGHS",
        "smaller_distance_solver",
        "faster_solver",
        "compute_mode_CBC",
        "compute_mode_HiGHS",
        "error_HiGHS",
        "smiles1",
        "smiles2"
    ]

    print("\n===== DIFFERENT-DISTANCE PAIRS =====")
    print(different[different_columns])

    different[different_columns].to_csv(
        "different_distance_pairs_analysis.csv",
        index=False
    )

# -----------------------------
# Export complete comparison
# -----------------------------
both_called.to_csv(
    "all_pairs_both_solvers_called.csv",
    index=False
)

print("\n===== EXPORTED FILES =====")
print("01_runtime_boxplot_same_distance.png")
print("02_runtime_per_pair_same_distance.png")
print("same_distance_pairs_analysis.csv")
print("cbc_skipped_pairs_analysis.csv")
print("different_distance_pairs_analysis.csv")
print("all_pairs_both_solvers_called.csv")