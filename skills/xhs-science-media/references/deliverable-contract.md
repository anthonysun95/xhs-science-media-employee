# Deliverable contract

Create this project structure:

```text
<project>/
  work/
    status.json
    topic-brief.md
    content-diagnosis.md
    source-ledger.md
    title-candidates.md
    selected-title.md
    article.md
    assets/
      anchor-paper.xml        # preferred when available
      anchor-paper.pdf        # PDF fallback; only one full-text format is required
      anchor-paper-first-page.png
      cover-visual.png
    scripts/
      export_cards_current_system.*  # create only when the bundled exporter cannot run
  web/
    index.html
    styles.css
    assets/
  deliverables/
    png/
      page-01.png
      page-02.png
      ...
    xiaohongshu-cards.pdf
    comment-hook.md
```

At least one full-text source must exist: `anchor-paper.xml`, `anchor-paper.pdf`, or the preserved human-uploaded equivalent.

## Card requirements

- Canvas: 1200x1600 pixels, exactly 3:4.
- Mapping: one `section.page` equals one PNG and one PDF page.
- Web technology: HTML and CSS only; no JavaScript and no interaction.
- Cover: first page, selected title verbatim.
- Evidence: last page, faithful anchor-paper first-page/front-matter image plus a Chinese title.
- Hook: deliver as Markdown, not as a card.
- Copy: preserve the approved article; splitting and typographic emphasis are allowed, rewriting is not.

## Quality gate

Reject the package when any condition fails:

- PNG count differs from `section.page` count.
- Any PNG is not 3:4.
- PDF page order or count differs from PNGs.
- A local image is missing.
- Text is clipped, too small for a mobile feed, or duplicated accidentally.
- The cover title is wrong.
- The paper result cannot support the article's key claim.
- `comment-hook.md` is missing or contains more than one final hook.

The bundled automatic validator remains intentionally narrow. Complete the visual and evidence checks manually without changing `scripts/validate_deliverables.py` unless the leader explicitly requests a stronger validator.
