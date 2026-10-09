# Phase 5 — Abstract, Keywords & Title

## Output
- `docs/Abstract_Keywords_Draft.md` — abstract (≤150 words), 3–5 keywords, confirmed title

## Target
Abstract: ≤150 words (IEEE Communications Letters binding limit). Unstructured format (no headings). Must be a self-contained summary: problem → method → key result → implication.

## Entry Condition
- Phase 4 complete: `docs/Discussion_Draft.md` exists and golden thread checker passes
- `docs/Results_Draft.md` locked with actual numerical results
- `docs/Methods_Draft.md` complete

## Exit Check
```powershell
# Check 1: Abstract draft exists
Test-Path "docs\Abstract_Keywords_Draft.md"

# Check 2: Abstract word count ≤ 150
python scripts\word_counter.py --file docs\Abstract_Keywords_Draft.md --section abstract --max 150
# Expected: exit code 0

# Check 3: Keywords are present and between 3 and 5
# (Manual check — verify 3–5 IEEE taxonomy index terms in the file)
```

## Characteristic Failure Mode
**Writing the abstract before the results are locked.**
An abstract written before figures are finalised will contain vague, hedged, or incorrect result statements. If the abstract says "results demonstrate improved performance" without a specific number, it will be weakened in peer review. Write the abstract last, copying specific numbers directly from `docs/Results_Draft.md`.

**Template to follow:**
> *[Problem statement: 1–2 sentences on the gap / motivation]*
> *[Method: 1–2 sentences naming the simulation framework and uML approach]*
> *[Key result: 1–2 sentences with specific numbers from locked figures]*
> *[Implication: 1 sentence on significance for 5G/B5G networks]*

## Section Plan

### Abstract (~150 words)
Pull content in this order:
1. **Problem:** 1 sentence — why static resource management fails in NOMA networks (from Introduction para 1)
2. **Gap:** 1 sentence — the absence of label-free traffic classification (from `docs/Gap_Matrix.md`)
3. **Method:** 2 sentences — SimPy-based NOMA simulation + K-Means/PCA unsupervised pipeline
4. **Result 1:** 1 sentence — throughput improvement (exact % from Tab 2)
5. **Result 2:** 1 sentence — latency improvement or SLA compliance gain (exact number from `docs/Results_Draft.md`)
6. **Implication:** 1 sentence — contribution to intelligent, label-efficient 5G resource management

### Keywords (3–5 IEEE taxonomy terms)
Choose from IEEE Thesaurus at https://www.ieee.org/publications/services/thesaurus.html:
- Non-orthogonal multiple access (NOMA)
- Network slicing
- Unsupervised learning
- Resource management
- Traffic classification
*(Verify each term exists in the IEEE Thesaurus before including)*

### Title Confirmation
Proposed final title for submission:

> **Adaptive Network Slicing in NOMA Systems via Unsupervised Traffic Classification for Efficient Resource Management**

*(Shorter, active, concise — suitable for IEEE Communications Letters. If authors prefer the original working title, record the decision here.)*

Alternative title options:
1. Original: *Adaptive Network Slicing in Non-Orthogonal Multiple Access (NOMA) Leveraging Unsupervised Learning for Traffic Classification and Resource Management* (long — may be truncated in indexing)
2. Shortened: *Unsupervised Learning-Aided Adaptive Network Slicing for NOMA Systems*
3. Action-first: *Traffic-Aware Adaptive Slicing in NOMA via Unsupervised Clustering*

Author must confirm the final title and record the decision in the Change Log.

## Sources / Inputs
- `docs/Results_Draft.md` — all numerical claims in the abstract copied from here
- `docs/Gap_Matrix.md` — gap statement condensed into 1 abstract sentence
- IEEE Thesaurus (live) — keyword validation

## Acceptance Checklist
- [ ] Abstract ≤150 words (verified by `word_counter.py`)
- [ ] Abstract contains at least one specific numerical result (e.g., "X% throughput improvement")
- [ ] Abstract contains no citation (IEEE Communications Letters style — no references in abstract)
- [ ] Abstract contains no undefined acronyms (spell out NOMA, QoS, etc. on first use)
- [ ] 3–5 keywords, each verified against IEEE Thesaurus
- [ ] Final title confirmed by author and recorded in Change Log
- [ ] No `[NEEDS_*]` placeholders remain in the abstract

## Handover
- `docs/Abstract_Keywords_Draft.md` → Phase 7 (front matter of final Word document)
- Confirmed title → Cover Letter (Phase 6) and manuscript header (Phase 7)
