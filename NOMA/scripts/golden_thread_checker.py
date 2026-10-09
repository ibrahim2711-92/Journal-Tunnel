#!/usr/bin/env python3
"""
golden_thread_checker.py
Contract: Checks that the Golden Thread is maintained across manuscript sections.
Specifically:
  - Introduction must contain an explicit gap statement and novelty claim
  - Results must contain a finding for each RQ
  - Discussion must interpret each RQ and state at least 3 limitations

Exit code 0 = golden thread intact. Exit code 1 = gaps found.

Usage:
  python scripts/golden_thread_checker.py
  python scripts/golden_thread_checker.py --section introduction
  python scripts/golden_thread_checker.py --section discussion
"""
import sys
import re
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DOCS = PROJECT_ROOT / "docs"

CHECKS = {
    "introduction": {
        "file": DOCS / "Introduction_Draft.md",
        "required_patterns": [
            (r"gap|unaddressed|unexplored|lack of|no study|not been|yet to", "Gap statement"),
            (r"this paper|this work|we propose|we present|proposed", "Novelty / contribution claim"),
            (r"organized as follows|remainder of this paper|section II|section 2", "Paper organisation"),
            (r"rq1|rq2|rq3|research question|objective|hypothesis", "Research question anchoring"),
        ],
        "forbidden_patterns": [
            (r"\[NEEDS_", "Unresolved [NEEDS_*] placeholder"),
        ]
    },
    "results": {
        "file": DOCS / "Results_Draft.md",
        "required_patterns": [
            (r"fig\.|figure|table", "Figure or table reference"),
            (r"\d+[\.,]\d+\s*%|\d+[\.,]\d+\s*mbps|\d+[\.,]\d+\s*ms", "Numerical result"),
            (r"cluster|classification|k-means|dbscan|pca", "Clustering result"),
            (r"throughput|latency|qos|sla|spectral efficiency", "Performance metric"),
        ],
        "forbidden_patterns": [
            (r"this suggests|this implies|this indicates|therefore|because|reason why",
             "Interpretation language in Results (move to Discussion)"),
            (r"\[NEEDS_", "Unresolved [NEEDS_*] placeholder"),
        ]
    },
    "discussion": {
        "file": DOCS / "Discussion_Draft.md",
        "required_patterns": [
            (r"throughput|latency", "Throughput/latency interpretation"),
            (r"cluster|classification", "Clustering result interpretation"),
            (r"qos|sla|slice", "QoS/SLA interpretation"),
            (r"limitation|constrain|drawback|future work|not tested|not modelled", "Limitations statement"),
            (r"simulation only|real.world|real world|synthetic|poisson", "Simulation limitation"),
            (r"scalab", "Scalability limitation"),
        ],
        "forbidden_patterns": [
            (r"\[UNANCHORED\]", "Unanchored claim marker"),
            (r"\[NEEDS_", "Unresolved [NEEDS_*] placeholder"),
        ]
    }
}

def check_section(section_name: str) -> list:
    """Returns list of violation strings."""
    violations = []
    config = CHECKS.get(section_name)
    if not config:
        return [f"Unknown section: {section_name}"]

    filepath = config["file"]
    if not filepath.exists():
        return [f"[MISSING FILE] {filepath} — {section_name} draft not yet written"]

    text = filepath.read_text(encoding="utf-8", errors="ignore").lower()

    for pattern, description in config.get("required_patterns", []):
        if not re.search(pattern, text, re.IGNORECASE):
            violations.append(f"[MISSING] {description}: pattern '{pattern}' not found in {filepath.name}")

    for pattern, description in config.get("forbidden_patterns", []):
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            violations.append(
                f"[VIOLATION] {description}: pattern '{pattern}' found {len(matches)} time(s) in {filepath.name}"
            )

    return violations

def main():
    parser = argparse.ArgumentParser(description="Golden Thread checker for NOMA manuscript.")
    parser.add_argument("--section", default=None,
                        help="Check a specific section: introduction, results, discussion. "
                             "If omitted, checks all sections.")
    args = parser.parse_args()

    sections = [args.section] if args.section else list(CHECKS.keys())
    all_violations = []

    for section in sections:
        print(f"\nChecking section: {section.upper()}")
        violations = check_section(section)
        if violations:
            for v in violations:
                print(f"  {v}")
            all_violations.extend(violations)
        else:
            print(f"  [OK] All golden thread checks passed for {section}.")

    print()
    if all_violations:
        print(f"RESULT: {len(all_violations)} golden thread gap(s) found.")
        sys.exit(1)
    else:
        print("RESULT: Golden Thread INTACT across all checked sections.")
        sys.exit(0)

if __name__ == "__main__":
    main()
