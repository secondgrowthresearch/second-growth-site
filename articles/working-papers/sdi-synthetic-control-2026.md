# Do Plant Closures Show Up in County-Level Economic Data?
## A synthetic-control test of two Central Valley food-processing closures

This page is a single, citable synthesis of work already published piece by piece elsewhere on this site — the [Sector Dependence Index](../the-index.md), the [synthetic-control method](../synthetic-control.md), and the [data and methodology](../methodology.md) behind both. It adds no new data; it packages an existing result into the form a researcher, reviewer, or outside collaborator can read and cite on its own.

## Summary

We tested whether two real Central Valley food-processing plant closures — Olam's Lemoore tomato-processing facility (567 jobs, July 2020) and Land O'Lakes' Tulare plant (80 jobs, 2010) — produced a detectable effect on local economic indicators, using the synthetic control method (Abadie, Diamond & Hainmueller, 2010). Across ten independent checks spanning county, city, and school-district geography, five outcome variables, and both annual and quarterly precision, **no effect was distinguishable from ordinary cross-unit noise in any check.** A positive control — the same method applied to a closure roughly ten times larger (Prima Wawona's 2024 Cutler liquidation, 5,411 jobs) — was also null on its correctly-matched outcome variable, which argues against the null being simply an artifact of small closure size within the range tested.

That null result is itself informative, not a dead end. It replicates, at the regional level, the central finding of the labor-displacement literature (Jacobson, LaLonde & Sullivan, 1993): aggregate statistics are structurally the wrong instrument for detecting individual worker harm, even when that harm is real. The direct implication for program evaluation: a program that measures its own labor-market effects using county- or regional-aggregate data — a common, inexpensive approach — risks the same false-negative problem documented here, independent of whether the underlying effect is real.

## Why this test

A plant closes, and a county's employment figures move the following year. Attributing the second fact to the first requires a counterfactual — a credible estimate of what the county's economy would have done in the closure's absence. The [Sector Dependence Index](../the-index.md) establishes *why* a closure like Olam's matters to Kings County's economic base in the first place: food manufacturing's Employment SDI there rose from 0.070 in 1990 to a peak of 0.419 in 2017, before falling to 0.150 by 2025. This test asks whether that theoretical importance is actually detectable in the county's own data.

## Method

[Synthetic control](../synthetic-control.md) constructs a counterfactual for a treated county, city, or school district as a weighted combination of untreated "donor" units, chosen so the combination's pre-treatment trajectory best matches the treated unit's own. The gap between the treated unit's realized post-treatment path and its synthetic counterfactual is the estimated effect.

Because a single treated unit precludes a classical hypothesis test, we use the standard placebo test: the identical procedure is rerun with every other donor-pool unit treated as if it were the real one, producing a distribution of placebo effect sizes the real result is ranked against. A result only counts as informative if that rank is extreme *and* the implied magnitude is plausible given the closure's actual size — a second check that proved necessary (see below). The method was implemented directly, not via a packaged library, specifically so each step is auditable. Full data sources: [Methodology](../methodology.md) and [Data](../data.md).

## Results

### Ten checks, two closures, no detected effect

