#!/usr/bin/env python3
"""
revision_diff_builder.py
Contract: For MS Word-based manuscripts, provides instructions and automation
for generating a tracked-changes revision document.
Since this project uses .docx (not LaTeX), latexdiff is not applicable.
Instead, this script:
  1. Verifies the original and revised .docx files exist
  2. Attempts to generate a simple text diff report for review
  3. Outputs instructions for Track Changes workflow in MS Word

Exit code 0 = diff report generated. Exit code 1 = error.

Usage:
  python scripts/revision_diff_builder.py
"""
import sys
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import date

PROJECT_ROOT = Path(__file__).parent.parent
REVISIONS_DIR = PROJECT_ROOT / "Revisions"
ORIGINAL_MANUSCRIPT = PROJECT_ROOT / "Manuscript" / "Main_Manuscript.docx"
REVISED_MANUSCRIPT = REVISIONS_DIR / "Manuscript_Revised.docx"
DIFF_REPORT_PATH = REVISIONS_DIR / "Manuscript_diff_report.md"

def extract_docx_text(path: Path) -> list[str]:
    """Extract paragraph-level text from a .docx file."""
    paragraphs = []
    try:
        with zipfile.ZipFile(path) as z:
            with z.open("word/document.xml") as f:
                tree = ET.parse(f)
        root = tree.getroot()
        for para in root.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"):
            texts = [
                t.text or ""
                for t in para.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t")
            ]
            text = "".join(texts).strip()
            if text:
                paragraphs.append(text)
    except Exception as e:
        print(f"[ERROR] Could not read {path}: {e}")
    return paragraphs

def generate_diff_report(original: list[str], revised: list[str]) -> str:
    """Generate a simple paragraph-level diff between original and revised texts."""
    import difflib
    diff = list(difflib.unified_diff(
        original, revised,
        fromfile="Original Submission",
        tofile="Revised Manuscript",
        lineterm=""
    ))
    return "\n".join(diff)

def main():
    REVISIONS_DIR.mkdir(exist_ok=True)

    violations = []

    if not ORIGINAL_MANUSCRIPT.exists():
        violations.append(f"Original manuscript not found: {ORIGINAL_MANUSCRIPT}")

    if not REVISED_MANUSCRIPT.exists():
        violations.append(f"Revised manuscript not found: {REVISED_MANUSCRIPT}")
        print(f"[INFO] Revised manuscript not yet created.")
        print(f"\nTo create the tracked-changes revision document:")
        print(f"1. Open Manuscript/Main_Manuscript.docx in Microsoft Word")
        print(f"2. Enable Track Changes: Review → Track Changes → Track Changes (Ctrl+Shift+E)")
        print(f"3. Make all revisions with tracking ON")
        print(f"4. Save as: Revisions/Manuscript_Revised.docx (keep tracking visible)")
        print(f"5. Save a clean copy (changes accepted): Revisions/Manuscript_Revised_Clean.docx")
        print(f"6. Re-run this script to generate the diff report.")

        # Write instructions file
        instructions = f"""# Tracked-Changes Instructions — IEEE Communications Letters Revision

**Date:** {date.today().strftime('%Y-%m-%d')}
**Project:** Adaptive Network Slicing in NOMA

## Step-by-Step Revision Workflow

Since this project uses MS Word (.docx), revision tracking is done via Microsoft Word's
built-in Track Changes feature (equivalent to latexdiff for LaTeX projects).

### Steps

1. **Open** `Manuscript/Main_Manuscript.docx` in Microsoft Word
2. **Enable Track Changes:** Review tab → Track Changes → Track Changes (Ctrl+Shift+E)
3. **Make all revisions** with tracking ON — do not accept or reject changes during editing
4. **Save as** `Revisions/Manuscript_Revised.docx` — keep Track Changes visible (for editors)
5. **Save a clean copy:** Save As → `Revisions/Manuscript_Revised_Clean.docx` → Accept All Changes
6. **Run this script** to generate the text diff report: `python scripts/revision_diff_builder.py`

### Files to Submit for Resubmission

| File | Purpose |
|---|---|
| `Revisions/Manuscript_Revised.docx` | Main revised manuscript (Track Changes ON) |
| `Revisions/Manuscript_Revised_Clean.docx` | Clean copy for editor (Track Changes accepted) |
| `Revisions/Response_to_Reviewers.md` | Point-by-point rebuttal |
| `Cover_Letter/Cover_Letter.md` | Updated cover letter (note revision submission) |

### Notes
- Never modify the original `Manuscript/Main_Manuscript.docx` — it represents the submitted version
- Every change in the revised manuscript must be referenced in Response_to_Reviewers.md
- If the editor requests a specific format for the response document, follow that format over this template
"""
        (REVISIONS_DIR / "Manuscript_diff_instructions.md").write_text(instructions, encoding="utf-8")
        print(f"\nInstructions written to: {REVISIONS_DIR / 'Manuscript_diff_instructions.md'}")

    if violations:
        print(f"\nREQUIREMENTS NOT MET:")
        for v in violations:
            print(f"  [FAIL] {v}")
        sys.exit(1)

    # Both files exist — generate text diff
    print(f"Extracting text from original: {ORIGINAL_MANUSCRIPT.name}")
    original_paragraphs = extract_docx_text(ORIGINAL_MANUSCRIPT)

    print(f"Extracting text from revised: {REVISED_MANUSCRIPT.name}")
    revised_paragraphs = extract_docx_text(REVISED_MANUSCRIPT)

    print(f"Generating diff report...")
    diff_text = generate_diff_report(original_paragraphs, revised_paragraphs)

    report = f"""# Manuscript Text Diff Report
**Generated:** {date.today().strftime('%Y-%m-%d')}
**Original:** Manuscript/Main_Manuscript.docx
**Revised:** Revisions/Manuscript_Revised.docx

> NOTE: This is a paragraph-level text diff for reference.
> The authoritative tracked-changes document is Revisions/Manuscript_Revised.docx
> with Microsoft Word Track Changes visible.

---

```diff
{diff_text if diff_text else 'No differences detected at paragraph level.'}
```
"""

    DIFF_REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"Diff report written to: {DIFF_REPORT_PATH}")
    print("RESULT: Diff report generated successfully.")
    sys.exit(0)

if __name__ == "__main__":
    main()
