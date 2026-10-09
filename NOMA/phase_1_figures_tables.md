# Phase 1 — Figures & Tables Lock

## Output
- `figures/fig1_system_architecture.png` (600 DPI, EPS source)
- `figures/fig2_cluster_plot.png` (300 DPI, EPS source)
- `figures/fig3_throughput_comparison.png` (300 DPI, EPS source)
- `figures/fig4_latency_cdf.png` (300 DPI, EPS source)
- `figures/fig5_qos_per_slice.png` (300 DPI, EPS source)
- `tables/tab1_simulation_parameters.md`
- `tables/tab2_algorithm_comparison.md`
- `docs/Results_Draft.md` — results section text (~500 words, zero interpretation)

## Target
All 5 figures at correct DPI/format. Results text written factually — no discussion, no interpretation, no claims about why results occurred.

## Entry Condition
- Gate 2 passed: `Data/Final/` non-empty, `reproducibility_runner.py` exits 0
- `Manuscript/references.bib` exists (≥20 entries from Phase 0B)

## Exit Check
```powershell
# Check 1: All figures exist
@("fig1_system_architecture","fig2_cluster_plot","fig3_throughput_comparison",
  "fig4_latency_cdf","fig5_qos_per_slice") | ForEach-Object {
  Test-Path "figures\$_.png"
}
# Expected: all True

# Check 2: DPI check (run figure checker)
python scripts\figure_checker.py
# Expected: 0 figures below 300 DPI

# Check 3: Results draft exists
Test-Path "docs\Results_Draft.md"

# Check 4: Results draft contains no interpretation language
Select-String -Path "docs\Results_Draft.md" -Pattern "(this suggests|this indicates|this shows|therefore|because|reason|implies|demonstrates that)"
# Expected: zero matches (flag any hits as violations of R5)
```

## Characteristic Failure Mode — Results Section
**Inserting discussion or interpretation into the results section.**
The results section states what the data shows, using precise numerical values, with figure/table references. It does not state why, does not speculate, and does not compare to other works. Every sentence in `docs/Results_Draft.md` must be checkable against a cell in `Data/Final/`. Sentences that cannot be verified against a data cell are interpretation and must be moved to Phase 4 (Discussion).

**Test:** Replace every "this suggests/implies/demonstrates" with a flagging comment `<!-- INTERPRETATION — MOVE TO DISCUSSION -->` and resolve before exit check.

## Figure Specifications

### Fig 1 — System Architecture Diagram
- **Content:** End-to-end pipeline: Base Station → NOMA channel → Traffic feature extraction → uML pipeline (PCA → clustering) → Slice assignment → Adaptive resource allocation → User equipment
- **Type:** Block diagram (no simulation data required — conceptual)
- **Tool:** Python matplotlib or draw.io → export EPS
- **DPI:** 600 (line art)
- **Format:** EPS (primary), PNG (review copy)
- **Font size in figure:** ≥8pt (IEEE minimum)
- **Color:** Use distinct colors but ensure B&W legibility (use patterns/hatching)

### Fig 2 — Cluster Visualisation (PCA/t-SNE scatter)
- **Content:** 2D projection of traffic feature space, colored by cluster assignment (K-Means); show eMBB/URLLC/mMTC regions if separable
- **Data source:** `Data/Final/simulation_results.csv` — feature columns
- **Tool:** `scripts/generate_figures.py` → matplotlib → EPS
- **DPI:** 300

### Fig 3 — Throughput Comparison (Bar chart)
- **Content:** Mean throughput (Mbps) for static baseline vs. adaptive slicing, per slice type (eMBB, URLLC, mMTC); error bars = 95% CI
- **Data source:** `Data/Final/simulation_results.csv`
- **DPI:** 300

### Fig 4 — Latency CDF
- **Content:** Cumulative distribution of packet latency (ms) for static vs. adaptive, per slice type
- **Data source:** `Data/Final/simulation_results.csv`
- **DPI:** 300

### Fig 5 — QoS per Slice Type (Multi-panel)
- **Content:** SLA compliance rate (%) across simulation time for each of 3 slice types; static vs. adaptive as two lines per panel
- **Panels:** (a) eMBB, (b) URLLC, (c) mMTC
- **DPI:** 300

## Table Specifications

### Tab 1 — Simulation Parameters
```markdown
| Parameter | Value |
|---|---|
| Simulation duration | X time units |
| Number of users | X |
| NOMA power allocation | X:X ratio |
| Traffic model | Poisson, λ = X |
| Number of slices | 3 (eMBB, URLLC, mMTC) |
| Clustering algorithm | K-Means (k=3), DBSCAN (ε=X) |
| Random seed | X |
| Python / SimPy version | 3.11 / 4.1 |
```

### Tab 2 — Algorithm Comparison
```markdown
| Metric | Static Slicing | Adaptive Slicing (Proposed) | Improvement |
|---|---|---|---|
| Mean throughput (Mbps) | X | X | X% |
| Mean latency (ms) | X | X | X% |
| SLA compliance (%) | X | X | +X pp |
| Spectral efficiency | X | X | X% |
```

## Sources / Inputs
- `Data/Final/simulation_results.csv`
- `scripts/generate_figures.py` (to be created in Phase 0C)
- `scripts/figure_checker.py`

## Acceptance Checklist
- [ ] All 5 figures present in `figures/` at correct DPI (verified by `figure_checker.py`)
- [ ] All figures in EPS or PNG format; fonts ≥8pt; B&W legible
- [ ] Both tables written in `tables/` with no empty data cells (all values from `Data/Final/`)
- [ ] `docs/Results_Draft.md` written (~500 words, zero interpretation language)
- [ ] Golden Thread table in `CLAUDE.md` updated: `[NEEDS_FINDING]` cells filled with actual results
- [ ] `figure_checker.py` exits with 0 DPI violations

## Handover
- `figures/` → Phase 7 (Assembly into Word document)
- `tables/` → Phase 7 (Assembly)
- `docs/Results_Draft.md` → Phase 4 (Discussion — interpret these findings)
- Updated Golden Thread → Phase 3 (Introduction references the findings)
