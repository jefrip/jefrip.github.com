# Design: Migrate Jefri's Blog from GitHub Pages to Cloudflare Pages

**Date:** 2026-08-09
**Status:** Approved
**Repo:** `jefrip/jefrip.github.com`
**Domain:** `jefri-p.com` (Dynadot, registered until 2027-06-26)

## 1. Goal & Motivation

The blog (`jefri-p.com`, hosted on GitHub Pages) is currently **down** — the domain's
A record points at `185.53.179.128` which returns HTTP 410. The user wants the blog
back online, hosted on Cloudflare, with a **modernized theme** while preserving all
existing content and URLs.

## 2. Current State (as explored)

- Jekyll **3.8.5** + Jekyll-Bootstrap **0.3.0** era layout/theme
- **29 posts** (2011–2026), permalink format `/:year/:month/:title`
- Custom domain `jefri-p.com` (CNAME file in repo)
- Plugins: `jekyll-paginate`, `jekyll-sitemap`, `jekyll-github-metadata`
- Local plugin `_plugins/debug.rb` (dev-only debug filter)
- Disqus comments (shortname `jefri`) — **to be dropped**
- Google Analytics UA-27115677-1 — **dead** (Universal Analytics retired 2023)
- Lunr client-side search (`search.json` + jQuery) — **kept**, replaced by Chirpy search
- Google site verification file `google1b89562a4ceeb854.html`
- WordPress-import artifacts in post frontmatter (`!ruby/object:Hpricot::Doc`,
  `meta:`, `status: publish`, `type: post`, `_edit_last`, etc.)

## 3. Approach (approved: Option A — modernized)

**Keep Jekyll, upgrade 3.8 → 4.x, adopt the Chirpy theme, host on Cloudflare Pages.**

Rationale: content is Jekyll-native (lowest migration risk), Cloudflare Pages has
first-class Jekyll build support, URLs preserved trivially, free CDN/SSL/analytics.

## 4. Target Architecture

```
GitHub repo (jefrip/jefrip.github.com)  ← source of truth, unchanged
        │ git push
        ▼
Cloudflare Pages (free tier)            ← builds Jekyll 4.x, hosts _site/
        │ custom domain
        ▼
jefri-p.com → Cloudflare DNS + CDN + SSL + Web Analytics
```

### Components

| Component | Decision |
|---|---|
| Build | Cloudflare Pages connected to GitHub repo; `jekyll build`; output `_site/`; auto-deploy on push; instant rollback |
| Hosting | Cloudflare Pages free tier (unlimited bandwidth) |
| DNS | Nameservers at Dynadot → Cloudflare's (required for apex CNAME); dead A record replaced |
| Analytics | Cloudflare Web Analytics (free, cookieless) replaces dead UA |
| Comments | Disqus removed entirely |
| Search | Chirpy built-in search (client-side, from search.json) |
| URLs | Preserved exactly: `/:year/:month/:title` via Chirpy permalink config |
| Theme | **Chirpy** (Jekyll 4.x compatible, dark/light mode, tags/categories, search) |

### Removals

- `CNAME` file (Cloudflare Pages manages the domain natively)
- `_plugins/debug.rb` (dev-only)
- `jekyll-github-metadata` plugin (requires GitHub API at build time)
- Rakefile JB-era helpers (replaced by Cloudflare Pages build config)
- Disqus embed + config
- Google Analytics UA snippet

### Kept

- All 29 post files + content
- `_data/` (authors.yml, categories.yml, tags.yml)
- `atom.xml`, `rss.xml`, `sitemap.txt`, `404.html`
- Google site verification file (harmless, keep)

## 5. Content Migration & Cleanup

### Frontmatter normalization

WordPress-import artifacts break modern Jekyll builds (Psych 4 rejects
`!ruby/object:` YAML tags). Each post's frontmatter is normalized to:

```yaml
---
layout: post
title: "..."
date: 2013-12-09 03:31:15 +0700
categories: [staffblogui, php]
tags: [kohana]
---
```

Dropped fields: `status`, `type`, `published`, `meta:`, `_edit_last`, `excerpt`
(with ruby-object tags), `author.login`.

### Verification gate

- Every URL from the old `sitemap.txt` must render with identical content
- Compare against a local `jekyll build` of the current repo before go-live
- Charset/encoding quirks in 2011–2012 posts checked explicitly

## 6. Build Pipeline & Deployment

### Repo restructure (one-time, in implementation)

```
_config.yml        → Chirpy config (url: https://jefri-p.com, permalinks, pagination)
Gemfile            → jekyll 4.x, chirpy, jekyll-sitemap, jekyll-paginate, webrick
_posts/            → 29 normalized posts
_data/             → kept
_pages/, layouts   → rebuilt for Chirpy
assets/            → theme assets + existing images
CNAME              → deleted
```

### Cloudflare Pages settings

- Framework preset: Jekyll
- Build command: `jekyll build`
- Output directory: `_site/`
- Ruby ≥ 3.1 (Chirpy requirement; Cloudflare's Jekyll preset handles)

## 7. DNS Cutover & Launch

1. **Prereqs (user):** Cloudflare account; Dynadot login
2. **Build & stage (this environment):** restructure, normalize, local build, verify URLs
3. **Connect:** user links GitHub repo → Cloudflare Pages (one-time OAuth); first
   deploy previews at `jefri-p.pages.dev`
4. **Cutover:** add `jefri-p.com` custom domain; point Dynadot nameservers to
   Cloudflare's two NS records; old A record replaced automatically
5. **Launch checks:** https loads w/ valid SSL; http→https redirect; sample old URLs
   return 200 with same content; 404/sitemap/atom/rss reachable; Web Analytics live

### Downtime risk

Effectively zero — site is already down (410); `pages.dev` preview works before DNS
moves; cutover only improves availability.

## 8. Out of Scope (for now)

- Rewriting post content (typos, outdated info)
- Translating posts
- Adding new features beyond theme/search/analytics (newsletter, etc.)
- Moving off the GitHub repo as source of truth
