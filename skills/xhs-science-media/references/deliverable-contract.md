# Deliverable contract

Create this project structure:

```text
<project>/
  work/
    status.json
    run-checkpoint.json
    topic-brief.md
    content-diagnosis.md
    source-ledger.md
    terminology.md
    cover-brief.md
    title-candidates.md
    selected-title.md
    article.md
    assets/
      anchor-paper.xml        # preferred when available
      anchor-paper.pdf        # PDF fallback; only one full-text format is required
      anchor-paper-first-page.png
      cover-reference.*
      cover-visual.png        # required for image modes; omitted for text-only mode
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
- Cover: the first `section.page` must also be `cover-page`, follow `work/cover-brief.md`, and contain one non-empty `h1` using the selected title verbatim. Image modes contain exactly one locally stored `cover-visual`; text-only mode adds `cover-text-only` and contains no image. Explicit leader requirements override the bundled cover template. When no requirements are supplied, default to an original generated background plus HTML/CSS title layout. The title should be at least `8cqw` or `96px` on the canonical canvas and remain visually dominant unless the approved brief explicitly requires another hierarchy.
- Body: every card between the cover and evidence card must also be `content-page`. Body cards are text-only: one non-empty plain-language `h2`, 1-3 short paragraphs, and optionally a small kicker, page number, or one simple emphasis line. Target about 120-180 Chinese characters, exactly one conclusion, and no more than two numbers per card. Default to a `70cqw` text column, about `3.15cqw` body type, `1.7-1.8` line height, and 1-3 emphasized phrases. Use `short-page` to center short text blocks in the upper `75-80%`; start longer cards about `16-18cqw` from the top. They must not contain `img`, `picture`, `svg`, `canvas`, `figure`, `table`, or complex dashboard/grid components.
- Evidence: the final `section.page` must also be `paper-page`. It contains one concise Chinese `h2`, exactly one faithful `anchor-paper-first-page` image, and optionally 1-2 short source lines. It must not contain another illustration, long conclusion, or mechanism recap.
- Imagery: when the cover brief uses generated imagery, it appears only on the cover. The faithful paper screenshot is the only non-text visual after the cover.
- Hook: deliver as Markdown, not as a card.
- Copy: preserve the approved article; splitting and typographic emphasis are allowed, rewriting is not.

## Quality gate

Reject the package when any condition fails:

- PNG count differs from `section.page` count.
- Any PNG is not 3:4.
- PDF page order or count differs from PNGs.
- A local image is missing.
- Text is clipped, too small for a mobile feed, or duplicated accidentally.
- Canonical terminology differs between the cover, cards, caption, hook, or source text.
- The cover title is wrong.
- The first card lacks `cover-page`, a non-empty `h1`, or the image/text-only structure required by `work/cover-brief.md`.
- The cover conflicts with explicit leader requirements, uses the bundled default despite a supplied direction, or makes the title visually secondary without an approved reason.
- Any body card lacks `content-page`, lacks a non-empty `h2`, or contains an image, diagram, table, dashboard, or other complex visual element.
- The last card lacks `paper-page`, a concise Chinese `h2`, or exactly one faithful anchor-paper first-page screenshot.
- The final evidence card contains extra imagery or enough text to compete with the paper screenshot.
- The paper result cannot support the article's key claim.
- `comment-hook.md` is missing or contains more than one final hook.

The automatic validator enforces structural card roles and machine-checkable requirements. Complete cover-brief fidelity, visual integration, whitespace balance, simplicity, legibility, and evidence checks manually with a contact sheet plus full-size inspection of the first, second, longest, and final cards.
