#!/usr/bin/env python3
"""
inventory_builder.py
Contract: Scans Literatures/ for PDF files, attempts to extract title, authors,
year, journal, and DOI from each. Outputs literatures_inventory.json.
If metadata cannot be extracted automatically, creates a stub entry for manual completion.

Exit code 0 = inventory built. Non-zero = error.

Usage:
  python scripts/inventory_builder.py
"""
import sys
import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
LITERATURES_DIR = PROJECT_ROOT / "Literatures"
OUTPUT_PATH = PROJECT_ROOT / "literatures_inventory.json"

def extract_doi_from_text(text: str) -> str | None:
    """Extract a DOI from text using common patterns."""
    match = re.search(r'\b10\.\d{4,}/\S+', text)
    if match:
        doi = match.group(0).rstrip(".,;)>")
        return doi
    return None

def extract_year_from_text(text: str) -> str | None:
    match = re.search(r'\b(19|20)\d{2}\b', text)
    return match.group(0) if match else None

def build_stub_entry(filepath: Path) -> dict:
    """Build a stub entry for manual completion."""
    return {
        "bib_key": filepath.stem.replace(" ", "").replace("-", ""),
        "title": f"[NEEDS_TITLE: extracted from {filepath.name}]",
        "authors": ["[NEEDS_AUTHORS]"],
        "year": "[NEEDS_YEAR]",
        "journal": "[NEEDS_JOURNAL]",
        "doi": "[NEEDS_DOI]",
        "pdf_path": str(filepath.relative_to(PROJECT_ROOT)),
        "verified": False,
        "notes": "Auto-generated stub. Fill all [NEEDS_*] fields manually."
    }

def attempt_pdf_extraction(filepath: Path) -> dict:
    """Try to extract metadata from PDF using pdfplumber or PyPDF2 if available."""
    entry = build_stub_entry(filepath)
    
    # Try pdfplumber
    try:
        import pdfplumber
        with pdfplumber.open(filepath) as pdf:
            # Try metadata first
            meta = pdf.metadata or {}
            if meta.get("Title"):
                entry["title"] = meta["Title"]
            if meta.get("Author"):
                entry["authors"] = [meta["Author"]]
            
            # Try first page text
            if pdf.pages:
                first_page_text = pdf.pages[0].extract_text() or ""
                doi = extract_doi_from_text(first_page_text)
                if doi:
                    entry["doi"] = doi
                year = extract_year_from_text(first_page_text)
                if year:
                    entry["year"] = year
        return entry
    except ImportError:
        pass

    # Try PyPDF2
    try:
        import PyPDF2
        with open(filepath, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            meta = reader.metadata or {}
            if meta.get("/Title"):
                entry["title"] = meta["/Title"]
            if meta.get("/Author"):
                entry["authors"] = [meta["/Author"]]
            if reader.pages:
                first_page_text = reader.pages[0].extract_text() or ""
                doi = extract_doi_from_text(first_page_text)
                if doi:
                    entry["doi"] = doi
        return entry
    except ImportError:
        pass

    # No PDF library available
    print(f"  [INFO] No PDF extraction library found (pdfplumber or PyPDF2).")
    print(f"  Install with: pip install pdfplumber")
    return entry

def main():
    if not LITERATURES_DIR.exists():
        print(f"[ERROR] Literatures/ directory not found.")
        sys.exit(1)

    pdf_files = list(LITERATURES_DIR.glob("*.pdf"))
    if not pdf_files:
        print("[INFO] No PDF files found in Literatures/. Inventory will be empty.")
        # Create empty inventory
        OUTPUT_PATH.write_text(json.dumps([], indent=2), encoding="utf-8")
        print(f"Empty inventory written to {OUTPUT_PATH}")
        sys.exit(0)

    print(f"Found {len(pdf_files)} PDF file(s) in Literatures/\n")

    inventory = []
    needs_manual = []

    for pdf in sorted(pdf_files):
        print(f"Processing: {pdf.name}")
        entry = attempt_pdf_extraction(pdf)
        
        unresolved = [k for k, v in entry.items() if isinstance(v, str) and "[NEEDS_" in v]
        if unresolved:
            needs_manual.append(pdf.name)
            print(f"  [STUB] Fields needing manual completion: {unresolved}")
        else:
            entry["verified"] = True
            print(f"  [OK] DOI: {entry.get('doi', 'N/A')}")
        
        inventory.append(entry)

    OUTPUT_PATH.write_text(json.dumps(inventory, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nInventory written to: {OUTPUT_PATH}")
    print(f"Total entries: {len(inventory)}")
    print(f"Needing manual completion: {len(needs_manual)}")

    if needs_manual:
        print("\nManually complete these entries in literatures_inventory.json:")
        for f in needs_manual:
            print(f"  - {f}")
        print("\nFor each, verify: title, authors, year, journal, DOI")
        print("Set 'verified': true only when all fields are confirmed.")

    sys.exit(0)

if __name__ == "__main__":
    main()
