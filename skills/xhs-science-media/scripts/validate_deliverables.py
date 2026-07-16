#!/usr/bin/env python3
import argparse
import re
import struct
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote


FORBIDDEN_BODY_TAGS = {"img", "picture", "svg", "canvas", "figure", "table"}


def normalized_text(parts) -> str:
    return re.sub(r"\s+", " ", "".join(parts)).strip()


class CardParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pages: list[dict] = []
        self.current: dict | None = None
        self.capture: tuple[str, list[str]] | None = None

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attr_map = {key.lower(): (value or "") for key, value in attrs}
        classes = set(attr_map.get("class", "").split())

        if tag == "section" and "page" in classes:
            self.current = {
                "classes": classes,
                "tags": set(),
                "images": [],
                "h1": [],
                "h2": [],
                "p": [],
            }
            self.pages.append(self.current)
            return

        if self.current is None:
            return

        self.current["tags"].add(tag)
        if tag == "img":
            self.current["images"].append(
                {
                    "src": attr_map.get("src", "").strip(),
                    "alt": attr_map.get("alt", "").strip(),
                    "classes": classes,
                }
            )
        if tag in {"h1", "h2", "p"}:
            self.capture = (tag, [])

    def handle_data(self, data):
        if self.capture is not None:
            self.capture[1].append(data)

    def handle_endtag(self, tag):
        tag = tag.lower()
        if self.capture is not None and self.capture[0] == tag and self.current is not None:
            self.current[tag].append(normalized_text(self.capture[1]))
            self.capture = None
        if tag == "section":
            self.current = None


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as fh:
        signature = fh.read(24)
    if signature[:8] != b"\x89PNG\r\n\x1a\n" or signature[12:16] != b"IHDR":
        raise ValueError(f"Not a valid PNG: {path}")
    return struct.unpack(">II", signature[16:24])


def pdf_page_count(path: Path):
    try:
        from pypdf import PdfReader
    except ImportError:
        return None
    return len(PdfReader(str(path)).pages)


def read_selected_title(path: Path) -> str | None:
    if not path.exists():
        return None
    candidates = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip().strip("#*- ").strip()
        if not line or line.lower() in {"selected title", "title", "已选标题", "选定标题"}:
            continue
        match = re.match(r"^(?:title|标题)\s*[:：]\s*(.+)$", line, flags=re.I)
        candidates.append(match.group(1).strip() if match else line)
    return candidates[0] if candidates else None


def cover_title_is_large(css: str) -> bool:
    for selector, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css, flags=re.S):
        if "h1" not in selector.lower():
            continue
        match = re.search(r"font-size\s*:\s*(\d+(?:\.\d+)?)\s*(cqw|px)\b", body, flags=re.I)
        if not match:
            continue
        value = float(match.group(1))
        unit = match.group(2).lower()
        if (unit == "cqw" and value >= 8) or (unit == "px" and value >= 96):
            return True
    return False


def local_image_errors(root: Path, html_path: Path, pages: list[dict]) -> list[str]:
    errors = []
    for page_number, page in enumerate(pages, start=1):
        for item in page["images"]:
            src = item["src"]
            if not src:
                errors.append(f"Card {page_number} has an image with no src")
                continue
            if re.match(r"^(?:[a-z]+:)?//", src, flags=re.I) or src.startswith("data:"):
                errors.append(f"Card {page_number} image must be a local file: {src}")
                continue
            clean_src = unquote(src.split("?", 1)[0].split("#", 1)[0])
            target = (html_path.parent / clean_src).resolve()
            if not target.is_relative_to(root.resolve()):
                errors.append(f"Card {page_number} image is outside the project: {src}")
            elif not target.is_file():
                errors.append(f"Card {page_number} image is missing: {src}")
    return errors


