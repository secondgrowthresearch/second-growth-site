# Does MLRP's Claimed Employment Co-Benefit Reach the Farm Labor It Displaces?
## A methodology memo

California's Multibenefit Land Repurposing Program (MLRP) pays landowners to take farmland out of production for groundwater, habitat, flood, and community-health benefits. One of the co-benefits the program's own materials claim is "Employment Opportunities." This memo asks a narrow question: when land comes out of production, does the farm labor that worked it actually capture whatever new employment the repurposing creates, or does someone else?

This question has a direct model. Dr. Emanuel Alcala's 2024 CVHPI study of south Fresno warehouse development asked the same thing about a different land-use shift: did local residents capture the new jobs, or did commuting outsiders? Alcala's method was a simple before/after comparison (2015 vs. 2021, per the brief's own errata), with no formal control group. The share of residents both living and employed in the tract fell 16.5% near the Amazon fulfillment center and 5.5% near the Ulta distribution center, while employment held by people living outside each tract grew 44% and 18% respectively. That result is the direct template for this question.

## What MLRP's own data currently shows

Before proposing a design, it's worth being honest about what currently exists to measure. We pulled the state's own June 2023 Regional Block Grant awards list and the 2025 MLRP Annual Report (51 pages, Department of Conservation) directly, for the four counties this project already covers:

- **Kings/Fresno (Westside Subbasin, Westlands Water District GSA):** still in planning. The region's Multibenefit Agricultural Land Repurposing Plan (MALRP) only went to public review in August–September 2025, and the implementation packet was just submitted to the state. No approved acreage, no jobs claim of any kind yet.
- **Tulare (Kaweah Subbasin + Tule Subbasin):** the most advanced of the four. Five approved implementation projects (Paregien Basin Phase II, 55 acres; Flying Dragon Ranch, 58 acres; Wuk'nain Riparian Restoration, 10+ acres; Mathews Ditch Basin, ~100 acres; Johnson Slough Basin, 25 acres) plus a 400+ acre land-fallowing and cover-cropping program in the Tule Subbasin. None of these project descriptions mention employment.
- **Stanislaus (Turlock Subbasin):** four small pilot projects totaling 58 acres (Braden Farms, Rainbow Farms, Sperry Farms, Santa Fe Ranch), against a stated regional target of "up to 5,000 acres of orchard removal." No employment mentioned.

Directly from the state's own 2025 report: *"little data exists for the Jobs Created indicator, as most projects are in very early stages of implementation."* Job creation is listed as an **optional, self-reported** program indicator, not an independently measured one. Across the full 51-page report, the only mention of farm labor at the individual-project level is one line on an unrelated Merced County project: "supporting farmer, rancher, and farm worker leadership through cover cropping." It's not a measured outcome, just a phrase.

This matters for what follows: the question this memo asks can't yet be answered with existing MLRP data, because the relevant data mostly doesn't exist. The contribution here is a design for how it should be measured once it does, not an analysis of results that don't yet exist.

## The displacement-capture parallel

Alcala's framing, applied directly to MLRP: when land goes out of row-crop or orchard production and into habitat, recharge, or flood infrastructure, two different kinds of labor are in play.

1. **The labor displaced.** The farmworkers who worked that specific parcel before repurposing: planting, pruning, irrigating, harvesting. This is the population whose livelihood the land-use change directly removes.
2. **The labor the project creates.** Habitat restoration, recharge-basin construction, swale building, and ongoing maintenance all require labor too — some of it skilled (engineering, environmental consulting), some of it not (site clearing, planting, long-term upkeep).

The resident-vs-outsider question becomes: does the displaced farm labor from (1) have any realistic path into the jobs created by (2), or are those jobs captured by specialized contractors, environmental consulting firms, and construction crews with no connection to the land's prior agricultural workforce? Alcala found, for a structurally similar land-use transition, that local residents lost ground rather than gained it. There's no reason to assume MLRP's labor market behaves differently by default. There's also no evidence yet, one way or the other, because the data doesn't exist (see above).

Alcala's own measure has a version of this same resolution problem, one level down. His resident-capture figure is tract-wide — people who both live and work anywhere in census tract 15 or 18 — not people specifically hired at the Amazon or Ulta facility itself. It answers a firm-level question with a tract-level proxy, the same geographic mismatch our [synthetic-control test](sdi-synthetic-control-2026.md) found at the county level, just one step finer. That's not a flaw unique to his study; it's direct evidence, not just an analogy, for why the design below has to be parcel- and worker-level rather than aggregated at any geography.

A precise version of the question, stated so it could actually be tested once implementation project data matures: **of the people employed on an MLRP project's construction, restoration, and ongoing-maintenance payroll, what share previously worked the specific parcel being repurposed, versus coming from outside that specific displaced workforce?** This is a narrower and more falsifiable question than "did the region gain or lose jobs," which our synthetic-control test already showed is close to undetectable at the scale these projects currently operate at.

## Causal design

Our [synthetic-control test](sdi-synthetic-control-2026.md) established a concrete detection threshold: even a documented 567-job closure, and a 5,411-job positive control, couldn't be distinguished from ordinary county-level noise without a sustained gap 14 to 225 times larger than the real closure. The MLRP projects currently implemented in these four counties are measured in acres, not jobs, and the acreages are small: roughly 250 acres across Tulare's five approved projects, 58 acres across Stanislaus's four pilots, zero yet in Kings/Fresno. Even under generous labor-intensity assumptions, the number of farmworkers affected by land this limited is almost certainly in the single digits to low tens, not hundreds — far below what our synthetic-control test already showed county- or even city-level aggregate data can detect.

This is not an argument for using a better aggregate method instead of a simple before/after comparison. A synthetic control, applied to a treatment this small, would be exactly as underpowered as Alcala's before/after comparison, or any other county-aggregate design. The problem isn't methodological sophistication; it's that the "treatment" itself — acres of land repurposed, and the handful of jobs tied to it — sits below the resolution any aggregate instrument can see.

**The tool already exists.** Alcala's own tract-level numbers come from Census OnTheMap, built on LEHD origin-destination data that matches a specific worksite address to a worker's home census block. That's exactly the matching logic the design below needs, just applied one level finer (parcel, not tract). The gap isn't a missing method; it's that MLRP's implementing contractors don't yet report worksite-level employment the way QCEW-covered employers do. Once worksite addresses are identifiable, the matching step is solved, not novel.

**The design this implies.** Following Jacobson, LaLonde & Sullivan's own resolution to the same structural problem — linked individual wage records, not aggregate statistics — the right design here is parcel- and worker-level, not regional:

- Identify, parcel by parcel, who worked the land before repurposing (farm labor contractor records, UI wage records tied to the specific agricultural employer, or direct outreach through organizations like LCJA or farmworker unions already embedded in these communities).
- Identify, for the same parcel's restoration/construction/maintenance contracts, who is actually hired, and whether any overlap exists with the pre-repurposing workforce — the same worksite-to-residence match OnTheMap already does at the tract level, run instead at the parcel level.
- Track this at the project level as MLRP's own project count grows, rather than waiting for enough acreage to accumulate that a regional aggregate test might someday have power, since the detection-threshold finding above suggests that point is very far off at current project scale.

This is also, concretely, a stronger and more specific design than Alcala's own before/after comparison — not because synthetic control outranks before/after in the abstract, but because it's pitched at the population the question is actually about, the same design lesson our own synthetic-control test drew out for its own two closures.

## The testable claim

Stated so it can fail: **once any MLRP implementation project reports worksite-level payroll data, the share of that payroll held by workers who previously worked the specific parcel being repurposed will be at or below the resident-capture rates Alcala found for a structurally similar land-use shift (16.5% loss near the Amazon center, 5.5% near Ulta) — not higher.**

This is falsifiable in either direction. If displaced farm labor shows up on restoration and maintenance payrolls at a rate comparable to or better than pre-repurposing employment, the claim is wrong, and MLRP's employment co-benefit is real for the people it displaces. If no MLRP data ever reaches worksite-level granularity, the claim is untested, not confirmed — the section above already establishes that this is the current state, and it's the reason this memo proposes a design rather than reports a result.

## Sources

- Alcala, E., Ramirez, A., & Morales, D., [*Fresno Economy and the Environment: A Place-Based Data Brief*](https://chhs.fresnostate.edu/cvhpi/documents/economyenviro.pdf) (Central Valley Health Policy Institute, Fresno State, 2024). *Access: web-blocked — the host refuses automated fetches; confirmed readable directly in a browser.*
- Jacobson, L. S., LaLonde, R. J., & Sullivan, D. G., ["Earnings Losses of Displaced Workers,"](https://www.jstor.org/stable/2117574) *American Economic Review* (1993).
- California Department of Conservation, 2025 MLRP Annual Report; June 2023 Regional Block Grant awards list. *Access: not-captured — a public URL exists for these sources and this project hasn't yet recorded it.*
- This project's own [synthetic-control test](sdi-synthetic-control-2026.md) of two real Central Valley plant closures, whose detection-threshold finding motivates the design above.

Back to [Working Papers](../working-papers.md) and [the Index](../the-index.md).
