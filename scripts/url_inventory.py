#!/usr/bin/env python3
"""Derive expected post URLs from frontmatter date + filename slug."""
import re, sys, pathlib, datetime

POSTS = pathlib.Path("_posts")
OUT = pathlib.Path("docs/superpowers/expected-urls.txt")

def frontmatter_date(text: str) -> datetime.date:
    m = re.search(r"^date:\s*([0-9]{4})-([0-9]{2})-([0-9]{2})", text, re.M)
    if not m:
        raise SystemExit(f"No date in frontmatter of {text[:200]!r}")
    return datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))

def slug_from_filename(name: str) -> str:
    # _posts/2013-12-09-kohana-framework-3-x-error-zlib-output-compression.html
    m = re.match(r"\d{4}-\d{2}-\d{2}-(.+)\.(md|markdown|html)$", name)
    if not m:
        raise SystemExit(f"Unexpected filename: {name}")
    return m.group(1)

urls = []
for f in sorted(POSTS.iterdir()):
    text = f.read_text(encoding="utf-8", errors="replace")
    d = frontmatter_date(text)
    slug = slug_from_filename(f.name)
    urls.append(f"https://jefri-p.com/{d.year:04d}/{d.month:02d}/{slug}/")

OUT.write_text("\n".join(urls) + "\n")
print(f"Wrote {len(urls)} expected URLs to {OUT}")
