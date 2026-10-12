# Methodology: the Sector Dependence Index

This page is written for readers who want to verify, replicate, or challenge the calculation behind [the Sector Dependence Index](the-index.md) — not a general introduction. If you want the plain-language version first, start there.

**Where this method comes from**: the Sector Dependence Index draws on established techniques in regional economics — not something invented for this project. We adapted and combined them for a specific question: how concentrated is a local economy in a single industry, and how much of that concentration is actually exported out of the region rather than just circulating money already there.

## How the index is built

We start by comparing how concentrated a sector's employment is in a county against a benchmark economy (the U.S. or California). A sector more concentrated locally than in the benchmark is treated as "export-oriented" — the kind of activity that brings outside money into a place, not merely activity that serves local demand. Only the share of a sector's employment above what the local population alone would support, if the sector were no more concentrated than the benchmark, counts toward that export-oriented total — we isolate that share for every sector and county.

The index itself asks a different question than a raw job count: of everything a county's economy exports elsewhere, what share rides on this one sector? We compute two versions — one weighted by employment, one by income — since a sector's share of jobs and its share of economic weight can diverge, as they do for several of the counties in our first case study.

**What "Income SDI" actually is, precisely:** it is not a measure of total personal or household income — it's each sector's basic (export-oriented) employment, re-weighted by that sector's own average annual pay, before the share is taken:

```
basic income, sector = basic jobs, sector × average annual pay, sector
Income SDI, sector    = basic income, sector ÷ sum(basic income, every sector)
```

"Average annual pay" here is QCEW's own wage-and-salary figure — the same payroll data the Employment SDI is built from, not a separate income dataset. That means Income SDI excludes proprietors' income and capital income (profits, rents, returns to ownership), the way a payroll-based QCEW figure always does. We're naming it precisely so "income" isn't read as broader than it is: this is a payroll-weighted variant of the employment index, not an independent measure of a sector's total economic weight.

One assumption underlies the basic version of this calculation: that the benchmark economy is roughly self-sufficient in the sector being measured, neither a significant net exporter nor importer. We don't take that on faith — we check it against real trade data wherever we can, and adjust the result when the data says the assumption doesn't hold.

**The adjustment itself, so it's actually checkable:**

```
trade_adjustment_factor = 1 − (net exports ÷ benchmark output)
adjusted benchmark share = (benchmark sector employment ÷ benchmark total employment) × trade_adjustment_factor
LQ = (county sector employment ÷ county total employment) ÷ adjusted benchmark share
```

Net exports and benchmark output are both pulled for the same year and the same benchmark region. When the benchmark is a net exporter, the factor comes in below 1.0, which shrinks the adjusted benchmark share and *raises* the resulting LQ — the sector's apparent weight in the benchmark was partly an export artifact, not the benchmark's own internal demand. When the benchmark is a net importer, as both California and the United States have become in food processing in recent years (see below), the factor comes in above 1.0, which *lowers* the resulting LQ. An unadjusted LQ (factor = 1.0) is the textbook version, implicitly assuming the benchmark neither exports nor imports the sector's output.

**What's real and applied today**: a true, year-by-year adjustment for **both benchmarks, 2010–2025** (2026 excluded on both — only partial-year trade data is published so far):
- **California benchmark**: computed from U.S. Census Bureau bulk monthly state-exports/imports-by-NAICS files (California only) and BEA's SAGDP2 state GDP-by-industry — both international trade only, no API key required.
- **United States benchmark**: the identical method and the identical Census source files, summed across every state instead of filtered to California, against BEA's SAGDP2 national total. Added 2026-10-12 — this closes a gap that existed on this page until that date, when the U.S.-benchmark comparison ran unadjusted. The U.S. factor reached **1.099 by 2025** (net exports at −9.9% of output) — a smaller net-import share than California's own, since the United States as a whole net-exports more of this sector than California specifically does, but the same directional story: both benchmarks have gone from net exporter to net importer in food processing since 2010.

