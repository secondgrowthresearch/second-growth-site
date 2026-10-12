# The gap the numbers don't show

Every closure in our [case studies](case-studies.md) documents a real company decision and a real headcount. What those pages don't do is show what happened to the county's economy *because* of any single closure — a plant closing and a county's employment numbers moving are both real, but showing one caused the other needs a different kind of check than a case study can give. This page documents that check: a real statistical method, run five independent ways, that consistently could not find a county-level effect large enough to distinguish from ordinary economic noise — and why that result is itself worth publishing, not a dead end.

<div class="stat-pair">
  <div class="stat-card">
    <p class="stat-number" data-target="5" data-decimals="0">0</p>
    <p class="stat-label">Independent checks run — two closures, three data sources, county and town geography, annual and quarterly precision.</p>
  </div>
  <div class="stat-card stat-card--absence">
    <p class="stat-number" data-target="0" data-decimals="0">0</p>
    <p class="stat-label">Checks that found an effect both statistically distinguishable from noise and plausible in size given the closure's own scale.</p>
  </div>
</div>

## What we were trying to measure

A plant closes. The county's total employment the following year is some number. Is that number lower than it *would have been* without the closure? Answering that needs a counterfactual — a credible guess at what the county's economy would have done anyway — and a single county obviously can't run twice, once with the closure and once without.

**Synthetic control** (Abadie, Diamond & Hainmueller, 2010) is the standard tool economists built for exactly this problem: take a pool of counties that *didn't* have the closure, and find the weighted combination of them whose economic trajectory best matches the treated county's trajectory *before* the closure. That weighted combination, projected forward, is the synthetic counterfactual. The gap between the real county's path and its synthetic twin's path, after the closure, is the estimated effect — and because there's no way to compute a classical p-value for a single treated county, the standard check is a **placebo test**: rerun the identical procedure on every *other* county in the donor pool, as if each one were the treated county, and see whether the real county's gap is actually unusual next to that whole distribution, or just ordinary county-to-county noise.

