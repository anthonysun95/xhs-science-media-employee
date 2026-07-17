# Evidence policy

## Editorial role of evidence

Start with the ordinary reader's decision problem, not with a paper. Define a provisional reader verdict and action hypothesis first; then search for evidence that supports, contradicts, narrows, or overturns it. Do not treat the verdict as a fact until verification is complete.

Evidence has three jobs:

1. prevent a false or overbroad verdict;
2. make a useful verdict credible;
3. supply one memorable reason the reader can understand.

Evidence determines factual scope and safety, but it does not have to determine the paper's section order as the article structure. When the leader provides an anchor paper, its central question and conclusion remain the narrative spine. Use roughly 30% of the post to establish what the paper compared, found, and could support, then use roughly 70% for guideline-supported practical interpretation and action. Keep detailed appraisal in `work/`.

## Source hierarchy

Prefer sources in this order:

1. Peer-reviewed primary research directly studying the claim.
2. Systematic reviews, meta-analyses, and current professional guidelines.
3. Government, university, medical-society, and standards-body publications.
4. High-quality secondary reporting only for discovery, never as the sole basis of the key claim.

For technical searches, rely on primary sources and official documentation. For health, legal, financial, or other high-stakes topics, verify current guidance before writing.

## Anchor-paper rule

Choose one anchor paper that provides a concrete, audience-relevant result. Confirm:

- the population and sample size;
- what was measured;
- the exact numerical result;
- whether it is observational or causal;
- publication year and journal;
- whether a legal full-text XML or PDF is available.

Treat the anchor paper as both the traceable source and the source of the central question. The card sequence should follow reader understanding rather than the paper's section order, but it must not drift into an adjacent topic that the title paper did not answer. Use converging papers, guidelines, or public-health guidance mainly to interpret the result and make the action section useful.

Do not select a paper merely because its title matches the topic. If no suitable paper exists, use the strongest authoritative source and revise the verdict to the strongest useful conclusion that source can support.

## Certainty and wording ladder

Use the highest justified level and write with the strongest truthful grammar:

1. **Authoritative guidance or converging human outcome evidence:** use direct declarative or imperative wording within the supported population and conditions. Example: `高温会增加老年人的健康负担；该开空调就开。`
2. **Consistent observational human evidence:** state the observed direction directly with risk/frequency language. Example: `长期暴露组的代谢异常更常见。` Do not add `可能` when `更常见` already expresses the correct scope.
3. **Animal or mechanistic evidence:** use it to explain why a conclusion is plausible, clearly naming the experimental context once. Do not present it as a proven human outcome.
4. **Single small or exploratory study:** do not let it carry an absolute headline alone. Pair it with stronger guidance or use it as supporting color.

Do not scatter academic hedges through every paragraph. Put the principal conclusion first, then consolidate any material limitation into one plain boundary sentence or the final evidence card. Avoid false balance: when high-quality sources converge, state the practical conclusion clearly even if minor uncertainty remains.

## Full-text acquisition order

After selecting the anchor paper, acquire the original article in this exact order:

1. **XML first.** Prefer publisher or repository JATS/NLM XML because it preserves structure, metadata, tables, and results for reliable extraction. Save it as `work/assets/anchor-paper.xml`.
2. **PDF second.** If legal XML full text is unavailable, obtain the publisher/repository PDF and save it as `work/assets/anchor-paper.pdf`.
3. **Human upload.** If neither XML nor PDF can be obtained, do not replace the anchor paper with a summary, abstract, or fabricated facsimile. Transition to `waiting_for_source_upload`, provide the exact title, journal, year, DOI/URL, and ask the leader to upload the article.

An abstract can be used to decide whether a paper is promising, but it does not satisfy the full-text requirement for final production.

For the final evidence-card image:

- XML source: render the article's front matter or the first rendered article viewport faithfully; do not invent a paginated PDF page.
- PDF source: render the actual first PDF page.
- Uploaded source: use the corresponding XML or PDF method.

## Source ledger

Record each used source in `work/source-ledger.md`:

```markdown
## Source name
- URL/DOI:
- Type:
- Population:
- Key result used:
- Limitation:
- Claim supported:
- Full-text format: XML/PDF/human upload
- Local path:
```

Keep citations close to the claims in the article source. Do not place raw citation clutter on every card; use the final paper card and the combined PDF metadata where appropriate.

## Claim boundaries

- Never fabricate a paper, DOI, quotation, result, sample size, or guideline.
- Never imply a treatment guarantees an outcome.
- Distinguish correlation, self-report, mechanism, and clinical recommendation.
- Preserve warnings for pregnancy, prescriptions, contraindications, and professional evaluation.
- If evidence conflicts, state the uncertainty instead of choosing the most clickable result.