| # | Closure | Geography | Outcome | Result |
|---|---|---|---|---|
| 1 | Olam, Lemoore (Kings), 2020 — 567 jobs | County | Total employment | No effect (placebo rank 45 of 54) |
| 1 | — | County | Food-mfg. employment | No effect (rank 18 of 54, p≈0.35) |
| 1 | — | County | Unemployment rate | No effect (rank 44 of 54) |
| 2 | Olam, Lemoore, 2020 | Town (Lemoore city) | Unemployment rate | No effect (rank 138 of 271); real ran *below* synthetic every post-treatment year |
| 3 | Land O'Lakes, Tulare, 2010 — 80 jobs | County | Total employment | Rank 4 of 30 looked significant but the gap was 2–3 orders of magnitude too large for an 80-job closure — not a real effect (see below) |
| 3 | — | County | Food-mfg. employment | No effect (rank 16 of 21) |
| 3 | — | County | Unemployment rate | No effect (rank 25 of 27) |
| 4 | Olam, Lemoore, 2020 | County, quarterly | Peak-season (Q3) food-mfg. employment | No effect once checked against full 1992–2025 history (rank 15 of 25, p≈0.62) |
| 5 | Olam, Lemoore, 2020 | County, quarterly | Avg. earnings, stable workforce | No effect (rank 16 of 36) |
| 5 | — | County, quarterly | Avg. earnings, separating workers | No effect (rank 26 of 27) |
| 6 | Land O'Lakes, Tulare, 2010 | County | CalFresh (SNAP) enrollment | Rank 2 of 24 looked significant but the gap reached 43,800 people by 2023 and ran the wrong direction — not a real effect (see below) |
| 7 | Olam, Lemoore, 2020 | County | CalFresh (SNAP) enrollment | Same problem, smaller scale (rank 1 of 21, 8,000-person gap, wrong direction) |
| 8 | Olam, Lemoore, 2020 | City, quarterly | Taxable sales receipts | No effect (rank 40 of 49 sampled placebo cities, p≈0.82) |
| 9 | Olam, Lemoore, 2020 | School district, annual | Elementary / high-school enrollment | No effect (rank 30 of 50, p≈0.61); real ran *above* synthetic — wrong direction for harm |
| 9 | Land O'Lakes, Tulare, 2010 | School district, annual | Elementary / high-school enrollment | No effect (rank 18–40 of 31–40, p≈0.29–0.59) |
| 10 | Both closures | County, annual | Net / gross migration (IRS SOI) | No effect in all four checks (ranks 15–45 of 54, p≈0.29–0.84) |

### Two false positives, caught before publication

Two checks (3 and 6/7) initially produced the most statistically extreme placebo ranks in the project — and both turned out to be artifacts. In each case the implied gap (4,700–14,400 jobs for an 80-job closure; 8,000–43,800 CalFresh enrollees for 80- and 567-job closures) was two to three orders of magnitude larger than the closure itself could plausibly cause, and the CalFresh checks ran in the wrong direction (enrollment *below* the synthetic counterfactual). Both are attributed to confounding regional shocks — the Great Recession and the 2012–2016 drought — rather than the closures under study. The general lesson: an extreme placebo rank is necessary but not sufficient for a real effect. A magnitude sanity check against the treatment's actual scale is required before any result ships as a finding.

### A positive control: does the method detect anything at ten times the scale?

