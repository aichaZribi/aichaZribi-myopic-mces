# check_imports.py

import importlib
import sys

packages = [
    "pulp",
    "highspy",
    "rdkit",
    "networkx",
    "numpy",
    "scipy",
    "joblib",
    "pandas",
    "sklearn",
    "myopic_mces",
]

print("Python:", sys.version)
print("Executable:", sys.executable)
print("-" * 80)

for pkg in packages:
    try:
        print(f"Importing {pkg}...", end=" ", flush=True)
        module = importlib.import_module(pkg)

        version = getattr(module, "__version__", "unknown")
        location = getattr(module, "__file__", "unknown")

        print("OK")
        print(f"  Version: {version}")
        print(f"  Location: {location}")

    except Exception as e:
        print("FAILED")
        print(f"  Error: {e}")

print("\nFinished.")