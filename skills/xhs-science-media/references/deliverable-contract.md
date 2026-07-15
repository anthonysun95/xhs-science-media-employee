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
- Cover: the first `section.page` must also be `cover-page`. It contains exactly one locally stored generated cover image, one non-empty `h1` using the selected title verbatim, and at most one short kicker or subtitle. The title must be at least `8cqw` or `96px` on the canonical canvas and visually integrated with the image through deliberate negative space, contrast, gradient, shadow, or color echo.
- Body: every card between the cover and evidence card must also be `content-page`. Body cards are text-only: one non-empty plain-language `h2`, 1-3 short paragraphs, and optionally a small kicker, page number, or one simple emphasis line. They must not contain `img`, `picture`, `svg`, `canvas`, `figure`, `table`, or complex dashboard/grid components.
- Evidence: the final `section.page` must also be `paper-page`. It contains one concise Chinese `h2`, exactly one faithful `anchor-paper-first-page` image, and optionally 1-2 short source lines. It must not contain another illustration, long conclusion, or mechanism recap.
- Imagery: generated imagery appears only on the cover. The faithful paper screenshot is the only non-text visual after the cover.
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
- The first card lacks `cover-page`, a generated `cover-visual`, or a non-empty `h1`.
- The cover title is smaller than `8cqw`/`96px`, visually secondary, or sits in an unrelated generic card layout instead of integrating with the image.
- Any body card lacks `content-page`, lacks a non-empty `h2`, or contains an image, diagram, table, dashboard, or other complex visual element.
- The last card lacks `paper-page`, a concise Chinese `h2`, or exactly one faithful anchor-paper first-page screenshot.
- The final evidence card contains extra imagery or enough text to compete with the paper screenshot.
- The paper result cannot support the article's key claim.
- `comment-hook.md` is missing or contains more than one final hook.

The automatic validator enforces structural card roles and machine-checkable requirements. Complete the visual-integration, simplicity, legibility, and evidence checks manually with a contact sheet plus full-size inspection of the first, second, and final cards.
