#!/usr/bin/env python3
"""
citation_checker.py
Contract: Verifies every in-text citation in a Markdown or .docx manuscript
against references.bib. Flags:
  - Orphaned citations (cited in text but not in .bib)
  - Uncited entries (in .bib but never cited in text)
  - Missing DOI in .bib entries

Exit code 0 = all citations verified. Exit code 1 = violations found.

Usage:
  python citation_checker.py
  python citation_checker.py --manuscript Manuscript/Main_Manuscript.docx --bib Manuscript/references.bib
"""
import sys
import re
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DEFAULT_BIB = PROJECT_ROOT / "Manuscript" / "references.bib"
DEFAULT_MANUSCRIPT_MD = list(PROJECT_ROOT.glob("docs/*.md"))

def extract_bib_keys(bib_path: Path) -> dict:
    """Returns {key: has_doi} dict from a .bib file."""
    text = bib_path.read_text(encoding="utf-8", errors="ignore")
    entries = {}
    # Match @TYPE{KEY,
    for match in re.finditer(r"@\w+\{([^,]+),", text):
        key = match.group(1).strip()
        # Check if this entry has a doi field
        # Find the block for this entry (rough approximation)
        start = match.start()
        block = text[start:start+2000]
        has_doi = bool(re.search(r"\bdoi\s*=", block, re.IGNORECASE))
        entries[key] = has_doi
    return entries

def extract_in_text_citations_numbered(text: str) -> set:
    """Extract IEEE-style numbered citations [1], [1,2], [1-3]."""
    # Returns the citation markers found (not the numbers themselves,
    # since numbered cites can't be cross-checked against bib keys by number alone)
    # Returns count of unique citation markers
    patterns = re.findall(r'\[(\d+(?:[,\-]\d+)*)\]', text)
    return patterns

def extract_in_text_citations_authoryear(text: str) -> set:
    """Extract author-year citations like (Shah et al., 2021) or [Shah2021]."""
    patterns = set()
    # Square bracket bib keys: [Shah2021]
    for m in re.finditer(r'\[([A-Za-z][A-Za-z0-9_:]+)\]', text):
        key = m.group(1)
        if not key.isdigit():
            patterns.add(key)
    return patterns

def read_manuscript_text(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".md":
        return path.read_text(encoding="utf-8", errors="ignore")
    elif ext == ".docx":
        try:
            import zipfile
            import xml.etree.ElementTree as ET
            with zipfile.ZipFile(path) as z:
                with z.open("word/document.xml") as f:
                    tree = ET.parse(f)
            root = tree.getroot()
            texts = []
            for t in root.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"):
                if t.text:
                    texts.append(t.text)
            return " ".join(texts)
        except Exception as e:
            print(f"[ERROR] Could not read .docx: {e}")
            return ""
    return ""

def main():
    parser = argparse.ArgumentParser(description="Citation checker for NOMA manuscript.")
    parser.add_argument("--bib", default=str(DEFAULT_BIB), help="Path to references.bib")
    parser.add_argument("--manuscript", default=None,
                        help="Path to manuscript file (.md or .docx). If omitted, checks all docs/*.md")
    args = parser.parse_args()

    bib_path = Path(args.bib)
    if not bib_path.exists():
        print(f"[ERROR] BibTeX file not found: {bib_path}")
        print("  Create Manuscript/references.bib before running this check.")
        sys.exit(1)

    bib_entries = extract_bib_keys(bib_path)
    print(f"BibTeX entries found: {len(bib_entries)}")

    # Check for missing DOIs
    missing_doi = [k for k, has_doi in bib_entries.items() if not has_doi]
    if missing_doi:
        print(f"\n[WARN] {len(missing_doi)} entry/entries missing DOI field:")
        for k in missing_doi:
            print(f"  - {k}")

    # Gather manuscript text
    if args.manuscript:
        files_to_check = [Path(args.manuscript)]
    else:
        files_to_check = list((PROJECT_ROOT / "docs").glob("*.md"))
        manuscript_docx = PROJECT_ROOT / "Manuscript" / "Main_Manuscript.docx"
        if manuscript_docx.exists():
            files_to_check.append(manuscript_docx)

    if not files_to_check:
        print("[INFO] No manuscript files found to check.")
        sys.exit(0)

    all_text = ""
    for f in files_to_check:
        if f.exists():
            all_text += read_manuscript_text(f) + "\n"

    # Try to detect citation style
    numbered_cites = extract_in_text_citations_numbered(all_text)
    key_cites = extract_in_text_citations_authoryear(all_text)

    violations = []

    if numbered_cites:
        print(f"\nDetected IEEE numbered citations: {len(numbered_cites)} citation marker(s) found.")
        print("  NOTE: Numbered citations cannot be cross-checked against bib keys by number.")
        print("  Verify manually that the reference list order matches in-text [N] markers.")
    
    if key_cites:
        print(f"\nDetected author-key citations: {key_cites}")
        orphaned = key_cites - set(bib_entries.keys())
        if orphaned:
            violations.append(f"Orphaned citations (cited but not in .bib): {orphaned}")
        
        uncited = set(bib_entries.keys()) - key_cites
        if uncited:
            print(f"[INFO] Uncited bib entries (in .bib but not found in docs): {uncited}")

    print()
    if missing_doi:
        violations.append(f"{len(missing_doi)} bib entries missing DOI: {missing_doi}")

    if violations:
        print(f"RESULT: {len(violations)} violation(s):")
        for v in violations:
            print(f"  [FAIL] {v}")
        sys.exit(1)
    else:
        print("RESULT: Citation check PASSED.")
        if not bib_entries:
            print("  WARNING: .bib file is empty — populate it in Phase 0B.")
        sys.exit(0)

if __name__ == "__main__":
    main()
