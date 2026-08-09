#!/usr/bin/env python3
"""Strip WordPress-import artifacts from post frontmatter. Body untouched."""
import re, pathlib, sys, yaml

POSTS = sorted(pathlib.Path("_posts").iterdir())
KEEP = ("layout", "title", "date", "categories", "tags")

# WordPress exports tag excerpt as `!ruby/object:Hpricot::Doc`; Psych 4/safe_load
# rejects unknown tags, so neutralize them (these keys are dropped anyway).
class _WP_Loader(yaml.SafeLoader):
    pass

def _drop_unknown(loader, tag_suffix, node):
    return None

_WP_Loader.add_multi_constructor("!", _drop_unknown)

for f in POSTS:
    raw = f.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\n(.*?)\n---\n", raw, re.S)
    if not m:
        print(f"SKIP (no frontmatter): {f.name}"); continue
    fm = yaml.load(m.group(1), Loader=_WP_Loader)
    body = raw[m.end():]
    clean = {k: fm[k] for k in KEEP if k in fm}
    if "layout" not in clean:
        clean["layout"] = "post"
    if "title" not in clean:
        print(f"WARN no title: {f.name}"); continue
    if "date" not in clean:
        mm = re.match(r"(\d{4}-\d{2}-\d{2})", f.name)
        if mm: clean["date"] = mm.group(1)
        else: print(f"WARN no date: {f.name}"); continue
    cats = clean.get("categories") or []
    tags = clean.get("tags") or []
    clean["categories"] = [cats] if isinstance(cats, str) else list(cats)
    clean["tags"] = [tags] if isinstance(tags, str) else list(tags)
    out = "---\n" + yaml.safe_dump(clean, sort_keys=False, allow_unicode=True).rstrip() + "\n---\n" + body
    f.write_text(out, encoding="utf-8")
    print(f"OK: {f.name} → {clean['date']} | {clean['title'][:50]}")
print("Done.")
