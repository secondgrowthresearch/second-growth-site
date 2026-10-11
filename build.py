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
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import markdown
from PIL import Image

ROOT = Path(__file__).parent
SITE = ROOT / "site"
SITE_NAME = "Second Growth"
SITE_TAGLINE = "Documenting what happens to a place's people and economy when the single industry that organized it exits."
DOMAIN = "https://secondgrowthresearch.org"
# GoatCounter site code (the subdomain of your dashboard URL, e.g.
# "secondgrowth" for secondgrowth.goatcounter.com) -- no cookies, no
# personal data, so it doesn't need a consent banner. Leave as None until
# an account exists; the analytics script is only emitted when this is set.
GOATCOUNTER_CODE = "secondgrowth"
# Per-page "Published/Last updated" bylines and the Recent Updates page +
# RSS feed are paused -- a very recent-looking last-updated date works
# against the site's credibility right now. Flip back to True (no other
# code changes needed) once enough time has passed; the real git-log
# dates this is built from aren't going anywhere in the meantime.
SHOW_DATES = False

# source markdown path (relative to ROOT) -> output path (relative to SITE, root-relative URL)
PAGES = [
    ("articles/home.md", "index.html"),
    ("articles/the-index.md", "the-index.html"),
    ("articles/case-studies.md", "case-studies.html"),
    ("articles/water-insecurity.md", "water-insecurity.html"),
    ("articles/environmental-impact.md", "environmental-impact.html"),
    ("articles/consolidation.md", "consolidation.html"),
    ("articles/compounding.md", "compounding.html"),
    ("articles/mechanisms.md", "mechanisms.html"),
    ("articles/mechanisms/recharge-basins.md", "mechanisms/recharge-basins.html"),
    ("articles/mechanisms/habitat-restoration.md", "mechanisms/habitat-restoration.html"),
    ("articles/mechanisms/land-repurposing.md", "mechanisms/land-repurposing.html"),
    ("articles/mechanisms/ceqa-leverage.md", "mechanisms/ceqa-leverage.html"),
    ("articles/mechanisms/ratemaking.md", "mechanisms/ratemaking.html"),
    ("articles/case-studies/kings-1993-safeway-hanford.md", "case-studies/kings-1993-safeway-hanford.html"),
    ("articles/case-studies/kings-2020-olam-lemoore.md", "case-studies/kings-2020-olam-lemoore.html"),
    ("articles/case-studies/kings-2023-lacey-milling-hanford.md", "case-studies/kings-2023-lacey-milling-hanford.html"),
    ("articles/case-studies/kings-2024-del-monte-hanford.md", "case-studies/kings-2024-del-monte-hanford.html"),
    ("articles/case-studies/kings-2025-leprino-lemoore.md", "case-studies/kings-2025-leprino-lemoore.html"),
    ("articles/case-studies/tulare-1991-tagus-ranch.md", "case-studies/tulare-1991-tagus-ranch.html"),
    ("articles/case-studies/tulare-1992-kraft-louis-rich-tulare.md", "case-studies/tulare-1992-kraft-louis-rich-tulare.html"),
    ("articles/case-studies/tulare-1992-lindsay-olive-growers-lindsay.md", "case-studies/tulare-1992-lindsay-olive-growers-lindsay.html"),
    ("articles/case-studies/tulare-2010-land-olakes-tulare.md", "case-studies/tulare-2010-land-olakes-tulare.html"),
    ("articles/case-studies/stanislaus-1993-conagra-banquet-turlock.md", "case-studies/stanislaus-1993-conagra-banquet-turlock.html"),
    ("articles/case-studies/stanislaus-2007-hershey-oakdale.md", "case-studies/stanislaus-2007-hershey-oakdale.html"),
    ("articles/case-studies/stanislaus-2012-dawn-foods-modesto.md", "case-studies/stanislaus-2012-dawn-foods-modesto.html"),
    ("articles/case-studies/stanislaus-2012-patterson-vegetable.md", "case-studies/stanislaus-2012-patterson-vegetable.html"),
    ("articles/case-studies/stanislaus-2013-post-foods-modesto.md", "case-studies/stanislaus-2013-post-foods-modesto.html"),
    ("articles/case-studies/stanislaus-2018-seneca-foods-modesto.md", "case-studies/stanislaus-2018-seneca-foods-modesto.html"),
    ("articles/case-studies/fresno-2016-conagra-helm.md", "case-studies/fresno-2016-conagra-helm.html"),
    ("articles/case-studies/fresno-2024-cargill-fresno.md", "case-studies/fresno-2024-cargill-fresno.html"),
    ("articles/case-studies/fresno-2024-ofi-firebaugh.md", "case-studies/fresno-2024-ofi-firebaugh.html"),
    ("articles/case-studies/tulare-2024-ruiz-foods-tulare.md", "case-studies/tulare-2024-ruiz-foods-tulare.html"),
    ("articles/case-studies/tulare-2024-prima-wawona-cutler.md", "case-studies/tulare-2024-prima-wawona-cutler.html"),
    ("articles/case-studies/stanislaus-2024-tropicale-foods-modesto.md", "case-studies/stanislaus-2024-tropicale-foods-modesto.html"),
    ("articles/case-studies/stanislaus-2024-reyes-coca-cola-modesto.md", "case-studies/stanislaus-2024-reyes-coca-cola-modesto.html"),
    ("articles/case-studies/stanislaus-2025-foster-farms-turlock.md", "case-studies/stanislaus-2025-foster-farms-turlock.html"),
    ("articles/case-studies/stanislaus-2025-bronco-wine-ceres.md", "case-studies/stanislaus-2025-bronco-wine-ceres.html"),
    ("articles/case-studies/stanislaus-2026-del-monte-modesto-hughson.md", "case-studies/stanislaus-2026-del-monte-modesto-hughson.html"),
    ("articles/case-studies/kings-kettleman-city.md", "case-studies/kings-kettleman-city.html"),
    ("articles/case-studies/kings-stratford.md", "case-studies/kings-stratford.html"),
    ("articles/case-studies/kings-corcoran.md", "case-studies/kings-corcoran.html"),
    ("articles/case-studies/kings-armona.md", "case-studies/kings-armona.html"),
    ("articles/case-studies/kings-avenal.md", "case-studies/kings-avenal.html"),
    ("articles/case-studies/fresno-lanare.md", "case-studies/fresno-lanare.html"),
    ("articles/case-studies/fresno-cantua-creek.md", "case-studies/fresno-cantua-creek.html"),
    ("articles/case-studies/fresno-shady-lakes-mhp.md", "case-studies/fresno-shady-lakes-mhp.html"),
    ("articles/case-studies/fresno-caruthers.md", "case-studies/fresno-caruthers.html"),
    ("articles/case-studies/tulare-allensworth.md", "case-studies/tulare-allensworth.html"),
    ("articles/case-studies/tulare-east-porterville.md", "case-studies/tulare-east-porterville.html"),
    ("articles/case-studies/tulare-tooleville.md", "case-studies/tulare-tooleville.html"),
    ("articles/case-studies/tulare-earlimart.md", "case-studies/tulare-earlimart.html"),
    ("articles/case-studies/tulare-strathmore.md", "case-studies/tulare-strathmore.html"),
    ("articles/case-studies/tulare-richgrove.md", "case-studies/tulare-richgrove.html"),
    ("articles/case-studies/tulare-plainview.md", "case-studies/tulare-plainview.html"),
    ("articles/case-studies/stanislaus-westley-grayson.md", "case-studies/stanislaus-westley-grayson.html"),
    ("articles/case-studies/stanislaus-keyes.md", "case-studies/stanislaus-keyes.html"),
    ("articles/case-studies/stanislaus-cowan-tract.md", "case-studies/stanislaus-cowan-tract.html"),
    ("articles/case-studies/stanislaus-salida.md", "case-studies/stanislaus-salida.html"),
    ("articles/methodology.md", "methodology.html"),
    ("articles/data.md", "data.html"),
    ("articles/about.md", "about.html"),
]

