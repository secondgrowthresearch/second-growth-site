# The Sector Dependence Index

## The question we're trying to measure

Before you can document what happens when a single industry leaves a place, you need a plain way to say how dependent that place was on the industry in the first place. A county where one processing sector accounts for a sliver of local employment is a different story than a county where that same sector is a large share of how people earn a living. We needed a consistent way to tell those two situations apart, across counties and across time — not a one-off judgment call for each case.

That's what the **Sector Dependence Index (SDI)** is for: a measure of how concentrated a local economy is in a single industry, built so the same method applies to any county and any sector, and can be compared fairly across both.

It's built on **location quotients**, a standard, long-established tool in regional economics — not something invented for this project. See [Methodology](methodology.md) for the full calculation, the data sources, and the honest limitations of the current version.

## What it shows: California's Central Valley food-processing sector

Our first application: how dependent four Central Valley counties are on **food manufacturing** (NAICS 311) — the sector behind the Del Monte and Olam/OFI plant closures we document in our [case studies](case-studies.md).

**Employment SDI, benchmarked against the United States, 2025:**

| County | Employment SDI | Income SDI |
|---|---|---|
| **Kings** (Hanford closure) | 0.153 | 0.195 |
| Fresno | 0.100 | 0.101 |
| Tulare | 0.119 | 0.184 |
| **Stanislaus** (Modesto/Hughson closure) | 0.205 | 0.227 |

In plain terms: in Kings County, food processing accounts for about 15% of the county's entire *basic* economy — every export-driven job in every sector, not just food processing. That share has risen steadily since 1990, when it was closer to 7%.

**Kings County's trajectory, 1990 → 2025 (US benchmark):**
- Employment SDI: **0.070 → 0.153** — more than doubled
- Income SDI: **0.074 → 0.195**

Stanislaus County — home to the larger Modesto/Hughson closure — tells a different story: it started the most dependent of the four counties in 1990, and has been diversifying *away* from food processing ever since (Employment SDI: 0.277 → 0.205). Kings County started the least dependent of the four and has been getting *more* concentrated. We haven't drawn conclusions from that contrast yet — it's a real, open question for further research, not yet explained here.

## Why this number, not just a job count

"Del Monte's closure cost roughly 500 jobs" is true but incomplete — it doesn't say whether those 500 jobs were marginal to Kings County's economy or central to it. The SDI answers that question directly, the way an economist would build the answer, using public employment data rather than an impression.

## A real refinement, not a finished number

The location-quotient calculation above assumes the benchmark economy (the US, or California) is roughly self-sufficient in food processing — neither a meaningful net importer nor exporter. We checked that assumption against real trade data rather than assuming it, and it turned out to matter: **California's international trade balance in this sector has flipped from a small surplus in 2010 to an $11.4 billion deficit in 2025.** Where we have the data to correct for this (California benchmark, 2010–2025), we do. Full detail, including what's still unadjusted and why, is in [Methodology](methodology.md).
