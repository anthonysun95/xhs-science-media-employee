#!/usr/bin/env python3
"""Create and update the resumable workflow state for one content project."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


PHASES = (
    "bootstrapping",
    "researching",
    "acquiring_source",
    "waiting_for_source_upload",
    "preparing_titles",
    "waiting_for_title",
    "producing",
    "rendering",
    "validating",
    "complete",
    "blocked",
)

TRANSITIONS = {
    "bootstrapping": {"researching", "blocked"},
    "researching": {"acquiring_source", "blocked"},
    "acquiring_source": {"waiting_for_source_upload", "preparing_titles", "blocked"},
    "waiting_for_source_upload": {"acquiring_source", "blocked"},
    "preparing_titles": {"waiting_for_title", "blocked"},
    "waiting_for_title": {"producing", "blocked"},
    "producing": {"rendering", "blocked"},
    "rendering": {"validating", "blocked"},
    "validating": {"rendering", "complete", "blocked"},
    "complete": set(),
    "blocked": {"bootstrapping"},
}

CORE_SKILL_STATUSES = ("available", "installed", "bundled-current-run", "error")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def state_path(project: Path) -> Path:
    return project.resolve() / "work" / "status.json"


def load(project: Path) -> tuple[Path, dict]:
    path = state_path(project)
    if not path.is_file():
        raise FileNotFoundError(f"State file does not exist: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("phase") not in PHASES:
        raise ValueError(f"Unknown phase in state file: {data.get('phase')}")
    return path, data


def save(path: Path, data: dict) -> None:
    data["updated_at"] = now()
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def append_history(data: dict, event: str, **details: object) -> None:
    item = {"at": now(), "event": event}
    item.update({key: value for key, value in details.items() if value is not None})
    data.setdefault("history", []).append(item)


def transition(data: dict, target: str, note: str | None = None) -> None:
    current = data["phase"]
    if target == current:
        return
    if target not in TRANSITIONS[current]:
        raise ValueError(f"Invalid transition: {current} -> {target}")
    data["phase"] = target
    append_history(data, "transition", source=current, target=target, note=note)


def command_init(args: argparse.Namespace) -> int:
    path = state_path(args.project)
    if path.exists():
        print(path.read_text(encoding="utf-8"), end="")
        return 0
    timestamp = now()
    data = {
        "schema_version": 1,
        "topic": args.topic,
        "phase": "bootstrapping",
        "core_skills": {},
        "anchor_source": {"format": None, "path": None, "citation": None},
        "title_candidates": [],
        "selected_title": None,
        "history": [{"at": timestamp, "event": "initialized"}],
        "updated_at": timestamp,
    }
    save(path, data)
    print(path.read_text(encoding="utf-8"), end="")
    return 0


def command_show(args: argparse.Namespace) -> int:
    path, _ = load(args.project)
    print(path.read_text(encoding="utf-8"), end="")
    return 0


def command_transition(args: argparse.Namespace) -> int:
    path, data = load(args.project)
    transition(data, args.phase, args.note)
    save(path, data)
    print(json.dumps({"phase": data["phase"]}, ensure_ascii=False))
    return 0


def command_core_skill(args: argparse.Namespace) -> int:
    path, data = load(args.project)
    data.setdefault("core_skills", {})[args.name] = args.status
    append_history(data, "core_skill", name=args.name, status=args.status)
    save(path, data)
    return 0


def command_source(args: argparse.Namespace) -> int:
    path, data = load(args.project)
    data["anchor_source"] = {
        "format": args.format,
        "path": args.path,
        "citation": args.citation,
    }
    append_history(
        data,
        "anchor_source",
        format=args.format,
        path=args.path,
        citation=args.citation,
    )
    save(path, data)
    return 0


def command_titles(args: argparse.Namespace) -> int:
    if len(args.title) != 5:
        raise ValueError("Exactly five title candidates are required.")
    path, data = load(args.project)
    if data["phase"] != "preparing_titles":
        raise ValueError("Title candidates can only be recorded in preparing_titles.")
    data["title_candidates"] = list(args.title)
    append_history(data, "title_candidates_recorded", count=5)
    save(path, data)
    return 0


def command_select_title(args: argparse.Namespace) -> int:
    path, data = load(args.project)
    if data["phase"] != "waiting_for_title":
        raise ValueError("A title can only be selected in waiting_for_title.")
    data["selected_title"] = args.title
    append_history(data, "title_selected", title=args.title)
    transition(data, "producing")
    save(path, data)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage Xiaohongshu project state.")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init")
    init.add_argument("project", type=Path)
    init.add_argument("--topic", required=True)
    init.set_defaults(func=command_init)

    show = sub.add_parser("show")
    show.add_argument("project", type=Path)
    show.set_defaults(func=command_show)

    move = sub.add_parser("transition")
    move.add_argument("project", type=Path)
    move.add_argument("phase", choices=PHASES)
    move.add_argument("--note")
    move.set_defaults(func=command_transition)

    core = sub.add_parser("set-core-skill")
    core.add_argument("project", type=Path)
    core.add_argument("name")
    core.add_argument("status", choices=CORE_SKILL_STATUSES)
    core.set_defaults(func=command_core_skill)

    source = sub.add_parser("set-source")
    source.add_argument("project", type=Path)
    source.add_argument("format", choices=("xml", "pdf", "human-upload-xml", "human-upload-pdf"))
    source.add_argument("path")
    source.add_argument("--citation")
    source.set_defaults(func=command_source)

    titles = sub.add_parser("set-titles")
    titles.add_argument("project", type=Path)
    titles.add_argument("--title", action="append", required=True)
    titles.set_defaults(func=command_titles)

    selected = sub.add_parser("select-title")
    selected.add_argument("project", type=Path)
    selected.add_argument("title")
    selected.set_defaults(func=command_select_title)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
