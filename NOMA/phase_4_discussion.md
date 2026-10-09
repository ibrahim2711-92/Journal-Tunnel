# Phase 4 — Discussion & Limitations

## Output
- `docs/Discussion_Draft.md` — full discussion and conclusion section (~400–500 words combined)

## Target
~450 words. Every result from `docs/Results_Draft.md` is interpreted in the context of the existing literature. Limitations are stated explicitly and honestly. The conclusion does not introduce new claims not supported by the results.

## Entry Condition
- Gate 3 passed: `docs/Introduction_Draft.md` exists and golden thread checker passes
- `docs/Results_Draft.md` locked (Phase 1 complete)
- `Manuscript/references.bib` available for comparison citations

## Exit Check
```powershell
# Check 1: Discussion draft exists
Test-Path "docs\Discussion_Draft.md"

# Check 2: Word count
python scripts\word_counter.py --file docs\Discussion_Draft.md --min 380 --max 520

# Check 3: Every RQ in the Golden Thread table is addressed
python scripts\golden_thread_checker.py --section discussion
# Expected: 0 unanswered-RQ warnings

# Check 4: Limitations section is present and non-empty
Select-String -Path "docs\Discussion_Draft.md" -Pattern "limitation"
# Expected: ≥3 matches (at least 3 distinct limitation sentences)

# Check 5: No unanchored claims
Select-String -Path "docs\Discussion_Draft.md" -Pattern "\[UNANCHORED\]"
# Expected: zero matches (author must clear all flags)
```

## Characteristic Failure Mode — Discussion
**Repeating the results without providing broader contextual interpretation, or glossing over limitations.**
Every paragraph in the Discussion must do one of three things:
1. **Interpret** — explain *why* the result occurred, drawing on the system model or prior literature
2. **Compare** — position the result against cited related works (with specific numerical comparisons where possible)
3. **Limit** — honestly state what the result does NOT prove, what was not tested, and what future work is needed

If a paragraph merely restates "our method achieved X% throughput" without any of the above, it is a defect. Flag it with `<!-- RESULT REPEAT — ADD INTERPRETATION -->`.

## Section Plan

### Discussion Para 1 — Interpretation of Clustering Results (~100 words)
- Interpret Fig 2 (cluster plot): what does the separation tell us about NOMA traffic structure?
- Compare silhouette score against what has been reported in similar clustering studies (cite from `references.bib`)
- Why does unsupervised clustering work here? Link to the feature design in Methods 2.3

### Discussion Para 2 — Throughput & Latency Improvement (~100 words)
- Interpret Fig 3 and Fig 4: why does adaptive slicing outperform static slicing?
- Explain the mechanism: cluster-driven allocation reduces resource waste for low-demand slices and reallocates to high-demand slices dynamically
- Quantify the improvement (numbers from `docs/Results_Draft.md`) and compare to a cited baseline from the literature

### Discussion Para 3 — QoS & SLA Compliance (~80 words)
- Interpret Fig 5: which slice type benefits most and why?
- Tension to address: does URLLC (latency-critical) benefit at the expense of mMTC (throughput-tolerant)? Explain the trade-off honestly
- If QoS is not uniformly improved across all slices, state this as a result, not a failure to report

### Discussion Para 4 — Limitations (~100 words)
**All three limitations must appear. Do not soften or omit them:**
1. *Simulation only:* Results are from a SimPy discrete-event simulation; real-world radio channel effects (fading, interference from neighbouring cells, hardware imperfections) are not modelled
2. *Traffic model:* Poisson arrival model is a simplification; real 5G traffic is bursty and correlated; the clustering pipeline has not been validated on real traffic traces
3. *Scale:* Tested with [N] users; scalability to dense user deployments (hundreds of users per cell) has not been demonstrated

### Conclusion (~80 words)
- One sentence: restate the core contribution (not the results — the contribution)
- Two sentences: state the primary finding and its significance for 5G/B5G network management
- One sentence: state the next step (real-world validation with real traffic data)
- Do NOT introduce any new claim, concept, or figure reference not already in the paper

## Sources / Inputs
- `docs/Results_Draft.md` — every claim in the discussion must trace to a number here
- `Manuscript/references.bib` — comparison papers must be cited
- Golden Thread table in `CLAUDE.md` — every RQ row must have a corresponding discussion paragraph

## Acceptance Checklist
- [ ] Draft is 380–520 words (verified by `word_counter.py`)
- [ ] Every RQ from the Golden Thread table has a corresponding discussion paragraph
- [ ] All three limitations explicitly stated in a dedicated sub-paragraph or paragraph
- [ ] No result is stated in the Discussion that is not in `docs/Results_Draft.md`
- [ ] All comparison claims cite a specific paper in `Manuscript/references.bib`
- [ ] Conclusion ≤80 words, introduces no new claims
- [ ] `golden_thread_checker.py` exits with 0 unanswered-RQ warnings
- [ ] Zero `[UNANCHORED]` flags remaining

## Handover
- `docs/Discussion_Draft.md` → Phase 7 (Discussion/Conclusion section of final Word document)
- Limitations list → Phase 5 (Abstract mentions one key limitation)
- Conclusion text → Phase 5 (Abstract synthesis)
