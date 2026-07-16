---
name: xhs-science-media
description: "Turn one topic into an audience-first, decision-led, evidence-verified Xiaohongshu popular-science publishing package through a resumable digital-employee workflow. Define the ordinary reader's problem, useful provisional verdict, and action first; then verify the claim scope without turning the post into a paper review. Use three planned leader checkpoints: exactly five titles, the complete pre-layout draft, and a user-directed cover brief/reference before layout. Respect explicit cover requirements; otherwise default to an original generated cover visual plus HTML/CSS typography. Build readable 3:4 cards and export validated PNG/PDF deliverables. Trigger for 小红书选题、普通读者科普、科研科普、文献支撑内容、新媒体数字员工、图文卡片、PNG/PDF成品 or end-to-end social content production."
---

# Xiaohongshu science media employee

## Operating contract

Accept one topic as the minimum input. Run the workflow autonomously and persist state so another model can resume without repeating finished work.

Use exactly three planned leader checkpoints:

1. Research and secure the anchor source, then present exactly five numbered titles and nothing else. Wait for the leader to select 1-5 or provide a replacement title.
2. After title selection, complete and humanize the full card-by-card draft. Show it before layout and wait for copy approval.
3. After copy approval, notify the leader that layout is ready to begin and ask for one high-performing cover reference plus any explicit cover requirements: image mode, required text, alignment, color, filters, and elements to keep or remove. Do not begin layout until cover direction is supplied or explicitly waived. If the leader already supplied a reference or requirements, record them and continue without asking again.

After the cover direction is available, finish the cover, cards, exports, and validation without another creative approval.

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
- [references/execution-resilience.md](references/execution-resilience.md) before any generation, rendering, export, or validation work.
- [references/evidence-policy.md](references/evidence-policy.md) before literature research.
- [references/deliverable-contract.md](references/deliverable-contract.md) before creating files.

## Startup preflight

1. Locate an existing project for the topic. If `work/status.json` exists, load it before doing any work and resume from its phase. Also load `work/run-checkpoint.json` when present, verify the listed artifacts, and resume from the first incomplete step instead of replaying the whole phase. Otherwise initialize the project with `scripts/project_state.py` and initialize granular checkpoints with `scripts/run_checkpoint.py`. Run Python scripts with the interpreter available in the current environment; do not assume its command is literally `python`.
2. Verify that these four core skills are available: `dbs-content`, `dbs-xhs-title`, `dbs-resonate`, and `humanizer-zh`. Do not invoke `content-research-writer`; the editorial diagnosis and source ledger already define the evidence scope. If a resumed project's legacy state still lists it, leave the history intact but treat it as disabled and never make it a prerequisite.
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

## Phase 2: draft production after title selection

Record the selected title in `work/selected-title.md` and the state file, transition to `producing`, and prepare the complete draft for the pre-layout approval checkpoint.

### Write the article

Use the chosen title verbatim. Default to roughly 30% anchor-paper content and 70% reality-facing expansion. The paper portion must establish the question, intervention, decisive result, and one material boundary; the expansion must turn those findings into ordinary-language choices, eating or behavior instructions, and safety guidance supported by the paper or authoritative guidelines.

Use this content spine:

1. Title
2. Immediate reader verdict
3. Why this matters in ordinary life
4. The common belief or behavior that needs correcting
5. One simple explanation of why the result makes sense
6. What the reader should do now
7. Compact evidence receipt and one material boundary

### Lock the narrative and terminology

Before drafting, make the title's central question the article's mainline. When the title compares two interventions, page 2 must answer that comparison directly; the study and practical cards must then explain and operationalize that answer. Do not replace the paper's actual question with a looser adjacent topic.

Create `work/terminology.md` with one canonical public-facing term for every repeated concept. Use the same term in the cover, card titles, card body, post caption, comment hook, and source card. For example, once `5:2轻断食`, `每天持续控卡`, `肝脏脂肪`, and `内脏脂肪` are chosen, do not later switch to `间歇组`, `持续组`, or `肝脂`. Prefer complete ordinary-language terms over unexplained abbreviations.

