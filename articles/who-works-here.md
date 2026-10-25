# Who works here

Every other page on this site measures jobs: how many exist, in which sector, in which county, over time. None of it says who actually holds those jobs, what they're paid, or how the basic shape of the work — employee of a company, or worker for a contractor — has been shifting underneath the headlines. This page closes that gap directly, using the same rigor as everywhere else on this site: real government data, real caveats where the data runs thin, and a real limitation named as plainly as a real finding.

<div class="stat-pair">
  <div class="stat-card">
    <p class="stat-number" data-target="15" data-decimals="0" data-suffix="%">0%</p>
    <p class="stat-label">How far below Fresno County's own average pay its largest food-manufacturing sector has fallen — up from 2% above average 35 years ago, exactly as that sector consolidated into fewer, larger plants.</p>
  </div>
  <div class="stat-card">
    <p class="stat-number" data-target="33" data-decimals="0" data-suffix="%">0%</p>
    <p class="stat-label">Roughly what a farm-labor-contractor employee earns for every dollar a direct-hire crop-farming worker earns, per the peer-reviewed literature — not narrowing over time.</p>
  </div>
</div>

## Who holds these jobs

No standard Census product publishes food-manufacturing employment broken out by demographics at the county level — checked directly, not assumed: the detailed tables that do this (B24134/135/136) exist only at the national level; querying any of them for a specific county returns nothing. The workaround here is a custom tabulation from ACS's own microdata (PUMS, 2019-2023), filtered to food-manufacturing workers in each county's own geography:

<div class="table-scroll">
<table>
  <thead><tr><th>County</th><th>% Male</th><th>% Hispanic</th><th>% Foreign-born</th><th>Median earnings (Male / Female)</th></tr></thead>
  <tbody>
    <tr><td>Kings</td><td>82%</td><td>61%</td><td>34%</td><td>$40,000 ($40,000 / $35,000)</td></tr>
    <tr><td>Fresno</td><td>56%</td><td>70%</td><td>51%</td><td>$35,000 ($38,000 / $31,000)</td></tr>
    <tr><td>Tulare</td><td>66%</td><td>78%</td><td>37%</td><td>$44,000 ($48,000 / $34,000)</td></tr>
    <tr><td>Stanislaus</td><td>58%</td><td>60%</td><td>44%</td><td>$40,000 ($50,000 / $30,000)</td></tr>
  </tbody>
</table>
</div>

Every county's food-manufacturing workforce is majority-Hispanic, majority-male, and substantially foreign-born, with a consistent gender earnings gap — women earn 68-88% of men's median across all four counties. Kings' numbers are the thinnest of the four (the underlying sample has some demographic sub-cells with only a handful of people in them) and should be read as directional, not precise.

<div class="research-note">
<span class="research-note-label">What we found</span>
The broader "Manufacturing" category (NAICS 31-33, not just food) is directly published at the county level and pays noticeably more than the food-manufacturing-specific figures above: Kings $48,553 median (19.3% female, 4,792 workers), Fresno $44,353 (28.8%, 27,322), Tulare $51,373 (24.3%, 16,067), Stanislaus $55,263 (29.1%, 29,473). Food manufacturing specifically pays less than manufacturing broadly in every one of these counties — a real signal about this sector's own position inside the local labor market, not just a gap in what's measured.
</div>

## Wages, and whether they're holding through consolidation

[Consolidation](consolidation.md) documents ownership thinning into fewer, larger operations, nationally and in parts of this project's own four counties. This page answers the question that page couldn't: when consolidation actually happens, what does it do to pay?

The two clearest cases point in opposite directions, and the difference tracks consolidation itself, not the sector. In **Fresno County, meat and poultry processing (NAICS 3116)** single-handedly drove the county's entire net gain in food-manufacturing jobs — and its real, inflation-adjusted wages have been essentially flat for 35 years while the county's own overall pay grew 25%. Its pay-to-county-average ratio fell from 1.02 (above average) to 0.85 (15% below), exactly as the number of plants in that sector shrank. In **Tulare County, dairy processing (NAICS 3115)** was the single biggest driver of that county's food-manufacturing growth too — but its establishment count *grew* alongside employment, with no consolidation, and it kept a large, durable pay premium over the county average the entire time (1.78× in 1990, still 1.64× in 2025). No subsector in either county shows wages falling in absolute dollars; the erosion, where it exists, is always *relative* to each county's own wage growth, and it shows up specifically and only where plant ownership actually consolidated.