We built this method directly (`methodology/synthetic_control.py` in the project's research repository) rather than relying on a packaged tool, specifically so every step is checkable.

## What five checks on the same two closures found

<div class="chart">
  <p class="chart-title">Kings County total employment: real vs. synthetic, 1990–2025</p>
  <p class="chart-subtitle">Olam's Lemoore tomato plant closed July 2020 (567 jobs). The two lines track each other closely through the entire post-closure period — no visible divergence.</p>
  <svg viewBox="0 0 830 300" role="img" aria-labelledby="sc-chart-title sc-chart-desc">
    <title id="sc-chart-title">Kings County total covered employment, real vs. synthetic control, 1990–2025</title>
    <desc id="sc-chart-desc">The real and synthetic employment lines for Kings County track closely together for the entire 36-year period, including the six years after Olam's 2020 closure, with no sustained divergence.</desc>
    <line class="gridline" x1="50" y1="228.3" x2="740" y2="228.3"></line>
    <line class="gridline" x1="50" y1="186.7" x2="740" y2="186.7"></line>
    <line class="gridline" x1="50" y1="145.0" x2="740" y2="145.0"></line>
    <line class="gridline" x1="50" y1="103.3" x2="740" y2="103.3"></line>
    <line class="gridline" x1="50" y1="61.7"  x2="740" y2="61.7"></line>
    <line class="gridline" x1="50" y1="20.0"  x2="740" y2="20.0"></line>
    <text x="44" y="232" text-anchor="end" font-size="12">30k</text>
    <text x="44" y="190" text-anchor="end" font-size="12">35k</text>
    <text x="44" y="149" text-anchor="end" font-size="12">40k</text>
    <text x="44" y="107" text-anchor="end" font-size="12">45k</text>
    <text x="44" y="65"  text-anchor="end" font-size="12">50k</text>
    <text x="44" y="24"  text-anchor="end" font-size="12">55k</text>

    <line x1="641.4" y1="20" x2="641.4" y2="270" stroke="var(--chart-muted)" stroke-width="1.5" stroke-dasharray="4 3"></line>
    <text x="645" y="30" font-size="10.5" fill="var(--chart-text-secondary)">Olam closes, 2020</text>

    <path fill="none" stroke="var(--chart-cat-2)" stroke-width="2" stroke-dasharray="6 4" stroke-linejoin="round" stroke-linecap="round"
      d="M50.0,222.1 69.7,222.8 89.4,221.7 109.1,218.5 128.9,210.6 148.6,203.7 168.3,197.2 188.0,190.0 207.7,186.6 227.4,175.8 247.1,173.3 266.9,168.8 286.6,164.7 306.3,157.9 326.0,153.7 345.7,143.4 365.4,129.5 385.1,122.7 404.9,123.4 424.6,139.9 444.3,142.8 464.0,141.6 483.7,130.7 503.4,122.3 523.1,112.0 542.9,101.3 562.6,95.9 582.3,90.3 602.0,83.1 621.7,73.9 641.4,89.3 661.1,74.8 680.9,59.4 700.6,58.0 720.3,54.1 740.0,52.3"></path>

    <path fill="none" stroke="var(--chart-cat-1)" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"
      d="M50.0,224.5 69.7,223.7 89.4,222.0 109.1,216.7 128.9,205.9 148.6,207.6 168.3,179.2 188.0,174.2 207.7,193.3 227.4,191.8 247.1,174.5 266.9,175.4 286.6,173.8 306.3,160.7 326.0,156.8 345.7,145.7 365.4,129.0 385.1,113.0 404.9,121.1 424.6,133.7 444.3,139.0 464.0,140.1 483.7,137.3 503.4,132.2 523.1,118.6 542.9,97.2 562.6,96.0 582.3,87.7 602.0,78.3 621.7,71.2 641.4,88.4 661.1,88.2 680.9,70.1 700.6,61.8 720.3,55.0 740.0,44.7"></path>

    <text x="745" y="48" font-size="11" font-weight="700" fill="var(--chart-cat-1)">Real</text>
    <text x="745" y="56" font-size="11" font-weight="700" fill="var(--chart-cat-2)">Synthetic</text>

    <text x="50" y="290" text-anchor="start" font-size="10.5">1990</text>
    <text x="641.4" y="290" text-anchor="middle" font-size="10.5">2020</text>
    <text x="740" y="290" text-anchor="end" font-size="10.5">2025</text>
    <line class="axis-line" x1="50" y1="270" x2="740" y2="270"></line>
  </svg>
  <p class="chart-source">Source: BLS QCEW, Second Growth synthetic-control calculation. Donor pool: 54 California counties. Placebo-test rank: 45th of 54 comparable counties — not distinguishable from ordinary cross-county variation. See the full table below for every outcome checked.</p>
</div>

<div class="table-scroll">
<table>
  <thead><tr><th>Check</th><th>Closure</th><th>Geography</th><th>Outcome</th><th>Result</th></tr></thead>
  <tbody>
    <tr><td rowspan="3">1</td><td rowspan="3">Olam, Lemoore (Kings), 2020 — 567 jobs</td><td rowspan="3">County</td><td>Total employment</td><td>No effect (placebo rank 45 of 54)</td></tr>
    <tr><td>Food-manufacturing employment</td><td>No effect distinguishable from noise (rank 18 of 54, p≈0.35)</td></tr>
    <tr><td>Unemployment rate</td><td>No effect (rank 44 of 54)</td></tr>
    <tr><td>2</td><td>Olam, Lemoore, 2020</td><td>Town (Lemoore city)</td><td>Unemployment rate</td><td>No effect (rank 138 of 271); real rate ran <em>below</em> synthetic every post-treatment year</td></tr>
    <tr><td rowspan="3">3</td><td rowspan="3">Land O'Lakes, Tulare, 2010 — 80 jobs</td><td rowspan="3">County</td><td>Total employment</td><td>Gap looked significant (rank 4 of 30) but was 2–3 orders of magnitude too large for an 80-job closure — not a real effect, see below</td></tr>
    <tr><td>Food-manufacturing employment</td><td>No effect (rank 16 of 21)</td></tr>
    <tr><td>Unemployment rate</td><td>No effect (rank 25 of 27)</td></tr>
    <tr><td>4</td><td>Olam, Lemoore, 2020</td><td>County, quarterly</td><td>Peak-season (Q3) food-mfg. employment</td><td>No effect once checked against full history (rank 15 of 25, p≈0.62) — see below</td></tr>
    <tr><td rowspan="2">5</td><td rowspan="2">Olam, Lemoore, 2020</td><td rowspan="2">County, quarterly</td><td>Avg. earnings, stable workforce</td><td>No effect (rank 16 of 36)</td></tr>
    <tr><td>Avg. earnings, separating workers</td><td>No effect (rank 26 of 27)</td></tr>
  </tbody>
</table>
</div>

## Two bugs and one false positive, caught before they became wrong claims

<div class="research-note">
<span class="research-note-label">What we found</span>
The first version of our weight-fitting code used a general-purpose optimizer (scipy's SLSQP) that <strong>silently returned its own unoptimized starting guess while reporting success</strong> — caught only because we tested it against a case with a known, exact answer first, not because anything looked wrong on the real data. Switching to a different solver (trust-constr, with an exact gradient and Hessian supplied) fixed it; we now keep that test in the project's methodology repository specifically so this can't regress unnoticed.
</div>

<div class="research-note">
<span class="research-note-label">What we found</span>
The town-level placebo test (check 2, above) initially produced a placebo-ratio distribution with a maximum value of <strong>46 million</strong> — not a real result, but a divide-by-near-zero artifact: a handful of the 271 comparison towns had an almost perfectly flat pre-closure trend, trivial to fit, so any tiny post-period wobble produced an absurd ratio. Filtering to only the placebo towns whose pre-closure fit quality was actually comparable to Lemoore's own fixed it — and changed the honest conclusion from "looks significant" to "no effect."
</div>

<div class="research-note">
<span class="research-note-label">What we found</span>
Check 3's Tulare total-employment result looked like the strongest finding of the whole exercise by its statistical rank — until we checked the actual size of the gap against the actual size of the closure. Land O'Lakes eliminated 80 jobs; the "gap" we found ran 4,700 to 14,400 jobs below the synthetic counterfactual, every year from 2011 to 2023. An 80-job closure cannot plausibly produce a gap two to three orders of magnitude larger than itself. We read this as the Great Recession's uneven regional recovery and the 2012–2016 drought hitting Tulare's agriculture-heavy economy — both real, both coinciding with the closure, neither caused by it. Logged as a misattribution risk we caught, not a finding about Land O'Lakes.
</div>

<div class="research-note">
<span class="research-note-label">What we found</span>
Check 4 started from a real, separate observation: quarterly data showed no separations spike in the exact quarter Olam's closure took effect. The explanation turned out to matter — Central Valley food processing is strongly seasonal, so a permanent closure's effect should show up as a <em>missing seasonal hiring surge</em>, not an active layoff spike, since workers who'd have been seasonally rehired simply weren't. Looking only at peak-season (Q3) employment, Kings County's food-manufacturing workforce looked like it had stepped down by roughly 600 jobs in 2020 and never recovered — compelling by eye, and wrong: checked against the county's own full 1992–2025 history rather than just the unusually high years right before 2020, gaps of that size turn out to be ordinary for this specific series. The lesson applies beyond this one check: a short comparison window plus ordinary mean reversion looks exactly like a structural break if it isn't tested against a unit's own full history.
</div>

## Why a consistent null result is itself informative

None of this means Olam's or Land O'Lakes' workers weren't really affected. It means **county-level aggregate statistics are structurally the wrong instrument to find out** — and that's not a guess, it's the central, well-replicated finding of the actual economics literature on mass layoffs. Jacobson, LaLonde & Sullivan's 1993 study (and three decades of work since) found that individually displaced workers suffer large, persistent earnings losses — commonly 15–25% or more, for years — in counties where the *aggregate* employment and unemployment rate show no detectable effect at all. That isn't a contradiction in their results. It's the expected pattern: a county's aggregate economy absorbs a few hundred lost jobs through ordinary hiring and churn, even while the specific people who lost those jobs don't recover what they had.

The right instrument for "were real people hurt" is individual worker records — state unemployment-insurance wage records, linked across employers over time. Those records exist. They are not public, and were not available to this project. Census LEHD's Quarterly Workforce Indicators (used in checks 4 and 5, above) is the closest public approximation — real, quarterly, NAICS-specific flow data — and even it stops short of showing where a specific displaced worker went or what they earned next; it can only show aggregate separation counts and the pay of workers immediately before they left.

## A gap in what this project has actually measured

Every number in this entire check, and in the [Sector Dependence Index](the-index.md) itself, measures **NAICS 311 — food *manufacturing*: processing, canning, packing.** It does not measure NAICS 111, crop production — the field labor that grows what these plants process. Those are different workforces, different employers, and a different, weaker exposure channel: a grower who loses one buyer can often still sell to a different processor, so a single plant's closure doesn't automatically translate into reduced demand for field labor the way it directly eliminates processing-line jobs. This project's language elsewhere sometimes refers to "the farm-labor economy" broadly; the data behind every closure case study and every SDI figure has only ever covered the processing side of that economy. We're naming that precisely here so it isn't left to blur.

## What this doesn't claim

- **This is not evidence that Olam's or Land O'Lakes' closures had no real effect on anyone.** It's evidence that county-level aggregate data couldn't detect one — a different, narrower claim.
- **We are not asserting field/farm labor was unaffected by either closure.** This check never measured that population at all; see above.
- **The Q3 "seasonal hiring surge" explanation (check 4) is a plausible mechanism we checked and found didn't hold up statistically** — it's documented because the reasoning behind it is sound and may apply better to a different closure, not because it was confirmed here.
- **We are not recommending against trying this method on a different closure or a different outcome.** Five checks on two closures is not exhaustive — it's what this pass covered, logged honestly either way.

## Sources

- Abadie, A., Diamond, A., & Hainmueller, J., ["Synthetic Control Methods for Comparative Case Studies: Estimating the Effect of California's Tobacco Control Program,"](https://doi.org/10.1198/jasa.2009.ap08746) *Journal of the American Statistical Association* (2010) — the method's original statement.
- Jacobson, L. S., LaLonde, R. J., & Sullivan, D. G., ["Earnings Losses of Displaced Workers,"](https://www.jstor.org/stable/2117574) *American Economic Review* (1993) — the founding result on individual displaced-worker earnings losses persisting despite no detectable aggregate effect.
- U.S. Bureau of Labor Statistics, Quarterly Census of Employment and Wages (QCEW) and Local Area Unemployment Statistics (LAUS) — the same sources behind [the Index](the-index.md); extended here to a 54-county donor pool and to incorporated-city geography.
- U.S. Census Bureau, LEHD Quarterly Workforce Indicators (QWI) — quarterly, NAICS-specific employment, hires, separations, and earnings; bulk file, not the API.
- This project's own case studies: [Olam's Lemoore closure](case-studies/kings-2020-olam-lemoore.md) and [Land O'Lakes' Tulare closure](case-studies/tulare-2010-land-olakes-tulare.md).

Full citation detail and source archive: [Data](data.md). Back to [Case Studies](case-studies.md) and [the Index](the-index.md).