## Honest limitations

We'd rather state these plainly than have a reader find them first.

- **International trade only.** The net-export data captures trade crossing international borders, not California's domestic market — shipments to and from other U.S. states, which is almost certainly the larger channel for a sector like food processing. No general-purpose, free, state-and-sector-level *interstate* trade-flow dataset exists in the U.S. — this is a known, long-standing gap in American regional economics, not something specific to our research. Using international net exports as the available proxy is standard applied-economics practice for exactly that reason.
- **A sector-bundling mismatch.** No free, government source breaks out food manufacturing (NAICS 311) alone at the state-output level — the finest available breakout bundles it with beverage and tobacco manufacturing (NAICS 312). Our net-export figures are 311-only; our output denominator is 311+312. This makes our trade-adjustment factor a slight understatement of the true 311-only adjustment.
- **The real direction surprised our own prior assumption.** Before we had real trade data, we assumed food processing was heavily export-oriented at both the California and U.S. benchmark levels, and that correcting for it would raise the measured dependence. The real data shows California's position in this sector has in fact flipped to a net-*import* deficit in recent years — which, where we've applied the correction, *lowers* the adjusted figures relative to an unadjusted run. We're noting this as an example of why we check assumptions against data rather than publish them as fact.
- **County-level location quotients assume a closed local labor market.** The method compares where people work, county by county, against where the benchmark's jobs sit — it has no way to see whether the people holding those jobs actually live in the county being measured. California's Central Valley has real, documented cross-county commuting; a county whose food-processing workforce commutes in from a neighbor would show the same SDI as one whose workforce lives entirely within its own borders, even though the local economic dependence those two situations represent isn't quite the same thing. We haven't yet built a commuting-adjusted version of this index — Census LEHD LODES (origin-destination employment data) or a switch to commuting-zone geography instead of county boundaries are the standard ways regional economists handle this; neither is applied here yet.
- **Location quotients are a real but imprecise technique, not a survey.** The method (sometimes called "minimum requirements") infers export-oriented employment from a concentration ratio rather than measuring actual sales or shipments out of the region. It's standard, long-used, and the right tool for the question — but it's sensitive to which benchmark geography is chosen and assumes every county in the benchmark would otherwise consume the sector's output in roughly the same proportion, an assumption real regional economies don't perfectly satisfy. We're naming this as a property of the method itself, not something specific to how we've applied it.
- **QCEW only ever counts formal, on-the-books employees — categorically, not as a threshold that a larger operation clears and a smaller one doesn't.** We checked the specific mechanism we first suspected (a federal exemption letting small agricultural employers skip unemployment-insurance coverage, which would then exclude them from QCEW) and it doesn't apply here: California's own UI law requires registration at $100 in quarterly wages, far below the federal agricultural carve-out, so small farms in this state are covered the same as any other employer (confirmed directly against EDD's own DE 1AG registration form; see Leigh, Du & McCurdy, *Annals of Epidemiology*, 2014, which names California specifically as the exception to the usual small-farm undercount). The real, narrower gap that remains: QCEW counts *employees*, full stop — sole proprietors, unpaid family labor on a family operation, and workers paid off the books are structurally invisible to it, regardless of the employer's size. Every employment and SDI figure on this site inherits that boundary. We're naming it precisely, the same way we corrected ourselves on the UI-threshold question, rather than letting the weaker version of the claim stand uncorrected.

## Data sources

- Employment and wages: U.S. Bureau of Labor Statistics, Quarterly Census of Employment and Wages (QCEW), county and state/national level, 1990–2026
- Trade: U.S. Census Bureau, state exports/imports by NAICS (bulk files)
- Output: U.S. Bureau of Economic Analysis, Regional Economic Accounts (SAGDP2)
- Closure and layoff documentation: California EDD WARN Act filings, original news reporting, company records

Full source list with citation detail: [Data](data.md).

Stanislaus, Fresno, and Tulare counties are computed using this same method; see [the Index](the-index.md) for the results.