def validate_card_roles(root: Path, html_path: Path, html: str) -> tuple[list[str], int]:
    errors: list[str] = []
    parser = CardParser()
    parser.feed(html)
    pages = parser.pages
    page_count = len(pages)

    if page_count == 0:
        return ["No section.page cards found"], 0
    if not 7 <= page_count <= 10:
        errors.append(f"Card count {page_count} is outside the required 7-10 range")

    css_path = html_path.parent / "styles.css"
    if not css_path.exists():
        errors.append("Missing web/styles.css")
        css = ""
    else:
        css = css_path.read_text(encoding="utf-8")

    cover = pages[0]
    if "cover-page" not in cover["classes"]:
        errors.append("Card 1 must have class cover-page")
    if len(cover["images"]) != 1:
        errors.append("Card 1 must contain exactly one generated cover image")
    else:
        image = cover["images"][0]
        if "cover-visual" not in image["classes"]:
            errors.append("Card 1 image must have class cover-visual")
        if "cover-visual" not in Path(image["src"]).stem:
            errors.append("Card 1 image file must be the generated cover-visual asset")
    h1_texts = [text for text in cover["h1"] if text]
    if len(h1_texts) != 1:
        errors.append("Card 1 must contain exactly one non-empty h1 title")
    selected_title = read_selected_title(root / "work" / "selected-title.md")
    if selected_title and h1_texts and normalized_text([selected_title]) != normalized_text([h1_texts[0]]):
        errors.append("Card 1 h1 does not match work/selected-title.md")
    if not cover_title_is_large(css):
        errors.append("Cover h1 font-size must be at least 8cqw or 96px")
    if not all(token in css for token in (".cover-visual", ".cover-copy")):
        errors.append("Cover CSS must style both .cover-visual and .cover-copy")
    if not re.search(r"linear-gradient|text-shadow|mix-blend-mode|filter\s*:", css, flags=re.I):
        errors.append("Cover CSS must integrate title and image with contrast treatment")

    for index, page in enumerate(pages[1:-1], start=2):
        if "content-page" not in page["classes"]:
            errors.append(f"Card {index} must have class content-page")
        forbidden = sorted(page["tags"] & FORBIDDEN_BODY_TAGS)
        if forbidden:
            errors.append(f"Card {index} must be text-only; forbidden tags: {', '.join(forbidden)}")
        h2_texts = [text for text in page["h2"] if text]
        if len(h2_texts) != 1:
            errors.append(f"Card {index} must contain exactly one non-empty h2")
        paragraph_count = len([text for text in page["p"] if text])
        if paragraph_count < 1 or paragraph_count > 4:
            errors.append(f"Card {index} must keep text simple: 1-4 short p elements including kicker")

    paper = pages[-1]
    if "paper-page" not in paper["classes"]:
        errors.append(f"Card {page_count} must have class paper-page")
    paper_titles = [text for text in paper["h2"] if text]
    if len(paper_titles) != 1 or not re.search(r"[\u4e00-\u9fff]", paper_titles[0]):
        errors.append(f"Card {page_count} must contain exactly one non-empty Chinese h2")
    if len(paper["images"]) != 1:
        errors.append(f"Card {page_count} must contain exactly one paper screenshot")
    else:
        image = paper["images"][0]
        if "anchor-paper-first-page" not in image["classes"]:
            errors.append(f"Card {page_count} paper image must have class anchor-paper-first-page")
        if "anchor-paper-first-page" not in Path(image["src"]).stem:
            errors.append(f"Card {page_count} must use the anchor-paper-first-page asset")
    if paper["tags"] & {"picture", "svg", "canvas", "table"}:
        errors.append(f"Card {page_count} must remain a simple title-and-paper page")
    if len([text for text in paper["p"] if text]) > 3:
        errors.append(f"Card {page_count} has too much supporting text")

    errors.extend(local_image_errors(root, html_path, pages))
    return errors, page_count


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    html_path = root / "web" / "index.html"
    png_dir = root / "deliverables" / "png"
    pdf_path = root / "deliverables" / "xiaohongshu-cards.pdf"
    hook_path = root / "deliverables" / "comment-hook.md"

    if not html_path.exists():
        return ["Missing web/index.html"]

    html = html_path.read_text(encoding="utf-8")
    if re.search(r"<script\b", html, flags=re.I):
        errors.append("JavaScript is not allowed in the screenshot webpage")
    role_errors, page_count = validate_card_roles(root, html_path, html)
    errors.extend(role_errors)

    pngs = sorted(png_dir.glob("page-*.png")) if png_dir.exists() else []
    if len(pngs) != page_count:
        errors.append(f"PNG count {len(pngs)} does not match card count {page_count}")
    for png in pngs:
        try:
            width, height = png_size(png)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if (width, height) != (1200, 1600):
            errors.append(f"{png.name} is {width}x{height}, not the canonical 1200x1600")

    if not pdf_path.exists():
        errors.append("Missing deliverables/xiaohongshu-cards.pdf")
    else:
        pdf_count = pdf_page_count(pdf_path)
        if pdf_count is not None and pdf_count != page_count:
            errors.append(f"PDF page count {pdf_count} does not match card count {page_count}")

    if not hook_path.exists() or not hook_path.read_text(encoding="utf-8").strip():
        errors.append("Missing or empty deliverables/comment-hook.md")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Xiaohongshu card deliverables")
    parser.add_argument("project_folder", type=Path)
    args = parser.parse_args()
    errors = validate(args.project_folder.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("OK: deliverables match the Xiaohongshu card contract")
    return 0


if __name__ == "__main__":
    sys.exit(main())
