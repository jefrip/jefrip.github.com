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
