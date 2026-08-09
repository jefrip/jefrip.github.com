#!/usr/bin/env python3
"""Derive expected post URLs from frontmatter date + filename slug."""
import re, sys, pathlib, datetime

POSTS = pathlib.Path("_posts")
OUT = pathlib.Path("docs/superpowers/expected-urls.txt")

def frontmatter_date(block: str, filename: str) -> datetime.date:
    m = re.search(r"^date:\s*([0-9]{4})-([0-9]{2})-([0-9]{2})", block, re.M)
    if not m:
        raise SystemExit(f"No date in frontmatter of {filename}")
    return datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))

def slug_from_filename(name: str) -> str:
    # _posts/2013-12-09-kohana-framework-3-x-error-zlib-output-compression.html
    m = re.match(r"\d{4}-\d{2}-\d{2}-(.+)\.(md|markdown|html)$", name)
    if not m:
        raise SystemExit(f"Unexpected filename: {name}")
    return m.group(1)

urls = []
for f in sorted(POSTS.iterdir()):
    raw = f.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\n(.*?)\n---\n", raw, re.S)
    if not m:
        raise SystemExit(f"No frontmatter block in {f.name}")
    d = frontmatter_date(m.group(1), f.name)
    fname_date = f.name[:10]
    if d.isoformat() != fname_date:
        print(f"WARNING: date mismatch in {f.name}: frontmatter={d.isoformat()} filename={fname_date}")
        raise SystemExit(f"Aborting: frontmatter date {d.isoformat()} does not match filename date {fname_date}")
    slug = slug_from_filename(f.name)
    urls.append(f"https://jefri-p.com/{d.year:04d}/{d.month:02d}/{slug}/")

OUT.write_text("\n".join(urls) + "\n")
print(f"Wrote {len(urls)} expected URLs to {OUT}")
