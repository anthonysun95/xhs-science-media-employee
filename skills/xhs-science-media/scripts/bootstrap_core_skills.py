#!/usr/bin/env python3
"""Check and install the five bundled core skills without overwriting user files."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path


CORE_SKILLS = (
    "dbs-content",
    "dbs-xhs-title",
    "content-research-writer",
    "dbs-resonate",
    "humanizer-zh",
)


def default_skill_dir(platform: str) -> Path:
    home = Path.home()
    if platform == "current":
        if os.environ.get("CODEX_HOME"):
            return Path(os.environ["CODEX_HOME"]).expanduser() / "skills"
        if os.environ.get("CLAUDE_CONFIG_DIR"):
            return Path(os.environ["CLAUDE_CONFIG_DIR"]).expanduser() / "skills"
        if os.environ.get("AGENTS_HOME"):
            return Path(os.environ["AGENTS_HOME"]).expanduser() / "skills"
        if os.environ.get("GROK_HOME"):
            return Path(os.environ["GROK_HOME"]).expanduser() / "skills"
        platform = "codex"

    roots = {
        "codex": Path(os.environ.get("CODEX_HOME", home / ".codex")),
        "claude": Path(os.environ.get("CLAUDE_CONFIG_DIR", home / ".claude")),
        "agents": Path(os.environ.get("AGENTS_HOME", home / ".agents")),
        "grok": Path(os.environ.get("GROK_HOME", home / ".grok")),
    }
    return roots[platform].expanduser() / "skills"


def check_skill(path: Path) -> bool:
    return path.is_dir() and (path / "SKILL.md").is_file()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check or install the five bundled core skills."
    )
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--check", action="store_true", help="Only report status.")
    action.add_argument(
        "--install-missing",
        action="store_true",
        help="Install missing skills from the bundled canonical copies.",
    )
    parser.add_argument(
        "--platform",
        choices=("current", "codex", "claude", "agents", "grok"),
        default="current",
        help="Select the target Agent skill home when --dest is omitted.",
    )
    parser.add_argument("--dest", type=Path, help="Explicit target skills directory.")
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    bundle_root = skill_root / "assets" / "core-skills"
    target_root = (args.dest or default_skill_dir(args.platform)).resolve()
    install = bool(args.install_missing)
    results: dict[str, dict[str, str]] = {}
    failed = False
    missing = False

    for name in CORE_SKILLS:
        source = bundle_root / name
        target = target_root / name
        if check_skill(target):
            results[name] = {"status": "available", "path": str(target)}
            continue

        missing = True
        if not install:
            results[name] = {"status": "missing", "path": str(target)}
            continue

        if not check_skill(source):
            failed = True
            results[name] = {
                "status": "error",
                "path": str(target),
                "message": f"Bundled source is incomplete: {source}",
            }
            continue

        try:
            target_root.mkdir(parents=True, exist_ok=True)
            shutil.copytree(source, target)
            results[name] = {"status": "installed", "path": str(target)}
        except FileExistsError:
            if check_skill(target):
                results[name] = {"status": "available", "path": str(target)}
            else:
                failed = True
                results[name] = {
                    "status": "error",
                    "path": str(target),
                    "message": "Target exists but is not a valid skill; it was not overwritten.",
                }
        except OSError as exc:
            failed = True
            results[name] = {
                "status": "error",
                "path": str(target),
                "message": str(exc),
            }

    print(
        json.dumps(
            {
                "target": str(target_root),
                "mode": "install-missing" if install else "check",
                "skills": results,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    if failed:
        return 1
    if missing and not install:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