## A workforce increasingly working through contractors, not employers

A separate, older shift sits underneath the plant-level story: California agriculture has been moving hired farm labor away from direct employment and toward **farm labor contractors (NAICS 115115)** for decades — by 2015, already more than 40% of the state's hired farm workers were contractor-employed; by 2018-21, 74% of the state's crop-support workforce worked for contractors specifically, roughly the opposite ratio from the rest of the country. This isn't new, and it isn't something this project's own almond/pistachio acreage story explains — nut harvest is heavily mechanized (tree shakers, not hand crews), which argues against a harvest-labor channel, and the county-level growth itself doesn't line up cleanly with the 2014-2024 acreage boom: Fresno's contractor employment actually peaked in 2014, before the boom accelerated; Tulare's sharpest growth was 2012-2015; Kings shows an unexplained 51% jump in just the most recent year on record; Stanislaus actually declined net over the full 35 years.

The best-documented, dated candidate driver is California's own 2016 minimum-wage increase and agricultural overtime law (cutting the overtime threshold from 60 to 40 hours a week, phased 2019-2025) — a 2017 California Department of Food and Agriculture source names this directly, with a specific mechanism: a contractor can split one worker's hours across several client farms to limit any single employer's overtime exposure. Plausible and well-timed, not proven causal. A different, tempting explanation was checked and ruled out: a 2015 state law (AB 1897) made growers jointly liable for a contractor's wage violations — that *closes* a liability-shield motive for using contractors, rather than creating one, so it argues against, not for, a contractor-growth story starting in 2015.

Contractor pay sits well below direct-hire pay, and the comparison depends on what it's measured against. Against this project's own food-manufacturing wage data, the gap is real and large but *narrowing* — contractor pay rose from roughly 26-33% of food-manufacturing pay in 1990 to 39-56% by 2025, across all four counties. Against direct-hire **crop farming** specifically — the comparison the peer-reviewed literature actually uses — contractor workers earn roughly a third as much, and that gap is not clearly narrowing. Both are real measurements of different things. One grounding, non-statistical data point: in 2023, California's Labor Commissioner's Office took a $1.9 million wage-theft enforcement action against a Fresno-area farm labor contractor and two growers, covering 356 workers.

## The field-labor side nobody here had measured

Every number anywhere else on this site, in either direction, measures NAICS 311 — food *processing*. Actual field labor — NAICS 111, crop production, the workforce that grows what gets processed — has been declining for decades in two of this project's four counties, independent of any plant closure: Fresno fell 59.1% (26,529 to 10,859 jobs, 1990-2025), Tulare fell 47.2% (10,574 to 5,582), both accelerating after 2015. Kings goes the opposite direction in its own tree-nut-farming subsector specifically (+52.1%). Within fruit and tree-nut farming, grape-vineyard labor collapsed (-75.9% in Fresno, -79.0% in Tulare) while tree-nut-farming labor grew (+216.9% and +114.4% respectively) — consistent with the acreage shift documented in [Same Land, Different Crop](mechanization.md), though the nut-labor gain is far smaller than the grape-labor loss in both counties.

Tulare's field-labor decline did accelerate after 2014, the same window its idle land grew 70% — directionally consistent, but this is a two-endpoint comparison (only two idle-acreage data points exist) riding on top of a decline that was already running for 25 years before 2014, not a new inflection. And in Kings, field-labor employment looks flat or data-dark over the same period that its farm-labor-contractor employment grew roughly 6.5-fold — a real signal that at least some of this is reclassification into contracted labor, not pure headcount loss.

