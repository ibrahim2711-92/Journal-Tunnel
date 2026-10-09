# Phase 3 — Introduction & Gap Framing

## Output
- `docs/Introduction_Draft.md` — full introduction section (~400–500 words)

## Target
~450 words. The introduction must funnel from the broad domain (5G/NOMA/network slicing) to the specific gap, to the specific contribution of this paper — in that order. No textbook overview. No ≥3 paragraphs of background before the gap appears.

## Entry Condition
- Phase 1 complete: `docs/Results_Draft.md` exists and figures are locked
- `docs/Gap_Matrix.md` exists with a written gap statement (from Phase 0B)
- `Manuscript/references.bib` has ≥20 verified entries

## Exit Check (Gate 3)
```powershell
# Check 1: Introduction draft exists
Test-Path "docs\Introduction_Draft.md"

# Check 2: Word count within target
python scripts\word_counter.py --file docs\Introduction_Draft.md --min 380 --max 520

# Check 3: Golden thread checker (gap + novelty + RQ anchoring)
python scripts\golden_thread_checker.py --section introduction
# Expected: 0 gap warnings

# Check 4: No [NEEDS_*] placeholders
Select-String -Path "docs\Introduction_Draft.md" -Pattern "\[NEEDS_"
# Expected: zero matches (all citations in bib, gap statement confirmed)
```

## Characteristic Failure Mode — Introduction
**Writing an overly broad textbook overview instead of quickly honing in on the specific literature gap.**
The introduction is NOT a tutorial on 5G, NOMA, or machine learning. Reviewers of IEEE Communications Letters are experts in wireless communications. They do not need three paragraphs explaining what NOMA is. Arrive at the specific gap by the end of paragraph two at the latest.

**Anti-pattern to avoid (from quarantine draft):**
> *"With the swift development of telecommunication networks, the demand for robust resource management methods capable of supporting diverse services and applications has surged…"*
→ This is acceptable as a single opening sentence. But if it continues for two more paragraphs before reaching the gap, it is a structural defect.

**Correct structure:**
- Paragraph 1 (≤3 sentences): establish the problem domain and its urgency
- Paragraph 2 (≤4 sentences): survey what has been done — cite the key works from Phase 0B
- Paragraph 3 (≤3 sentences): state the gap — copy the gap statement from `docs/Gap_Matrix.md`
- Paragraph 4 (≤3 sentences): state the contribution and paper organisation

## Section Plan

### Para 1 — Domain & Problem (~80 words)
- 5G/B5G demand for efficient, heterogeneous resource management
- NOMA as a spectral efficiency solution (cite Ding et al.)
- Network slicing as a virtualisation paradigm (cite Shah et al.)
- Hook: the dynamic nature of traffic makes static resource management insufficient

### Para 2 — Related Work Survey (~120 words)
- Existing network slicing approaches: what they do and where they fall short
- Supervised ML approaches: why they require labeled data and why that is a limitation
- Existing unsupervised ML in networking: what exists (cite Akbar, Rajasekaran, Domeke, Shu & Taleb)
- Crucial: each cited work must be in `Manuscript/references.bib` with a verified DOI

### Para 3 — The Gap (verbatim from `docs/Gap_Matrix.md`) (~80 words)
- Copy the gap statement written in Phase 0B
- Do not paraphrase — this is the verified, author-approved gap statement
- Ends with: *"To address this gap, this paper proposes…"*

### Para 4 — Contribution & Paper Organisation (~120 words)
- Explicitly list the contributions as bullet points or numbered items:
  1. A SimPy-based simulation framework for NOMA network slicing under heterogeneous traffic
  2. An unsupervised learning pipeline (K-Means + PCA) for traffic classification without labeled data
  3. An adaptive resource allocation scheme driven by cluster assignments
  4. Performance evaluation across throughput, latency, and SLA compliance metrics
- One sentence on paper organisation: *"The remainder of this paper is organised as follows: Section II describes the system model and methodology…"*

## Sources / Inputs
- `docs/Gap_Matrix.md` — gap statement (copy verbatim)
- `Manuscript/references.bib` — all citations must be in the bib
- `docs/Results_Draft.md` — contribution claims must be achievable given locked results

## Acceptance Checklist
- [ ] Draft is 380–520 words (verified by `word_counter.py`)
- [ ] Gap statement appears by paragraph 2 (no later)
- [ ] Gap statement is word-for-word from `docs/Gap_Matrix.md`
- [ ] Contribution list explicitly names 3–4 specific contributions
- [ ] All citations in the introduction are in `Manuscript/references.bib` with confirmed DOIs
- [ ] Paper organisation paragraph is present
- [ ] `golden_thread_checker.py` exits with 0 gap warnings
- [ ] Gate 3 exit checks all pass

## Handover
- `docs/Introduction_Draft.md` → Phase 7 (Introduction section of final Word document)
- Gate 3 approval → unlocks Phase 4 (Discussion)
