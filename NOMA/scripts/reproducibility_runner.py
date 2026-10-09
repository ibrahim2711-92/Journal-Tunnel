#!/usr/bin/env python3
"""
reproducibility_runner.py
Contract: Executes the simulation pipeline from a clean state and verifies
that all files in Data/Final/ can be regenerated. Compares MD5 hashes of
generated outputs against those recorded in docs/Data_Code_Manifest.md.

Exit code 0 = reproducible. Exit code 1 = failure or mismatch.

Usage:
  python scripts/reproducibility_runner.py
"""
import sys
import subprocess
import hashlib
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
SIMULATION_SCRIPT = PROJECT_ROOT / "scripts" / "simulation_main.py"
FINAL_DATA_DIR = PROJECT_ROOT / "Data" / "Final"
MANIFEST_PATH = PROJECT_ROOT / "docs" / "Data_Code_Manifest.md"

def md5_file(filepath: Path) -> str:
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def extract_manifest_hashes(manifest_path: Path) -> dict:
    """Parse MD5 hashes from Data_Code_Manifest.md table rows."""
    hashes = {}
    if not manifest_path.exists():
        return hashes
    text = manifest_path.read_text(encoding="utf-8")
    # Match table rows like: | filename.csv | Description | md5hash |
    for match in re.finditer(r"\|\s*([^\|]+\.(?:csv|json|pkl|npy))\s*\|[^\|]+\|\s*([a-f0-9]{32})\s*\|", text):
        filename = match.group(1).strip()
        md5 = match.group(2).strip()
        hashes[filename] = md5
    return hashes

def main():
    violations = []

    # Step 1: Check simulation script exists
    if not SIMULATION_SCRIPT.exists():
        print(f"[FAIL] simulation_main.py not found at {SIMULATION_SCRIPT}")
        print("  This script must be created in Phase 0C before Gate 2 can pass.")
        sys.exit(1)

    # Step 2: Run the simulation
    print(f"Running simulation: {SIMULATION_SCRIPT}")
    result = subprocess.run(
        [sys.executable, str(SIMULATION_SCRIPT)],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"[FAIL] Simulation exited with code {result.returncode}")
        print("STDOUT:", result.stdout[-2000:])
        print("STDERR:", result.stderr[-2000:])
        sys.exit(1)
    print("[OK] Simulation completed successfully.")
    print(result.stdout[-500:] if result.stdout else "")

    # Step 3: Check Data/Final/ is non-empty
    if not FINAL_DATA_DIR.exists() or not list(FINAL_DATA_DIR.iterdir()):
        print(f"[FAIL] Data/Final/ is empty after simulation run.")
        violations.append("Data/Final/ is empty — simulation did not produce output files.")
    else:
        final_files = list(FINAL_DATA_DIR.iterdir())
        print(f"[OK] Data/Final/ contains {len(final_files)} file(s):")
        for f in final_files:
            print(f"  {f.name} — MD5: {md5_file(f)}")

    # Step 4: Compare against manifest hashes
    manifest_hashes = extract_manifest_hashes(MANIFEST_PATH)
    if not manifest_hashes:
        print(f"\n[WARN] No MD5 hashes found in {MANIFEST_PATH}")
        print("  Record hashes in docs/Data_Code_Manifest.md after first successful run.")
        print("  Future runs will compare against these hashes to verify reproducibility.")
    else:
        print(f"\nComparing {len(manifest_hashes)} hash(es) from manifest...")
        for filename, expected_hash in manifest_hashes.items():
            target = FINAL_DATA_DIR / filename
            if not target.exists():
                violations.append(f"Expected output file not found: {filename}")
                continue
            actual_hash = md5_file(target)
            if actual_hash != expected_hash:
                violations.append(
                    f"Hash mismatch for {filename}:\n"
                    f"  Expected: {expected_hash}\n"
                    f"  Actual:   {actual_hash}"
                )
            else:
                print(f"  [OK] {filename}: hashes match")

    print()
    if violations:
        print(f"RESULT: {len(violations)} reproducibility violation(s):")
        for v in violations:
            print(f"  [FAIL] {v}")
        sys.exit(1)
    else:
        print("RESULT: Reproducibility check PASSED. Gate 2 conditions met.")
        sys.exit(0)

if __name__ == "__main__":
    main()
