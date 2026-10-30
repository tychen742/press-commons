#!/usr/bin/env python3
"""Copy ThinkPress Commons pages into a book, or build the commons site.

A book lists the pages it uses in `commons.yml` at its root:

    target_dir: chapters/appendices        # where synced pages go
    figures_dir: figures/commons           # where their images go
    vars:
      book_title: Think AI Systems
      book_folder: ais
      python_version: "3.13"
    pages:
      - page: python-installation          # pages/python-installation.md (or .ipynb)
        file: development_setup/python_installation.md   # relative to target_dir; same extension as the page
        intro: |                           # optional book-specific note
          Labs run in the browser; install Python only to work locally.
        slots:                             # optional customization of marked places in the page
          examples: "Text appended to the page's default."     # a string appends
          install:
            mode: replace                  # or append (the default)
            file: authoring/python_install.md   # text from a file, relative to the book root

Usage:
    python sync.py BOOK_DIR            # sync pages into a book
    python sync.py BOOK_DIR --check    # report pages that are out of date
    python sync.py --site              # write the standalone site into site/

Synced pages carry a marker comment; edit the page here, never the copy.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
PAGES = ROOT / "pages"
FIGURES = ROOT / "figures"
MARKER = "<!-- Synced from press-commons/pages/{page}{ext}. Do not edit here: edit the commons page and run sync.py. -->"
PLACEHOLDER = re.compile(r"\{\{\s*([a-z_]+)\s*\}\}")
FIGURE_REF = re.compile(r"(?<![\w/.-])figures/([\w.-]+\.(?:png|jpg|jpeg|gif|svg))")
SLOT = re.compile(r"<!-- slot: ([a-z0-9_]+) -->(.*?)<!-- /slot: \1 -->", re.DOTALL)
DOC_REF = re.compile(r"\{doc\}`(?:([^`<]*?)\s*<)?([a-z0-9_-]+)>?`")
SITE_VARS = {"book_title": "your ThinkPress book", "book_folder": "mycourse", "python_version": "3.13"}


def page_file(page: str) -> Path:
    """Return the source file of a commons page: Markdown or a Jupyter notebook."""
    for ext in (".md", ".ipynb"):
        if (PAGES / f"{page}{ext}").exists():
            return PAGES / f"{page}{ext}"
    raise SystemExit(f"{page}: no page in {PAGES.relative_to(ROOT)}/ (.md or .ipynb)")


def page_exists(page: str) -> bool:
    return any((PAGES / f"{page}{ext}").exists() for ext in (".md", ".ipynb"))


def read_cells(path: Path) -> list[dict] | None:
    """Return a notebook's cells, or None for a Markdown page."""
    return json.loads(path.read_text())["cells"] if path.suffix == ".ipynb" else None


def page_title(page: str) -> str:
    path = page_file(page)
    cells = read_cells(path)
    texts = ["".join(c["source"]) for c in cells if c["cell_type"] == "markdown"] if cells else [path.read_text()]
    for text in texts:
        for line in text.splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    return page


def add_marker(text: str, page: str, ext: str, intro: str | None) -> str | None:
    """Insert the marker (and intro) after the H1 of `text`, or return None if it has no H1."""
    lines = text.splitlines()
    h1 = next((i for i, line in enumerate(lines) if line.startswith("# ")), None)
    if h1 is None:
        return None
    insert = ["", MARKER.format(page=page, ext=ext)]
    if intro:
        insert += ["", intro.strip()]
    lines[h1 + 1:h1 + 1] = insert
    return "\n".join(lines)


def render(page: str, variables: dict, figure_prefix: str, intro: str | None = None,
           links: dict | None = None, slots: dict | None = None) -> tuple[str, set[str]]:
    """Return the page text with placeholders filled, figure and page links rewritten, and the marker added.

    `links` maps commons page names to doc paths in the target (relative to this page).
    Links to commons pages the target does not include become plain text: the commons
    site is for staff (not students or the public), so readers cannot follow them.
    A notebook page is returned as notebook JSON, with the changes made in its Markdown cells.

    A page marks places a book may customize with `<!-- slot: name -->default<!-- /slot: name -->`.
    `slots` maps a slot name to {"mode": "append" | "replace", "text": ...}; slot markers are
    always removed from the output, and a slot the page does not define is an error.
    """
    path = page_file(page)
    cells = read_cells(path)
    figures: set[str] = set()
    slots = slots or {}
    seen: set[str] = set()

    def fill_slot(m):
        name, default = m.group(1), m.group(2)
        seen.add(name)
        slot = slots.get(name)
        if slot is None:
            return default
        if slot["mode"] == "replace":
            return slot["text"]
        return default.rstrip("\n") + "\n" + slot["text"]

    def transform(src: str) -> str:
        missing = sorted({m.group(1) for m in PLACEHOLDER.finditer(src)} - set(variables))
        if missing:
            raise SystemExit(f"{page}: no value for placeholder(s) {', '.join(missing)} in vars")
        text = PLACEHOLDER.sub(lambda m: str(variables[m.group(1)]), src)

        if links is not None:
            def relink(m):
                label, target = m.group(1), m.group(2)
                if not page_exists(target):
                    return m.group(0)
                if target in links:
                    return f"{{doc}}`{label} <{links[target]}>`" if label else f"{{doc}}`{links[target]}`"
                # Students cannot open the commons site, so readers get the title as plain text.
                return f"*{label or page_title(target)}*"
            text = DOC_REF.sub(relink, text)

        figures.update(FIGURE_REF.findall(text))
        text = FIGURE_REF.sub(lambda m: f"{figure_prefix}{m.group(1)}", text)
        # Slots are filled last: the book's own text is not rewritten as commons text.
        return SLOT.sub(fill_slot, text)

    def check_slots() -> None:
        unknown = sorted(set(slots) - seen)
        if unknown:
            raise SystemExit(f"{page}: no slot named {', '.join(unknown)} in the commons page")

    if cells is None:
        marked = add_marker(transform(path.read_text()), page, path.suffix, intro)
        if marked is None:
            raise SystemExit(f"{page}: page has no H1")
        check_slots()
        return marked.rstrip() + "\n", figures

    nb = json.loads(path.read_text())
    marked_h1 = False
    for cell in nb["cells"]:
        if cell["cell_type"] != "markdown":
            continue
        text = transform("".join(cell["source"]))
        if not marked_h1:
            with_marker = add_marker(text, page, path.suffix, intro)
            if with_marker is not None:
                text, marked_h1 = with_marker, True
        cell["source"] = text.splitlines(keepends=True)
    if not marked_h1:
        raise SystemExit(f"{page}: page has no H1")
    check_slots()
    return json.dumps(nb, indent=1, ensure_ascii=False) + "\n", figures


