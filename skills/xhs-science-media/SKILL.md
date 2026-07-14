---
name: xhs-science-media
description: "Turn one topic into a research-backed Xiaohongshu publishing package through a resumable digital-employee workflow. Before work, verify and install the five bundled core skills. Research an anchor paper, prefer XML full text then PDF, show exactly five titles as the only planned leader checkpoint, then autonomously write, humanize, generate a cover, build 3:4 HTML/CSS cards, export one PNG per card plus a combined PDF, and deliver a separate comment hook. Trigger for 小红书选题、科研科普、文献支撑内容、新媒体数字员工、图文卡片、PNG/PDF成品 or end-to-end social content production."
---

# Xiaohongshu science media employee

## Operating contract

Accept one topic as the minimum input. Run the workflow autonomously and persist state so another model can resume without repeating finished work.

Use exactly one planned leader checkpoint:

1. Research and secure the anchor source first.
2. Present exactly five numbered titles and nothing else.
3. Wait for the leader to select 1-5 or provide a replacement title.
4. After selection, finish every deliverable without requesting outline, draft, visual, or export approval.

An additional leader request is allowed only for a true blocker. In particular, if neither XML nor PDF full text can be obtained legally, ask the leader to upload the article. Permission prompts required by the current operating system are operational permissions, not creative approvals.

At the start, read:

- [references/component-routing.md](references/component-routing.md) for the required core-skill preflight and optional capability fallbacks.
- [references/state-machine.md](references/state-machine.md) before creating or resuming a project.
- [references/evidence-policy.md](references/evidence-policy.md) before literature research.
- [references/deliverable-contract.md](references/deliverable-contract.md) before creating files.

## Startup preflight

1. Locate an existing project for the topic. If `work/status.json` exists, load it before doing any work and resume from its phase. Otherwise initialize it with `scripts/project_state.py`. Run Python scripts with the interpreter available in the current environment; do not assume its command is literally `python`.
2. Verify that these five core skills are available: `dbs-content`, `dbs-xhs-title`, `content-research-writer`, `dbs-resonate`, and `humanizer-zh`.
3. If any core skill is missing, run `scripts/bootstrap_core_skills.py --install-missing` for the current Agent skill directory. The package contains canonical bundled copies under `assets/core-skills/`; do not replace an existing installation.
4. A newly installed skill may not appear in the runtime catalog until the next turn. For the current run, read its bundled `SKILL.md` directly and follow it. Record every core skill as `available`, `installed`, or `bundled-current-run` in `work/status.json`.
5. Do not substitute an improvised equivalent for a missing core skill. If the bundled copy is damaged or cannot be installed/read, set the state to `blocked` and report the exact failure.

## Phase 1: research and title gate

Transition through `researching`, `acquiring_source`, and `preparing_titles` as defined by the state machine. Keep internal analysis in `work/`; do not expose it to the leader.

1. Convert the topic into a specific audience problem and content promise.
2. Search current primary literature and authoritative guidance. Select one anchor paper whose result can carry the article. Save its URL, citation, result, limitations, and source availability in `work/source-ledger.md`.
3. Acquire the legal full text using this strict order: XML first, PDF second. If neither is obtainable, transition to `waiting_for_source_upload`, give the leader the exact paper citation/DOI, and ask them to upload the article. Resume from the uploaded file without repeating research.
4. Use `dbs-content` to define audience tension, useful stance, evidence-to-popularization ratio, content spine, and avoidable claims. Save the diagnosis in `work/content-diagnosis.md`.
5. Use `dbs-xhs-title` to generate exactly five genuinely distinct, supportable titles. Every title must retain its source formula number in the internal file, cover at least three trigger types across the set, and stay within the platform title-length rule.
6. Save the titles and formula traceability in `work/title-candidates.md`, transition to `waiting_for_title`, and reply using only this form:

```text
1. 标题
2. 标题
3. 标题
4. 标题
5. 标题

回复数字 1-5，或直接发你想用的标题。
```

Do not include research notes, explanations, title formulas, outlines, skill names, or recommended choices at this checkpoint.

## Phase 2: automatic production after title selection

Record the selected title in `work/selected-title.md` and the state file, transition to `producing`, then continue without another planned approval.

### Write the article

Use the chosen title verbatim. Default to roughly 20% science and 80% clear popular explanation unless the topic requires a stricter balance.

Use this content spine:

1. Title
2. Opening that names the audience situation
3. What the evidence says
4. What the reader should do
5. Conclusion

Keep the comment hook separate from the card deck. Save one strong final hook in `deliverables/comment-hook.md`.

Use `content-research-writer` for the cited draft. Then use `dbs-resonate`: extract all claims, choose one core mechanism, run the five-dimensional resonance diagnosis, and revise weak or competing passages. Finally use `humanizer-zh` to remove AI phrasing while preserving meaning, citations, risk warnings, uncertainty, and the selected title. Save the publication copy to `work/article.md`.

Never upgrade association into causation or a probabilistic result into a guarantee.

### Prepare visual sources

Use the acquired anchor source:

- XML: retain `work/assets/anchor-paper.xml`; render the article front matter or first rendered viewport into `work/assets/anchor-paper-first-page.png` without inventing metadata.
- PDF: retain `work/assets/anchor-paper.pdf`; render page 1 into `work/assets/anchor-paper-first-page.png`.
- Human upload: preserve the uploaded original and apply the XML or PDF path above according to its format.

Create an original 3:4 cover visual. Prefer imagery without text, then overlay the exact selected title in HTML/CSS so Chinese typography stays correct. Do not add brands, watermarks, unsupported medical claims, or unrelated products.

### Build the card deck

Transition to `rendering`. Copy `assets/card-template/` into `web/` and populate it. Use only HTML and CSS; do not add JavaScript or interaction.

Follow these invariants:

- Make every `section.page` exactly one screenshot card.
- Use a 3:4 canvas with a canonical export size of 1200x1600.
- Preserve the approved article wording while splitting it across cards.
- Use 7-10 cards unless content density requires another count.
- Put the cover first.
- Put the anchor-paper first-page image last, with a concise Chinese title.
- Do not create a comment-hook card.
- Keep all images local and make the page printable without network access.

### Export and validate

Run `scripts/export_cards.py <project-folder>`. It selects a supported local browser and PDF renderer on Windows, macOS, or Linux and preserves the Windows PowerShell exporter as a native fallback.

If the generic exporter cannot run because this operating system exposes different tools, inspect the available browser/PDF commands, create `work/scripts/export_cards_current_system` in the platform's native script format, test it, and use it. Do not ask for creative approval. The script must export:

- one PNG per `section.page`;
- one combined PDF with the same page order;
- the static screenshot webpage.

Transition to `validating`, run `scripts/validate_deliverables.py <project-folder>`, and fix all failures before delivery. Keep the current validator behavior unchanged unless the leader explicitly asks to strengthen it. Inspect a contact sheet or representative full-size pages for overflow, missing assets, inaccurate text, and unreadable paper imagery.

Transition to `complete` only after every required artifact exists and validation passes.

## Final leader handoff

Return only the decision-relevant outcome:

1. Selected title.
2. Links to the PNG folder, combined PDF, and static webpage.
3. The final comment hook, both inline and as a file link.
4. A one-line evidence note naming the anchor paper and whether XML or PDF was used.

Do not narrate intermediate tooling, retries, or internal files unless the leader asks.
