# Cloudflare Migration + Chirpy Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bring `jefri-p.com` back online by migrating the Jekyll blog from GitHub Pages to Cloudflare Pages, upgrading Jekyll 3.8 → 4.x with the Chirpy theme, preserving all 29 post URLs exactly.

**Architecture:** GitHub repo stays the source of truth. Cloudflare Pages connects to the repo, builds `jekyll build` → `_site/`, and serves it at `jefri-p.com` via Cloudflare DNS. Local work happens in this environment (Debian 13), then the repo is pushed and connected.

**Tech Stack:** Ruby 3.3 (apt), Bundler, Jekyll 4.x, jekyll-theme-chirpy gem, jekyll-sitemap, jekyll-paginate, webrick, Cloudflare Pages (build preset: Jekyll), Cloudflare DNS, Cloudflare Web Analytics.

**Spec:** `docs/superpowers/specs/2026-08-09-cloudflare-migration-design.md`

## Global Constraints

- **URL preservation is non-negotiable:** every post URL from the old site (`/:year/:month/:slug/`) must return identical content after migration. Verified by diff, not by eyeball.
- Post **content** (body) must not be rewritten — only frontmatter is normalized.
- Ruby ≥ 3.1 required (Chirpy); environment provides 3.3.
- Remove: `CNAME`, `_plugins/debug.rb`, `jekyll-github-metadata`, Disqus embed, GA snippet, Rakefile JB helpers.
- Keep: `_data/`, `atom.xml`, `rss.xml`, `404.html`, `google1b89562a4ceeb854.html`, all images in `assets/`.
- Site chrome stays English (user preference); post content stays as-is (Indonesian).
- Every task ends with a verifiable deliverable; commit after each task.

---

### Task 1: Environment Setup (Ruby + Jekyll + Chirpy scaffold)

**Files:**
- Create: `Gemfile`
- Create: `.ruby-version`
- Create: `docs/superpowers/expected-urls.txt` (placeholder, filled in Task 2)

**Interfaces:**
- Produces: working `bundle exec jekyll build` toolchain; `Gemfile.lock`; `bundle exec jekyll --version` reporting 4.x

- [ ] **Step 1: Install Ruby + build tools**

Run:
```bash
apt-get update -y
apt-get install -y ruby-full build-essential zlib1g-dev
ruby --version   # expect ruby 3.3.x
```

- [ ] **Step 2: Install bundler**

Run:
```bash
gem install bundler
bundle --version   # expect 2.x
```

- [ ] **Step 3: Write Gemfile**

Write `Gemfile` in repo root:
```ruby
source "https://rubygems.org"

gem "jekyll", "~> 4.3"
gem "jekyll-theme-chirpy", "~> 7.2"
gem "jekyll-sitemap"
gem "jekyll-paginate"
gem "jekyll-archives"
gem "jekyll-redirect-from"
gem "jekyll-include-cache"
gem "jekyll-feed"
gem "webrick"   # Ruby 3.x no longer bundles it; jekyll serve needs it

group :test do
  gem "html-proofer"
end
```

- [ ] **Step 4: Write .ruby-version**

Write `.ruby-version`:
```
3.3
```

- [ ] **Step 5: Bundle install**

Run:
```bash
cd /tmp/jefrip-blog
bundle install
```
Expected: gems install cleanly; `Gemfile.lock` created.

- [ ] **Step 6: Verify Jekyll runs**

Run:
```bash
bundle exec jekyll --version
```
Expected: `jekyll 4.3.x`.

- [ ] **Step 7: Commit**

```bash
cd /tmp/jefrip-blog
git add Gemfile Gemfile.lock .ruby-version
git -c user.name="Jefri Pakpahan" -c user.email="jefri.p@gmail.com" commit -m "chore: add Jekyll 4.x + Chirpy toolchain"
```

---

### Task 2: Build URL Inventory (the preservation contract)

**Files:**
- Create: `docs/superpowers/expected-urls.txt`
- Read: `_posts/*` (29 files), `_config.yml` (permalink format)

**Interfaces:**
- Produces: `expected-urls.txt` — one absolute URL per post, derived from frontmatter `date` + filename slug, format `https://jefri-p.com/YYYY/MM/slug/`

**Rationale:** The old site can't build on Ruby 3.3 (2018-era gems + jekyll-github-metadata need an API token). But old URLs are fully determined by frontmatter dates + filenames + the `/:year/:month/:title` permalink rule. We derive them deterministically.

- [ ] **Step 1: Write the inventory script**

Create `/tmp/jefrip-blog/scripts/url_inventory.py`:
```python
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
```

