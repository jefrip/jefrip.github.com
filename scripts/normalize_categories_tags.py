#!/usr/bin/env python3
"""Fix jekyll-archives slug collisions: lowercase + dedupe categories/tags.

jekyll-archives slugifies category/tag names, so case-variant values such as
'Kohana' and 'kohana' both map to /categories/kohana/ and collide. This script
lowercases every category/tag value and dedupes within each post, rewriting
ONLY the `categories:`/`tags:` blocks of the frontmatter — every other line
(layout, title, date, ...) and the whole body stay byte-identical.

Post URLs (permalink /:year/:month/:title/) are unaffected.
"""
import collections
import pathlib
import re
import sys

import yaml

POSTS = sorted(pathlib.Path("_posts").iterdir())
FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)
PLAIN = re.compile(r"^[A-Za-z0-9._+-]+$")


def slug(s: str) -> str:
    return s.strip().lower()


def split(raw: str):
    m = FM_RE.match(raw)
    if not m:
        return None, None, None
    return m.group(1), m.end(), yaml.safe_load(m.group(1))


def render_scalar(v: str) -> str:
    return v if PLAIN.match(v) else yaml.safe_dump(v).strip()


def main() -> int:
    before = collections.defaultdict(list)   # slug -> [(post, key, raw)]
    after = collections.defaultdict(list)    # slug -> [(post, key, value)]
    changed = []

    for f in POSTS:
        raw = f.read_text(encoding="utf-8")
        block, body_start, fm = split(raw)
        if block is None:
            print(f"SKIP (no frontmatter): {f.name}")
            continue

        new_values = {}
        for key in ("categories", "tags"):
            vals = fm.get(key) or []
            if isinstance(vals, str):
                vals = [vals]
            for v in vals:
                before[slug(v)].append((f.name, key, v))
            seen, norm = set(), []
            for v in vals:
                sv = slug(v)
                if sv not in seen:
                    seen.add(sv)
                    norm.append(sv)
            new_values[key] = norm

        # Textual rewrite: replace only the categories:/tags: blocks.
        lines = block.split("\n")
        out, i = [], 0
        while i < len(lines):
            line = lines[i]
            key = line.split(":", 1)[0]
            if key in ("categories", "tags") and line.startswith(key + ":"):
                out.append(f"{key}:")
                for v in new_values[key]:
                    out.append(f"- {render_scalar(v)}")
                i += 1
                while i < len(lines) and re.match(r"^\s*- ", lines[i]):
                    i += 1
                continue
            out.append(line)
            i += 1

        new_block = "\n".join(out)
        if new_block != block:
            f.write_text("---\n" + new_block + "\n---\n" + raw[body_start:], encoding="utf-8")
            changed.append(f.name)
            print(f"CHANGED {f.name}: categories={new_values['categories']} tags={new_values['tags']}")
        else:
            print(f"ok      {f.name}")

        # Re-read for the residual-collision scan.
        _, _, fm2 = split(f.read_text(encoding="utf-8"))
        for key in ("categories", "tags"):
            for v in (fm2.get(key) or []):
                after[slug(v)].append((f.name, key, v))

    print("\n=== pre-normalization slug collision map ===")
    n = 0
    for s, entries in sorted(before.items()):
        raws = sorted({e[2] for e in entries})
        if len(raws) > 1:
            print(f"  {s!r} <- {raws}  ({len(entries)} occurrences)")
            n += 1
    if n == 0:
        print("  (none)")

    print("=== residual collision check (post-normalization) ===")
    bad = 0
    for s, entries in sorted(after.items()):
        raws = sorted({e[2] for e in entries})
        if len(raws) > 1:
            print(f"  STILL COLLIDING: {s!r} <- {raws}")
            bad += 1
    print(f"changed {len(changed)} post(s); residual collisions: {bad}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
