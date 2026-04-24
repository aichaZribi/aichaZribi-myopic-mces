# MCES returns:
# (i, distance, runtime_inside_mces, compute_mode, ilp_solver)

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
output_csv = r"C:\Users\HP\Desktop\thesis\script\example\filter_mass_diff_and_size\filtered_pairs_false_800_1000.csv"

target_mass_min = 800
target_mass_max = 1000
tolerance = 1.5          # ±1 mass difference
TIME_LIMIT = 60           # seconds


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
        result = MCES(smiles1, smiles2)
        queue.put(("ok", result))
    except Exception as e:
        queue.put(("error", str(e)))


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

            # skip header if present
            if str(pair_id).lower() == "index":
                continue

            mass1 = get_mass(smiles1)
            print(mass1)
            mass2 = get_mass(smiles2)

            if mass1 is None or mass2 is None:
                continue

            # filter by mass range and mass difference
            if not (
                target_mass_min <= mass1 <= target_mass_max and
                target_mass_min <= mass2 <= target_mass_max and
                abs(mass1 - mass2) <= tolerance
            ):
                continue

            queue = Queue()
            process = Process(target=run_mces, args=(smiles1, smiles2, queue))

            skipped = 0
            distance = None
            solver_called = 0
            compute_mode = None
            runtime_sec = None
            runtime_inside_mces = None

            start = time.time()
            process.start()
            process.join(TIME_LIMIT)

            if process.is_alive():
                # timeout
                process.terminate()
                process.join()
                skipped = 1
                runtime_sec = TIME_LIMIT
                print(f"Skipped pair {pair_id}: exceeded {TIME_LIMIT} seconds")

            else:
                runtime_sec = time.time() - start

                if not queue.empty():
                    status, payload = queue.get()

                    if status == "ok":
                        result = payload

                        # MCES returns:
                        # (i, distance, runtime_inside_mces, compute_mode, ilp_solver)
                        if result is not None:
                            distance = result[1] if len(result) > 1 else None
                            runtime_inside_mces = result[2] if len(result) > 2 else None
                            compute_mode = result[3] if len(result) > 3 else None
                            solver_called = result[4] if len(result) > 4 else 0

                    else:
                        print(f"MCES error for pair {pair_id}: {payload}")

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
                solver_called
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
            "solverCalled"
        ])
        writer.writerows(results)

    print("Done.")
    print("Number of selected pairs:", len(results))


if __name__ == "__main__":
    freeze_support()
    main()