For a 9-card comparison post, use this default role map unless the material clearly requires another structure:

1. cover: title and comparison;
2. bottom line: direct verdict and the most useful advantage;
3. study: who, how long, and what was compared;
4. results: the decisive outcome and no more than two useful numbers;
5-7. practical implementation: expand the paper's intervention details and authoritative guidance;
8. choice: who fits which option and who needs professional review;
9. evidence: paper first-page image and compact source text.

Keep every card's job unique. If two adjacent cards can be merged without losing a decision-relevant idea, merge them. Page 2 gives the answer; the result card supplies the receipt rather than restating the same paragraph. Do not spend a card on a secondary null result that does not change the reader's decision. State a material non-significant comparison once in the result body when needed for accuracy.

Use positive, outcome-led card titles. Prefer `两种都有效，5:2轻断食依从性更高` over negative frames such as `没有稳赢` or `没拉开差距`. Conflict and contrast should sharpen the choice, not make a useful result sound empty.

When the paper reports a concrete intervention, expand how it was actually carried out before inventing generic advice. Separate three layers internally: `论文原方案`, `指南支持的现实做法`, and `编辑推演`. Never present an invented menu as the paper's recommended recipe.

Keep the comment hook separate from the card deck. Save one strong final hook in `deliverables/comment-hook.md`.

Write the cited working draft directly from `work/content-diagnosis.md` and `work/source-ledger.md`. Then use `dbs-resonate`: extract all claims, choose one core mechanism, run the five-dimensional resonance diagnosis, and revise weak or competing passages. Finally use `humanizer-zh` to remove AI phrasing while preserving meaning, citations, risk warnings, uncertainty, and the selected title. Save the publication copy to `work/article.md`.

Do not write like a paper abstract or organize the article by study methods. Avoid jargon, abbreviations, pathway inventories, and sample-detail dumps unless they directly increase reader understanding.

Never upgrade association into causation or a probabilistic result into a guarantee. In reader-facing copy, prefer direct outcome language that matches the evidence level, and state the material boundary once instead of hedging every paragraph.

Before layout, run the ordinary-reader test:

- The first two cards reveal the practical conclusion without requiring study context.
- Each card has one takeaway that can be repeated in one sentence.
- Use no more than one unfamiliar scientific term per card; explain it immediately in ordinary language.
- Replace pathway lists and experimental chronology with one accurate analogy or short cause-and-effect chain when explanation is needed.
- Keep numbers only when they make the size, urgency, or credibility of the result clearer.
- Remove any paragraph that mainly proves the writer read the paper but does not help the reader decide, understand, remember, or act.
- For each body card, write about 120-180 Chinese characters, one conclusion, and no more than two numbers. Split the copy into short paragraphs rather than making a dense block. Treat this as a readability target, not a reason to pad or cut away necessary safety information.
- Run an adjacency audit: write each card's one-sentence job and merge or rewrite any neighboring cards with the same job.
- Search the complete draft for every canonical term and forbidden synonym from `work/terminology.md`; correct the cards, caption, hook, and source text together before presenting the draft.

### Handle leader revisions without restarting

Classify feedback before acting:

- **Terminology-only or sentence-level correction:** patch every exact occurrence, search again to confirm the old term is gone, and do not rerun research, title generation, resonance diagnosis, or humanization.
- **Single-card content correction:** revise that card and the matching caption passage, then check the cards immediately before and after it for repetition.
- **Narrative or conclusion change:** revise the affected card roles, rerun the adjacency and evidence-boundary checks, and invalidate only layout/export artifacts downstream of the approved copy.

Never regenerate valid cover assets, source screenshots, or unrelated pages for a copy-only correction. Show the updated draft or changed pages promptly so the leader can verify the exact revision.

Save the complete card-by-card draft to `work/article.o�;��$z{-���jם��6�73�'6�W&6R�Ɩ�R#�X�����ɮK�Έ^8i��X��8[�NK��K��D�����h�~X�nYʎK�N��K�^Xh^8#�����F�c���6V7F������������&�G�����F���