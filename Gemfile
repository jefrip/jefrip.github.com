# Theme via the local gem (bundled at build time — no GitHub fetch needed,
# which is reliable on Cloudflare Pages where remote_theme can fail).
source "https://rubygems.org"

gem "jekyll", "~> 4.3"
gem "jekyll-theme-chirpy"
gem "jekyll-seo-tag"
gem "jekyll-sitemap"
gem "jekyll-feed"
gem "jekyll-redirect-from"
gem "jekyll-archives"
gem "jekyll-paginate"
gem "jekyll-include-cache"
gem "webrick"   # Ruby 3.x no longer bundles it; jekyll serve needs it

group :test do
  gem "html-proofer"
end
