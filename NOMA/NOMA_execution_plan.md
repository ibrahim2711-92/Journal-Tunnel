# NOMA Adaptive Slicing — Master Execution Plan

**Title:** Adaptive Network Slicing in Non-Orthogonal Multiple Access (NOMA) Leveraging Unsupervised Learning for Traffic Classification and Resource Management
**Target Journal:** IEEE Communications Letters (IEEE Communications Society)
**Publisher:** IEEE
**Article Type:** Original Research (Letter)
**Target Submission Date:** [NEEDS_DATE: OI-003]
**Guidelines Status:** ⚠️ PARTIALLY VERIFIED — must be confirmed from live IEEE portal before Gate 1

---

## 1 — Overview

This plan governs every session of manuscript work. **Ground truth is always the disk (R1).** At the start of each session, run `Get-ChildItem` (Windows) or `ls` on the relevant output directories to verify what actually exists before claiming a phase is complete.

The workflow is **results-first**: simulation code must run, figures must be locked, and results text must be written before any Discussion or Conclusion prose is drafted. This prevents the most common failure mode — a Discussion that over-interprets or contradicts the actual data.

All phases are executed by the AI agent against the instruction files (`phase_*.md`). Authors review and approve gate transitions. No gate is passed on the agent's claim alone — deliverables must be physically present on disk and pass the stated exit check.

---

## 2 — Status Board

| Phase | Title | Output Path(s) | Hard Gate | Word / Page Target | Status |
|---|---|---|---|---|---|
| **0A** | Journal & Template Lock | `docs/IEEE_CommLetters_Guidelines_Extract.md` | ✅ Gate 1 | — | **Not Started** |
| **0B** | Literature & Gap Matrix | `Literatures/`, `Manuscript/references.bib`, `docs/Gap_Matrix.md` | — | ≥15 verified refs | **Not Started** |
| **0C** | Data & Code Freeze | `Data/Final/`, `scripts/`, `docs/Data_Code_Manifest.md` | ✅ Gate 2 | — | **Not Started** |
| **1** | Figures & Tables Lock | `figures/` (fig1–5), `tables/`, `docs/Results_Draft.md` | — | ~500 words results | **Not Started** |
| **2** | Methods & Protocols | `docs/Methods_Draft.md` | — | ~600–800 words | **Not Started** |
| **3** | Introduction & Gap Framing | `docs/Introduction_Draft.md` | ✅ Gate 3 | ~400–500 words | **Not Started** |
| **4** | Discussion & Limitations | `docs/Discussion_Draft.md` | — | ~400–500 words | **Not Started** |
| **5** | Abstract, Keywords & Title | `docs/Abstract_Keywords_Draft.md` | — | ≤150 words abstract | **Not Started** |
| **6** | Cover Letter & Compliance | `Cover_Letter/Cover_Letter.md`, `docs/Declarations.md` | ✅ Gate 4 | — | **Not Started** |
| **7** | Final Manuscript Assembly | `Manuscript/Main_Manuscript.docx` + `Main_Manuscript.pdf` | — | ≤5 pages (IEEE 2-col) | **Not Started** |
| **8** | Peer Review & Rebuttal Pipeline | `Revisions/Response_to_Reviewers_Template.md` | — | — | **Not Started** |

---

## 3 — Target Journal Profile

| Attribute | Detail |
|---|---|
| **Journal** | IEEE Communications Letters |
| **Publisher** | IEEE / IEEE Communications Society |
| **Scope** | Short, high-impact communications on original research in communications and networking |
| **Impact Factor** | ~4.1 (2023–2024 JCR) |
| **Review Turnaround** | ~6–10 weeks typical |
| **Page Limit** | 5 pages (standard two-column IEEE format); mandatory overlength page charges (MOPC) for >5 pp |
| **Open Access** | Hybrid — optional Gold OA (APC ~\$2,295 USD) |
| **Template** | IEEE two-column format; official Word template via ieee.org/template-selector |
| **Citation Style** | IEEE numbered [1], [2], … with DOIs |
| **Abstract** | Unstructured, ≤150 words |
| **Keywords** | 3–5 IEEE taxonomy index terms |
| **Special Sections** | Data Availability Statement (upon acceptance); no Highlights or Graphical Abstract required |
| **Submission Portal** | ScholarOne Manuscripts (manuscriptcentral.com/comml-ieee) |

> **⚠️ OI-001** — All figures above are drawn from web search and training knowledge. The live *Information for Authors* page must be accessed and verified before Gate 1.

---

## 4 — Critical Path & Dependency Map

```
[0A Journal Lock] ──────────────────────────────── GATE 1
       │
       ├──▶ [0B Literature & Gap Matrix]
       │           │
       │           ▼
       └──▶ [0C Data & Code Freeze] ──────────── GATE 2
                   │
                   ▼
             [1 Figures & Tables Lock] ◀── (requires 0B + 0C)
                   │
          ┌────────┴────────┐
          ▼                 ▼
   [2 Methods]        [3 Introduction] ──── GATE 3
          │                 │
          └────────┬────────┘
                   ▼
           [4 Discussion & Limitations]
                   │
                   ▼
           [5 Abstract, Keywords & Title]
                   │
                   ▼
           [6 Cover Letter & Compliance] ── GATE 4
                   │
                   ▼
           [7 Final Assembly → .docx + PDF]
                   │
                   ▼
           [8 Peer Review Scaffold] (post-submission)
```

