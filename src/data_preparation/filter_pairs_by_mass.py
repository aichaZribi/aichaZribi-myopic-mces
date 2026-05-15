# -*- coding: utf-8 -*-

import csv
import time
from multiprocessing import Process, Queue, freeze_support

from rdkit import Chem
from rdkit.Chem import Descriptors
from myopic_mces import MCES


# =========================
# SETTINGS
# =========================
input_csv = r"C:\Users\HP\Desktop\thesis\script\example\example_compound_data.csv"
output_csv = r"C:\Users\HP\Desktop\thesis\script\example\filter_mass_diff_and_size\filtered_pairs_800_1000_Highs_2.csv"

target_mass_min = 800
target_mass_max = 1000
tolerance = 1.5
TIME_LIMIT = 60


# =========================
# HELPERS
# =========================
def get_mass(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    return Descriptors.MolWt(mol)


def run_mces(smiles1, smiles2, queue):
    """
    Run MCES in child process and send result back via queue.
    """
    try:
        result = MCES(smiles1, smiles2, solver="HiGHS_CMD")
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

    if result is None:
        return distance, runtime_inside_mces, compute_mode, solver_called, ilp_solver

    if len(result) > 1:
        distance = result[1]

    if len(result) > 2:
        runtime_inside_mces = result[2]

    if len(result) > 3:
        compute_mode = result[3]

    if len(result) > 4:
        ilp_solver = result[4]

    # Infer whether ILP solver was used
    if ilp_solver not in [None, "", 0, "0", "None"]:
        solver_called = 1

    return distance, runtime_inside_mces, compute_mode, solver_called, ilp_solver


# =========================
# MAIN
# =========================
def main():
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
                target_mass_min <= mass1 <= target_mass_max
                and target_mass_min <= mass2 <= target_mass_max
                and abs(mass1 - mass2) <= tolerance
            ):
                continue

            queue = Queue()
            process = Process(target=run_mces, args=(smiles1, smiles2, queue))

            skipped = 0
            distance = None
            solver_called = 0
            compute_mode = None
            ilp_solver = None
            runtime_sec = None
            runtime_inside_mces = None
            raw_result = None
            error_message = None

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
                raw_result,
                error_message
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
            "raw_mces_result",
            "error_message"
        ])

        writer.writerows(results)

    print("Done.")
    print("Number of selected pairs:", len(results))


if __name__ == "__main__":
    freeze_support()
    main()