# Phase 0A — Target Journal & Template Lock

## Output
- `docs/IEEE_CommLetters_Guidelines_Extract.md`
- `Manuscript/templates/` — IEEE Word template (.dotx or .docx)

## Target
No word count. Deliverable is a structured guidelines extract file and a downloaded/verified template.

## Entry Condition
- `CLAUDE.md` exists on disk
- `NOMA_execution_plan.md` exists on disk

## Exit Check (Gate 1)
Run the following checks before declaring Phase 0A complete:

```powershell
# Check 1: Guidelines extract exists
Test-Path "docs\IEEE_CommLetters_Guidelines_Extract.md"

# Check 2: Template directory is non-empty
(Get-ChildItem "Manuscript\templates\").Count -gt 0

# Check 3: No [NEEDS_*] placeholders remain in the guidelines extract
Select-String -Path "docs\IEEE_CommLetters_Guidelines_Extract.md" -Pattern "\[NEEDS_"
# Expected: zero matches
```

**Gate 1 passes when:** both files exist, template is present, and zero `[NEEDS_*]` remain in the guidelines extract.

## Characteristic Failure Mode
**Do not copy generic IEEE formatting advice from training knowledge into the guidelines extract.**
The extract must be sourced from the live *Information for Authors* page at:
`https://www.comsoc.org/publications/journals/ieee-communications-letters`
and the ScholarOne portal notes at:
`https://mc.manuscriptcentral.com/comml-ieee`

If the page is unreachable, state so explicitly in the extract, use the most recent published Letters as proxy, and escalate OI-001 to CRITICAL BLOCKING.

## Procedure

### Step 1 — Retrieve the live guidelines
Navigate to the IEEE Communications Letters author information page. Extract and record every binding constraint. If pages are unreachable, use the web search tool and cross-reference at least two independent sources.

### Step 2 — Populate the guidelines extract
Write `docs/IEEE_CommLetters_Guidelines_Extract.md` with this exact structure:

```
# IEEE Communications Letters — Author Guidelines Extract
**Date retrieved:** YYYY-MM-DD
**Source URL:** [live URL]
**Status:** VERIFIED / PARTIALLY VERIFIED / PROXY (explain)

## Binding Constraints
### Page & Length
### Abstract
### Template & Formatting
### Figures & Artwork
### Tables
### References & Citations
### Required Declarations
### Special Deliverables
### Submission Process

## Advisory Notes

## Ambiguities / Silences
(Items the guide does not address — note them explicitly)
```

### Step 3 — Download the Word template
Go to: `https://template-selector.ieee.org/` → select *IEEE Transactions* template (applies to Letters) → download `.docx` → save to `Manuscript/templates/IEEE_CommLetters_template.docx`.

### Step 4 — Scope check
Verify that the proposed paper (NOMA + unsupervised learning + simulation) falls within the stated scope of IEEE Communications Letters. If a scope mismatch is found, escalate to the author immediately before any further work.

## Sources / Inputs
- IEEE Communications Letters information page (live)
- IEEE template selector (live)
- ScholarOne submission portal notes

## Acceptance Checklist
- [ ] `docs/IEEE_CommLetters_Guidelines_Extract.md` written with retrieval date and source URL
- [ ] All binding constraints marked **Binding** or **Advisory**
- [ ] Word template saved to `Manuscript/templates/`
- [ ] Page limit confirmed (expected: 5 pages)
- [ ] Abstract limit confirmed (expected: ≤150 words)
- [ ] Citation style confirmed (expected: IEEE numbered [1], [2], …)
- [ ] OI-001 updated to RESOLVED or PARTIALLY RESOLVED with explanation
- [ ] Gate 1 exit check passes (all three PowerShell checks return expected results)

## Handover
Passes to:
- **Phase 0B** — gap matrix construction uses confirmed citation style and reference limit
- **Phase 7** — assembly uses the template downloaded here
- **CLAUDE.md** — update the Target Journal Constraints table with verified values
