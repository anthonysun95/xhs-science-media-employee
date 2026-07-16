---
name: xhs-science-media
description: "Turn one topic into an audience-first, decision-led, evidence-verified Xiaohongshu popular-science publishing package through a resumable digital-employee workflow. Define the ordinary reader's problem, useful provisional verdict, and action first; then search supporting and disconfirming evidence to set the truthful claim scope without turning the post into a paper review. Before work, verify the five bundled core skills; show exactly five titles as the only planned leader checkpoint; then autonomously write, humanize, generate a cover, build 3:4 HTML/CSS cards, export PNG/PDF deliverables, and create a separate comment hook. Trigger for 小红书选题、普通读者科普、科研科普、文献支撑内容、新媒体数字员工、图文卡片、PNG/PDF成品 or end-to-end social content production."
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

## Audience-first editorial doctrine

Write for an ordinary reader making a real-life decision, not for a researcher reviewing a paper.

1. Define the **provisional reader verdict** first: one plain, useful sentence stating what the reader may need to believe or do after reading. Treat it as a hypothesis until evidence verification is complete.
2. Define the **reader payoff**: what risk, mistake, cost, symptom, or missed opportunity this verdict helps them avoid.
3. Search for supporting and disconfirming evidence to verify, strengthen, qualify, or falsify that verdict. Evidence controls factual scope, but it does not have to become the narrative outline.
4. If the intended verdict is not supportable, revise it to the strongest useful conclusion that is supportable. Do not fill the article with caveats to preserve a weak angle.
5. Lead with the conclusion and practical consequence. Put methods, sample details, pathways, and limitations later, and include only what helps the reader understand or trust the conclusion.

Use the strongest truthful grammar:

- State robust population-level findings and authoritative recommendations directly.
- Use imperatives for practical actions supported by current guidance: `该开空调就开`, not `或许可以考虑开空调`.
- Do not weaken every sentence with `可能`, `或许`, `提示`, `一定程度上`, or `尚需更多研究`. Consolidate material uncertainty into one clear boundary sentence or the evidence card.
- A direct statement about group-level risk is not a guarantee about every individual. Keep that distinction internally and disclose it once when material.
- Never use `一定`, `百分百`, `治愈`, `保证`, or `人人都会` unless the source literally supports that scope.
- Never make a human causal claim from animal or observational evidence alone. Assertive delivery does not change the evidence level.

The final copy should feel decisive because the conclusion is well chosen and well supported, not because uncertainty was hidden.

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

1. Convert the topic into a specific audience problem. Write a provisional reader verdict, reader payoff, and desired action in `work/content-brief.md` before searching for a paper.
2. Search current primary literature and authoritative guidance around that verdict. Look for support, contradiction, boundary conditions, and the most decision-relevant result. Select one anchor paper as the strongest visible receipt, not as the article outline. Save its URL, citation, result, limitations, and source availability in `work/source-ledger.md`.
3. Acquire the legal full text using this strict order: XML first, PDF second. If neither is obtainable, transition to `waiting_for_source_upload`, give the leader the exact paper citation/DOI, and ask them to upload the article. Resume from the uploaded file without repeating research.
4. Use `dbs-content` to finalize the reader verdict, audience tension, useful stance, action, conviction ladder, evidence-to-popularization ratio, content spine, and avoidable claims. Save the diagnosis in `work/content-diagnosis.md`.
5. Use `dbs-xhs-title` to generate exactly five genuinely distinct, supportable titles. Prefer a direct warning, benefit, mistake, or action over `某研究发现` or a journal-led title. Every title must retain its source formula number in the internal file, cover at least three trigger types across the set, and stay within the platform title-length rule.
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

Use the chosen title verbatim. Default to roughly 10-15% science and 85-90% plain-language explanation, consequence, and action. Scientific detail earns space only when it makes the conclusion easier to understand, remember, or trust.

Use this content spine:

1. Title
2. Immediate reader verdict
3. Why this matters in ordinary life
4. The common belief or behavior that needs correcting
5. One simple explanation of why the result makes sense
6. What the reader should do now
7. Compact evidence receipt and one material boundary

Keep the comment hook separate from the card deck. Save one strong final hook in `deliverables/comment-hook.md`.

Use `content-research-writer` for the cited draft. Then use `dbs-resonate`: extract all claims, choose one core mechanism, run the five-dimensional resonance diagnosis, and revise weak or competing passages. Finally use `humanizer-zh` to remove AI phrasing while preserving meaning, citations, risk warnings, uncertainty, and the selected title. Save the publication copy to `work/article.md`.

Do not write like a paper abstract or organize the article by study methods. Avoid jargon, abbreviations, pathway inventories, and sample-detail dumps unless they directly increase reader understanding.