**Parallel tasks allowed after Gate 2:**
- Phase 2 (Methods) and Phase 3 (Introduction) may be drafted in parallel once Figures & Tables are locked.

---

## 5 — Hard Gates & Exit Checks

### Gate 1 — Journal Constraint & Scope Gate (After Phase 0A)
**Blocks:** Phase 0B, 0C
**Checks:**
- [ ] `docs/IEEE_CommLetters_Guidelines_Extract.md` exists on disk
- [ ] Page limit, abstract limit, citation style, and template source are confirmed from the live IEEE portal
- [ ] Word template downloaded to `Manuscript/templates/`
- [ ] Proposed study scope confirmed to fit IEEE Communications Letters (original research, concise, comms/networking topic)

### Gate 2 — Data Reproducibility & Code Lock Gate (After Phase 0C)
**Blocks:** Phase 1 (Figures & Tables)
**Checks:**
- [ ] `Data/Final/` directory is non-empty and contents listed in `docs/Data_Code_Manifest.md`
- [ ] `scripts/reproducibility_runner.py` executes end-to-end without errors from a clean Python environment
- [ ] Random seeds pinned and recorded in `CLAUDE.md` and `docs/Data_Code_Manifest.md`
- [ ] All Python dependencies listed in `scripts/requirements.txt`

### Gate 3 — Novelty & Gap Alignment Gate (After Phase 3)
**Blocks:** Phase 4 (Discussion)
**Checks:**
- [ ] `docs/Introduction_Draft.md` exists on disk
- [ ] Introduction contains an explicit, one-paragraph research gap statement (not a general background paragraph)
- [ ] Introduction contains a one-to-two sentence novelty claim mapped to at least one row in the Golden Thread table
- [ ] `scripts/golden_thread_checker.py` runs and produces zero gap warnings

### Gate 4 — Co-Author & Compliance Sign-Off Gate (After Phase 6)
**Blocks:** Phase 7 (Final Assembly)
**Checks:**
- [ ] `Cover_Letter/Cover_Letter.md` exists on disk with editor name, journal name, and novelty summary
- [ ] `docs/Declarations.md` contains: CRediT author statement, Data Availability Statement, Conflict of Interest statement, Funding statement (or explicit waiver)
- [ ] All `[NEEDS_*]` markers in `CLAUDE.md` resolved or explicitly acknowledged as outstanding Open Items
- [ ] All co-authors (Ibrahim ABUBAKAR, Hamza MUSA) have confirmed their CRediT roles in writing

---

## 6 — Data & Evidence Provenance Map

| Source | Description | Location | Access | Status |
|---|---|---|---|---|
| Simulation (primary) | SimPy-generated NOMA network traffic data | `Data/Raw/` → `Data/Final/` | Local — generated by `scripts/` | Not started |
| Literature | Referenced papers verifying NOMA, slicing, uML claims | `Literatures/` | Open-access + DOI-verified | Not started |
| Quarantine — prior draft | Pre-existing docx text (unverified citations) | `Literatures_quarantine/` | Read-only pending review | Quarantined |

**Data Sharing Terms:** Simulation code and generated datasets will be made available via [NEEDS_REPO: OI-006] upon acceptance.

---

## 7 — Milestones

| ID | Milestone | Triggered By | Target Date |
|---|---|---|---|
| **M1** | Scaffold Locked | This document approved by authors | Today |
| **M2** | Results & Figures Locked | Gate 2 passed + Phase 1 complete | [NEEDS_DATE] |
| **M3** | Full Draft Assembled & PDF Compiled | Phase 7 complete | [NEEDS_DATE] |
| **M4** | Submission Package Ready | Gate 4 passed | [NEEDS_DATE] |
| **M5** | Peer-Review Rebuttal Scaffolded | Editor decision received | Post-submission |

---

## 8 — Open Items Table

| ID | Description | Blocking Phase | Owner | Status |
|---|---|---|---|---|
| OI-001 | Verify IEEE Communications Letters *Information for Authors* from live portal; confirm page limit, APC, abstract limit | Gate 1 / Phase 0A | AI + Author | **OPEN — Critical** |
| OI-002 | Lead/Corresponding Author name, ORCID iD, affiliation, and contact email | Phase 6 (Cover Letter) | Author | **OPEN** |
| OI-003 | Target submission date | Phase planning | Author | **OPEN** |
| OI-004 | Backup journal specific names (Springer: which journal? Elsevier: which journal?) | Phase 0A | Author | **OPEN** |
| OI-005 | Python random seed — must be pinned before code freeze | Gate 2 / Phase 0C | Author | **OPEN** |
| OI-006 | Code/data repository choice (GitHub, Zenodo, OSF, Figshare) | Phase 6 | Author | **OPEN** |
| OI-007 | CRediT roles for Lead Author — only Writing–Original Draft assigned to Ibrahim and Hamza so far | Phase 6 | Author | **OPEN** |
| OI-008 | Quarantine review: verify all citations in `Literatures_quarantine/` docs before integrating any text | Phase 0B | AI + Author | **OPEN** |
| OI-009 | Confirm ethics waiver explicitly: no human subjects, no sensitive data — record in `docs/Declarations.md` | Phase 6 | Author | **OPEN** |
| OI-010 | Funding statement: none to declare, or list grant/institution | Phase 6 | Author | **OPEN** |

---

## 9 — Change Log

| Date | Change | Author |
|---|---|---|
| 2026-10-04 | Scaffold created; quarantine applied to pre-existing draft docx files | AI Agent |
