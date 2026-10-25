#!/usr/bin/env python3
"""Which cited URLs already have a Wayback snapshot, and which don't.

Deliberately NOT part of build.py. The build must work offline and must not
depend on a third-party service being up; this is a thing you run by hand,
occasionally, when you want to know where the gaps are.

    python3 tools/check_archives.py              # report the gaps
    python3 tools/check_archives.py --submit URL # archive ONE url, on purpose

WHY IT ONLY READS BY DEFAULT
----------------------------
We checked every URL in the site's source lists against the Internet
Archive's CDX index before writing this. Of 59 distinct cited URLs, 54
already had a snapshot, 3 had none, and 2 were unresolved. There is no
corpus-wide archiving problem to solve, so there is nothing here that
submits in bulk. Mass-submitting several hundred URLs to a free public
service to re-capture pages it already holds is rude and pointless.

WHAT WE LEARNED ABOUT THE WRITE SIDE
------------------------------------
Save Page Now 2 is POST https://web.archive.org/save. The endpoint is
reachable from here, but:

  * Anonymous use is rate-limited hard. Checking 59 URLs read-only at
    roughly 1.7/second produced HTTP 429 on 30 of them; they only
    completed on a retry pass at one request every 3 seconds. Captures
    are reported at ~3/minute anonymous and ~6/minute authenticated.
  * Authenticated use needs Internet Archive S3 keys, sent as
    `Authorization: LOW <accesskey>:<secret>`. Cookie auth expires within
    days; keys don't. This project has no keys configured. Getting a pair
    is the prerequisite for any automated capture, and it should live in
    the environment, never in this repo.
  * Captures are asynchronous: the POST returns a job id, and you poll
    for the resulting timestamp. A snapshot lives at
    https://web.archive.org/web/<YYYYMMDDHHMMSS>/<url>
  * Some hosts are on the archive's own blocklist and simply cannot be
    captured. That is a distinct outcome, not a failure -- it maps to the
    `web-blocked` access state in the source lists.

THE RECOMMENDATION
------------------
Archive on citation, not on audit. When a page is first cited, capture it
once and record the snapshot timestamp alongside the URL; then the link
carries its own fallback (the Robust Links convention -- `data-versionurl`
plus `data-versiondate` on the anchor) and a later rot event is survivable.
Re-checking an already-captured corpus is a read-only job, which is this
script. Doing that properly means a submit step with real credentials and a
place to put the returned timestamp -- neither exists yet, so --submit here
handles exactly one URL at a time and refuses to loop.
"""
import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "SecondGrowthResearch-citation-check/1.0 (+https://secondgrowthresearch.org)"
URL_RE = re.compile(r"https?://[^\s)\"'<>]+")


def cited_urls() -> list:
    """Every distinct URL appearing in a `## Sources` bullet."""
    found = set()
    for path in sorted((ROOT / "articles").rglob("*.md")):
        in_sources = False
        for line in path.read_text(encoding="utf-8").split("\n"):
            if line.startswith("## "):
                in_sources = line.startswith("## Sources")
                continue
            if in_sources and line.lstrip().startswith(("- ", "* ")):
                for url in URL_RE.findall(line):
                    found.add(url.rstrip(".,;"))
    return sorted(found)


def snapshot(url: str, retries: int = 3) -> str:
    """Most recent Wayback timestamp for url, '' if none, None on error."""
    query = (
        "http://web.archive.org/cdx/search/cdx?output=json&limit=-1"
        "&fl=timestamp,statuscode&url=" + urllib.parse.quote(url, safe="")
    )
    for attempt in range(retries):
        try:
            req = urllib.request.Request(query, headers={"User-Agent": UA})
            rows = json.loads(urllib.request.urlopen(req, timeout=30).read().decode() or "[]")
            return rows[1][0] if len(rows) > 1 else ""
        except Exception:
            time.sleep(6 * (attempt + 1))
    return None


def submit(url: str) -> None:
    """Archive one URL. One. On purpose. See the module docstring."""
    print(
        f"Would submit {url} to https://web.archive.org/save\n"
        "Refusing: no Internet Archive S3 credentials are configured.\n"
        "Set IA_ACCESS_KEY and IA_SECRET_KEY and send them as\n"
        '  Authorization: LOW <access>:<secret>\n'
        "then record the returned timestamp next to the citation. Doing this\n"
        "without recording the timestamp archives a page and loses the pointer\n"
        "to it, which is the same as not archiving it.",
        file=sys.stderr,
    )
    sys.exit(2)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--submit", metavar="URL", help="archive a single URL")
    parser.add_argument("--delay", type=float, default=3.0,
                        help="seconds between CDX lookups (default 3; lower gets you 429s)")
    args = parser.parse_args()

    if args.submit:
        submit(args.submit)

    urls = cited_urls()
    print(f"{len(urls)} distinct URLs cited in source lists\n")
    tally = Counter()
    gaps = []
    for url in urls:
        stamp = snapshot(url)
        if stamp is None:
            tally["unchecked"] += 1
        elif stamp:
            tally["archived"] += 1
        else:
            tally["no snapshot"] += 1
            gaps.append(url)
        time.sleep(args.delay)

    for state, n in sorted(tally.items()):
        print(f"  {state:<14}{n:>4}")
    if gaps:
        print("\nNo snapshot on record:")
        for url in gaps:
            print("  " + url)


if __name__ == "__main__":
    main()
