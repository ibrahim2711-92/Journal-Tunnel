# Phase 2 — Methods & Protocols

## Output
- `docs/Methods_Draft.md` — full methods section (~600–800 words)
- `Supplementary/Simulation_Protocol.md` — extended protocol for exact replication

## Target
~700 words for IEEE Communications Letters (must fit within the 5-page limit alongside all other sections). Every parameter, version, and algorithmic choice is explicitly stated with numeric precision. A reader with the same stack must be able to reproduce all figures without contacting the authors.

## Entry Condition
- Phase 0C complete: `docs/Data_Code_Manifest.md` exists and Gate 2 passed
- `Data/Final/` locked (do not modify after this point)

## Exit Check
```powershell
# Check 1: Methods draft exists
Test-Path "docs\Methods_Draft.md"

# Check 2: Word count within target
python scripts\word_counter.py --file docs\Methods_Draft.md --min 600 --max 850
# Expected: exit code 0

# Check 3: No [NEEDS_*] placeholders remain
Select-String -Path "docs\Methods_Draft.md" -Pattern "\[NEEDS_"
# Expected: zero matches

# Check 4: All parameter values in the draft match Data_Code_Manifest.md
# (Manual cross-check by author — sign off in the Methods draft footer)
```

## Characteristic Failure Mode — Methods Section
**Failing to state exact software versions, parameters, or random seeds.**
Vague descriptions like "we used a clustering algorithm" or "an appropriate threshold was chosen" are defects. Every algorithmic choice must state: (a) the specific algorithm name, (b) the specific hyperparameter values used, (c) the justification or citation. Methods sections that omit these details fail IEEE peer review in the reproducibility check and must be sent back.

**Anti-pattern to avoid from the quarantine draft:**
> *"Clustering techniques, for instance, can classify traffic with similar characteristics"*
→ This is background, not a method. Replace with: *"K-Means clustering (k=3, random_state=42, max_iter=300) was applied to the normalised feature matrix F ∈ ℝ^{N×d} …"*

## Section Plan

### 2.1 — System Model (~150 words)
- NOMA downlink system description: base station, user equipment, power allocation model
- Frequency/time resource structure
- Define notation: P_total, α_i (power allocation coefficients), h_i (channel gains)
- Reference the system diagram (Fig 1)

### 2.2 — Traffic Generation & Simulation Environment (~150 words)
- SimPy version, simulation duration, time step
- Traffic arrival model (Poisson process, λ per slice type)
- User counts and slice type distributions
- Random seed: state the exact integer and justify its use for reproducibility

### 2.3 — Feature Extraction (~100 words)
- List the exact features extracted from simulated traffic (e.g., packet inter-arrival time, packet size, queue length, signal-to-interference-plus-noise ratio)
- Normalisation method: StandardScaler (zero mean, unit variance)

### 2.4 — Unsupervised Learning Pipeline (~150 words)
- **PCA:** number of components, variance explained threshold
- **K-Means:** k value, initialisation method (k-means++), convergence criterion, number of random restarts
- **DBSCAN (comparison):** ε and min_samples values, distance metric
- Cluster-to-slice mapping logic (how cluster labels are assigned to eMBB/URLLC/mMTC)
- Silhouette score used as internal cluster quality metric

### 2.5 — Adaptive Resource Allocation Framework (~100 words)
- How cluster assignments feed into slice resource allocation
- Resource adjustment rule (e.g., proportional bandwidth allocation based on cluster size and QoS class)
- Static baseline definition (equal resource split — the comparison point for all figures)

### 2.6 — Evaluation Metrics (~80 words)
- Throughput (Mbps): definition
- Latency (ms): definition (end-to-end packet delay in simulation)
- SLA compliance (%): proportion of packets meeting per-slice latency threshold
- Spectral efficiency (bps/Hz): definition
- All metrics reported as mean ± 95% CI over [N] simulation runs

## Sources / Inputs
- `docs/Data_Code_Manifest.md` — all parameter values drawn from here
- `scripts/simulation_main.py` — algorithmic choices confirmed against the code
- `Manuscript/references.bib` — cite original K-Means, DBSCAN, SimPy papers

## Acceptance Checklist
- [ ] Draft is 600–850 words (verified by `word_counter.py`)
- [ ] Every algorithm has its exact hyperparameters stated numerically
- [ ] Random seed stated as an integer in the text
- [ ] Python and SimPy version numbers appear in the text (or a footnote)
- [ ] System model notation is consistent with Fig 1
- [ ] Evaluation metrics are precisely defined (no vague "performance metric")
- [ ] Zero `[NEEDS_*]` placeholders in the draft
- [ ] Supplementary protocol written to `Supplementary/Simulation_Protocol.md`
- [ ] All parameter values cross-checked against `docs/Data_Code_Manifest.md` (author sign-off at draft footer)

## Handover
- `docs/Methods_Draft.md` → Phase 7 (Methods section of the final Word document)
- `Supplementary/Simulation_Protocol.md` → Phase 6 (listed in Data Availability Statement)