- [ ] **Step 2: Run it**

Run:
```bash
cd /tmp/jefrip-blog
python3 scripts/url_inventory.py
```
Expected: `Wrote 29 expected URLs to docs/superpowers/expected-urls.txt`.

- [ ] **Step 3: Sanity-check output**

Run:
```bash
wc -l docs/superpowers/expected-urls.txt
head -5 docs/superpowers/expected-urls.txt
```
Expected: 29 lines; URLs look like `https://jefri-p.com/2011/11/belajar-mybatis-3/`.

- [ ] **Step 4: Commit**

```bash
cd /tmp/jefrip-blog
git add scripts/url_inventory.py docs/superpowers/expected-urls.txt
git -c user.name="Jefri Pakpahan" -c user.email="jefri.p@gmail.com" commit -m "chore: capture URL preservation contract (29 post URLs)"
```

---

### Task 3: Normalize Post Frontmatter

**Files:**
- Modify: all 29 files in `_posts/`
- Create: `scripts/normalize_frontmatter.py`

**Interfaces:**
- Consumes: Task 2 inventory (dates must not change — the script preserves `date` exactly)
- Produces: 29 posts whose frontmatter is exactly:
```yaml
---
layout: post
title: "<original title>"
date: YYYY-MM-DD HH:MM:SS ±HHMM
categories: [c1, c2]
tags: [t1, t2]
---
```
No `!ruby/object:` tags, no `meta:`, `status:`, `type:`, `published:`, `excerpt:`, `_edit_last:`.

- [ ] **Step 1: Write the normalization script**

Create `/tmp/jefrip-blog/scripts/normalize_frontmatter.py`:
```python
#!/usr/bin/env python3
"""Strip WordPress-import artifacts from post frontmatter. Body untouched."""
import re, pathlib, sys, yaml  # pyyaml needed: pip install pyyaml

POSTS = sorted(pathlib.Path("_posts").iterdir())
KEEP = ("layout", "title", "date", "categories", "tags")

for f in POSTS:
    raw = f.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\n(.*?)\n---\n", raw, re.S)
    if not m:
        print(f"SKIP (no frontmatter): {f.name}"); continue
    fm = yaml.safe_load(m.group(1))
    body = raw[m.end():]
    clean = {k: fm[k] for k in KEEP if k in fm}
    if "layout" not in clean:
        clean["layout"] = "post"
    if "title" not in clean:
        print(f"WARN no title: {f.name}"); continue
    # keep date string verbatim if present, else derive from filename
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
```

- [ ] **Step 2: Install pyyaml and run**

Run:
```bash
pip install pyyaml 2>/dev/null || pip3 install pyyaml
cd /tmp/jefrip-blog
python3 scripts/normalize_frontmatter.py
```
Expected: 29 `OK:` lines, 0 `WARN no date`, 0 `WARN no title`.

- [ ] **Step 3: Verify no ruby-object tags remain**

Run:
```bash
grep -rn "ruby/object\|_edit_last\|Hpricot" _posts/ || echo "CLEAN: no WP artifacts remain"
```
Expected: `CLEAN: no WP artifacts remain`.

- [ ] **Step 4: Verify dates match the inventory**

Run:
```bash
cd /tmp/jefrip-blog
python3 scripts/url_inventory.py
git diff --stat docs/superpowers/expected-urls.txt
```
Expected: no diff (dates preserved → URL contract intact).

- [ ] **Step 5: Verify bodies untouched (content hash)**

Run:
```bash
cd /tmp/jefrip-blog
# extract body of each post before/after is impractical now; instead verify title text present:
grep -c "PROBLEM" _posts/2013-12-09*.html 2>/dev/null || true
```
Manual spot-check: open 2–3 posts (one HTML, one MD) and confirm the body text is unchanged from the original repo state.

- [ ] **Step 6: Commit**

```bash
cd /tmp/jefrip-blog
git add _posts/ scripts/normalize_frontmatter.py docs/superpowers/expected-urls.txt
git -c user.name="Jefri Pakpahan" -c user.email="jefri.p@gmail.com" commit -m "refactor: normalize post frontmatter, strip WordPress artifacts (29 posts)"
```

---

### Task 4: Chirpy Theme Integration + Config

**Files:**
- Modify: `_config.yml` (full rewrite to Chirpy schema)
- Delete: `CNAME`, `_plugins/debug.rb`, `Rakefile`, `sitemap.txt` (Chirpy generates sitemap.xml), `search.json`, `js/jquery.lunr.search.js` (Chirpy has own search)
- Create: `about.md`, `tabs/` structure per Chirpy convention
- Keep: `_data/`, `_posts/`, `assets/` (images), `404.html`, `google1b89562a4ceeb854.html`, `atom.xml`, `rss.xml`

