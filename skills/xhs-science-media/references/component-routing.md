# Component routing

## Required core skills

Verify these four skills before research begins. Install missing skills from `assets/core-skills/` with `scripts/bootstrap_core_skills.py`; do not replace an existing installation with an approximation.

| Stage | Required skill | Binding behavior |
|---|---|---|
| Content diagnosis | `dbs-content` | Find the audience problem, central stance, content spine, information density, and avoidable claims. Use it as diagnosis, not ghostwriting. |
| Title gate | `dbs-xhs-title` | Produce exactly five supportable Xiaohongshu titles. Retain formula numbers internally and cover at least three trigger types. |
| Resonance check | `dbs-resonate` | Extract claims, identify one core tension, diagnose resonance, and revise with concrete textual changes. |
| Natural Chinese | `humanizer-zh` | Remove AI phrasing, promotional inflation, vague attribution, formulaic transitions, and sermon-like tone without changing facts. |

Do not invoke or require `content-research-writer`. Perform literature acquisition, source-ledger maintenance, claim verification, and evidence review through the workflow in `SKILL.md` and `references/evidence-policy.md`.

Bundled sources live in `assets/core-skills/<skill-name>/`. Never overwrite a user's existing skill installation. In runtimes that discover skills only at session start, read the bundled `SKILL.md` directly for the current run after installation.

## Optional capabilities with required equivalents

These names are convenient when installed, but their absence must not stop the workflow. Execute the required behavior with native tools or a local script.

| Stage | Optional skill/capability | Equivalent behavior when absent |
|---|---|---|
| Paper parsing/rendering | `pdf` | Parse or render XML/PDF with available document tools; preserve the source and verify the final first-page image. |
| Cover visual | `imagegen` | Use image generation only when `work/cover-brief.md` calls for it or when the leader supplied no cover direction and the default cover path applies. Otherwise use the requested paper, supplied image, composite, or text-only treatment. |
| Static cards | `sites-building` | Write local HTML/CSS directly from the bundled template. Do not add JavaScript. |
| Browser QA | `browser:control-in-app-browser` | Use an available headless browser, screenshot tool, or rendered-page inspection workflow. |

Run components internally. The leader sees the five-title checkpoint, the complete pre-layout draft, the cover-reference checkpoint, any true source blocker, and the final deliverables.

Keep the workflow, source order, checkpoints, state files, and output contract identical across models. Allow reasoning, voice, and visual judgment to vary inside those boundaries.