To test whether the null results above reflect the method's genuine insensitivity to closures of this size — rather than a general inability to detect any effect — we applied the identical procedure to Prima Wawona's March 2024 Cutler liquidation (5,411 jobs, the largest closure in this project's case-study record), using Tulare County, 1995–2023 pre-period, 2024–2025 post-period.

| Outcome | 2024 gap | 2025 gap | Placebo rank | Result |
|---|---|---|---|---|
| Total county employment | +1,679 (wrong direction) | −2,289 | 21 of 54 (p≈0.38) | No effect |
| NAICS 311 employment | +374 (wrong direction) | −863 | 7 of 54 (p≈0.15) | Most extreme rank in the project, but not significant — and likely the wrong outcome series (see note) |
| Unemployment rate | +0.5 pt | +0.3 pt | 18 of 54 (p≈0.35) | No effect |

*Note:* independent verification (a commercial NAICS classification database, profile dated while the facility operated) indicates Prima Wawona's operating entity was classified under NAICS 424480 (fresh produce merchant wholesale), not NAICS 311 — meaning its workforce was likely never counted in the food-manufacturing series this project's SDI and synthetic-control analysis is built on. The NAICS 311 result above is treated as uninformative for that reason, not as a near-miss. **Total employment — the outcome actually matched to this closure — is squarely null (rank 21 of 54).** Even at nearly ten times Olam's scale, the correctly-matched outcome series shows no detectable effect, which argues against the insensitivity in the checks above being merely a function of closure size within the range tested here.

### How large an effect would this method actually detect?

Reading the spread of post-period RMSPE (root-mean-squared prediction error) across the full placebo distribution gives a direct estimate of this method's detection threshold, in the same units as the outcome itself (jobs):

| | Kings (Olam, 567 jobs) | Tulare (Land O'Lakes, 80 jobs) |
|---|---|---|
| Avg. total employment, pre-period | 38,919 | 129,381 |
| Real closure's post-period RMSPE | 939 jobs | 4,760 jobs |
| Placebo distribution, median | 1,172 jobs | 5,117 jobs |
| Placebo distribution, 90th pctile | 7,697 jobs | 18,029 jobs |

Both real closures fit their synthetic counterfactuals about as well as, or better than, a typical untreated county fits its own — registering as unusual at even a loose p≈0.10 threshold would require a sustained gap 14–225 times larger than the closures actually tested. Prima Wawona's own post-period RMSPE (≈2,007 jobs, on a closure nearly ten times Olam's size) remains below the *median* placebo county's typical fit error in the same donor pool — a concrete illustration of how much noise this instrument is working against.

## Discussion

A consistent null result across ten checks, two closures, five outcome families, and three geographies is not evidence that these closures had no real effect on anyone. It is evidence that **county-level (and city- and district-level) aggregate statistics are structurally the wrong instrument to detect that effect** — precisely the finding Jacobson, LaLonde & Sullivan (1993) established for individual displaced workers using linked administrative wage records, which show large, persistent individual earnings losses even where aggregate county statistics show nothing. These results extend that finding, empirically, to a regional food-processing setting and to a battery of outcome variables (migration, benefit enrollment, school enrollment, taxable sales) well beyond employment and unemployment rate alone — none of which detect an effect either.

This has a direct implication for public program evaluation more broadly: a program whose own evaluation of labor-market effects relies on county- or regional-aggregate data — a common, inexpensive approach — risks the same false-negative problem documented here, independent of whether the program's underlying effect is real. The right instrument, following Jacobson et al. and the results above, is individual- or worker-level data: linked unemployment-insurance wage records, or the closest public approximation, Census LEHD's Quarterly Workforce Indicators — which itself, as used above, can show aggregate separations and pre-separation pay but not where a specific displaced worker went or what they earned next.

## Limitations

- **Scope.** Every figure here measures NAICS 311 (food *manufacturing* — processing, canning, packing), not NAICS 111 (crop production). Field/farm labor is a different workforce with a different, weaker exposure channel to any single plant's closure, and isn't measured here.
- **Closed-labor-market assumption.** County-level measures (including the underlying SDI) compare where people *work*, not where they *live*; cross-county commuting, which is real and documented in the Central Valley, isn't captured.
- **Small sample of closures.** Two primary closures plus one positive control isn't a large-N test of the method's general sensitivity; it establishes a specific, well-documented detection threshold for closures in this size range and these donor pools, not a universal claim.
- **Migration data coverage.** IRS SOI migration data available for this analysis runs through 2022-23 only, and matches calendar years to tax-filing years approximately, not exactly.
- **Not a claim of no harm.** This page does not claim, and shouldn't be read as claiming, that the workers displaced by either closure were unaffected — only that the aggregate instruments tested here can't detect whatever effect occurred (see Discussion).

## What this motivates next

The clearest implication for further applied work is methodological: evaluating whether a policy's claimed labor-market benefits reach a specific displaced population requires data and a research design pitched at the population actually affected, not aggregate county statistics — which this page shows can fail to detect even a well-documented, ten-times-larger closure. That is the starting point for [our methodology memo on California's Multibenefit Land Repurposing Program](mlrp-methodology-memo-2026.md), which extends this same detection-threshold finding to a live state program.

## Sources

- Abadie, A., Diamond, A., & Hainmueller, J., ["Synthetic Control Methods for Comparative Case Studies: Estimating the Effect of California's Tobacco Control Program,"](https://doi.org/10.1198/jasa.2009.ap08746) *Journal of the American Statistical Association* (2010) — the method's original statement.
- Jacobson, L. S., LaLonde, R. J., & Sullivan, D. G., ["Earnings Losses of Displaced Workers,"](https://www.jstor.org/stable/2117574) *American Economic Review* (1993) — the founding result this page's discussion extends.
- Markey, S., Pierce, J. T., Vodden, K., & Roseland, M., *Second Growth: Community Economic Development in Rural British Columbia* (UBC Press, 2005) — the source of this project's name.
- All underlying employment, trade, benefit-enrollment, tax, school, and migration data, with full access notes: see [Measuring Closures](../synthetic-control.md) and [Data](../data.md).

Back to [Working Papers](../working-papers.md), [the Index](../the-index.md), and [Case Studies](../case-studies.md).