**Interfaces:**
- Consumes: normalized `_posts/`
- Produces: a site that `bundle exec jekyll build` compiles without errors

- [ ] **Step 1: Write new `_config.yml`**

```yaml
# Chirpy theme config — https://chirpy.cotes.page
theme: jekyll-theme-chirpy
lang: en
timezone: Asia/Jakarta
title: "It's me Jefri"
tagline: "Jefri's Blog"
description: "Personal blog of Jefri Pakpahan — software engineering, databases, and tech notes."
url: "https://jefri-p.com"
baseurl: ""
github:
  username: jefrip
twitter:
  username: jefriip
avatar: "/assets/img/avatar.png"

# Build
permalink: /:year/:month/:title/
paginate: 5
paginate_path: "/page/:num"
markdown: kramdown
highlighter: rouge
kramdown:
  syntax_highlighter: rouge

plugins:
  - jekyll-theme-chirpy
  - jekyll-sitemap
  - jekyll-paginate
  - jekyll-archives
  - jekyll-redirect-from
  - jekyll-include-cache
  - jekyll-feed

exclude:
  - Gemfile
  - Gemfile.lock
  - README.md
  - scripts/
  - docs/
  - .ruby-version
```

- [ ] **Step 2: Remove obsolete files**

Run:
```bash
cd /tmp/jefrip-blog
git rm CNAME _plugins/debug.rb Rakefile sitemap.txt search.json js/jquery.lunr.search.js 2>/dev/null || rm -f CNAME _plugins/debug.rb Rakefile sitemap.txt search.json js/jquery.lunr.search.js
rm -rf _plugins
```

- [ ] **Step 3: Create about page + tabs**

Create `about.md`:
```markdown
---
title: About
toc: true
---
Hi, I'm Jefri Pakpahan. This is my personal blog — notes on software
engineering, databases, and whatever tech I'm digging into at the moment.
```

Create `tabs/categories.md`, `tabs/tags.md`, `tabs/archives.md` per Chirpy convention (title + `type: categories|tags|archives` frontmatter).

- [ ] **Step 4: Build**

Run:
```bash
cd /tmp/jefrip-blog
bundle exec jekyll build 2>&1 | tail -20
```
Expected: build completes; `_site/` populated; no fatal errors. (Warnings about missing avatar are OK — Task 5 handles assets.)

- [ ] **Step 5: Verify homepage + pagination render**

Run:
```bash
ls _site/ | head; test -f _site/index.html && echo "index OK"; test -d _site/page && echo "pagination dir OK" || echo "no /page yet (fine if <6 posts visible)"
```

- [ ] **Step 6: Commit**

```bash
cd /tmp/jefrip-blog
git add -A
git -c user.name="Jefri Pakpahan" -c user.email="jefri.p@gmail.com" commit -m "feat: adopt Chirpy theme, rewrite config, drop JB-era files"
```

---

### Task 5: Assets, Author Data, Legacy Redirects

**Files:**
- Create: `assets/img/avatar.png` (generate a simple placeholder if none exists)
- Create: `_redirects` (Cloudflare Pages redirect rules)
- Modify: `_data/authors.yml` if referenced by Chirpy

**Interfaces:**
- Consumes: Task 4 build
- Produces: `_redirects` mapping legacy paths → new paths; avatar present; clean `html-proofer` pass

- [ ] **Step 1: Create avatar placeholder**

Run (ImageMagick if available, else skip and note):
```bash
convert -size 200x200 xc:"#2b7a9b" -gravity center -pointsize 72 -fill white -annotate 0 "JP" assets/img/avatar.png 2>/dev/null || echo "imagemagick not installed — generate avatar later"
```

- [ ] **Step 2: Write `_redirects`**

