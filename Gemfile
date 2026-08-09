source "https://rubygems.org"

# Minimal set that lets Cloudflare Pages (github-pages build) run Chirpy via
# remote_theme. The theme gem itself is NOT listed — remote_theme fetches it
# from GitHub at build time, so it must not be in the Gemfile (github-pages
# whitelist rejects it otherwise and `bundle install` fails).
gem "jekyll", "~> 4.3"
gem "jekyll-remote-theme"
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
