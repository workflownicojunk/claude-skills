#!/usr/bin/env python3
"""
DOCX to PDF converter via LibreOffice CLI.

Usage:
    python3 convert-to-pdf.py input.docx [output_dir]

Requires: LibreOffice (brew install --cask libreoffice)
"""

import subprocess
import sys
import os
from pathlib import Path

LIBREOFFICE_PATHS = [
    '/Applications/LibreOffice.app/Contents/MacOS/soffice',
    '/usr/bin/libreoffice',
    '/usr/local/bin/soffice',
]


def find_libreoffice():
    for path in LIBREOFFICE_PATHS:
        if os.path.exists(path):
            return path
    result = subprocess.run(['which', 'soffice'], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    return None


def convert_to_pdf(input_path, output_dir=None):
    soffice = find_libreoffice()
    if not soffice:
        print("FEHLER: LibreOffice nicht gefunden.")
        print("Installieren mit: brew install --cask libreoffice")
        sys.exit(1)

    input_path = Path(input_path).resolve()
    if not input_path.exists():
        print(f"FEHLER: Datei nicht gefunden: {input_path}")
        sys.exit(1)

    if output_dir is None:
        output_dir = input_path.parent
    else:
        output_dir = Path(output_dir).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        soffice,
        '--headless',
        '--convert-to', 'pdf',
        '--outdir', str(output_dir),
        str(input_path),
    ]

    print(f"Konvertiere: {input_path.name} -> PDF")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

    if result.returncode != 0:
        print(f"FEHLER: {result.stderr}")
        sys.exit(1)

    pdf_path = output_dir / input_path.with_suffix('.pdf').name
    if pdf_path.exists():
        size_mb = pdf_path.stat().st_size / 1024 / 1024
        print(f"PDF erstellt: {pdf_path} ({size_mb:.1f} MB)")
        return str(pdf_path)
    else:
        print("FEHLER: PDF wurde nicht erstellt.")
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 convert-to-pdf.py input.docx [output_dir]")
        sys.exit(1)

    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    convert_to_pdf(sys.argv[1], output_dir)