# basename of source .md file -> root-relative output URL, for link rewriting
LINK_MAP = {Path(src).name: "/" + out for src, out in PAGES}

# Split into two groups -- content/topic pages a reader is actually here
# for, vs. reference pages about how the research itself is done. Same
# nine pages as before; now visually distinguished instead of sitting at
# equal weight (see .nav-group-secondary in style.css).
NAV_PRIMARY = [
    ("/", "Home"),
    ("/the-index.html", "The Index"),
    ("/case-studies.html", "Case Studies"),
    ("/water-insecurity.html", "Water Insecurity"),
    ("/environmental-impact.html", "Environmental Impact"),
    ("/consolidation.html", "Consolidation"),
]
# Compounding Impact and Mechanisms both describe themselves, in their own
# body text, as built from the five pages above rather than as original
# findings in their own right ("adds no single new claim" / "reference
# material, not a recommendation") -- secondary nav is where that
# distinction already lives for every other synthesis/reference page, and
# it's visually de-emphasized there (see .nav-group-secondary in
# style.css), which is the point: it genuinely lightens primary nav rather
# than just relabeling the same weight.
NAV_SECONDARY = [
    ("/methodology.html", "Methodology"),
    ("/data.html", "Data"),
    ("/compounding.html", "Compounding Impact"),
    ("/mechanisms.html", "Mechanisms"),
    ("/about.html", "About"),
]
if SHOW_DATES:
    NAV_SECONDARY.insert(2, ("/updates.html", "Updates"))
