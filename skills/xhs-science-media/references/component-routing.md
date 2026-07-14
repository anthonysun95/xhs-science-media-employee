# Component routing

## Required core skills

The digital employee must verify these five skills before research begins. Missing core skills are installed from the package's bundled copies with `scripts/bootstrap_core_skills.py`; they are not replaced by approximate behavior.

| Stage | Required skill | Binding behavior |
|---|---|---|
| Content diagnosis | `dbs-content` | Find the audience problem, central stance, content spine, information density, and avoidable claims. Use it as diagnosis, not ghostwriting. |
| Title gate | `dbs-xhs-title` | Produce exactly five supportable Xiaohongshu titles. Internally retain the formula number for every title and cover at least three trigger types. |
| Research and drafting | `content-research-writer` | Research primary sources, maintain close citations, outline, draft, and perform the final evidence review. |
| Resonance check | `dbs-resonate` | Extract all claims, identify one core mechanism, run the five resonance dimensions, and revise with concrete textual changes. |
| Natural Chinese | `humanizer-zh` | Remove AI phrasing, promotional inflation, vague attribution, formulaic transitions, and sermon-like tone without changing facts. |

Bundled sources live in `assets/core-skills/<skill-name>/`. Never overwrite a user's existing skill installation. In runtimes that discover skills only at session start, read the bundled `SKILL.md` directly for the current run after installation.

## Optional capabilities with required equivalents

These names are convenient when installed, but their absence must not stop the workflow. Execute the required behavior with the current model's native tools or a local script.

| Stage | Optional skill/capability | Equivalent behavior when absent |
|---|---|---|
| Paper parsing/rendering | `pdf` | Parse or render XML/PDF with available document tools; preserve the source and verify the final first-page image. |
| Cover visual | `imagegen` | Use any authorized image-generation capability; if none exists, create an original CSS/typographic cover visual without unsupported imagery. |
| Static cards | `sites-building` | Write local HTML/CSS directly from the bundled template. Do not add JavaScript. |
| Browser QA | `browser:control-in-app-browser` | Use an available headless browser, screenshot tool, or rendered-page inspection workflow. |

Run all components internally. The leader sees only the five-title gate, a source-upload request when truly required, and final deliverables.

When different models run this skill, keep the workflow, source order, checkpoint, state files, and output contract identical. Allow the model's reasoning, voice, and visual judgment to vary inside those boundaries.
