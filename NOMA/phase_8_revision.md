# Phase 8 — Peer Review & Rebuttal Pipeline

## Output
- `Revisions/Response_to_Reviewers_Template.md` — point-by-point rebuttal matrix scaffold
- `Revisions/Response_to_Reviewers.md` — completed response (filled after decision letter arrives)
- `Revisions/Manuscript_diff_instructions.md` — instructions for tracked-changes revision document

## Target
A rebuttal matrix that maps every reviewer comment to an explicit manuscript edit with a line-number reference. No defensive or dismissive responses. All changes traceable.

## Entry Condition
- `Manuscript/Main_Manuscript.pdf` submitted to ScholarOne
- Editor decision letter received (Major Revision, Minor Revision, or Reject & Resubmit)

## Exit Check
```powershell
# Check 1: Response template exists
Test-Path "Revisions\Response_to_Reviewers_Template.md"

# Check 2: Completed response exists (after filling)
Test-Path "Revisions\Response_to_Reviewers.md"

# Check 3: Every reviewer comment row has a non-empty response AND a manuscript change reference
# (Manual check — verify no rows have empty "Manuscript Change" column)
Select-String -Path "Revisions\Response_to_Reviewers.md" -Pattern "\| \[RESPONSE\] \|"
# Expected: zero matches (all placeholders resolved)

# Check 4: Revised manuscript exists
Test-Path "Revisions\Manuscript_Revised.docx"
```

## Characteristic Failure Mode — Revisions
**Providing defensive responses to reviewers without making explicit, traceable edits in the manuscript.**
Every response to a reviewer concern must end with one of:
- *"We have revised the manuscript accordingly. See [Section X, paragraph Y / Table N / Figure N], revised text: '[new text]'."*
- *"We respectfully disagree because [specific scientific reason]. No change was made to the manuscript, but we have added the following clarification: '[text]'."*

A response that says "We agree with the reviewer" without quoting the new text and its location is a defect. Editors track whether authors actually made the changes they claim.

## Rebuttal Matrix Template

`Revisions/Response_to_Reviewers_Template.md`:

```markdown
# Response to Reviewers — [JOURNAL: IEEE Communications Letters]
**Manuscript:** [CONFIRMED TITLE]
**Manuscript ID:** [ScholarOne ID]
**Date of Response:** YYYY-MM-DD
**Decision received:** Major Revision / Minor Revision

---
## General Response
[2–3 sentences thanking the reviewers and summarising the major changes made]

---
## Reviewer 1

### Comment R1.1
> [Paste reviewer comment verbatim here]

**Response:**
[Your response — acknowledge the validity, explain your change, or give scientific justification for no change]

**Manuscript Change:**
[Section X, Line Y: Old text: "..." → New text: "..."]
OR
[No change made. Added clarification in Discussion, para 3: "..."]

---
### Comment R1.2
> [Paste reviewer comment verbatim here]

**Response:** [RESPONSE]

**Manuscript Change:** [MANUSCRIPT CHANGE]

---
## Reviewer 2

### Comment R2.1
> [...]

**Response:** [RESPONSE]

**Manuscript Change:** [MANUSCRIPT CHANGE]

---
## Editor Comments (if any)

### Comment E1
> [...]

**Response:** [RESPONSE]

**Manuscript Change:** [MANUSCRIPT CHANGE]

---
## Summary of All Changes

| Change | Location | Triggered By |
|---|---|---|
| [Description of change] | [Section/Figure/Table] | [R1.1 / R2.3 / etc.] |
```

## Tracked-Changes Instructions

`Revisions/Manuscript_diff_instructions.md`:

Since this project uses MS Word (not LaTeX), tracked changes are implemented via:

1. **Open** `Manuscript/Main_Manuscript.docx` in Microsoft Word
2. **Enable Track Changes:** Review → Track Changes → Track Changes (Ctrl+Shift+E)
3. **Make all revisions with tracking ON** — do not accept changes during editing
4. **Save as** `Revisions/Manuscript_Revised.docx` (keep tracking visible)
5. **Also save a clean copy** (tracking accepted) as `Revisions/Manuscript_Revised_Clean.docx` for the editor

> **Note:** If the journal later requires a LaTeX diff (e.g., for `latexdiff`), the project would need to be converted. This is logged as a future contingency only.

## Sources / Inputs
- Editor decision letter (uploaded to `Revisions/Decision_Letter.pdf` upon receipt)
- `Manuscript/Main_Manuscript.docx` — the submitted version (do not modify; copy to `Revisions/` first)
- Reviewer comments (copy verbatim into the template — never paraphrase)

## Acceptance Checklist
- [ ] `Revisions/Response_to_Reviewers_Template.md` written and on disk before submission
- [ ] Upon decision receipt: Decision letter saved to `Revisions/Decision_Letter.pdf`
- [ ] All reviewer comments copied verbatim into the rebuttal matrix (no paraphrasing)
- [ ] Every comment row has a non-empty Response AND a Manuscript Change reference
- [ ] Zero defensive-only responses (every disagreement gives a scientific reason)
- [ ] `Revisions/Manuscript_Revised.docx` created with Track Changes enabled
- [ ] `Revisions/Manuscript_Revised_Clean.docx` created (clean copy for editor)
- [ ] Summary of changes table is complete

## Handover
- `Revisions/Response_to_Reviewers.md` + `Revisions/Manuscript_Revised.docx` → Upload to ScholarOne for resubmission
- Updated `Manuscript/references.bib` if new references added in revision
- Update `NOMA_execution_plan.md` Change Log with revision date and decision type
