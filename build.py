"""
Static site builder for Second Growth.
Reads the Markdown content under articles/, converts it to HTML,
rewrites internal links, and writes a deployable static site to site/.

No framework, no build system beyond this script and the `markdown` package
(pip install markdown) — deliberately simple so it's easy to maintain by hand.
Run: python build.py
"""

import re
import shutil
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
SITE = ROOT / "site"
SITE_NAME = "Second Growth"
SITE_TAGLINE = "Documenting what happens to a place's people and economy when the single industry that organized it exits."

# source markdown path (relative to ROOT) -> output path (relative to SITE, root-relative URL)
PAGES = [
    ("articles/home.md", "index.html"),
    ("articles/the-index.md", "the-index.html"),
    ("articles/case-studies.md", "case-studies.html"),
    ("articles/methodology.md", "methodology.html"),
    ("articles/data.md", "data.html"),
    ("articles/about.md", "about.html"),
]

# basename of source .md file -> root-relative output URL, for link rewriting
LINK_MAP = {Path(src).name: "/" + out for src, out in PAGES}

NAV = [
    ("/", "Home"),
    ("/the-index.html", "The Index"),
    ("/case-studies.html", "Case Studies"),
    ("/methodology.html", "Methodology"),
    ("/data.html", "Data"),
    ("/about.html", "About"),
]

MD_LINK_RE = re.compile(r"\]\(([^)]+)\)")


def rewrite_links(md_text: str) -> str:
    def repl(match: re.Match) -> str:
        href = match.group(1)
        if href.startswith(("http://", "https://", "mailto:")):
            return match.group(0)
        basename = href.split("/")[-1]
        if basename in LINK_MAP:
            return "](" + LINK_MAP[basename] + ")"
        return match.group(0)

    return MD_LINK_RE.sub(repl, md_text)


def page_title(html_body: str, fallback: str) -> str:
    match = re.search(r"<h1[^>]*>(.*?)</h1>", html_body, re.S)
    if match:
        return re.sub("<[^>]+>", "", match.group(1)).strip()
    return fallback


def render_page(title: str, body_html: str, out_path: Path) -> str:
    nav_links = "\n".join(
        f'      <a href="{href}">{label}</a>' for href, label in NAV
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — {SITE_NAME}</title>
<meta name="description" content="{SITE_TAGLINE}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/">{SITE_NAME}</a>
    <nav>
{nav_links}
    </nav>
  </div>
</header>
<main class="wrap content">
{body_html}
</main>
<footer class="site-footer">
  <div class="wrap">
    <p>{SITE_NAME} &middot; <a href="/about.html">About</a></p>
  </div>
</footer>
</body>
</html>
"""


def main() -> None:
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)

    md = markdown.Markdown(extensions=["tables", "sane_lists"])

    for src_rel, out_rel in PAGES:
        src_path = ROOT / src_rel
        out_path = SITE / out_rel
        out_path.parent.mkdir(parents=True, exist_ok=True)

        raw = src_path.read_text(encoding="utf-8")
        raw = rewrite_links(raw)
        md.reset()
        body_html = md.convert(raw)
        title = page_title(body_html, fallback=out_rel)
        display_title = "Home" if title == SITE_NAME else title
        out_path.write_text(render_page(display_title, body_html, out_path), encoding="utf-8")
        print(f"built {out_rel}")

    # Assets
    shutil.copytree(ROOT / "assets", SITE / "assets", dirs_exist_ok=True)
    print("copied assets/ (style.css)")

    # No CNAME: no domain has been registered yet.

    print(f"\nSite built at {SITE}")


if __name__ == "__main__":
    main()
