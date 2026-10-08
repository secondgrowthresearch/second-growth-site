# Methodology: the Sector Dependence Index

This page is written for readers who want to verify, replicate, or challenge the calculation behind [the Sector Dependence Index](the-index.md) — not a general introduction. If you want the plain-language version first, start there.

**Where this method comes from**: the Sector Dependence Index draws on established techniques in regional economics — not something invented for this project. We adapted and combined them for a specific question: how concentrated is a local economy in a single industry, and how much of that concentration is actually exported out of the region rather than just circulating money already there.

## How the index is built

We start by comparing how concentrated a sector's employment is in a county against a benchmark economy (the U.S. or California). A sector more concentrated locally than in the benchmark is treated as "export-oriented" — the kind of activity that brings outside money into a place, not merely activity that serves local demand. Only the share of a sector's employment above what the local population alone would support, if the sector were no more concentrated than the benchmark, counts toward that export-oriented total — we isolate that share for every sector and county.

The index itself asks a different question than a raw job count: of everything a county's economy exports elsewhere, what share rides on this one sector? We compute two versions — one weighted by employment, one by income — since a sector's share of jobs and its share of economic weight can diverge, as they do for several of the counties in our first case study.

One assumption underlies the basic version of this calculation: that the benchmark economy is roughly self-sufficient in the sector being measured, neither a significant net exporter nor importer. We don't take that on faith — we check it against real trade data wherever we can, and adjust the result when the data says the assumption doesn't hold.

**What's real and applied today**: a true, year-by-year adjustment for the **California benchmark, 2010–2025**, computed from:
- **Net exports**: U.S. Census Bureau bulk monthly state-exports/imports-by-NAICS files (international trade only; no API key required)
- **Output**: BEA's SAGDP2 state GDP-by-industry (current-dollar, no API key required)

**What this isn't yet**: the U.S.-benchmark comparison still runs unadjusted (factor = 1.0) — extending it needs the same Census data summed nationally instead of filtered to California, a pull we haven't run yet.

## Honest limitations

We'd rather state these plainly than have a reader find them first.

- **International trade only.** The net-export data captures trade crossing international borders, not California's domestic market — shipments to and from other U.S. states, which is almost certainly the larger channel for a sector like food processing. No general-purpose, free, state-and-sector-level *interstate* trade-flow dataset exists in the U.S. — this is a known, long-standing gap in American regional economics, not something specific to our research. Using international net exports as the available proxy is standard applied-economics practice for exactly that reason.
- **A sector-bundling mismatch.** No free, government source breaks out food manufacturing (NAICS 311) alone at the state-output level — the finest available breakout bundles it with beverage and tobacco manufacturing (NAICS 312). Our net-export figures are 311-only; our output denominator is 311+312. This makes our trade-adjustment factor a slight understatement of the true 311-only adjustment.
- **The real direction surprised our own prior assumption.** Before we had real trade data, we assumed food processing was heavily export-oriented at both the California and U.S. benchmark levels, and that correcting for it would raise the measured dependence. The real data shows California's position in this sector has in fact flipped to a net-*import* deficit in recent years — which, where we've applied the correction, *lowers* the adjusted figures relative to an unadjusted run. We're noting this as an example of why we check assumptions against data rather than publish them as fact.

## Data sources

- Employment and wages: U.S. Bureau of Labor Statistics, Quarterly Census of Employment and Wages (QCEW), county and state/national level, 1990–2026
- Trade: U.S. Census Bureau, state exports/imports by NAICS (bulk files)
- Output: U.S. Bureau of Economic Analysis, Regional Economic Accounts (SAGDP2)
- Closure and layoff documentation: California EDD WARN Act filings, original news reporting, company records

Full source list with citation detail: [Data](data.md).

Stanislaus, Fresno, and Tulare counties are computed using this same method; see [the Index](the-index.md) for the results.
