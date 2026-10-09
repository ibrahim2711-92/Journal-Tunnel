#!/usr/bin/env python3
"""
word_counter.py
Contract: Counts words in a Markdown or .docx file.
Supports --min, --max (word count), --max-pages (IEEE 2-col page estimate).
Exits 0 if within limits, 1 if limits exceeded.

Usage:
  python word_counter.py --file docs/Methods_Draft.md --min 600 --max 850
  python word_counter.py --file Manuscript/Main_Manuscript.docx --max-pages 5
"""
import sys
import argparse
import re
from pathlib import Path

def count_words_markdown(filepath: Path) -> int:
    text = filepath.read_text(encoding="utf-8")
    # Strip markdown syntax: headers, links, bold, italic, code blocks
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)  # fenced code
    text = re.sub(r"`[^`]+`", "", text)                      # inline code
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)              # images
    text = re.sub(r"\[.*?\]\(.*?\)", "", text)               # links
    text = re.sub(r"[#*_>\-|]", " ", text)                   # markdown syntax
    words = text.split()
    return len(words)

def count_words_docx(filepath: Path) -> int:
    try:
        import zipfile
        import xml.etree.ElementTree as ET
        with zipfile.ZipFile(filepath) as z:
            with z.open("word/document.xml") as f:
                tree = ET.parse(f)
        root = tree.getroot()
        texts = []
        for t in root.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"):
            if t.text:
                texts.append(t.text)
        return len(" ".join(texts).split())
    except Exception as e:
        print(f"[ERROR] Could not read .docx file: {e}")
        sys.exit(1)

def estimate_ieee_pages(word_count: int) -> float:
    """
    Rough estimate of IEEE two-column page count from word count.
    IEEE two-column format fits approximately 750–900 words per page
    (excluding figures/tables). This is a conservative estimate.
    """
    WORDS_PER_PAGE = 800
    return word_count / WORDS_PER_PAGE

def main():
    parser = argparse.ArgumentParser(description="Word counter for manuscript sections.")
    parser.add_argument("--file", required=True, help="Path to .md or .docx file")
    parser.add_argument("--min", type=int, default=None, help="Minimum word count")
    parser.add_argument("--max", type=int, default=None, help="Maximum word count")
    parser.add_argument("--max-pages", type=float, default=None,
                        help="Maximum estimated IEEE two-column pages")
    parser.add_argument("--section", default=None,
                        help="Section name (for reporting only)")
    args = parser.parse_args()

    filepath = Path(args.file)
    if not filepath.exists():
        print(f"[ERROR] File not found: {filepath}")
        sys.exit(1)

    ext = filepath.suffix.lower()
    if ext == ".md":
        count = count_words_markdown(filepath)
    elif ext == ".docx":
        count = count_words_docx(filepath)
    else:
        print(f"[ERROR] Unsupported file type: {ext}. Use .md or .docx")
        sys.exit(1)

    section_label = f" [{args.section}]" if args.section else ""
    print(f"Word count{section_label}: {count}")

    violations = []

    if args.min is not None and count < args.min:
        violations.append(f"BELOW minimum: {count} < {args.min} words")

    if args.max is not None and count > args.max:
        violations.append(f"EXCEEDS maximum: {count} > {args.max} words")

    if args.max_pages is not None:
        pages = estimate_ieee_pages(count)
        print(f"Estimated IEEE pages (words only, excl. figures): ~{pages:.1f} pages")
        if pages > args.max_pages:
            violations.append(
                f"EXCEEDS page estimate: ~{pages:.1f} pages > {args.max_pages} pages\n"
                f"  NOTE: Page count is approximate (excludes figures/tables).\n"
                f"  Always verify final page count in the IEEE Word template."
            )

    if violations:
        print("\nLIMIT VIOLATIONS:")
        for v in violations:
            print(f"  [FAIL] {v}")
        sys.exit(1)
    else:
        print("All word/page limits: PASS")
        sys.exit(0)

if __name__ == "__main__":
    main()
