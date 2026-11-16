---
title: "Do Plant Closures Show Up in County-Level Economic Data? A Sector Dependence Index and Synthetic-Control Test of Two Central Valley Food-Processing Closures"
author: Adrian Cuevas
status: DRAFT — Node 1a of the Second Growth / ʻĀina to Table research portfolio
date: 2026-11-16
---

# Do Plant Closures Show Up in County-Level Economic Data?
## A Sector Dependence Index and Synthetic-Control Test of Two Central Valley Food-Processing Closures

**Adrian Cuevas**
*Draft, 2026-11-16. Prepared as part of an applied-economics research portfolio supporting a PhD application in Agricultural & Resource Economics, UC Davis.*

---

## Abstract

I document two real plant closures in California's Central Valley — Olam's Lemoore tomato-processing facility (567 jobs, July 2020) and Land O'Lakes' Tulare plant (80 jobs, 2010) — and test whether either closure produced a detectable effect on local economic indicators using the synthetic control method (Abadie, Diamond & Hainmueller, 2010). Across ten independent checks spanning county, city, and school-district geography, five outcome variables, and both annual and quarterly precision, I find **no effect distinguishable from ordinary cross-unit noise in any check**. A positive control — the same method applied to a closure roughly ten times larger (Prima Wawona's 2024 Cutler liquidation, 5,411 jobs) — is also null on its correctly-matched outcome variable, suggesting the result is not simply an artifact of small closure size within the range tested. I argue this null result is itself informative, not a dead end: it replicates, at the regional level, the central finding of the labor-displacement literature (Jacobson, LaLonde & Sullivan, 1993) that aggregate statistics are structurally the wrong instrument for detecting individual worker harm, even when that harm is real. I close by naming the direct policy implication: a program that evaluates its own labor-market effects using county- or regional-aggregate data — as public program evaluations commonly do — risks the same false-negative problem documented here, a consideration directly relevant to evaluating California's Multibenefit Land Repurposing Program's claimed employment co-benefits.

---

## 1. Introduction

A plant closes, and a county's employment figures move the following year. Attributing the second fact to the first requires a counterfactual: a credible estimate of what the county's economy would have done in the closure's absence. This paper builds that counterfactual directly, using the synthetic control method, for two real Central Valley food-processing closures, and reports an honest result: across every outcome variable and geography tested, the method cannot distinguish either closure's effect from ordinary county-to-county variation.

This is not presented as a negative result to be explained away. Following Jacobson, LaLonde & Sullivan (1993) and three decades of subsequent displaced-worker literature, individually displaced workers suffer large, persistent earnings losses even in local economies where aggregate statistics show no detectable change — a county absorbs a few hundred lost jobs through ordinary hiring and churn even as the specific people who held those jobs do not recover what they had. The null results below are consistent with, and extend empirically to a new regional setting, that well-established pattern.

### 1.1 Economic setting

The two closures sit within a broader empirical project (Second Growth) documenting food-manufacturing (NAICS 311) decline across four Central Valley counties — Kings, Fresno, Tulare, and Stanislaus — using a purpose-built **Sector Dependence Index (SDI)**, described in Section 2. The SDI establishes *why* a given closure matters to a county's economic base; the synthetic-control exercise in Sections 3–5 tests whether that theoretical importance is detectable in practice.

## 2. The Sector Dependence Index

The SDI measures how concentrated a county's economy is in food manufacturing, built on **location quotients** — a standard regional-economics tool — combined with **economic base theory**: the premise that a local economy's health rests disproportionately on its export-oriented ("basic") employment, since that is the channel through which outside money enters a local economy and is then re-spent locally.

**Location quotient:**
```
LQ = (county sector employment / county total employment) ÷ (benchmark sector employment / benchmark total employment)
```

**Trade-adjusted benchmark share**, used because the standard LQ assumes the benchmark economy is roughly trade-balanced in the sector — an assumption checked against real U.S. Census trade data rather than taken on faith:
```
trade_adjustment_factor = 1 − (net exports ÷ benchmark output)
adjusted benchmark share = (benchmark sector employment / benchmark total employment) × trade_adjustment_factor
```

Applied to Kings County (home to the Olam closure), food manufacturing's Employment SDI — its share of the county's entire basic-employment base — rose from 0.070 in 1990 to a peak of 0.419 in 2017, before falling to 0.150 by 2025. This establishes that food processing has, at various points, carried substantial weight in Kings County's export base — motivating the question of whether a specific closure within that sector is empirically detectable. Full derivation, data sources, and limitations: Second Growth, "Methodology" (2026).

## 3. Empirical method: synthetic control

**Synthetic control** (Abadie, Diamond & Hainmueller, 2010) constructs a counterfactual for a treated unit (here, a county, city, or school district experiencing a closure) as a weighted combination of untreated "donor" units, chosen so the combination's pre-treatment trajectory best matches the treated unit's own pre-treatment trajectory. The gap between the treated unit's realized post-treatment path and its synthetic counterfactual is the estimated effect.

Because a single treated unit precludes a classical hypothesis test, I use the standard **placebo test**: the identical procedure is rerun with every other unit in the donor pool treated as if it were the treated unit, producing a distribution of placebo effect sizes against which the real unit's result is ranked. A result is informative only if the real unit's rank is extreme relative to this placebo distribution — and, independently, only if the magnitude of the implied gap is plausible given the actual size of the closure being tested (a check that proved necessary; see Section 5.1).

The method was implemented directly (not via a packaged library) specifically so each step is auditable.

## 4. Data

| Source | Use | Access |
|---|---|---|
| U.S. BLS, Quarterly Census of Employment and Wages (QCEW) & Local Area Unemployment Statistics (LAUS) | County/city total and sector employment, unemployment rate | Bulk file |
| U.S. Census Bureau, LEHD Quarterly Workforce Indicators (QWI) | Quarterly NAICS-specific employment, hires, separations, earnings | Bulk file |
| California Dept. of Social Services, CalFresh (SNAP) enrollment (DFA 256 / CF 256) | County-level benefit enrollment, Nov. 2003–present | Bulk file |
| California Dept. of Tax & Fee Administration, Taxable Sales by City | Quarterly city-level taxable sales, 2009 Q1–present | Open Data Portal |
| California Dept. of Education, historical School Enrollment | School-district enrollment, 1981-82 through 2022-23 | Bulk file |
| IRS Statistics of Income, County-to-County Migration Data | Annual net/gross migration from consecutive-year tax-return addresses, 2007-08 through 2022-23 | Public |
| California EDD WARN Act filings; original news reporting; company records | Closure documentation (dates, headcounts) | Public |

All data were obtained as bulk downloads directly from the issuing agency, not scraped from web pages, for reproducibility.

## 5. Results

### 5.1 Ten checks, two closures, no detected effect

| # | Closure | Geography | Outcome | Result |
|---|---|---|---|---|
| 1 | Olam, Lemoore (Kings), 2020 — 567 jobs | County | Total employment | No effect (placebo rank 45 of 54) |
| 1 | — | County | Food-mfg. employment | No effect (rank 18 of 54, p≈0.35) |
| 1 | — | County | Unemployment rate | No effect (rank 44 of 54) |
| 2 | Olam, Lemoore, 2020 | Town (Lemoore city) | Unemployment rate | No effect (rank 138 of 271); real ran *below* synthetic every post-treatment year |
| 3 | Land O'Lakes, Tulare, 2010 — 80 jobs | County | Total employment | Rank 4 of 30 looked significant but gap was 2–3 orders of magnitude too large for an 80-job closure — not a real effect (see 5.2) |
| 3 | — | County | Food-mfg. employment | No effect (rank 16 of 21) |
| 3 | — | County | Unemployment rate | No effect (rank 25 of 27) |
| 4 | Olam, Lemoore, 2020 | County, quarterly | Peak-season (Q3) food-mfg. employment | No effect once checked against full 1992–2025 history (rank 15 of 25, p≈0.62) |
| 5 | Olam, Lemoore, 2020 | County, quarterly | Avg. earnings, stable workforce | No effect (rank 16 of 36) |
| 5 | — | County, quarterly | Avg. earnings, separating workers | No effect (rank 26 of 27) |
| 6 | Land O'Lakes, Tulare, 2010 | County | CalFresh (SNAP) enrollment | Rank 2 of 24 looked significant but gap reached 43,800 people by 2023 and ran the wrong direction — not a real effect (see 5.2) |
| 7 | Olam, Lemoore, 2020 | County | CalFresh (SNAP) enrollment | Same problem, smaller scale (rank 1 of 21, 8,000-person gap, wrong direction) |
| 8 | Olam, Lemoore, 2020 | City, quarterly | Taxable sales receipts | No effect (rank 40 of 49 sampled placebo cities, p≈0.82) |
| 9 | Olam, Lemoore, 2020 | School district, annual | Elementary / high-school enrollment | No effect (ratio-free rank 30 of 50, p≈0.61); real ran *above* synthetic — wrong direction for harm |
| 9 | Land O'Lakes, Tulare, 2010 | School district, annual | Elementary / high-school enrollment | No effect (rank 18–40 of 31–40, p≈0.29–0.59) |
| 10 | Both closures | County, annual | Net / gross migration (IRS SOI) | No effect in all four checks (ranks 15–45 of 54, p≈0.29–0.84) |

### 5.2 Two false positives, caught before publication

Two checks (3 and 6/7) initially produced the most statistically extreme placebo ranks in the project — and both were artifacts. In each case, the implied gap (4,700–14,400 jobs for an 80-job closure; 8,000–43,800 CalFresh enrollees for 80- and 567-job closures) was two to three orders of magnitude larger than the closure itself could plausibly cause, and in the CalFresh checks ran in the wrong direction (enrollment *below* the synthetic counterfactual). Both are attributed to confounding regional shocks (the Great Recession and 2012–2016 drought for check 3) rather than the closures under study. This underscores a general lesson: an extreme placebo rank is a necessary but not sufficient condition for a real effect — a magnitude sanity check against the treatment's actual scale is required before any result is reported as a finding.

### 5.3 A positive control: does the method detect anything at ten times the scale?

To test whether the null results above reflect the method's genuine insensitivity to closures of this size — rather than a general inability to detect any effect — I apply the identical procedure to Prima Wawona's March 2024 Cutler liquidation (5,411 jobs, the largest closure in the underlying project's case-study record), using Tulare County, 1995–2023 pre-period, 2024–2025 post-period.

| Outcome | 2024 gap | 2025 gap | Placebo rank | Result |
|---|---|---|---|---|
| Total county employment | +1,679 (wrong direction) | −2,289 | 21 of 54 (p≈0.38) | No effect |
| NAICS 311 employment | +374 (wrong direction) | −863 | 7 of 54 (p≈0.15) | Most extreme rank in the project, but not significant — and likely the wrong outcome series (see note) |
| Unemployment rate | +0.5 pt | +0.3 pt | 18 of 54 (p≈0.35) | No effect |

*Note:* independent verification (a commercial NAICS classification database, profile dated while the facility operated) indicates Prima Wawona's operating entity was classified under NAICS 424480 (fresh produce merchant wholesale), not NAICS 311 — meaning its workforce was likely never counted in the food-manufacturing series this project's SDI and synthetic-control analysis is built on. The NAICS 311 result above is treated as uninformative for that reason, not as a near-miss. **Total employment — the outcome actually matched to this closure — is squarely null (rank 21 of 54).** Even at nearly ten times Olam's scale, the correctly-matched outcome series shows no detectable effect, suggesting the method's insensitivity across Sections 5.1–5.2 is not merely a function of closure size within the range tested here.

### 5.4 How large an effect would this method actually detect?

Reading the spread of post-period RMSPE (root-mean-squared prediction error) across the full placebo distribution gives a direct estimate of this method's detection threshold in the same units as the outcome itself (jobs):

| | Kings (Olam, 567 jobs) | Tulare (Land O'Lakes, 80 jobs) |
|---|---|---|
| Avg. total employment, pre-period | 38,919 | 129,381 |
| Real closure's post-period RMSPE | 939 jobs | 4,760 jobs |
| Placebo distribution, median | 1,172 jobs | 5,117 jobs |
| Placebo distribution, 90th pctile | 7,697 jobs | 18,029 jobs |

Both real closures fit their synthetic counterfactuals about as well as, or better than, a typical untreated county fits its own — to register as unusual at even a loose p≈0.10 threshold would require a sustained gap 14–225 times larger than the closures actually tested. Prima Wawona's own post-period RMSPE (≈2,007 jobs, on a closure nearly ten times Olam's size) remains below the *median* placebo county's typical fit error in the same donor pool — a concrete illustration of how much noise this instrument is working against.

## 6. Discussion

The consistent null result across ten checks, two closures, five outcome families, and three geographies is not evidence that these closures had no real effect on anyone. It is evidence that **county-level (and city- and district-level) aggregate statistics are structurally the wrong instrument to detect that effect** — precisely the finding Jacobson, LaLonde & Sullivan (1993) established for individual displaced workers using linked administrative wage records, which show large, persistent individual earnings losses even where aggregate county statistics show nothing. The present results extend that finding, empirically, to a regional food-processing setting and to a battery of outcome variables (migration, benefit enrollment, school enrollment, taxable sales) well beyond employment and unemployment rate alone — none of which detect an effect either.

This has a direct methodological implication for public program evaluation more broadly: a program whose own evaluation of labor-market effects relies on county- or regional-aggregate data — a common and inexpensive approach — risks the same false-negative problem documented here, independent of whether the program's underlying effect is real. The right instrument, following Jacobson et al. and the results above, is individual- or worker-level data: linked unemployment-insurance wage records, or the closest public approximation, Census LEHD's Quarterly Workforce Indicators — which itself, as used in Checks 4–5 above, can show aggregate separations and pre-separation pay but not where a specific displaced worker went or what they earned next.

## 7. Limitations

- **Scope.** Every figure in this paper measures NAICS 311 (food *manufacturing* — processing, canning, packing), not NAICS 111 (crop production). Field/farm labor is a different workforce with a different, weaker exposure channel to any single plant's closure, and was not measured here.
- **Closed-labor-market assumption.** County-level measures (including the underlying SDI) compare where people *work*, not where they *live*; cross-county commuting, which is real and documented in the Central Valley, is not captured.
- **Small sample of closures.** Two primary closures (plus one positive-control closure) is not a large-N test of the method's general sensitivity; it establishes a specific, well-documented detection threshold for closures in this size range and these donor pools, not a universal claim.
- **Migration data coverage.** IRS SOI migration data available for this analysis runs through 2022-23 only, and matches calendar years to tax-filing years approximately, not exactly.
- **Not a claim of no harm.** This paper does not claim, and should not be read as claiming, that the workers displaced by either closure were unaffected — only that the aggregate instruments tested here cannot detect whatever effect occurred (see Section 6).

## 8. Conclusion and directions for future work

A rigorous, ten-check synthetic-control test finds no detectable effect of two real Central Valley food-processing closures on any county-, city-, or district-level aggregate outcome tested — a result that is itself informative once read against the established displaced-worker literature, rather than a dead end. The clearest implication for future applied work, including a planned extension of this project to California's Multibenefit Land Repurposing Program (MLRP), is methodological: evaluating whether a policy's claimed labor-market benefits reach a specific displaced population requires data and a research design pitched at the population actually affected — not aggregate county statistics, which this paper shows can fail to detect even a well-documented, ten-times-larger closure.

## References

- Abadie, A., Diamond, A., & Hainmueller, J. (2010). "Synthetic Control Methods for Comparative Case Studies: Estimating the Effect of California's Tobacco Control Program." *Journal of the American Statistical Association*. https://doi.org/10.1198/jasa.2009.ap08746
- Jacobson, L. S., LaLonde, R. J., & Sullivan, D. G. (1993). "Earnings Losses of Displaced Workers." *American Economic Review*. https://www.jstor.org/stable/2117574
- Markey, S., Pierce, J. T., Vodden, K., & Roseland, M. (2005). *Second Growth: Community Economic Development in Rural British Columbia.* UBC Press.
- U.S. Bureau of Labor Statistics. Quarterly Census of Employment and Wages (QCEW); Local Area Unemployment Statistics (LAUS).
- U.S. Census Bureau. LEHD Quarterly Workforce Indicators (QWI); state exports/imports by NAICS (bulk files).
- U.S. Bureau of Economic Analysis. Regional Economic Accounts (SAGDP2).
- California Department of Social Services. CalFresh Participation and Benefit Issuance Report (DFA 256 / CF 256).
- California Department of Tax and Fee Administration. Taxable Sales, by City.
- California Department of Education. Historical School Enrollment data files.
- Internal Revenue Service. Statistics of Income (SOI), County-to-County Migration Data.
- California Employment Development Department. WARN Act filings.

---
*Underlying data, code (`methodology/synthetic_control.py`), and the live, interactive version of the Sector Dependence Index are published at secondgrowthresearch.org.*
