#!/usr/bin/env python3
"""Maintain granular, artifact-aware checkpoints for resumable production."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ledger_path(project: Path) -> Path:
    return project.resolve() / "work" / "run-checkpoint.json"


def load(path: Path) -> dict:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"schema_version": 1, "steps": {}, "history": [], "updated_at": now()}


def save(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = now()
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def artifact_state(project: Path, artifacts: list[str]) -> list[dict]:
    states = []
    for item in artifacts:
        path = project / item
        states.append({
            "path": item,
            "exists": path.is_file(),
            "bytes": path.stat().st_size if path.is_file() else 0,
        })
    return states


def main() -> int:
    parser = argparse.ArgumentParser(description="Create, update, or inspect a production checkpoint ledger.")
    parser.add_argument("project", type=Path)
    parser.add_argument("--step")
    parser.add_argument("--status", choices=("pending", "in_progress", "complete", "error"))
    parser.add_argument("--next", dest="next_outcome", default="")
    parser.add_argument("--note", default="")
    parser.add_argument("--artifact", action="append", default=[])
    parser.add_argument("--show", action="store_true")
    args = parser.parse_args()

    project = args.project.resolve()
    path = ledger_path(project)
    data = load(path)

    if args.step:
        if not args.status:
            parser.error("--status is required when --step is used")
        artifacts = args.artifact
        states = artifact_state(project, artifacts)
        if args.status == "complete" and artifacts and not all(s["exists"] and s["bytes"] > 0 for s in states):
            missing = ", ".join(s["path"] for s in states if not s["exists"] or s["bytes"] <= 0)
            parser.error(f"cannot mark complete; missing or empty artifact(s): {missing}")
        event = {
            "at": now(),
            "step": args.step,
            "status": args.status,
            "next_outcome": args.next_outcome,
            "note": args.note,
            "artifacts": states,
        }
        data["steps"][args.step] = event
        data["history"].append(event)
        data["current_step"] = args.step if args.status in {"pending", "in_progress", "error"} else ""
        data["next_outcome"] = args.next_outcome
        save(path, data)

    if args.show or not args.step:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
