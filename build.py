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
GOATCOUNTER_CODE = None

# source markdown path (relative to ROOT) -> output path (relative to SITE, root-relative URL)
PAGES = [
    ("articles/home.md", "index.html"),
    ("articles/the-index.md", "the-index.html"),
    ("articles/case-studies.md", "case-studies.html"),
    ("articles/water-insecurity.md", "water-insecurity.html"),
    ("articles/environmental-impact.md", "environmental-impact.html"),
    ("articles/consolidation.md", "consolidation.html"),
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
NAV_SECONDARY = [
    ("/methodology.html", "Methodology"),
    ("/data.html", "Data"),
    ("/about.html", "About"),
]
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


def generate_webp(photos_dir: Path) -> None:
    """Build-time WebP copies of every JPEG in the output directory --
    generated, not committed to source (the .jpg originals stay
    authoritative). <picture> in the rendered HTML offers these first;
    a browser without WebP support just falls through to the JPEG."""
    for jpg_path in sorted(photos_dir.glob("*.jpg")):
        with Image.open(jpg_path) as img:
            img.save(jpg_path.with_suffix(".webp"), "WEBP", quality=82)


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


def render_page(title: str, body_html: str, out_path: Path, out_rel: str) -> str:
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
</main>
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

    for src_rel, out_rel in PAGES:
        src_path = ROOT / src_rel
        out_path = SITE / out_rel
        out_path.parent.mkdir(parents=True, exist_ok=True)

        raw = src_path.read_text(encoding="utf-8")
        raw = rewrite_links(raw)
        md.reset()
        body_html = md.convert(raw)
        body_html = rewrite_images(body_html, photo_info)
        title = page_title(body_html, fallback=out_rel)
        display_title = "Home" if title == SITE_NAME else title
        out_path.write_text(render_page(display_title, body_html, out_path, out_rel), encoding="utf-8")
        print(f"built {out_rel}")

    # Assets
    shutil.copytree(ROOT / "assets", SITE / "assets", dirs_exist_ok=True)
    print("copied assets/ (style.css)")

    generate_webp(SITE / "assets" / "photos")
    print("generated WebP copies of assets/photos/*.jpg")

    # sitemap.xml + robots.txt -- every PAGES entry, root-relative URLs
    # resolved against DOMAIN the same way canonical/OG tags are.
    url_entries = "\n".join(
        f"  <url><loc>{DOMAIN}{'/' if out_rel == 'index.html' else '/' + out_rel}</loc></url>"
        for _, out_rel in PAGES
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