def load_slots(entry: dict, book: Path) -> dict:
    """Read a page entry's `slots` from commons.yml: a string appends; a mapping sets mode, text or file."""
    slots = {}
    for name, spec in (entry.get("slots") or {}).items():
        if isinstance(spec, str):
            spec = {"text": spec}
        mode = spec.get("mode", "append")
        if mode not in ("append", "replace"):
            raise SystemExit(f"{entry['page']}: slot {name} mode must be append or replace")
        if ("text" in spec) == ("file" in spec):
            raise SystemExit(f"{entry['page']}: slot {name} needs exactly one of text or file")
        text = spec["text"] if "text" in spec else (book / spec["file"]).read_text()
        slots[name] = {"mode": mode, "text": text.rstrip("\n")}
    return slots


def sync_book(book: Path, check: bool) -> int:
    cfg_file = book / "commons.yml"
    if not cfg_file.exists():
        raise SystemExit(f"{cfg_file} not found")
    cfg = yaml.safe_load(cfg_file.read_text())
    target = book / cfg.get("target_dir", "chapters/appendices")
    fig_dir = book / cfg.get("figures_dir", "figures/commons")
    variables = cfg.get("vars", {})
    outputs = {e["page"]: target / e["file"] for e in cfg["pages"]}
    stale = 0
    for entry in cfg["pages"]:
        out = outputs[entry["page"]]
        if out.suffix != page_file(entry["page"]).suffix:
            raise SystemExit(f"{entry['page']}: book file {entry['file']} must end in {page_file(entry['page']).suffix}")
        prefix = os.path.relpath(fig_dir, out.parent).replace(os.sep, "/") + "/"
        links = {p: os.path.splitext(os.path.relpath(o, out.parent))[0].replace(os.sep, "/") for p, o in outputs.items()}
        text, figures = render(entry["page"], variables, prefix, entry.get("intro"), links,
                              load_slots(entry, book))
        current = out.read_text() if out.exists() else None
        old_figures = [n for n in sorted(figures)
                       if not (fig_dir / n).exists() or (fig_dir / n).read_bytes() != (FIGURES / n).read_bytes()]
        if current == text and not old_figures:
            continue
        stale += 1
        if check:
            print(f"out of date: {out.relative_to(book)}" + (f" (figures: {', '.join(old_figures)})" if old_figures else ""))
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        if current != text:
            out.write_text(text)
        for name in old_figures:
            fig_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(FIGURES / name, fig_dir / name)
        print(f"synced: {entry['page']} -> {out.relative_to(book)}" + (f" (figures: {', '.join(old_figures)})" if old_figures else ""))
    if not stale:
        print("all commons pages up to date")
    return 1 if (check and stale) else 0


def build_site() -> int:
    """Write the standalone site (site/) from the pages with neutral values."""
    site = ROOT / "site"
    pages_out = site / "pages"
    if pages_out.exists():
        shutil.rmtree(pages_out)
    pages_out.mkdir(parents=True)
    names = sorted(p.stem for p in PAGES.iterdir() if p.suffix in (".md", ".ipynb"))
    for name in names:
        text, figures = render(name, SITE_VARS, "../figures/")
        (pages_out / page_file(name).name).write_text(text)
    if (site / "figures").exists():
        shutil.rmtree(site / "figures")
    shutil.copytree(FIGURES, site / "figures", ignore=shutil.ignore_patterns(".gitkeep"))
    print(f"site: {len(names)} pages in {site.relative_to(ROOT)}/pages")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("book", nargs="?", type=Path)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--site", action="store_true")
    args = ap.parse_args()
    if args.site:
        return build_site()
    if not args.book:
        ap.error("give a book directory, or --site")
    return sync_book(args.book.resolve(), args.check)


if __name__ == "__main__":
    sys.exit(main())
