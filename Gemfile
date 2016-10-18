source "https://rubygems.org"

require 'json'
require 'open-uri'
versions = JSON.parse(open('https://pages.github.com/versions.json').read)
gem 'wdm', '~> 0.1.0' if Gem.win_platform?
gem "jekyll", "~> 3.1"
gem 'github-pages', versions['github-pages']