NAV = NAV_PRIMARY + NAV_SECONDARY

MD_LINK_RE = re.compile(r"\]\(([^)]+)\)")
# Chart/map source-citation text is written as literal HTML inside JS string
# literals (e.g. layer.source = '...see <a href="methodology.md">...'), not
# as Markdown links -- MD_LINK_RE never sees it, so without this second pass
# every "see Methodology"/"see Data" citation link across the site 404s.
HTML_HREF_RE = re.compile(r'href="([^"]+\.md)"')
# Every photo on the site is hand-authored as <img src="/assets/photos/X.jpg"
# alt="...">, always exactly this shape (checked directly: 8 occurrences,
# none carry extra attributes) -- a single regex safely rewrites all of them.
IMG_TAG_RE = re.compile(r'<img src="(/assets/photos/[^"]+\.jpg)" alt="([^"]*)">')


def rewrite_links(md_text: str) -> str:
    def repl(match: re.Match) -> str:
        href = match.group(1)
        if href.startswith(("http://", "https://", "mailto:")):
            return match.group(0)
        basename = href.split("/")[-1]
        if basename in LINK_MAP:
            return "](" + LINK_MAP[basename] + ")"
        return match.group(0)

    def html_repl(match: re.Match) -> str:
        basename = match.group(1).split("/")[-1]
        if basename in LINK_MAP:
            return 'href="' + LINK_MAP[basename] + '"'
        return match.group(0)

    md_text = HTML_HREF_RE.sub(html_repl, md_text)

    return MD_LINK_RE.sub(repl, md_text)


def analyze_photos() -> dict:
    """basename.jpg -> (width, height), read directly from the source
    files. Rendering needs real pixel dimensions (not guesses) so <img>
    tags can carry explicit width/height and avoid layout shift while the
    image itself is still loading."""
    info = {}
    for path in (ROOT / "assets" / "photos").glob("*.jpg"):
        with Image.open(path) as img:
            info[path.name] = img.size
    return info


def rewrite_images(html: str, photo_info: dict) -> str:
    """<img src=".../X.jpg" alt="..."> -> a <picture> offering a WebP
    source (smaller, generated at build time -- see generate_webp()) with
    the original JPEG as the fallback <img>, now carrying explicit
    width/height and loading="lazy" so offscreen photos don't block the
    rest of the page and don't cause layout shift once they do load."""

    def repl(match: re.Match) -> str:
        src, alt = match.group(1), match.group(2)
        webp_src = src[:-4] + ".webp"
        size = photo_info.get(src.rsplit("/", 1)[-1])
        dims = f' width="{size[0]}" height="{size[1]}"' if size else ""
        return (
            f'<picture><source srcset="{webp_src}" type="image/webp">'
            f'<img src="{src}" alt="{alt}"{dims} loading="lazy" decoding="async"></picture>'
        )

    return IMG_TAG_RE.sub(repl, html)


# Every stat-pair number is authored with a placeholder "0"-style initial
# text (e.g. <p class="stat-number" data-target="11.4" data-decimals="1"
# data-prefix="$" data-suffix="B">$0.0B</p>) -- the client-side count-up
# script (see the inline <script> near the end of render_page's template)
# overwrites it on scroll-into-view. That's fine for a JS-enabled browser,
# but it means the raw HTML -- what a crawler, a text-extraction tool, or
# a browser with JS disabled actually sees -- shows meaningless zeros for
# every headline number on the site. Fixed at build time instead of by
# hand-editing ~100 instances across ~49 files (error-prone, and silently
# drifts out of sync the next time a number changes): compute the correct
# display text directly from each element's own data-target/data-decimals/
# data-prefix/data-suffix using the exact same formatting the JS uses, so
# there is exactly one source of truth (the data attributes) and the
# static fallback can never disagree with the animated value.
STAT_NUMBER_RE = re.compile(
    r'(<p class="stat-number"((?:\s+data-[a-z]+="[^"]*")*)>)[^<]*(</p>)'
)
STAT_ATTR_RE = re.compile(r'data-([a-z]+)="([^"]*)"')


def fix_stat_number_fallbacks(html: str) -> str:
    def repl(match: re.Match) -> str:
        open_tag, attrs_blob, close_tag = match.group(1), match.group(2), match.group(3)
        attrs = dict(STAT_ATTR_RE.findall(attrs_blob))
        target = attrs.get("target")
        if target is None:
            return match.group(0)
        decimals = int(attrs.get("decimals", "0") or "0")
        prefix = attrs.get("prefix", "")
        suffix = attrs.get("suffix", "")
        text = f"{prefix}{float(target):.{decimals}f}{suffix}"
        return f"{open_tag}{text}{close_tag}"

    return STAT_NUMBER_RE.sub(repl, html)


