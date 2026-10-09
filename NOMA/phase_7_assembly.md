# Phase 7 — Final Manuscript Assembly

## Output
- `Manuscript/Main_Manuscript.docx` — compiled manuscript using IEEE Word template
- `Manuscript/Main_Manuscript.pdf` — PDF export of the final Word document
- `Manuscript/references.bib` — final verified BibTeX (copied from root)

## Target
≤5 pages in IEEE two-column format. Zero citation errors. Zero undefined cross-references. All figures embedded at correct resolution. Word count within journal limits.

## Entry Condition
- Gate 4 passed: Cover Letter and all Declarations complete
- All phase drafts exist on disk:
  - `docs/Introduction_Draft.md` ✓
  - `docs/Methods_Draft.md` ✓
  - `docs/Results_Draft.md` ✓
  - `docs/Discussion_Draft.md` ✓
  - `docs/Abstract_Keywords_Draft.md` ✓
- All figures in `figures/` pass `figure_checker.py`
- All tables in `tables/` finalized

## Exit Check
```powershell
# Check 1: Main manuscript exists
Test-Path "Manuscript\Main_Manuscript.docx"

# Check 2: PDF export exists
Test-Path "Manuscript\Main_Manuscript.pdf"

# Check 3: Word count check across all sections
python scripts\word_counter.py --file Manuscript\Main_Manuscript.docx --max-pages 5
# Expected: ≤5 pages in IEEE two-column format (exit 0)

# Check 4: Citation audit
python scripts\citation_checker.py --manuscript Manuscript\Main_Manuscript.docx --bib Manuscript\references.bib
# Expected: 0 orphaned citations, 0 missing DOIs

# Check 5: Figure resolution audit
python scripts\figure_checker.py
# Expected: 0 figures below 300 DPI

# Check 6: No [NEEDS_*] placeholders in the assembled manuscript
# (Manual scan before submission)
```

## Characteristic Failure Mode
**Exceeding the 5-page limit without catching it before submission.**
IEEE Communications Letters enforces a hard 5-page limit. Pages 6+ incur mandatory overlength page charges (MOPC) or rejection. The assembled manuscript must be checked in the IEEE Word template (two-column, 10pt font, standard margins) before the exit check is declared passed. If the draft exceeds 5 pages, content must be cut — not reformatted with smaller fonts or margins.

**Priority cut order if over-length:**
1. Trim redundant background sentences in the Introduction (the most common source of bloat)
2. Abbreviate the Methods — move extended protocol detail to `Supplementary/Simulation_Protocol.md`
3. Trim Discussion paragraphs — ensure each sentence does interpretive work, not repetition
4. Reduce figure count (merge Fig 3 and Fig 4 into a dual-panel figure if necessary)

## Assembly Procedure

### Step 1 — Download and open the IEEE template
Use `Manuscript/templates/IEEE_CommLetters_template.docx`. Do not modify the template styles (font, column width, spacing). All content is typed/pasted into the template body.

### Step 2 — Assemble content in this order
1. **Title** (from `docs/Abstract_Keywords_Draft.md` — confirmed title)
2. **Author block:** `[NEEDS_LEAD_AUTHOR: OI-002]`, Ibrahim ABUBAKAR, Hamza MUSA + affiliations
3. **Abstract** (from `docs/Abstract_Keywords_Draft.md` — copy verbatim, ≤150 words)
4. **Keywords** (from `docs/Abstract_Keywords_Draft.md` — 3–5 IEEE taxonomy terms)
5. **I. Introduction** (from `docs/Introduction_Draft.md`)
6. **II. System Model & Methodology** (from `docs/Methods_Draft.md`)
7. **III. Results** (from `docs/Results_Draft.md`) — embed Fig 1–5 and Tab 1–2
8. **IV. Discussion & Conclusion** (from `docs/Discussion_Draft.md`)
9. **Data Availability Statement** (from `docs/Declarations.md`)
10. **Conflict of Interest** (from `docs/Declarations.md`)
11. **Funding** (from `docs/Declarations.md`)
12. **CRediT Author Statement** (from `docs/Declarations.md`)
13. **References** (formatted as IEEE numbered list from `Manuscript/references.bib`)

### Step 3 — Figure embedding
- Insert each figure at the correct location in the text
- Caption format: `Fig. 1. [Caption text.]` (IEEE style uses period, not colon)
- Ensure each figure is referenced in the text as `Fig. 1`, `Fig. 2`, etc. before it appears

### Step 4 — Reference list
- Format as IEEE numbered list: `[1] A. Author, "Title," *Journal*, vol. X, pp. Y–Z, Year. doi: 10.xxx/xxx.`
- Use `scripts/citation_checker.py` to confirm every in-text `[N]` has a matching entry and every entry is cited

### Step 5 — Final checks before PDF export
- Page count: ≤5 pages in the IEEE template
- Abstract: ≤150 words
- All acronyms defined on first use
- No tracked changes, comments, or editor markup remaining
- File saved as `Manuscript/Main_Manuscript.docx`
- Export to PDF: `Manuscript/Main_Manuscript.pdf`

## Sources / Inputs
- `Manuscript/templates/IEEE_CommLetters_template.docx`
- All `docs/*.md` draft files
- `figures/` — all 5 figures
- `tables/` — both tables
- `Manuscript/references.bib`
- `docs/Declarations.md`

## Acceptance Checklist
- [ ] Manuscript assembled in the official IEEE Word template (two-column)
- [ ] ≤5 pages in the final template (verified by page count, not word count alone)
- [ ] Abstract ≤150 words in the assembled document
- [ ] All figures embedded with IEEE-style captions (`Fig. N. Caption.`)
- [ ] All tables embedded with IEEE-style captions (above the table: `TABLE I — TITLE`)
- [ ] All in-text citations are IEEE numbered format `[1]`, `[2]`, …
- [ ] Reference list matches `Manuscript/references.bib` — verified by `citation_checker.py`
- [ ] Zero `[NEEDS_*]` placeholders in the assembled manuscript (or explicitly flagged Open Items)
- [ ] `Main_Manuscript.pdf` exported and visually inspected (fonts embedded, figures crisp)
- [ ] `word_counter.py` exits 0 (page limit compliant)

## Handover
- `Manuscript/Main_Manuscript.docx` + `Main_Manuscript.pdf` → Upload to ScholarOne (`mc.manuscriptcentral.com/comml-ieee`)
- `Cover_Letter/Cover_Letter.md` → Upload as cover letter file in ScholarOne
- `Supplementary/Simulation_Protocol.md` → Upload as supplementary file
- Submission confirmation → triggers Phase 8 (Rebuttal pipeline)
