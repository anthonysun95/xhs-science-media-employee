#!/usr/bin/env python3
"""Cross-platform HTML/CSS card export using a local Chromium browser and Poppler."""

from __future__ import annotations

import argparse
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def executable(candidates: list[str | Path]) -> Path | None:
    for candidate in candidates:
        text = str(candidate)
        found = shutil.which(text)
        if found:
            return Path(found)
        path = Path(text).expanduser()
        if path.is_file():
            return path
    return None


def find_browser() -> Path | None:
    candidates: list[str | Path] = [
        "msedge",
        "microsoft-edge",
        "google-chrome",
        "google-chrome-stable",
        "chromium",
        "chromium-browser",
        "chrome",
    ]
    system = platform.system()
    if system == "Windows":
        for variable in ("ProgramFiles(x86)", "ProgramFiles", "LOCALAPPDATA"):
            root = os.environ.get(variable)
            if root:
                candidates.extend(
                    [
                        Path(root) / "Microsoft" / "Edge" / "Application" / "msedge.exe",
                        Path(root) / "Google" / "Chrome" / "Application" / "chrome.exe",
                    ]
                )
    elif system == "Darwin":
        candidates.extend(
            [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
                "/Applications/Chromium.app/Contents/MacOS/Chromium",
            ]
        )
    return executable(candidates)


def find_pdftoppm() -> Path | None:
    candidates: list[str | Path] = ["pdftoppm", "pdftoppm.exe"]
    bundled = (
        Path.home()
        / ".cache"
        / "codex-runtimes"
        / "codex-primary-runtime"
        / "dependencies"
        / "native"
        / "poppler"
        / "Library"
        / "bin"
        / "pdftoppm.exe"
    )
    candidates.append(bundled)
    return executable(candidates)


def browser_command(
    browser: Path, html: Path, pdf: Path, profile: Path, headless: str
) -> list[str]:
    return [
        str(browser),
        headless,
        "--disable-gpu",
        "--hide-scrollbars",
        "--run-all-compositor-stages-before-draw",
        f"--user-data-dir={profile}",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf}",
        html.as_uri(),
    ]


def render_pdf(browser: Path, html: Path, pdf: Path, profile: Path) -> None:
    last_error = ""
    for headless in ("--headless=new", "--headless"):
        if pdf.exists():
            pdf.unlink()
        result = subprocess.run(
            browser_command(browser, html, pdf, profile, headless),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=90,
            check=False,
        )
        if result.returncode == 0 and pdf.is_file() and pdf.stat().st_size > 0:
            return
        last_error = (result.stderr or result.stdout or "unknown browser failure").strip()
    raise RuntimeError(f"HTML to PDF export failed: {last_error}")


def numeric_suffix(path: Path) -> int:
    match = re.search(r"(\d+)$", path.stem)
    return int(match.group(1)) if match else 0


def export(project: Path) -> tuple[Path, list[Path]]:
    project = project.resolve()
    html = project / "web" / "index.html"
    deliverables = project / "deliverables"
    png_dir = deliverables / "png"
    pdf = deliverables / "xiaohongshu-cards.pdf"

    if not html.is_file():
        raise FileNotFoundError(f"Missing webpage: {html}")
    browser = find_browser()
    pdftoppm = find_pdftoppm()
    missing = []
    if browser is None:
        missing.append("a Chromium browser (Edge, Chrome, or Chromium)")
    if pdftoppm is None:
        missing.append("pdftoppm from Poppler")
    if missing:
        raise RuntimeError(
            "Missing local export tool(s): "
            + ", ".join(missing)
            + ". Probe the current system and create work/scripts/"
            + "export_cards_current_system in its native script format."
        )

    deliverables.mkdir(parents=True, exist_ok=True)
    png_dir.mkdir(parents=True, exist_ok=True)
    if pdf.exists():
        pdf.unlink()
    for old in png_dir.glob("page-*.png"):
        old.unlink()

    with tempfile.TemporaryDirectory(prefix="xhs-card-browser-") as temporary:
        render_pdf(browser, html, pdf, Path(temporary))

    prefix = png_dir / "page"
    result = subprocess.run(
        [str(pdftoppm), "-png", "-r", "96", str(pdf), str(prefix)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
        check=False,
    )
    if result.returncode != 0:
        message = (result.stderr or result.stdout or "unknown Poppler failure").strip()
        raise RuntimeError(f"PDF to PNG export failed: {message}")

    generated = sorted(png_dir.glob("page-*.png"), key=numeric_suffix)
    staged: list[Path] = []
    for index, source in enumerate(generated, 1):
        temporary = png_dir / f".xhs-export-{index:02d}.png"
        source.replace(temporary)
        staged.append(temporary)
    final: list[Path] = []
    for index, source in enumerate(staged, 1):
        target = png_dir / f"page-{index:02d}.png"
        source.replace(target)
        final.append(target)
    return pdf, final


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export one PNG per CSS page plus a combined PDF."
    )
    parser.add_argument("project_folder", type=Path)
    args = parser.parse_args()
    try:
        pdf, pngs = export(args.project_folder)
    except (FileNotFoundError, OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Exported {len(pngs)} cards and {pdf}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
