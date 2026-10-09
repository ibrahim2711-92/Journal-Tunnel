#!/usr/bin/env python3
"""
cover_letter_builder.py
Contract: Generates a formatted cover letter to the Editor-in-Chief of
IEEE Communications Letters by filling the Cover_Letter/Cover_Letter.md template
with values from CLAUDE.md and docs/Abstract_Keywords_Draft.md.

Exit code 0 = cover letter generated. Exit code 1 = missing required fields.

Usage:
  python scripts/cover_letter_builder.py
"""
import sys
import re
from pathlib import Path
from datetime import date

PROJECT_ROOT = Path(__file__).parent.parent
COVER_LETTER_DIR = PROJECT_ROOT / "Cover_Letter"
ABSTRACT_DRAFT = PROJECT_ROOT / "docs" / "Abstract_Keywords_Draft.md"
OUTPUT_PATH = COVER_LETTER_DIR / "Cover_Letter.md"

COVER_LETTER_DIR.mkdir(exist_ok=True)

def extract_section(text: str, heading: str) -> str:
    """Extract text after a markdown heading."""
    pattern = rf"#+\s*{re.escape(heading)}\s*\n(.*?)(?=\n#+|\Z)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""

def main():
    missing = []

    # Read abstract draft
    if not ABSTRACT_DRAFT.exists():
        print(f"[ERROR] {ABSTRACT_DRAFT} not found. Complete Phase 5 first.")
        sys.exit(1)

    abstract_text = ABSTRACT_DRAFT.read_text(encoding="utf-8")
    abstract = extract_section(abstract_text, "Abstract")
    title_match = re.search(r"\*\*([^*]+)\*\*|^#\s+(.+)$", abstract_text, re.MULTILINE)

    # Try to extract confirmed title
    title = "[NEEDS_CONFIRMED_TITLE: OI-002 — confirm from docs/Abstract_Keywords_Draft.md]"
    for line in abstract_text.splitlines():
        line = line.strip()
        if line.startswith("##") and "title" in line.lower():
            continue
        if "title" in abstract_text.lower():
            title_section = extract_section(abstract_text, "Title")
            if title_section and "[NEEDS_" not in title_section:
                title = title_section.split("\n")[0].strip("> ").strip()
                break

    if "[NEEDS_" in title:
        missing.append("Confirmed title (complete Phase 5 first)")

    # Read abstract body
    abstract_body = abstract if abstract else "[NEEDS_ABSTRACT: complete Phase 5]"
    if "[NEEDS_" in abstract_body:
        missing.append("Abstract body (complete Phase 5 first)")

    today = date.today().strftime("%B %d, %Y")

    cover_letter = f"""# Cover Letter — IEEE Communications Letters

**Date:** {today}

---

To: The Editor-in-Chief
**IEEE Communications Letters**
IEEE Communications Society

Dear Editor-in-Chief,

We are pleased to submit our original research article titled:

> **{title}**

for consideration for publication in *IEEE Communications Letters*. This manuscript presents original work that has not been previously published and is not currently under consideration for publication elsewhere. All named authors have read and approved the final manuscript and consent to its submission.

**Scientific Contribution:**

This paper proposes an adaptive network slicing framework for Non-Orthogonal Multiple Access (NOMA) systems, driven by unsupervised machine learning for traffic classification. The key contributions are:

1. A SimPy-based simulation framework modelling NOMA downlink with heterogeneous traffic across eMBB, URLLC, and mMTC slice types.
2. An unsupervised learning pipeline (K-Means clustering + PCA dimensionality reduction) that classifies traffic patterns without requiring labeled training data.
3. An adaptive resource allocation scheme driven by cluster assignments, evaluated against a static baseline across throughput, latency, and SLA compliance metrics.

Our results demonstrate [NEEDS_KEY_RESULT: fill from docs/Results_Draft.md after Phase 1], confirming the potential of label-efficient unsupervised approaches for intelligent 5G/B5G resource management — a topic of direct relevance to the readership of IEEE Communications Letters.

**Fit to IEEE Communications Letters:**

This work addresses a concise, high-impact problem in wireless communications and networking, suitable for the Letters format. The research aligns with the journal's focus on original, brief communications in communications systems, including resource management, multiple access technologies, and machine learning-driven network optimisation.

**Declarations:**

- The authors declare no conflict of interest.
- This research received no external funding [NEEDS_FUNDING: update if applicable — OI-010].
- This is a computational simulation study; no human or animal subjects were involved; ethical approval is not required.
- Data and code will be made available at [NEEDS_REPO: OI-006] upon acceptance.

The corresponding author for this manuscript is [NEEDS_CORRESPONDING_AUTHOR: OI-002].

We thank the Editors and Reviewers for their time and consideration.

Sincerely,

[NEEDS_LEAD_AUTHOR_NAME: OI-002]
[NEEDS_AFFILIATION: OI-002]
[NEEDS_EMAIL: OI-002]
ORCID: [NEEDS_ORCID: OI-002]

---
*Co-authors: Ibrahim ABUBAKAR (Writing – Original Draft), Hamza MUSA (Writing – Original Draft)*
"""

    OUTPUT_PATH.write_text(cover_letter, encoding="utf-8")
    print(f"Cover letter written to: {OUTPUT_PATH}")

    if missing:
        print(f"\n[WARN] {len(missing)} field(s) still need completion:")
        for m in missing:
            print(f"  - {m}")
        print("\nFill all [NEEDS_*] markers in Cover_Letter/Cover_Letter.md before submission.")
        sys.exit(1)

    print("Cover letter generated successfully.")
    sys.exit(0)

if __name__ == "__main__":
    main()