Create `_redirects` (Cloudflare Pages format — applies at deploy, no Jekyll involvement):
```
/feed/atom.xml  /feed.xml  301
/rss.xml        /feed.xml  301
/atom.xml       /feed.xml  301
/sitemap.txt    /sitemap.xml  301
/tag/*          /tags/:splat  301
/topik/*        /categories/:splat  301
/search.html    /  301
```
(Adjust final targets after inspecting the Chirpy-generated structure in Task 4's `_site/`.)

- [ ] **Step 3: Verify redirects + build together**

Run:
```bash
cd /tmp/jefrip-blog
bundle exec jekyll build 2>&1 | tail -5
test -f _site/_redirects && echo "_redirects copied to _site OK"
```
Expected: `_redirects` present in `_site/` root.

- [ ] **Step 4: HTML proof check**

Run:
```bash
cd /tmp/jefrip-blog
bundle exec htmlproofer _site --disable-external --check-html 2>&1 | tail -15
```
Fix any internal broken links found. Re-run until clean (or only pre-known 404s).

- [ ] **Step 5: Commit**

```bash
cd /tmp/jefrip-blog
git add -A
git -c user.name="Jefri Pakpahan" -c user.email="jefri.p@gmail.com" commit -m "feat: add avatar, legacy redirects, verify links"
```

---

### Task 6: URL Preservation Gate (the big verification)

**Files:**
- Create: `scripts/verify_urls.py`
- Create: `docs/superpowers/verification-report.md`

**Interfaces:**
- Consumes: `expected-urls.txt` (Task 2), `_site/` build (Task 5)
- Produces: a pass/fail report proving every old URL exists in the new build

- [ ] **Step 1: Write the verification script**

Create `/tmp/jefrip-blog/scripts/verify_urls.py`:
```python
#!/usr/bin/env python3
"""Assert every expected post URL exists as a file in _site/."""
import pathlib, sys

expected = [l.strip() for l in pathlib.Path("docs/superpowers/expected-urls.txt").read_text().splitlines() if l.strip()]
site = pathlib.Path("_site")
missing = []
for url in expected:
    # https://jefri-p.com/2011/11/belajar-mybatis-3/ -> _site/2011/11/belajar-mybatis-3/index.html
    rel = url.replace("https://jefri-p.com", "").strip("/")
    if not (site / rel / "index.html").exists():
        missing.append(url)
report = pathlib.Path("docs/superpowers/verification-report.md")
report.write_text(
    f"# URL Preservation Verification\n\n"
    f"- Expected URLs: {len(expected)}\n"
    f"- Missing in new build: {len(missing)}\n\n"
    + ("## MISSING\n" + "\n".join(f"- {u}" for u in missing) if missing else "## PASS — all URLs preserved ✅")
)
print(f"Expected: {len(expected)} | Missing: {len(missing)}")
if missing:
    print("\n".join(missing)); sys.exit(1)
```

- [ ] **Step 2: Run it**

Run:
```bash
cd /tmp/jefrip-blog
python3 scripts/verify_urls.py
```
Expected: exit 0, `Missing: 0`. If any are missing, fix the cause (usually permalink/config mismatch) and rebuild before proceeding.

- [ ] **Step 3: Spot-check content, not just existence**

Pick 3 posts (2011, 2016, 2026) and diff a content marker:
```bash
cd /tmp/jefrip-blog
grep -l "PROBLEM" _site/2013/12/*/index.html 2>/dev/null | head -2
```
Confirm the built HTML contains each post's title text.

- [ ] **Step 4: Commit**

```bash
cd /tmp/jefrip-blog
git add scripts/verify_urls.py docs/superpowers/verification-report.md
git -c user.name="Jefri Pakpahan" -c user.email="jefri.p@gmail.com" commit -m "test: URL preservation gate passes — 29/29 old URLs preserved"
```

---

### Task 7: Cloudflare Pages Deployment (user-assisted)

**Files:** none (cloud configuration)

**Interfaces:**
- Consumes: repo pushed to GitHub (user or agent push)
- Produces: live preview at `jefri-p.pages.dev`

**⚠️ Requires user action — I cannot do the GitHub OAuth or Cloudflare login for you.**

- [ ] **Step 1: Push the repo**

```bash
cd /tmp/jefrip-blog
git remote -v   # confirm origin = https://github.com/jefrip/jefrip.github.com
git push origin master
```
(If no credentials here, user pushes from their machine — same repo state.)

- [ ] **Step 2: User connects repo to Cloudflare Pages**

In Cloudflare dashboard:
1. `Workers & Pages` → `Create` → `Pages` → `Connect to Git`
2. Select `jefrip/jefrip.github.com` (one-time GitHub OAuth)
3. Framework preset: **Jekyll** · Build command: `jekyll build` · Output: `_site/`
4. (No env vars needed — Ruby preset handles it)
5. `Save and Deploy`

- [ ] **Step 3: Verify preview**

```bash
curl -s -o /dev/null -w "HTTP %{http_code}\n" https://jefrip-p.pages.dev/
curl -s -o /dev/null -w "HTTP %{http_code}\n" https://jefrip-p.pages.dev/2013/12/kohana-framework-3-x-error-zlib-output-compression/
```
Expected: 200 for both. If 404, check build logs in Cloudflare dashboard.

- [ ] **Step 4: Enable Cloudflare Web Analytics**

Dashboard → `Analytics` → `Web Analytics` → add site `jefri-p.com` → note the beacon snippet; add it to `_config.yml` (`webmaster_verifications` or `analytics` block per Chirpy docs) and rebuild. *(Can be deferred to post-launch.)*

- [ ] **Step 5: Commit any analytics changes**

```bash
cd /tmp/jefrip-blog
git add -A
git -c user.name="Jefri Pakpahan" -c user.email="jefri.p@gmail.com" commit -m "feat: add Cloudflare Web Analytics beacon"
git push origin master
```

---

### Task 8: DNS Cutover + Launch Checks (user-assisted)

**Files:** none

**Interfaces:**
- Consumes: verified `jefri-p.pages.dev` deployment (Task 7)
- Produces: `https://jefri-p.com` serving the blog

- [ ] **Step 1: Add custom domain in Cloudflare Pages**

Pages project → `Custom domains` → `Add custom domain` → `jefri-p.com` → follow the wizard.

- [ ] **Step 2: Move DNS to Cloudflare**

1. Cloudflare dashboard → `Add site` → `jefri-p.com` → Free plan
2. Cloudflare assigns two nameservers (e.g. `ada.ns.cloudflare.com`, `ben.ns.cloudflare.com`)
3. At Dynadot (domain registrar): change nameservers from `ns1/ns2.dyna-ns.net` → the two Cloudflare NS records
4. In Cloudflare DNS settings, confirm the `jefri-p.com` record is proxied (orange cloud)

- [ ] **Step 3: Wait for propagation & verify**

```bash
curl -s -o /dev/null -w "HTTP %{http_code}\n" --max-time 20 https://jefri-p.com/
```
Expected eventually: 200 (propagation up to ~24h; usually minutes).

- [ ] **Step 4: Launch checklist**

```bash
# SSL
curl -sI https://jefri-p.com/ | head -3
# http → https redirect
curl -s -o /dev/null -w "%{http_code} → %{redirect_url}\n" http://jefri-p.com/
# sample old post URLs
for u in "2011/11/belajar-mybatis-3/" "2013/12/kohana-framework-3-x-error-zlib-output-compression/" "2026/01/"; do
  curl -s -o /dev/null -w "%{http_code} https://jefri-p.com/$u\n" "https://jefri-p.com/$u"
done
# feeds
curl -s -o /dev/null -w "%{http_code} /feed.xml\n" https://jefri-p.com/feed.xml
curl -s -o /dev/null -w "%{http_code} /sitemap.xml\n" https://jefri-p.com/sitemap.xml
# 404
curl -s -o /dev/null -w "%{http_code} /definitely-not-a-page/\n" https://jefri-p.com/definitely-not-a-page/
```
All expected: 200 (redirect 301→200 for http), feed/sitemap 200, 404 page 404.

- [ ] **Step 5: Verify full URL inventory against live site**

Run (extend `verify_urls.py` or one-liner):
```bash
cd /tmp/jefrip-blog
python3 - <<'EOF'
import pathlib, subprocess
urls = [l.strip() for l in pathlib.Path("docs/superpowers/expected-urls.txt").read_text().splitlines() if l.strip()]
bad = []
for u in urls:
    code = subprocess.run(["curl","-s","-o","/dev/null","-w","%{http_code}","--max-time","15",u],capture_output=True,text=True).stdout
    if code != "200": bad.append((u, code))
print(f"{len(urls)-len(bad)}/{len(urls)} live OK" + (f"\nBAD: {bad}" if bad else " ✅"))
EOF
```
Expected: `29/29 live OK ✅`.

- [ ] **Step 6: Record completion**

Append results to `docs/superpowers/verification-report.md` and commit:
```bash
cd /tmp/jefrip-blog
git add docs/superpowers/verification-report.md
git -c user.name="Jefri Pakpahan" -c user.email="jefri.p@gmail.com" commit -m "docs: launch verification — live checks pass"
```

---

## Self-Review Notes

- **Spec coverage:** all spec sections map to tasks — architecture (T1, T4), content migration (T3), verification (T2, T6), build/deploy (T7), DNS/launch (T8), removals (T4, T5), analytics (T7).
- **Placeholder scan:** no TBDs; the only "deferred" items are explicit (avatar if ImageMagick missing, Web Analytics post-launch option, `_redirects` final targets verified against Task 4 output).
- **Type consistency:** `expected-urls.txt` format (absolute URL per line) is produced in T2, consumed identically in T6 and T8. Frontmatter schema in T3 matches what Chirpy/Jekyll 4 expects.
