# Evidence policy

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

Do not select a paper merely because its title matches the topic. If no suitable paper exists, use the strongest authoritative source and explicitly weaken the claim.

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
