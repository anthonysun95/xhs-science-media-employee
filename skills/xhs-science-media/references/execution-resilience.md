# Resumable execution and anti-stall rules

Use these rules whenever generation, rendering, export, validation, or another tool call may take noticeable time.

## Granular checkpoint ledger

Maintain `work/run-checkpoint.json` with `scripts/run_checkpoint.py`. The ledger is separate from the editorial phase in `work/status.json`: the phase says where the project is; the ledger says exactly which expensive artifact step is finished.

Before a long step, mark it `in_progress`, name its expected artifacts, and record the next visible outcome. After the step, verify the artifacts exist and mark it `complete`. On failure, mark it `error` with a short actionable note.

Recommended rendering steps:

1. `cover_reference_ready`
2. `cover_asset_ready`
3. `web_layout_ready`
4. `proof_card_exported`
5. `full_package_exported`
6. `automatic_validation_passed`
7. `visual_inspection_passed`

## Resume behavior

At the beginning of every resumed turn:

1. Load `work/status.json` and `work/run-checkpoint.json`.
2. Confirm completed-step artifacts still exist and are non-empty.
3. Preserve valid outputs. Do not redo research, regenerate imagery, rewrite approved copy, or re-export valid files unless the user changed the relevant input.
4. Continue from the first pending, missing, or failed step.
5. If the user changes an upstream input, invalidate only that step and its downstream dependents.

## Long-step communication

Keep the leader informed during active work. State the current step and the next expected artifact before starting a long operation. Do not leave more than about 45-60 seconds without an update. If a command yields a running job, wait in short intervals and report progress between waits instead of starting a duplicate job.

## Split large operations

- Generate or acquire one asset at a time and save it immediately.
- Build the webpage before export.
- Export one proof card before a full batch when the system path is untested.
- Export PNG/PDF before running validation.
- If PDF creation succeeds but PNG conversion fails, keep the PDF and resume with `scripts/export_png_from_pdf.ps1` on Windows instead of replaying browser rendering.
- Run automatic validation before contact-sheet and full-size visual inspection.
- Apply large file changes as small logical patches so a retry does not replay unrelated edits.

An unchanged external state or a slow tool is not itself a blocker. Reuse the current job, poll it, and continue unless it produces an actionable error.
