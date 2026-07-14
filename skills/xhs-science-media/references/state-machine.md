# Resumable state machine

Store machine-readable state in `<project>/work/status.json`. Use `scripts/project_state.py` to initialize, inspect, and transition it. The state file is the source of truth for resuming work; Markdown files are the human-readable audit trail.

## States

| State | Meaning | Required next action |
|---|---|---|
| `bootstrapping` | Project exists; core skills are being checked. | Finish the five-skill preflight. |
| `researching` | Audience problem and candidate literature are being researched. | Select an anchor paper and record the source ledger. |
| `acquiring_source` | The anchor paper is selected; legal full text is being obtained. | Try XML, then PDF. |
| `waiting_for_source_upload` | XML and PDF are both unavailable. | Ask the leader for the exact paper and wait. |
| `preparing_titles` | Evidence is secured; five titles are being generated. | Save five traceable candidates. |
| `waiting_for_title` | The five-title checkpoint has been shown. | Accept 1-5 or a replacement title. |
| `producing` | Article, resonance pass, humanization, hook, and visual sources are being completed. | Finish publication copy and assets. |
| `rendering` | Static cards and exports are being produced. | Create HTML/CSS, PNGs, and PDF. |
| `validating` | Automated and visual checks are running. | Fix failures or mark complete. |
| `complete` | Every required deliverable exists and validation passed. | Hand off the final links and hook. |
| `blocked` | A non-recoverable operational failure is recorded. | Report the exact condition and preserve all state. |

## Normal transitions

```text
bootstrapping
  -> researching
  -> acquiring_source
  -> preparing_titles
  -> waiting_for_title
  -> producing
  -> rendering
  -> validating
  -> complete
```

Exception paths:

```text
acquiring_source -> waiting_for_source_upload -> acquiring_source
validating -> rendering -> validating
any active state -> blocked
```

## Resume rules

1. Read `work/status.json` before searching, writing, or exporting.
2. Never repeat a completed phase merely because a different model resumed the task.
3. In `waiting_for_title`, interpret a bare number 1-5 as the title decision, record the exact selected title, and transition to `producing`.
4. In `waiting_for_source_upload`, inspect a newly supplied file, preserve it in `work/assets/`, record its format, and transition back to `acquiring_source`.
5. In `rendering` or `validating`, reuse existing correct files and regenerate only missing or failing artifacts.
6. Do not overwrite a `complete` project unless the leader explicitly requests a revision.

## Minimum state fields

```json
{
  "schema_version": 1,
  "topic": "",
  "phase": "bootstrapping",
  "core_skills": {},
  "anchor_source": {
    "format": null,
    "path": null,
    "citation": null
  },
  "title_candidates": [],
  "selected_title": null,
  "history": [],
  "updated_at": ""
}
```

Every transition appends a timestamped history item. Never delete state history during a normal run.
