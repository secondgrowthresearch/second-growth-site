# Methodology: the Sector Dependence Index

This page is written for readers who want to verify, replicate, or challenge the calculation behind [the Sector Dependence Index](the-index.md) — not a general introduction. If you want the plain-language version first, start there.

## 1. Location quotient (LQ)

```
LQ = (community sector employment / community total employment)
     ÷ (benchmark sector employment / benchmark total employment)
```

An LQ above 1 means the sector is more concentrated locally than in the benchmark economy — the standard signal that it's an export-oriented ("basic") sector, not one that merely serves local demand. An LQ below 1 means the opposite.

## 2. Basic employment

Not every job in a sector counts as "basic" (export-driven) — only the share above what local population alone would support:

```
basic jobs = ((LQ − 1) / LQ) × sector employment
```

(zero wherever LQ ≤ 1).

## 3. Sector Dependence Index

**Employment SDI** is a sector's basic employment as a share of the county's *total* basic employment across every sector — not "how many jobs," but "what share of this county's entire export-driven economy rides on this one sector." **Income SDI** is the same idea, weighted by average income per sector rather than raw headcount, since a sector's job count and its income importance can diverge.

## 4. Trade adjustment

The plain LQ formula above implicitly assumes the *benchmark* region is roughly self-sufficient in the sector — neither a meaningful net exporter nor importer. That assumption doesn't always hold, and we check it against real data rather than asserting it.

`trade_adjustment_factor` is defined as the estimated share of benchmark sector employment attributable to the benchmark's own internal consumption — `1 − net_export_share_of_benchmark_output`. A factor below 1.0 (benchmark is a net exporter) raises the resulting LQ; a factor above 1.0 (benchmark is a net importer) lowers it.

**What's real and applied today**: a true, year-by-year factor for the **California benchmark, 2010–2025**, computed from:
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

## Where this is going

Stanislaus, Fresno, and Tulare counties are already computed using this same method (see [the Index](the-index.md) for the results). Next: extending the trade adjustment to the U.S. benchmark, and resolving the 311/312 output-bundling gap if a cleaner source is found.
