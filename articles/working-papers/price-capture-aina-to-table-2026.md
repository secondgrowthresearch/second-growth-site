# Who Captures the Price?
## A farm-gate-to-retail data audit for Central Valley specialty crops

Two other pieces on this site ask a version of the same question — when a land-use or policy change creates value, who actually captures it — applied to jobs: [our synthetic-control test](sdi-synthetic-control-2026.md) of two real plant closures, and [our MLRP methodology memo](mlrp-methodology-memo-2026.md) extending that same question to farm labor. This page asks the price analogue, using a different real asset: [ʻĀina to Table](https://ainatotable.com)'s own crop-pricing chart, built independently of this project to help Fresno-region growers and buyers see what a crop is actually worth at each stage of the chain it passes through.

The question looked simple going in: of the price paid at retail for a crop, what share reaches the grower as farm-gate return, and has that share moved over 2019–2024? It isn't. What follows is what the data covers, why the capture question as originally framed couldn't be answered with it, what the data does support instead, and a real, tested result once part of that gap closed.

## What the dataset currently covers

ʻĀina to Table's `price_per_acre_chart.csv` tracks 105 crops. Checked directly, not assumed:

- **31 crops** carry a real, crop-specific per-acre gross-return figure from the Fresno County Department of Agriculture's own annual crop reports (2019–2024) — these are the crops with "Traded openly" status, individually priced in the county's own data.
- **74 crops** carry "Few suppliers" status instead: the county doesn't report them individually at all. Their only per-acre figure, where one exists, is a blended category total — $10,168/acre for the whole Vegetable Crops bucket, $3,919/acre for the whole Fruit & Nut Crops bucket — spread in the source report across dozens of different crops at once, not attributable to any single one of them.
- **56 crops** carry a wholesale price per pound (USDA AMS terminal-market shipping-point quotes).
- **23 crops** carry a retail price per pound (USDA AMS National Retail Report — Specialty Crops, Southwest region, or the USDA ERS Fruit and Vegetable Prices national annual average as a fallback).
- **18 crops** carry both a wholesale and a retail price per pound at once — the actual usable subset for any wholesale-to-retail comparison: Blueberries, Pears, Tomatoes, Blackberries, Broccoli, Cabbage, Carrots, Cauliflower, Cilantro, Jicama, Kiwifruit, Mushroom, Potato, Radish, Raspberries, Spinach, Strawberries, Tomatillo.

## Why the original question couldn't be answered with this data

Cross-referencing that 18-crop subset against the per-acre column exposes the real problem.

Only 3 of the 18 — Blueberries, Pears, and Tomatoes — are "Traded openly" with their own per-acre figure. The other 15 are "Few suppliers": there's no crop-specific farm-gate figure for broccoli, cabbage, carrots, cauliflower, cilantro, jicama, kiwifruit, mushroom, potato, radish, raspberries, spinach, strawberries, or tomatillo at all — only the shared vegetable- or fruit-category blend, which can't be unwound back to any one of them. A share of retail price captured by the grower can't be computed for 15 of the 18 crops that otherwise have a complete wholesale-retail chain, because the farm-gate number they'd need doesn't exist at the crop level.

Even for the 3 that do have a real per-acre figure, the unit doesn't match. The per-acre figure is dollars of gross return per acre — price multiplied by yield, already bundled together. The wholesale and retail figures are dollars per pound. Converting one into the other requires yield per acre, which this chart didn't carry for any crop. This isn't a new problem for this data: ʻĀina to Table's own build process had already found and documented the identical mismatch when a farm-gate-to-retail "bracket" feature was scoped and then shelved for this exact reason — three different units (per-acre, per-shipping-pack, per-pound) with no verified conversion between any pair.

So the capture question, as originally posed, wasn't a data-gathering problem solvable by pulling one more report. It needed a fact this chart was never built to carry: pounds of yield per acre, by crop, for the same years.

## What the data does support — and a problem found while running it

Restricting to the commensurable part of the chain — wholesale $/lb versus retail $/lb, both real per-pound prices, no acreage involved — the 18-crop subset does support a wholesale-to-retail markup comparison. Computed directly from the chart (midpoint of each reported range):

| Crop | Wholesale $/lb | Retail $/lb | Retail ÷ wholesale |
|---|---|---|---|
| Blueberries | $4.23 | $6.51–$15.22 | 2.57× |
| Mushroom | $3.25–$3.33 | $5.00–$7.58 | 1.91× |
| Jicama | $0.67–$0.72 | $1.29 | 1.86× |
| Plums | $1.54–$1.57 | $2.66 | 1.71× |
| Cauliflower | $1.04 | $1.69 | 1.62× |
| Broccoli | $1.55–$1.64 | $1.29–$3.49 | 1.50× |
| Raspberries | $6.00–$6.55 | $5.31–$13.31 | 1.48× |
| Cabbage | $0.67 | $0.99 | 1.48× |
| Tomatillo | $0.53–$0.61 | $0.69–$0.99 | 1.47× |
| Blackberries | $7.78–$8.00 | $5.71–$14.26 | 1.27× |
| Pears | $1.51 | $1.49–$1.99 | 1.15× |
| Spinach | $4.00–$4.75 | $3.98 | 0.91× |
| Carrots | $1.00–$1.03 | $0.65–$1.25 | 0.94× |
| Tomatoes | $3.90–$4.20 | $1.99–$4.99 | 0.86× |
| Potato | $1.36–$1.40 | $0.50–$1.80 | 0.83× |
| Strawberries | $6.94–$7.06 | $4.99 | 0.71× |
| Cilantro | $2.73–$2.91 | $0.90–$2.43 | 0.59× |
| Radish | $2.29 | $0.45 | 0.20× |

7 of 18 in this subset — nearly two in five — show retail at or below wholesale, implausible on its face, since retail price should include the wholesale cost plus a margin in almost every real case. That's itself a finding, not noise to average away. Checking the source data directly rather than assuming a real price reversal: the two most extreme cases, Cilantro and Radish, are each flagged in the chart's own documentation as "derived, retail bunch size not independently confirmed" — their retail-per-pound figures are back-calculated from a bunch-count assumption, not measured directly, which is exactly where an error that large would come from. The other five (Spinach, Carrots, Tomatoes, Potato, Strawberries) carry no such explicit flag, but share a quieter version of the same problem: the wholesale and retail quotes are each single-week snapshots pulled on different dates, at different pack sizes, sourced from different USDA report families — nothing in the chain guarantees they're describing comparable grades, weeks, or geography.

Honest conclusion: the wholesale-to-retail markup, as currently matched, is a real number for some crops and noise for others, and this data alone can't yet tell you which is which for any individual crop. Reporting an average markup across the 18 without that caveat would overstate what's actually known.

## What it would take to actually answer the original question

The yield-per-acre gap named above turned out to already be closed, one layer down in the same pipeline that builds this chart. Fresno County's own crop reports state yield per acre directly — nothing derived — and a parsing script already extracts it, by crop, by year; that output was simply never joined into the price chart. Checked directly against the three "Traded openly" crops in the 18-crop subset:

- **Blueberries: yes**, real reconciled yield (ton/acre) for every year 2019–2024.
- **Pears: yes**, same.
- **Tomatoes: no.** The fresh "Tomatoes, Standard" line the chart uses never appears in the yield data under any year 2019–2024 — only an unrelated "Processed" blend does. This gap stays open.

One real data-quality finding surfaced while checking this, not assumed clean: the county's 2021 report renders its section headers as decorative graphics that standard text extraction scrambles into unreadable fragments, which had silently mislabeled Blueberries and Pears under the wrong crop category for that year in the underlying data. Fixed directly at the source, and re-verified against the report's own arithmetic — acreage × yield should equal total production, and production × price should equal total value — before trusting the corrected figures used below.

The second gap is still open: resolving the wholesale-to-retail anomaly above needs the wholesale and retail price for the same crop pulled from the same week and, where the source allows it, the same grade or pack-size class — not the current approach of pairing whichever snapshot each source happened to have on file. Both gaps, closed and open, still only reach the 3 "Traded openly" crops; the other 15 in the 18-crop subset are blocked by the category-blend problem above, which yield data does nothing to fix.

## The recomputed claim — tested, not hypothetical, and the result is mixed

With real yield data in hand for Blueberries and Pears, farm-gate price is directly computable — the county reports it as price-per-ton, which divides by 2,000 into a real farm-gate $/lb, comparable for the first time to the chart's own wholesale and retail columns.

One caveat stated up front, not glossed over: the farm-gate figure is an annual average for calendar year 2024, the most recent county report on file; the chart's wholesale and retail figures are weekly spot quotes from November 2026. That's a real time gap, not a matched comparison — the same kind of mismatch flagged above for the wholesale-to-retail link, now also present on the farm-gate side. The result below should be read as approximate.

| Crop | Farm-gate $/lb (2024) | Wholesale $/lb | Retail $/lb | Farm-gate share of retail |
|---|---|---|---|---|
| Blueberries | $2.87 | $4.23 | $6.51–$15.22 | **19–44%** |
| Pears | $1.15 | $1.51 | $1.49–$1.99 | **58–77%** |

**Blueberries lands where the general pattern USDA's own Food Dollar Series finds nationally for farm share of retail spending would predict — a minority share.** Farm-gate is $2.87/lb against a retail range of $6.51–$15.22/lb; even at retail's low end, the grower's share is under half.

**Pears doesn't.** Farm-gate at $1.15/lb against a retail range of $1.49–$1.99/lb puts the grower's share at 58–77% — a majority, the opposite of the Blueberries pattern. That holds across the entire retail range reported, not a rounding-margin difference.

One thing worth separating out before over-reading either result: for Blueberries, farm-gate ($2.87) is already 68% of the wholesale price ($4.23) — most of the gap to retail opens up after wholesale, not between farm and wholesale. Pears shows the same shape (farm-gate is 76% of wholesale's $1.51), with a smaller absolute wholesale-to-retail step. The two crops don't actually disagree about where the farm-to-wholesale leg sits — both put the grower close to the wholesale price. They disagree about how much the wholesale-to-retail leg adds on top, which is also exactly the leg this page already flagged above as the least reliably matched part of the chain.

A 2-crop result isn't a basis for a general statement about this region's produce economy either way — it's a boundary case that shows the pattern doesn't hold uniformly even within one county's specialty-crop chart, which is itself worth knowing before generalizing from a national benchmark to a Fresno-specific claim. Tomatoes remain untested, and the other 15 crops in the 18-crop subset remain untestable under the current data entirely.

## Sources

- ʻĀina to Table, `price_per_acre_chart.csv` (Fresno County Department of Agriculture crop reports, 2019–2024; USDA AMS terminal shipping-point quotes; USDA AMS National Retail Report — Specialty Crops, Southwest region; USDA ERS Fruit and Vegetable Prices, 2023 national average, as fallback where the retail report has no match). *Access: obtained — this project's own automated capture and manual downloads, landed on disk.*
- Fresno County Department of Agriculture, annual crop reports, 2019–2024. *Access: not-captured — a public URL exists for these reports and this project has not recorded it.*
- USDA Agricultural Marketing Service, National Retail Report — Specialty Crops (FVWRETAIL). *Access: web-blocked — automated fetch of this host times out on every path tried; confirmed accessible by logging in and downloading directly.*
- USDA Economic Research Service, Food Dollar Series (national farm-share benchmark). *Access: not-captured — cited by name only; this project has not yet pulled or checked its figures against the result above.*

Back to [Working Papers](../working-papers.md).
