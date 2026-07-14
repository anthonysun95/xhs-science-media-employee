#!/usr/bin/env python3
import argparse
import re
import struct
import sys
from pathlib import Path


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as fh:
        signature = fh.read(24)
    if signature[:8] != b"\x89PNG\r\n\x1a\n" or signature[12:16] != b"IHDR":
        raise ValueError(f"Not a valid PNG: {path}")
    return struct.unpack(">II", signature[16:24])


def pdf_page_count(path: Path):
    try:
        from pypdf import PdfReader
    except ImportError:
        return None
    return len(PdfReader(str(path)).pages)


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    html_path = root / "web" / "index.html"
    png_dir = root / "deliverables" / "png"
    pdf_path = root / "deliverables" / "xiaohongshu-cards.pdf"
    hook_path = root / "deliverables" / "comment-hook.md"

    if not html_path.exists():
        return ["Missing web/index.html"]

    html = html_path.read_text(encoding="utf-8")
    page_count = len(re.findall(r"<section\b[^>]*\bclass=[\"'][^\"']*\bpage\b", html, flags=re.I))
    if page_count == 0:
        errors.append("No section.page cards found")
    if re.search(r"<script\b", html, flags=re.I):
        errors.append("JavaScript is not allowed in the screenshot webpage")

    pngs = sorted(png_dir.glob("page-*.png")) if png_dir.exists() else []
    if len(pngs) != page_count:
        errors.append(f"PNG count {len(pngs)} does not match card count {page_count}")
    for png in pngs:
        try:
            width, height = png_size(png)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if width * 4 != height * 3:
            errors.append(f"{png.name} is {width}x{height}, not 3:4")

    if not pdf_path.exists():
        errors.append("Missing deliverables/xiaohongshu-cards.pdf")
    else:
        pdf_count = pdf_page_count(pdf_path)
        if pdf_count is not None and pdf_count != page_count:
            errors.append(f"PDF page count {pdf_count} does not match card count {page_count}")

    if not hook_path.exists() or not hook_path.read_text(encoding="utf-8").strip():
        errors.append("Missing or empty deliverables/comment-hook.md")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Xiaohongshu card deliverables")
    parser.add_argument("project_folder", type=Path)
    args = parser.parse_args()
    errors = validate(args.project_folder.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("OK: deliverables match the Xiaohongshu card contract")
    return 0


if __name__ == "__main__":
    sys.exit(main())
