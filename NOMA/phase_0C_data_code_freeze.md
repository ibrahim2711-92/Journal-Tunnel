# Phase 0C — Data & Code Freeze

## Output
- `scripts/simulation_main.py` — primary SimPy simulation entry point
- `scripts/requirements.txt` — pinned Python package versions
- `scripts/reproducibility_runner.py` — end-to-end clean-run verifier
- `Data/Raw/` — raw SimPy-generated output files (CSV/JSON)
- `Data/Processed/` — cleaned, feature-engineered datasets
- `Data/Final/` — locked dataset used for all manuscript figures and tables
- `docs/Data_Code_Manifest.md` — complete record of parameters, seeds, and versions

## Target
Simulation pipeline executes end-to-end without errors. All outputs in `Data/Final/` are reproducible from `scripts/simulation_main.py` with a fixed random seed.

## Entry Condition
- Gate 1 passed
- `docs/Gap_Matrix.md` exists (Phase 0B complete) — simulation parameters informed by the literature gap

## Exit Check (Gate 2)
```powershell
# Check 1: Final data directory is non-empty
(Get-ChildItem "Data\Final\").Count -gt 0

# Check 2: requirements.txt exists
Test-Path "scripts\requirements.txt"

# Check 3: End-to-end reproducibility run (clean environment)
cd scripts
python reproducibility_runner.py
# Expected exit code: 0

# Check 4: Data manifest exists and seed is pinned
Select-String -Path "docs\Data_Code_Manifest.md" -Pattern "RANDOM_SEED"
# Expected: exactly one match with a numeric value (not [NEEDS_SEED])
```

## Characteristic Failure Mode
**Failing to state exact software versions, parameters, or random seeds.**
Every configurable parameter in the simulation must be recorded in `docs/Data_Code_Manifest.md`. Parameters that are not recorded cannot be reproduced. A simulation that cannot be reproduced from scratch invalidates all figures derived from it and fails Gate 2.

## Procedure

### Step 1 — Design the simulation
The simulation must model:
1. A NOMA downlink system with ≥2 user classes (e.g., eMBB, URLLC, mMTC)
2. A traffic generator producing heterogeneous load profiles over a simulated time window
3. A resource management module: (a) static baseline, (b) adaptive slicing driven by unsupervised clustering
4. Performance metrics logged per time step: throughput (bps), latency (ms), SLA compliance (%), spectral efficiency

### Step 2 — Implement the unsupervised learning pipeline
```
Traffic features (e.g., packet size, inter-arrival time, queue length)
    → Feature normalisation (StandardScaler)
    → Dimensionality reduction (PCA or t-SNE for visualisation)
    → Clustering (K-Means + DBSCAN — evaluate both)
    → Cluster label → slice type mapping
    → Adaptive resource allocation per cluster
```

### Step 3 — Pin parameters and record everything
`docs/Data_Code_Manifest.md` must contain:

```markdown
# Data & Code Manifest

## Simulation Parameters
| Parameter | Value |
|---|---|
| RANDOM_SEED | [INTEGER — e.g. 42] |
| Simulation duration | [e.g. 1000 time units] |
| Number of users | [e.g. 50] |
| NOMA power allocation ratio | [e.g. 0.8 / 0.2] |
| Slice types | eMBB, URLLC, mMTC |
| Traffic model | [e.g. Poisson arrivals, λ=...] |
| K-Means k | [e.g. 3] |
| PCA components | [e.g. 2] |
...

## Python Environment
| Package | Version |
|---|---|
| Python | 3.11.x |
| simpy | 4.1.x |
| scikit-learn | 1.x.x |
| numpy | 1.x.x |
| pandas | 2.x.x |
| matplotlib | 3.x.x |

## Data Files
| File | Description | MD5 hash |
|---|---|---|
| Data/Final/simulation_results.csv | Locked output | [hash] |
...

## Reproducibility Statement
Running `python scripts/reproducibility_runner.py` from a clean environment
with `scripts/requirements.txt` installed reproduces all files in `Data/Final/`
with bit-identical output (confirmed YYYY-MM-DD).
```

### Step 4 — Lock the dataset
Once results are confirmed reproducible:
1. Copy `Data/Processed/` outputs to `Data/Final/`
2. Record MD5 hashes for each file in the manifest
3. **Do not modify `Data/Final/` after Gate 2 passes.** Any change requires a new Gate 2 sign-off.

## Sources / Inputs
- `docs/Gap_Matrix.md` — confirms which traffic scenarios to simulate
- Python environment (SimPy, scikit-learn, etc.)

## Acceptance Checklist
- [ ] `scripts/simulation_main.py` runs without errors from a clean install
- [ ] `scripts/requirements.txt` lists all packages with pinned versions
- [ ] `Data/Final/` is non-empty and MD5-hashed in `docs/Data_Code_Manifest.md`
- [ ] `RANDOM_SEED` is a specific integer (not `[NEEDS_SEED]`) in the manifest and `CLAUDE.md`
- [ ] `scripts/reproducibility_runner.py` exits with code 0
- [ ] Simulation covers all three RQs in the Golden Thread table
- [ ] Gate 2 exit checks pass

## Handover
- `Data/Final/` → Phase 1 (Figures & Tables generation)
- `docs/Data_Code_Manifest.md` → Phase 2 (Methods), Phase 6 (Data Availability Statement)
- `scripts/requirements.txt` → Phase 7 (Supplementary), Phase 8 (replication package)