<div class="research-note">
<span class="research-note-label">What we found</span>
Field-labor pay moved the opposite direction from field-labor headcount. Real, inflation-adjusted pay for direct-hire field labor (NAICS 111) rose substantially in every county over this same 35-year window — Fresno +92.2%, Tulare +61.2%, Kings' tree-nut subsector +104.9% (there, paired with employment growth, not against it) — even as Fresno's and Tulare's headcounts fell by half or more. That pay has also been steadily closing the gap with each county's own average pay, not falling further behind (roughly 0.43-0.68× in 1990 to 0.76-0.92× by 2025). And direct-hire field labor is paid *more* than farm-labor-contractor labor in every county, at every point checked, by a factor of 1.13 to 2.43 — confirming, with this project's own data, what the academic literature above could only state for the state as a whole. Whether that direct-hire-versus-contractor gap is widening or narrowing has no single answer across the three counties — Kings narrows, Fresno's tree-nut subsector widens, Tulare roughly round-trips — reported as the genuinely mixed result it is. None of this is the full field-labor picture: QCEW's own documented agricultural-coverage gaps apply here too, and the reported average pay mixes full-time and seasonal work rather than counting individual workers.
</div>

## What this doesn't claim

- **The demographic profile above is residence-based, not workplace-based, and the underlying sample is small** (1,046 person-records across all four counties combined). It's sanity-checked against this project's own QCEW employment counts (55-90% of the workplace-based total, the right order of magnitude once cross-county commuting is accounted for) but carries no formal margin of error — stated as a real limitation, not glossed over.
- **The 2016 minimum-wage/overtime law is a well-timed, named candidate driver for farm-labor-contractor growth, not a proven cause.** The county-level timing is messy enough (Fresno peaked in 2014, before the law passed) that this should be read as one real contributing factor among others, not the whole explanation.
- **NAICS 111 is not the full field-labor picture.** QCEW has documented historical coverage gaps for agricultural employment, and a meaningful share of hired farm labor is captured under the farm-labor-contractor code instead of the crop code actually worked — this page's own field-labor and contractor sections should be read together, not as two independent counts that simply add up.
- **Why Fresno's meat/poultry sector consolidated with a measurable wage cost while Tulare's dairy sector didn't has a real, better-supported answer now — union contract coverage, and a confirmed federal antitrust settlement naming Foster Farms specifically — not raw firm count or ownership structure.** See [Consolidation](consolidation.md) for the full finding, including the one piece that's still a real gap: California Dairies Inc's own union status at its Tulare plants couldn't be confirmed directly.

## Sources

- U.S. Census Bureau, American Community Survey 5-Year Estimates, Public Use Microdata Sample (PUMS), 2019-2023 — custom tabulation, food-manufacturing workers by county. *Access: obtained — bulk data file downloaded from the agency, not a web page.*
- U.S. Census Bureau, American Community Survey, Subject Tables S2403/S2413 (Industry by Sex, Industry by Earnings) — published county-level Manufacturing (NAICS 31-33) figures. *Access: obtained — bulk data file downloaded from the agency, not a web page.*
- U.S. Bureau of Labor Statistics, Quarterly Census of Employment and Wages (QCEW), county-industry-annual files — NAICS 311 subsector wages and establishment counts, NAICS 115115 (Farm Labor Contractors and Crew Leaders), and NAICS 111 (Crop Production), 1990-2025. *Access: obtained — bulk data file downloaded from the agency, not a web page.*
- [Martin, P., Hooker, B., Rutledge, Z., Stockton, M., "California has 882,000 farmworkers to fill 413,000 jobs," *California Agriculture* (2024)](https://californiaagriculture.org/article/94420-california-has-882-000-farmworkers-to-fill-413-000-jobs) — farm labor contractor employment share and wage-comparison literature.
- California Department of Food and Agriculture (2017) — on the agricultural minimum-wage and overtime law's effect on farm labor costs. *Access: not-captured — a public URL exists for this source and this project has not recorded it.*
- California Labor Commissioner's Office, 2023 wage-theft enforcement action (Fresno-area farm labor contractor and two growers, $1.9 million, 356 workers). *Access: not-captured — a public URL exists for this source and this project has not recorded it.*

Full citation detail and source archive: [Data](data.md). See [Consolidation](consolidation.md) for the ownership side of the wage finding above, and [Same Land, Different Crop](mechanization.md) for the land-use shift behind the field-labor numbers. Back to [Case Studies](case-studies.md).