def generate_webp(photos_dir: Path) -> None:
    """Build-time WebP copies of every JPEG in the output directory --
    generated, not committed to source (the .jpg originals stay
    authoritative). <picture> in the rendered HTML offers these first;
    a browser without WebP support just falls through to the JPEG."""
    for jpg_path in sorted(photos_dir.glob("*.jpg")):
        with Image.open(jpg_path) as img:
            img.save(jpg_path.with_suffix(".webp"), "WEBP", quality=82)


def generate_pdfs(site: Path, pages: list) -> None:
    """One PDF per case-study page (see is_case_study_page()), rendered
    from the already-built HTML via a real browser engine (Playwright +
    Chromium) rather than a lighter HTML-to-PDF library -- this site's
    charts are inline SVG inside a CSS layout a simpler converter
    wouldn't render faithfully. Page-numbered header/footer and a
    retrieval date/URL come from the PDF template itself, not the page
    content, so they're accurate no matter when this runs.

    Serves `site` over a real local HTTP server rather than loading pages
    via file:// -- every page uses root-relative paths (/assets/style.css
    etc.), which file:// resolves against the filesystem root, not the
    site directory, silently dropping the stylesheet. Confirmed this the
    hard way (checked actual computed styles, not just a visual glance at
    the output) before settling on the HTTP approach.

    Skips cleanly (prints a warning, doesn't fail the whole build) if
    Playwright's browser isn't installed -- a missing PDF export
    shouldn't block the rest of the site from shipping."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("playwright not installed -- skipping PDF export")
        return

    targets = [out_rel for _, out_rel in pages if is_case_study_page(out_rel)]
    if not targets:
        return

    import functools
    import http.server
    import threading

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(site))
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()

    footer_template = """
    <div style="font-size:8px; width:100%; padding:0 0.5in; color:#666;
                display:flex; justify-content:space-between;">
      <span>secondgrowthresearch.org &mdash; retrieved <span class="date"></span></span>
      <span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>
    </div>
    """

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            for out_rel in targets:
                pdf_path = (site / out_rel).with_suffix(".pdf")
                page.goto(f"http://127.0.0.1:{port}/{out_rel}", wait_until="load")
                # Stat-pair numbers count up via a 1200ms JS animation
                # (requestAnimationFrame, not a network request) --
                # "load" doesn't wait for it, so without this a PDF could
                # capture a stat mid-count instead of its final value.
                page.wait_for_timeout(1500)
                page.pdf(
                    path=str(pdf_path),
                    format="Letter",
                    print_background=True,
                    display_header_footer=True,
                    header_template="<div></div>",
                    footer_template=footer_template,
                    margin={"top": "0.5in", "bottom": "0.6in", "left": "0.5in", "right": "0.5in"},
                )
            browser.close()
        print(f"generated {len(targets)} case-study PDFs")
    except Exception as exc:  # pragma: no cover -- CI environment issue, not a content bug
        print(f"PDF export failed ({exc}) -- continuing without it")
    finally:
        httpd.shutdown()


def page_title(html_body: str, fallback: str) -> str:
    match = re.search(r"<h1[^>]*>(.*?)</h1>", html_body, re.S)
    if match:
        return re.sub("<[^>]+>", "", match.group(1)).strip()
    return fallback


def page_description(html_body: str, max_len: int = 155) -> str:
    """First real paragraph after the H1, stripped to plain text and
    truncated at a word boundary -- gives every page its own, distinct
    meta description (and OG/Twitter description) instead of the one
    sitewide tagline every page previously shared. Falls back to
    SITE_TAGLINE if no usable paragraph is found (e.g. a page that opens
    straight into a stat-pair or chart rather than prose)."""
    paragraphs = re.findall(r"<p>(.*?)</p>", html_body, re.S)
    for raw in paragraphs:
        text = re.sub(r"<[^>]+>", "", raw)
        text = re.sub(r"\s+", " ", text).strip()
        if len(text) >= 40:  # skip stray short/empty paragraphs
            break
    else:
        return SITE_TAGLINE

    if len(text) <= max_len:
        return text
    truncated = text[:max_len].rsplit(" ", 1)[0]
    return truncated.rstrip(",;:") + "…"


def html_attr_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def is_case_study_page(out_rel: str) -> bool:
    """Individual closure/town case studies get a PDF export (see
    generate_pdfs()) -- the case-studies.html overview/timeline page
    itself doesn't (its interactive map and hand-built SVG timeline
    aren't a single linear document the way one closure's story is)."""
    return out_rel.startswith("case-studies/") and out_rel != "case-studies.html"


def rfc822_date(iso_date: str) -> str:
    """YYYY-MM-DD -> RFC 822 (e.g. 'Fri, 10 Oct 2026 00:00:00 GMT'), the
    format RSS <pubDate> actually requires -- ISO 8601 isn't valid here."""
    dt = datetime.strptime(iso_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return dt.strftime("%a, %d %b %Y %H:%M:%S GMT")


_GIT_DATES_CACHE: dict = {}


def git_dates(src_rel: str) -> tuple:
    """(first_commit_date, last_commit_date) for a source file, both
    YYYY-MM-DD or None if the file has no git history yet (e.g. staged but
    uncommitted). Real commit history, not a hand-maintained date someone
    has to remember to update -- the whole point is that this can't drift
    out of sync with what actually changed. Needs full history, not a
    shallow clone; see the fetch-depth: 0 in the deploy workflow."""
    if src_rel in _GIT_DATES_CACHE:
        return _GIT_DATES_CACHE[src_rel]
    try:
        result = subprocess.run(
            ["git", "log", "--follow", "--format=%ad", "--date=short", "--", src_rel],
            cwd=ROOT, capture_output=True, text=True, check=True,
        )
        dates = [d for d in result.stdout.strip().split("\n") if d]
    except (subprocess.CalledProcessError, FileNotFoundError):
        dates = []
    pair = (dates[-1], dates[0]) if dates else (None, None)
    _GIT_DATES_CACHE[src_rel] = pair
    return pair


def render_page(title: str, body_html: str, out_path: Path, out_rel: str, src_rel: str) -> str:
    primary_links = "\n".join(
        f'        <a href="{href}">{label}</a>' for href, label in NAV_PRIMARY
    )
    secondary_links = "\n".join(
        f'        <a href="{href}">{label}</a>' for href, label in NAV_SECONDARY
    )
    url_path = "/" if out_rel == "index.html" else "/" + out_rel
    canonical_url = DOMAIN + url_path
    full_title = f"{title} — {SITE_NAME}"
    description = html_attr_escape(page_description(body_html))
    full_title_attr = html_attr_escape(full_title)

    published, updated = git_dates(src_rel)
    date_line = ""
    if SHOW_DATES and published:
        date_line = (
            f"Published {published}"
            + (f" &middot; Last updated {updated}" if updated != published else "")
        )
    pdf_link = ""
    if is_case_study_page(out_rel):
        pdf_link = f'<a href="/{out_rel[:-5]}.pdf">Download as PDF</a>'
        if date_line:
            pdf_link = " &middot; " + pdf_link
    date_note = f'<p class="page-dates">{date_line}{pdf_link}</p>\n' if (date_line or pdf_link) else ""
    goatcounter_tag = (
        f'<script data-goatcounter="https://{GOATCOUNTER_CODE}.goatcounter.com/count" '
        f'async src="//gc.zgo.at/count.js"></script>\n'
        if GOATCOUNTER_CODE
        else ""
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — {SITE_NAME}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical_url}">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{full_title_attr}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical_url}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{full_title_attr}">
<meta name="twitter:description" content="{description}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Zilla+Slab:wght@500;600;700&family=Work+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
{goatcounter_tag}</head>
<body>
<a class="skip-link" href="#main-content">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/">{SITE_NAME}</a>
    <button type="button" class="nav-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu">
      <span class="nav-toggle-bar"></span>
      <span class="nav-toggle-bar"></span>
      <span class="nav-toggle-bar"></span>
    </button>
    <nav id="site-nav">
      <div class="nav-group nav-group-primary">
{primary_links}
      </div>
      <div class="nav-group nav-group-secondary">
{secondary_links}
      </div>
    </nav>
  </div>
</header>
<main class="wrap content" id="main-content">
{body_html}
{date_note}</main>
<footer class="site-footer">
  <div class="wrap">
    <p>{SITE_NAME} &middot; <a href="/about.html">About</a></p>
  </div>
</footer>
<div class="chart-tooltip" id="chart-tooltip" role="status" aria-live="polite"></div>
<script>
// Mobile nav toggle. Below the 600px breakpoint (see .nav-toggle /
// .nav-group-primary / .nav-group-secondary in style.css), the header nav
// is collapsed behind this hamburger button; above it, CSS keeps the nav
// always visible regardless of aria-expanded, so this script is inert on
// desktop -- no resize listener needed, the media query does that work.
(function () {{
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (!toggle || !nav) return;

  function setOpen(open) {{
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    nav.classList.toggle('nav-open', open);
  }}

  toggle.addEventListener('click', function () {{
    setOpen(toggle.getAttribute('aria-expanded') !== 'true');
  }});

  document.addEventListener('keydown', function (e) {{
    if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {{
      setOpen(false);
      toggle.focus();
    }}
  }});
}})();
</script>
<script>
// Generic hover/focus tooltip for any chart on the page. A chart hit
// element just needs class="chart-hit" plus data-label / data-value and
// optionally data-key-color (a swatch hex shown in the tooltip row).
// Dataviz skill contract: tooltips enhance, never gate -- every value here
// is also present as a direct label or in that chart's <details> table.
(function () {{
  var tip = document.getElementById('chart-tooltip');
  if (!tip) return;

  function showTip(el, x, y) {{
    var label = el.getAttribute('data-label') || '';
    var value = el.getAttribute('data-value') || '';
    var color = el.getAttribute('data-key-color');
    tip.textContent = '';
    var row = document.createElement('div');
    row.className = 'tt-row';
    if (color) {{
      var key = document.createElement('span');
      key.className = 'tt-key';
      key.style.background = color;
      row.appendChild(key);
    }}
    var labelNode = document.createTextNode(label + ': ');
    row.appendChild(labelNode);
    var valueNode = document.createElement('span');
    valueNode.className = 'tt-value';
    valueNode.appendChild(document.createTextNode(value));
    row.appendChild(valueNode);
    tip.appendChild(row);
    tip.style.left = x + 'px';
    tip.style.top = (y - 10) + 'px';
    tip.classList.add('visible');
  }}

  function hideTip() {{ tip.classList.remove('visible'); }}

  document.addEventListener('pointermove', function (e) {{
    var el = e.target.closest ? e.target.closest('.chart-hit') : null;
    if (el) {{
      var r = el.getBoundingClientRect();
      showTip(el, r.left + r.width / 2, r.top);
    }}
  }});
  document.addEventListener('pointerover', function (e) {{
    var el = e.target.closest ? e.target.closest('.chart-hit') : null;
    if (!el) hideTip();
  }});
  document.querySelectorAll('.chart-hit').forEach(function (el) {{
    el.addEventListener('focus', function () {{
      var r = el.getBoundingClientRect();
      showTip(el, r.left + r.width / 2, r.top);
    }});
    el.addEventListener('blur', hideTip);
  }});
}})();
</script>
<script>
// Generic click-to-enlarge lightbox for any <figure class="figure"><img>...
// on the page. Reuses the figure's own figcaption content directly, so the
// enlarged view never shows different text than the inline one.
(function () {{
  var figImages = document.querySelectorAll('.figure img');
  if (!figImages.length) return;

  var overlay = document.createElement('div');
  overlay.className = 'lightbox';
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-modal', 'true');
  overlay.setAttribute('aria-hidden', 'true');
  overlay.innerHTML = '<button type="button" class="lightbox-close" aria-label="Close enlarged image">&times;</button>' +
    '<img class="lightbox-img" alt="">' +
    '<p class="lightbox-caption"></p>';
  document.body.appendChild(overlay);

  var imgEl = overlay.querySelector('.lightbox-img');
  var capEl = overlay.querySelector('.lightbox-caption');
  var closeBtn = overlay.querySelector('.lightbox-close');
  var lastFocused = null;

  function open(trigger) {{
    lastFocused = trigger;
    imgEl.src = trigger.src;
    imgEl.alt = trigger.alt || '';
    var figcaption = trigger.closest('figure').querySelector('figcaption');
    capEl.innerHTML = figcaption ? figcaption.innerHTML : '';
    overlay.classList.add('visible');
    overlay.setAttribute('aria-hidden', 'false');
    closeBtn.focus();
    document.body.style.overflow = 'hidden';
  }}

  function close() {{
    overlay.classList.remove('visible');
    overlay.setAttribute('aria-hidden', 'true');
    imgEl.src = '';
    document.body.style.overflow = '';
    if (lastFocused) lastFocused.focus();
  }}

  figImages.forEach(function (img) {{
    img.setAttribute('tabindex', '0');
    img.setAttribute('role', 'button');
    img.setAttribute('aria-label', 'Click to enlarge');
    img.addEventListener('click', function () {{ open(img); }});
    img.addEventListener('keydown', function (e) {{
      if (e.key === 'Enter' || e.key === ' ') {{
        e.preventDefault();
        open(img);
      }}
    }});
  }});

  closeBtn.addEventListener('click', close);
  overlay.addEventListener('click', function (e) {{
    if (e.target === overlay) close();
  }});
  document.addEventListener('keydown', function (e) {{
    if (e.key === 'Escape' && overlay.classList.contains('visible')) close();
  }});
}})();
</script>
<script>
// Generic scroll-triggered count-up for any .stat-number element. Counts
// from 0 to data-target once, the first time it scrolls into view.
// data-decimals / data-prefix / data-suffix control formatting. Respects
// prefers-reduced-motion by jumping straight to the final value.
(function () {{
  var statEls = document.querySelectorAll('.stat-number');
  if (!statEls.length) return;
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function formatValue(el, value) {{
    var decimals = parseInt(el.getAttribute('data-decimals') || '0', 10);
    var prefix = el.getAttribute('data-prefix') || '';
    var suffix = el.getAttribute('data-suffix') || '';
    return prefix + value.toFixed(decimals) + suffix;
  }}

  function animate(el) {{
    var target = parseFloat(el.getAttribute('data-target'));
    if (reduceMotion || isNaN(target)) {{
      el.textContent = formatValue(el, target);
      return;
    }}
    var duration = 1200;
    var start = null;
    function step(ts) {{
      if (start === null) start = ts;
      var progress = Math.min((ts - start) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = formatValue(el, target * eased);
      if (progress < 1) requestAnimationFrame(step);
    }}
    requestAnimationFrame(step);
  }}

  if ('IntersectionObserver' in window) {{
    var observer = new IntersectionObserver(function (entries) {{
      entries.forEach(function (entry) {{
        if (entry.isIntersecting) {{
          animate(entry.target);
          observer.unobserve(entry.target);
        }}
      }});
    }}, {{threshold: 0.5}});
    statEls.forEach(function (el) {{ observer.observe(el); }});
  }} else {{
    statEls.forEach(function (el) {{ animate(el); }});
  }}
}})();
</script>
<script>
// Generic "Download data (CSV)" button for any .chart that has a <table>
// (every chart's "View as table" toggle). Reads the same table a reader
// already sees -- never a separate, possibly-divergent data file -- and
// serializes it client-side. Works on the full table regardless of which
// toggle/slider state a map chart is currently showing, since the table
// itself is the complete dataset, not a snapshot of the current view.
(function () {{
  function csvField(text) {{
    text = text.replace(/\\s+/g, ' ').trim();
    if (/[",\\n]/.test(text)) text = '"' + text.replace(/"/g, '""') + '"';
    return text;
  }}

  function tableToCSV(table) {{
    var lines = [];
    table.querySelectorAll('tr').forEach(function (row) {{
      var cells = row.querySelectorAll('th,td');
      lines.push(Array.from(cells).map(function (c) {{ return csvField(c.textContent); }}).join(','));
    }});
    return lines.join('\\r\\n');
  }}

  document.querySelectorAll('.chart').forEach(function (chart) {{
    var table = chart.querySelector('table');
    if (!table) return;

    var titleEl = chart.querySelector('.chart-title');
    var title = titleEl ? titleEl.textContent.trim() : 'data';
    var slug = title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-+|-+$)/g, '') || 'data';

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'chart-download-btn';
    btn.textContent = 'Download data (CSV)';
    btn.addEventListener('click', function () {{
      var csv = tableToCSV(table);
      var blob = new Blob([csv], {{type: 'text/csv;charset=utf-8;'}});
      var url = URL.createObjectURL(blob);
      var a = document.createElement('a');
      a.href = url;
      a.download = slug + '.csv';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      setTimeout(function () {{ URL.revokeObjectURL(url); }}, 1000);
    }});

    var sources = chart.querySelectorAll('.chart-source');
    var lastSource = sources.length ? sources[sources.length - 1] : null;
    if (lastSource && lastSource.parentNode) {{
      lastSource.parentNode.insertBefore(btn, lastSource);
    }} else {{
      chart.appendChild(btn);
    }}
  }});
}})();
</script>
</body>
</html>
"""


def validate_pages() -> None:
    """build.py hardcodes PAGES rather than globbing articles/ -- deliberate
    (explicit over magic), but it means a new .md file left out of PAGES
    previously built silently with no error and no page produced. This
    catches that failure mode loudly, before any output is written, instead
    of after a build that looked clean."""
    known_sources = {src_rel for src_rel, _ in PAGES}
    on_disk = {
        str(p.relative_to(ROOT)).replace("\\", "/")
        for p in (ROOT / "articles").rglob("*.md")
    }
    orphaned = sorted(on_disk - known_sources)
    if orphaned:
        raise SystemExit(
            "build.py: found .md file(s) under articles/ not listed in PAGES "
            "-- they would build silently with no output page:\n  "
            + "\n  ".join(orphaned)
            + "\n\nAdd each to the PAGES list in build.py, or delete it if unused."
        )


def main() -> None:
    validate_pages()

    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)

    md = markdown.Markdown(extensions=["tables", "sane_lists"])
    photo_info = analyze_photos()
    page_meta = []  # (out_rel, title, published, updated) -- feeds the Recent Updates page + RSS

    for src_rel, out_rel in PAGES:
        src_path = ROOT / src_rel
        out_path = SITE / out_rel
        out_path.parent.mkdir(parents=True, exist_ok=True)

        raw = src_path.read_text(encoding="utf-8")
        raw = rewrite_links(raw)
        md.reset()
        body_html = md.convert(raw)
        body_html = rewrite_images(body_html, photo_info)
        body_html = fix_stat_number_fallbacks(body_html)
        title = page_title(body_html, fallback=out_rel)
        display_title = "Home" if title == SITE_NAME else title
        out_path.write_text(render_page(display_title, body_html, out_path, out_rel, src_rel), encoding="utf-8")
        print(f"built {out_rel}")

        published, updated = git_dates(src_rel)
        page_meta.append((out_rel, title, published, updated))

    # Recent Updates page + RSS feed -- both built from the same git-log
    # dates as the per-page bylines above, so there's no separate
    # hand-maintained changelog to forget to update. "Updated" entries
    # (published != updated) surface first within each date, since a
    # correction or new finding on an existing page is often more
    # newsworthy than a fresh page landing the same day.
    # Paused along with SHOW_DATES above -- not built at all while off,
    # not just unlinked, so there's no orphaned page sitting at a
    # guessable URL.
    if SHOW_DATES:
        dated = [m for m in page_meta if m[2]]  # skip anything with no git history yet
        dated.sort(key=lambda m: (m[3] or m[2], m[2] != m[3]), reverse=True)

        rows = "\n".join(
            f'    <tr><td>{updated or published}</td>'
            f'<td><a href="/{out_rel}">{html_attr_escape(title)}</a></td>'
            f'<td>{"Updated" if updated and updated != published else "Published"}</td></tr>'
            for out_rel, title, published, updated in dated
        )
        updates_body = f"""<h1>Recent updates</h1>

<p>Every page on this site, in order of when it was last substantively changed — generated directly from this project's own git history, not a hand-maintained list. A page here because it was corrected or extended reads the same as one here because it's brand new; the "Updated"/"Published" column is the only thing that tells them apart.</p>

<table>
<thead><tr><th>Date</th><th>Page</th><th></th></tr></thead>
<tbody>
{rows}
</tbody>
</table>

<p class="chart-source">Also available as <a href="/updates.xml">an RSS feed</a>.</p>
"""
        updates_out = SITE / "updates.html"
        updates_out.write_text(
            render_page("Recent Updates", updates_body, updates_out, "updates.html", "build.py"),
            encoding="utf-8",
        )
        print("built updates.html")

        rss_items = "\n".join(
            f"""  <item>
    <title>{html_attr_escape(title)}</title>
    <link>{DOMAIN}/{out_rel}</link>
    <guid>{DOMAIN}/{out_rel}#{updated or published}</guid>
    <pubDate>{rfc822_date(updated or published)}</pubDate>
    <description>{"Updated" if updated and updated != published else "Published"} {updated or published}</description>
  </item>"""
            for out_rel, title, published, updated in dated[:30]
        )
        rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
  <title>{SITE_NAME} — Recent Updates</title>
  <link>{DOMAIN}/updates.html</link>
  <description>{SITE_TAGLINE}</description>
{rss_items}
</channel>
</rss>
"""
        (SITE / "updates.xml").write_text(rss, encoding="utf-8")
        print("wrote updates.xml (RSS)")
    else:
        print("skipped updates.html/updates.xml (SHOW_DATES is off)")

    # Assets
    shutil.copytree(ROOT / "assets", SITE / "assets", dirs_exist_ok=True)
    print("copied assets/ (style.css)")

    generate_webp(SITE / "assets" / "photos")
    print("generated WebP copies of assets/photos/*.jpg")

    generate_pdfs(SITE, PAGES)

    # sitemap.xml + robots.txt -- every PAGES entry, root-relative URLs
    # resolved against DOMAIN the same way canonical/OG tags are.
    sitemap_pages = PAGES + ([("", "updates.html")] if SHOW_DATES else [])
    url_entries = "\n".join(
        f"  <url><loc>{DOMAIN}{'/' if out_rel == 'index.html' else '/' + out_rel}</loc></url>"
        for _, out_rel in sitemap_pages
    )
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{url_entries}\n"
        "</urlset>\n"
    )
    (SITE / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print("wrote sitemap.xml")

    (SITE / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n" f"Sitemap: {DOMAIN}/sitemap.xml\n",
        encoding="utf-8",
    )
    print("wrote robots.txt")

    # Custom domain for GitHub Pages -- the site uses root-relative links
    # throughout (nav, /assets/..., fetch() calls), which only resolve
    # correctly when served from a domain's root, not a GitHub Pages
    # project subpath like <org>.github.io/<repo>/.
    (SITE / "CNAME").write_text("secondgrowthresearch.org\n", encoding="utf-8")
    print("wrote CNAME (secondgrowthresearch.org)")

    print(f"\nSite built at {SITE}")


if __name__ == "__main__":
    main()
