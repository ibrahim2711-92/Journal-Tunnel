#!/usr/bin/env python3
"""
latex_compiler.py
Wrapper script that redirects to docx_compiler.py for MS Word workflow.
"""
import sys
from pathlib import Path
import subprocess

SCRIPT_DIR = Path(__file__).parent
DOCX_COMPILER = SCRIPT_DIR / "docx_compiler.py"

if __name__ == "__main__":
    res = subprocess.run([sys.executable, str(DOCX_COMPILER)] + sys.argv[1:])
    sys.exit(res.returncode)
