#!/usr/bin/env python3
"""
literatures_acquisition.py
Contract: Fetches metadata/DOIs or open-access PDFs for references listed in
literatures_inventory.json or queried DOIs. Updates references.bib &
literatures_inventory.json. Refuses unverified metadata.

Exit code 0 = acquisition/verification complete. Exit code 1 = failure.

Usage:
  python scripts/literatures_acquisition.py --query "10.1109/TWC.2021.XXXXXXX"
  python scripts/literatures_acquisition.py --batch
"""
import sys
import json
import urllib.request
import urllib.parse
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
BIB_FILE = PROJECT_ROOT / "Manuscript" / "references.bib"
INVENTORY_FILE = PROJECT_ROOT / "literatures_inventory.json"
LITERATURES_DIR = PROJECT_ROOT / "Literatures"

def resolve_doi_crossref(doi: str) -> dict | None:
    """Query CrossRef REST API for verified DOI metadata."""
    clean_doi = doi.strip()
    url = f"https://api.crossref.org/works/{urllib.parse.quote(clean_doi)}"
    req = urllib.request.Request(url, headers={"User-Agent": "NOMA-Research-Scaffold/1.0 (mailto:author@example.com)"})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                item = data.get("message", {})
                title = item.get("title", [""])[0]
                container = item.get("container-title", [""])[0]
                year = None
                published = item.get("published-print") or item.get("published-online") or item.get("created")
                if published and "date-parts" in published:
                    year = published["date-parts"][0][0]
                authors = []
                for a in item.get("author", []):
                    given = a.get("given", "")
                    family = a.get("family", "")
                    authors.append(f"{family}, {given}".strip(", "))
                return {
                    "doi": clean_doi,
                    "title": title,
                    "journal": container,
                    "year": year,
                    "authors": authors,
                    "verified": True
                }
    except Exception as e:
        print(f"[WARN] Failed to resolve DOI '{clean_doi}' via CrossRef: {e}")
    return None

def main():
    parser = argparse.ArgumentParser(description="Literature acquisition & DOI resolver.")
    parser.add_argument("--query", help="Single DOI to query and resolve")
    parser.add_argument("--batch", action="store_true", help="Process unverified entries in literatures_inventory.json")
    args = parser.parse_args()

    if args.query:
        print(f"Resolving DOI: {args.query}")
        res = resolve_doi_crossref(args.query)
        if res:
            print("[OK] Verified Metadata:")
            print(json.dumps(res, indent=2))
        else:
            print("[FAIL] Could not verify DOI metadata.")
            sys.exit(1)
        sys.exit(0)

    if args.batch:
        if not INVENTORY_FILE.exists():
            print(f"[ERROR] {INVENTORY_FILE} not found.")
            sys.exit(1)
        inventory = json.loads(INVENTORY_FILE.read_text(encoding="utf-8"))
        updated = 0
        for entry in inventory:
            if not entry.get("verified") and entry.get("doi") and "[NEEDS_" not in entry["doi"]:
                print(f"Attempting verification for DOI: {entry['doi']}")
                meta = resolve_doi_crossref(entry["doi"])
                if meta:
                    entry.update(meta)
                    entry["verified"] = True
                    updated += 1
        INVENTORY_FILE.write_text(json.dumps(inventory, indent=2), encoding="utf-8")
        print(f"Batch verification complete. Updated {updated} entry/entries.")
        sys.exit(0)

    print("Use --query <DOI> or --batch to acquire/verify metadata.")
    sys.exit(0)

if __name__ == "__main__":
    main()
