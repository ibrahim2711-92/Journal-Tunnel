#!/usr/bin/env python3
"""
figure_checker.py
Contract: Audits all images in figures/ for resolution (DPI >= 300 for photos,
>= 600 for line art/diagrams), format (PNG/EPS/TIFF/PDF), and reports violations.
Exit code 0 = all figures pass. Exit code 1 = one or more violations.
"""
import os
import sys
from pathlib import Path

FIGURES_DIR = Path(__file__).parent.parent / "figures"
PHOTO_MIN_DPI = 300
LINE_ART_MIN_DPI = 600  # for fig1 system architecture diagram
ALLOWED_EXTENSIONS = {".png", ".eps", ".tiff", ".tif", ".pdf"}

# Map figure names to their type for DPI requirement
LINE_ART_FIGURES = {"fig1_system_architecture"}  # diagrams need 600 DPI

violations = []

def check_png_dpi(filepath: Path) -> int | None:
    """Return DPI of a PNG file using basic header parsing, or None if unreadable."""
    try:
        import struct, zlib
        with open(filepath, "rb") as f:
            sig = f.read(8)
            if sig != b'\x89PNG\r\n\x1a\n':
                return None
            f.read(4)  # length
            chunk_type = f.read(4)
            if chunk_type != b'IHDR':
                return None
            f.read(13)  # IHDR data
            # Read pHYs chunk if present
            while True:
                length_bytes = f.read(4)
                if len(length_bytes) < 4:
                    break
                length = struct.unpack(">I", length_bytes)[0]
                chunk_type = f.read(4)
                data = f.read(length)
                f.read(4)  # CRC
                if chunk_type == b'pHYs' and len(data) >= 9:
                    ppux = struct.unpack(">I", data[0:4])[0]
                    ppuy = struct.unpack(">I", data[4:8])[0]
                    unit = data[8]
                    if unit == 1:  # meters
                        dpi_x = int(ppux * 0.0254)
                        return dpi_x
                if chunk_type == b'IDAT':
                    break
    except Exception:
        pass
    return None

def main():
    if not FIGURES_DIR.exists():
        print(f"[ERROR] figures/ directory not found at {FIGURES_DIR}")
        sys.exit(1)

    figure_files = list(FIGURES_DIR.iterdir())
    if not figure_files:
        print("[WARNING] figures/ directory is empty — no figures to check.")
        sys.exit(0)

    print(f"Checking {len(figure_files)} file(s) in {FIGURES_DIR}\n")

    for f in figure_files:
        if f.name.startswith("."):
            continue

        ext = f.suffix.lower()
        stem = f.stem.lower()

        # Format check
        if ext not in ALLOWED_EXTENSIONS:
            violations.append(f"[FORMAT] {f.name}: extension '{ext}' not in allowed set {ALLOWED_EXTENSIONS}")
            continue

        # DPI check (only possible for PNG; EPS/PDF/TIFF require external tools)
        if ext == ".png":
            dpi = check_png_dpi(f)
            required_dpi = LINE_ART_MIN_DPI if any(la in stem for la in LINE_ART_FIGURES) else PHOTO_MIN_DPI

            if dpi is None:
                print(f"[WARN ] {f.name}: DPI metadata not embedded in PNG — cannot verify. Embed DPI when generating figures.")
            elif dpi < required_dpi:
                violations.append(f"[DPI  ] {f.name}: {dpi} DPI — below required {required_dpi} DPI")
            else:
                print(f"[OK   ] {f.name}: {dpi} DPI >= {required_dpi} DPI")
        elif ext in {".eps", ".pdf"}:
            print(f"[SKIP ] {f.name}: EPS/PDF — DPI check requires external tool (Ghostscript). Verify manually.")
        elif ext in {".tiff", ".tif"}:
            print(f"[SKIP ] {f.name}: TIFF — DPI check requires Pillow. Run: pip install Pillow and re-run this script.")
        else:
            print(f"[OK   ] {f.name}: format accepted, DPI not checked for this format.")

    print()
    if violations:
        print(f"RESULT: {len(violations)} violation(s) found:")
        for v in violations:
            print(f"  {v}")
        sys.exit(1)
    else:
        print("RESULT: All figures pass format check.")
        sys.exit(0)

if __name__ == "__main__":
    main()