Never upgrade association into causation or a probabilistic result into a guarantee. In reader-facing copy, prefer direct outcome language that matches the evidence level, and state the material boundary once instead of hedging every paragraph.

Before layout, run the ordinary-reader test:

- The first two cards reveal the practical conclusion without requiring study context.
- Each card has one takeaway that can be repeated in one sentence.
- Use no more than one unfamiliar scientific term per card; explain it immediately in ordinary language.
- Replace pathway lists and experimental chronology with one accurate analogy or short cause-and-effect chain when explanation is needed.
- Keep numbers only when they make the size, urgency, or credibility of the result clearer.
- Remove any paragraph that mainly proves the writer read the paper but does not help the reader decide, understand, remember, or act.

### Prepare visual sources

Use the acquired anchor source:

- XML: retain `work/assets/anchor-paper.xml`; render the article front matter or first rendered viewport into `work/assets/anchor-paper-first-page.png` without inventing metadata.
- PDF: retain `work/assets/anchor-paper.pdf`; render page 1 into `work/assets/anchor-paper-first-page.png`.
- Human upload: preserve the uploaded original and apply the XML or PDF path above according to its format.

Create one original 3:4 cover visual and save it as `work/assets/cover-visual.png`. Generate the image without text and deliberately reserve negative space around the intended title position. Compose the visual subject, light, color, and empty space for the selected title rather than placing an unrelated picture behind a title box. Copy the image to `web/assets/cover-visual.png`, then overlay the exact selected title in HTML/CSS so Chinese typography stays correct.

Make the cover title large, high-contrast, and immediately readable at feed size. Use a cover-specific title size of at least `8cqw` or `96px` on a 1200px-wide canvas. Integrate the title with the image through placement, gradient, shadow, or color echo; do not shrink it into a generic information card. Do not add brands, watermarks, unsupported medical claims, or unrelated products.

### Build the card deck

Transition to `rendering`. Copy `assets/card-template/` into `web/` and populate it. Use only HTML and CSS; do not add JavaScript or interaction.

Follow these invariants:

- Make every `section.page` exactly one screenshot card.
- Use a 3:4 canvas with a canonical export size of 1200x1600.
- Preserve the approved article wording while splitting it across cards.
- Use 7-10 cards unless content density requires another count.
- Make card 1 a `cover-page` containing the generated `cover-visual`, the exact selected title in one `h1`, and at most one short kicker or subtitle. Do not put article paragraphs, charts, study screenshots, or evidence boxes on the cover.
- Make cards 2 through the penultimate card `content-page` text cards. Each card uses one plain-language `h2` and 1-3 short paragraphs; it may use a small kicker, page number, or one simple emphasis line. Do not use photos, generated images, paper screenshots, illustrations, diagrams, tables, multi-column dashboards, icon grids, SVG, or canvas elements on body cards.
- Make card 2 deliver the bottom line immediately. Do not make readers wait through background or study design before learning the result.
- Let each body card answer one ordinary-reader question: `跟我有什么关系？`, `为什么？`, or `现在怎么做？`.
- Make the final card a simple `paper-page`: one concise Chinese `h2`, one faithful anchor-paper first-page screenshot, and optionally 1-2 short source lines. Do not add a long conclusion, mechanism recap, decorative infographic, or extra image.
- Use no generated imagery after card 1. The anchor-paper screenshot on the final card is the only required non-text visual after the cover.
- Do not create a comment-hook card.
- Keep all images local and make the page printable without network access.

### Export and validate

Run `scripts/export_cards.py <project-folder>`. It selects a supported local browser and PDF renderer on Windows, macOS, or Linux and preserves the Windows PowerShell exporter as a native fallback.

If the generic exporter cannot run because this operating system exposes different tools, inspect the available browser/PDF commands, create `work/scripts/export_cards_current_system` in the platform's native script format, test it, and use it. Do not ask for creative approval. The script must export:

- one PNG per `section.page`;
- one combined PDF with the same page order;
- the static screenshot webpage.

Transition to `validating`, run `scripts/validate_deliverables.py <project-folder>`, and fix all failures before delivery. The validator must enforce the three card roles above: generated-image cover with a large `h1`, text-only body cards, and a simple final paper card with a Chinese `h2` and the anchor first-page image.

Inspect a contact sheet and the full-size first, second, and final cards. Reject the package if the cover title is not dominant or does not visually integrate with the image, if any body card looks like a dashboard or infographic, or if the final paper screenshot is too small to recognize as the source article.

Transition to `complete` only after every required artifact exists and validation passes.

## Final leader handoff

Return only the decision-relevant outcome:

1. Selected title.
2. Links to the PNG folder, combined PDF, and static webpage.
3. The final comment hook, both inline and as a file link.
4. A one-line evidence note naming the anchor paper and whether XML or PDF was used.

Do not narrate intermediate tooling, retries, or internal files unless the leader asks.
