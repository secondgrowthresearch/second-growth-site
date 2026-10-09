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
    ("articles/case-studies/kings-2020-olam-lemoore.md", "case-studies/kings-2020-olam-lemoore.html"),
    ("articles/case-studies/kings-2024-del-monte-hanford.md", "case-studies/kings-2024-del-monte-hanford.html"),
    ("articles/case-studies/kings-2025-leprino-lemoore.md", "case-studies/kings-2025-leprino-lemoore.html"),
    ("articles/case-studies/fresno-2024-ofi-firebaugh.md", "case-studies/fresno-2024-ofi-firebaugh.html"),
    ("articles/case-studies/stanislaus-2024-tropicale-foods-modesto.md", "case-studies/stanislaus-2024-tropicale-foods-modesto.html"),
    ("articles/case-studies/stanislaus-2024-reyes-coca-cola-modesto.md", "case-studies/stanislaus-2024-reyes-coca-cola-modesto.html"),
    ("articles/case-studies/stanislaus-2025-foster-farms-turlock.md", "case-studies/stanislaus-2025-foster-farms-turlock.html"),
    ("articles/case-studies/stanislaus-2026-del-monte-modesto-hughson.md", "case-studies/stanislaus-2026-del-monte-modesto-hughson.html"),
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
# Chart/map source-citation text is written as literal HTML inside JS string
# literals (e.g. layer.source = '...see <a href="methodology.md">...'), not
# as Markdown links -- MD_LINK_RE never sees it, so without this second pass
# every "see Methodology"/"see Data" citation link across the site 404s.
HTML_HREF_RE = re.compile(r'href="([^"]+\.md)"')


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
<link href="https://fonts.googleapis.com/css2?family=Zilla+Slab:wght@500;600;700&family=Work+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
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
<div class="chart-tooltip" id="chart-tooltip" role="status" aria-live="polite"></div>
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

    # Custom domain for GitHub Pages -- the site uses root-relative links
    # throughout (nav, /assets/..., fetch() calls), which only resolve
    # correctly when served from a domain's root, not a GitHub Pages
    # project subpath like <org>.github.io/<repo>/.
    (SITE / "CNAME").write_text("secondgrowthresearch.org\n", encoding="utf-8")
    print("wrote CNAME (secondgrowthresearch.org)")

    print(f"\nSite built at {SITE}")


if __name__ == "__main__":
    main()
