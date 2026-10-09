# Phase 6 — Cover Letter & Compliance

## Output
- `Cover_Letter/Cover_Letter.md` — formatted cover letter to the Editor-in-Chief
- `docs/Declarations.md` — all required declarations

## Target
Cover letter: 300–400 words. Declarations: complete, with no `[NEEDS_*]` markers except for those explicitly flagged as unresolvable Open Items.

## Entry Condition
- Phase 5 complete: `docs/Abstract_Keywords_Draft.md` exists with confirmed abstract and title
- All four manuscript drafts (Introduction, Methods, Results, Discussion) exist in `docs/`

## Exit Check (Gate 4)
```powershell
# Check 1: Cover letter exists
Test-Path "Cover_Letter\Cover_Letter.md"

# Check 2: Declarations exist
Test-Path "docs\Declarations.md"

# Check 3: Scan for unresolved NEEDS markers across all docs
Select-String -Path "docs\*.md","Cover_Letter\*.md","CLAUDE.md" -Pattern "\[NEEDS_" -Recurse
# Review output — any critical-path [NEEDS_*] (author name, ORCID, CRediT) blocks Gate 4

# Check 4: Co-author confirmation record
Select-String -Path "docs\Declarations.md" -Pattern "Ibrahim ABUBAKAR.*confirmed|Hamza MUSA.*confirmed"
# Expected: both names present with confirmed CRediT roles
```

## Characteristic Failure Mode
**Providing defensive or vague declarations that do not match the journal's exact required format.**
IEEE Communications Letters has specific required declaration texts. Do not write a generic "no conflicts exist" statement — use the journal's prescribed language. Check the verified guidelines in `docs/IEEE_CommLetters_Guidelines_Extract.md` for the exact wording of each declaration.

## Cover Letter Plan

`Cover_Letter/Cover_Letter.md`:

```
[Date: YYYY-MM-DD]

To: The Editor-in-Chief
IEEE Communications Letters

Dear Editor-in-Chief,

[Para 1 — Submission statement (~60 words)]
We submit our original research article, "[CONFIRMED TITLE]", for consideration
for publication in IEEE Communications Letters. This manuscript has not been
previously published and is not under consideration elsewhere.

[Para 2 — Core novelty (~100 words)]
This paper proposes [X]. The key contributions are:
• [Contribution 1 — from Introduction para 4]
• [Contribution 2]
• [Contribution 3]
Our simulation results demonstrate [key result with number] compared to a
static baseline, affirming the suitability of this work for the readership of
IEEE Communications Letters.

[Para 3 — Fit to journal (~60 words)]
We believe this work aligns with the journal's focus on concise, high-impact
communications in [specific area]. The paper addresses [gap] and will be of
interest to researchers working on [related areas].

[Para 4 — Corresponding author details (~40 words)]
The corresponding author for this manuscript is [NEEDS_CORRESPONDING_AUTHOR:
OI-002]. All co-authors have approved the final manuscript and agreed to
their stated CRediT roles.

Sincerely,
[NEEDS_LEAD_AUTHOR_NAME: OI-002]
[Affiliation]
[Email]
[ORCID: NEEDS_ORCID — OI-002]
```

## Declarations File Plan

`docs/Declarations.md`:

### CRediT Author Statement
```
Ibrahim ABUBAKAR: Writing – Original Draft
Hamza MUSA: Writing – Original Draft
[NEEDS_LEAD_AUTHOR: OI-002]: [NEEDS_CREDIT_ROLES: OI-007]
```

### Data Availability Statement
```
The simulation code and generated datasets used in this study are available at
[NEEDS_REPO: OI-006] upon publication. The simulation can be reproduced using
the scripts in /scripts/ with the parameters documented in
docs/Data_Code_Manifest.md.
```
*(If repository is not ready at submission, use: "Data available upon reasonable request from the corresponding author.")*

### Conflict of Interest Statement
```
The authors declare no conflict of interest.
```

### Funding Statement
```
This research received no specific grant from any funding agency in the public,
commercial, or not-for-profit sectors.
```
*(If this is incorrect, replace with the actual grant reference — OI-010)*

### Ethics Statement
```
This study is a computational simulation study involving no human subjects,
no animal subjects, and no personal data. Ethical approval is not required.
```

### Open Access Declaration
*(Complete only if Gold OA chosen — APC ~\$2,295 USD. If not, omit.)*

## Sources / Inputs
- `docs/Abstract_Keywords_Draft.md` — confirmed title and abstract for cover letter
- `docs/IEEE_CommLetters_Guidelines_Extract.md` — exact declaration wording
- `CLAUDE.md` — CRediT roles and Open Items

## Acceptance Checklist
- [ ] `Cover_Letter/Cover_Letter.md` written with submission date, editor address, novelty statement, and contribution list
- [ ] Cover letter references the confirmed title exactly
- [ ] CRediT statement lists all authors with specific roles (no vague "contributed equally")
- [ ] Data Availability Statement names the repository (or uses "upon request" if OI-006 unresolved)
- [ ] Conflict of Interest declaration uses IEEE-required language
- [ ] Ethics statement explicitly confirms computational study / no human subjects
- [ ] Funding statement complete (or waiver noted)
- [ ] Gate 4 exit checks pass
- [ ] Both co-authors have confirmed their CRediT roles (record confirmation method and date in `docs/Declarations.md`)

## Handover
- `Cover_Letter/Cover_Letter.md` → Phase 7 (submitted alongside the manuscript)
- `docs/Declarations.md` → Phase 7 (pasted into the manuscript required sections)
- Gate 4 approval → unlocks Phase 7 (Final Assembly)
