# -*- coding: utf-8 -*-

import csv
import time
from multiprocessing import Process, Queue, freeze_support
from pathlib import Path

from rdkit import Chem
from rdkit.Chem import Descriptors
from myopic_mces import MCES


# =========================
# SETTINGS
# =========================

BASE_DIR = Path(__file__).resolve().parents[2]
input_csv = BASE_DIR / "example" / "example_compound_data.csv"
output_csv = BASE_DIR /"example"/"filter_mass_diff_and_size"/"filtered_pairs_800_1000_CPLEX_PY_thread_1.csv"


tolerance = 1.5
TIME_LIMIT = 90

mass_ranges = [
    (500, 800)
]

#mass_ranges = [
#    (0, 200),
#   (200, 300),
#    (300, 500),
#    (500, 800),
#    (800, 1000),
#]

# =========================
# HELPERS
# =========================
def get_mass(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    return Descriptors.MolWt(mol)


def run_mces(smiles1, smiles2, solver_name, threads, queue):
    """
    Run MCES in child process and send result back via queue.
    """
    try:
        result = MCES(smiles1, smiles2,threshold_mode="", solver=solver_name, solver_options={"threads": threads,"timeLimit":90})
        queue.put(("ok", result))
    except Exception as e:
        queue.put(("error", str(e)))


def parse_mces_result(result):
    """
    MCES returns:
    (i, distance, runtime_inside_mces, compute_mode, ilp_solver)

    Important:
    result[4] is ilp_solver, NOT solverCalled.
    """
    distance = None
    runtime_inside_mces = None
    compute_mode = None
    ilp_solver = None
    solver_called = 0
    result_type = "unknown"
    is_exact = 0
    is_lower_bound = 0
    actual_threshold = None
    structural_lb = None
    skipped_by_structural_lb = 0

    if result is None:
        return (
            distance,
            runtime_inside_mces,
            compute_mode,
            solver_called,
            ilp_solver,
            result_type,
            is_exact,
            is_lower_bound,
            actual_threshold,
            structural_lb,
            skipped_by_structural_lb,
        )

    if len(result) > 1:
        distance = result[1]

    if len(result) > 2:
        runtime_inside_mces = result[2]

    if len(result) > 3:
        compute_mode = result[3]

    if len(result) > 4:
        ilp_solver = result[4]

    if len(result) > 5:
        actual_threshold = result[5]

    if len(result) > 6:
        structural_lb = result[6]

    if len(result) > 7:
        skipped_by_structural_lb = result[7]

    if ilp_solver not in [None, "", 0, "0", "None"]:
        solver_called = 1

    if compute_mode == 1:
        result_type = "exact"
        is_exact = 1
    elif compute_mode == 2:
        result_type = "lower_bound"
        is_lower_bound = 1

    return (
        distance,
        runtime_inside_mces,
        compute_mode,
        solver_called,
        ilp_solver,
        result_type,
        is_exact,
        is_lower_bound,
        actual_threshold,
        structural_lb,
        skipped_by_structural_lb
    )


# =========================
# MAIN
# =========================
def main(solver_name, threads, mass_min, mass_max, output_csv):
    results = []

    with open(input_csv, "r", encoding="utf-8") as f:
        reader = csv.reader(f)

        for row in reader:
            if len(row) < 3:
                continue

            pair_id = row[0]
            smiles1 = row[1]
            smiles2 = row[2]

            # Skip header
            if str(pair_id).lower() == "index":
                continue

            mass1 = get_mass(smiles1)
            mass2 = get_mass(smiles2)

            if mass1 is None or mass2 is None:
                print(f"Skipping pair {pair_id}: invalid SMILES")
                continue

            # Filter by mass range and mass difference
            if not (
                mass_min <= mass1 <= mass_max
                and mass_min <= mass2 <= mass_max
                and abs(mass1 - mass2) <= tolerance
            ):
                continue

            queue = Queue()
            process = Process(target=run_mces, args=(smiles1, smiles2, solver_name,threads, queue))

            skipped = 0
            distance = None
            solver_called = 0
            compute_mode = None
            ilp_solver = None
            runtime_sec = None
            runtime_inside_mces = None
            raw_result = None
            error_message = None
            result_type = "unknown"
            is_exact = 0
            is_lower_bound = 0
            actual_threshold = None
            structural_lb = None
            skipped_by_structural_lb = 0

            start = time.time()
            process.start()
            process.join(TIME_LIMIT)

            if process.is_alive():
                process.terminate()
                process.join()

                skipped = 1
                runtime_sec = TIME_LIMIT
                error_message = f"Exceeded {TIME_LIMIT} seconds"

                print(f"Skipped pair {pair_id}: exceeded {TIME_LIMIT} seconds")

            else:
                runtime_sec = time.time() - start

                if not queue.empty():
                    status, payload = queue.get()

                    if status == "ok":
                        raw_result = payload
                        print(f"Pair {pair_id} RAW MCES RESULT: {raw_result}")

                        (
                            distance,
                            runtime_inside_mces,
                            compute_mode,
                            solver_called,
                            ilp_solver,
                            result_type,
                            is_exact,
                            is_lower_bound,
                            actual_threshold,
                            structural_lb,
                            skipped_by_structural_lb
                        ) = parse_mces_result(raw_result)

                    else:
                        error_message = payload
                        print(f"MCES error for pair {pair_id}: {payload}")

                else:
                    error_message = "Process finished but queue was empty"
                    print(f"MCES error for pair {pair_id}: queue was empty")

            results.append([
                pair_id,
                smiles1,
                smiles2,
                mass1,
                mass2,
                abs(mass1 - mass2),
                runtime_sec,
                runtime_inside_mces,
                distance,
                compute_mode,
                skipped,
                solver_called,
                ilp_solver,
                actual_threshold,
                structural_lb,
                skipped_by_structural_lb,
                raw_result,
                error_message,
                result_type,
                is_exact,
                is_lower_bound,
            ])

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow([
            "pair_id",
            "smiles1",
            "smiles2",
            "mass1",
            "mass2",
            "mass_diff",
            "runtime_sec",
            "runtime_inside_mces",
            "distance",
            "compute_mode",
            "skipped",
            "solverCalled",
            "ilp_solver",
            "actual_threshold",
            "structural_lb",
            "skipped_by_structural_lb",
            "raw_mces_result",
            "error_message",
            "result_type",
            "is_exact",
            "is_lower_bound",
        ])

        writer.writerows(results)

    print("Done.")
    print("Number of selected pairs:", len(results))


if __name__ == "__main__":
    freeze_support()
    solvers = ["HiGHS_CMD"] #,"default","CPLEX_PY",
    threads_list = [8]

    for mass_min, mass_max in mass_ranges:

        for solver_name in solvers:

            for threads in threads_list:
                output_csv = (
                        BASE_DIR
                        / "example"
                        / "filter_mass_diff_and_size"
                        / f"filtered_pairs_{mass_min}_{mass_max}_{solver_name}_threads_{threads}_RASCAL_approach.csv"
                )

                print(
                    f"\nRunning range={mass_min}-{mass_max}, "
                    f"solver={solver_name}, "
                    f"threads={threads}"
                )

                main(
                    solver_name,
                    threads,
                    mass_min,
                    mass_max,
                    output_csv
                )