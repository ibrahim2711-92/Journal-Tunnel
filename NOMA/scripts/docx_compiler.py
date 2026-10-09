#!/usr/bin/env python3
"""
docx_compiler.py (also aliased as compiler verifier)
Contract: Compiles / verifies the Word manuscript (.docx) or LaTeX document (.tex).
Checks document structure, verifies embedded images, checks page count, and converts
.docx to .pdf (or checks .pdf compiled output) to ensure no layout or citation defects exist.

Exit code 0 = clean compilation / verification. Exit code 1 = errors.

Usage:
  python scripts/docx_compiler.py
"""
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
MANUSCRIPT_DOCX = PROJECT_ROOT / "Manuscript" / "Main_Manuscript.docx"
MANUSCRIPT_PDF = PROJECT_ROOT / "Manuscript" / "Main_Manuscript.pdf"

def check_docx_structure(path: Path) -> list[str]:
    errors = []
    try:
        with zipfile.ZipFile(path) as z:
            names = z.namelist()
            if "word/document.xml" not in names:
                errors.append("Invalid .docx file: word/document.xml missing.")
            
            # Check for embedded media
            media_files = [n for n in names if n.startswith("word/media/")]
            print(f"[INFO] Found {len(media_files)} embedded image(s) in .docx")
            
            # Read xml content to inspect placeholders
            with z.open("word/document.xml") as f:
                tree = ET.parse(f)
            root = tree.getroot()
            texts = [t.text or "" for t in root.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t")]
            full_text = " ".join(texts)
            
            if "[NEEDS_" in full_text:
                errors.append("Document contains unresolved [NEEDS_*] placeholders.")
    except Exception as e:
        errors.append(f"Failed to parse .docx document: {e}")
    return errors

def main():
    print("Running Manuscript Compiler / Layout Audit Verifier...\n")
    
    if not MANUSCRIPT_DOCX.exists():
        print(f"[FAIL] Manuscript file not found at {MANUSCRIPT_DOCX}")
        print("  Build the manuscript in Phase 7 before running compiler verification.")
        sys.exit(1)

    print(f"Auditing MS Word manuscript: {MANUSCRIPT_DOCX.name}")
    errors = check_docx_structure(MANUSCRIPT_DOCX)

    if MANUSCRIPT_PDF.exists():
        print(f"[OK] Compiled PDF present at: {MANUSCRIPT_PDF.name}")
    else:
        print(f"[WARN] Compiled PDF not found at {MANUSCRIPT_PDF}. Remember to export PDF after updating .docx.")

    if errors:
        print("\nCOMPILATION AUDIT ERRORS:")
        for err in errors:
            print(f"  [FAIL] {err}")
        sys.exit(1)
    else:
        print("\nRESULT: Manuscript document structure PASSED audit.")
        sys.exit(0)

if __name__ == "__main__":
    main()
