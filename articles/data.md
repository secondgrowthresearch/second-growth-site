# Data

Every number we publish is meant to be traceable back to a named, public source — not a proprietary dataset or an unsourced estimate. This page lists what we draw from.

## Employment and wages

**U.S. Bureau of Labor Statistics, Quarterly Census of Employment and Wages (QCEW).** County-level food-manufacturing (NAICS 311) employment and wages for Kings, Fresno, Tulare, and Stanislaus counties, 1990–2026, alongside matching California-statewide and U.S.-national benchmark data. The backbone of the [Sector Dependence Index](the-index.md). Extended to all 58 California counties and to U.S. Bureau of Labor Statistics Local Area Unemployment Statistics (LAUS), at both county and incorporated-city geography, for [the synthetic-control check](synthetic-control.md) on individual plant closures. Extended further, at the 4- and 6-digit subsector level, to NAICS 3114/3115/3116 wage and establishment-count trends for [Consolidation](consolidation.md), to NAICS 115115 (Farm Labor Contractors) and NAICS 111 (Crop Production) for [Who Works Here](who-works-here.md), and to all-sector employment for San Joaquin County's own logistics-sector growth, also on [Consolidation](consolidation.md). The healthcare-diversification figures on [the Index](the-index.md) isolate a single BLS reporting change (NAICS 624120, in-home supportive-care providers newly captured as UI-covered establishments starting with 2013 data) from this same source.

**U.S. Census Bureau, Population Estimates Program, and U.S. Bureau of Economic Analysis, Regional Economic Accounts (county GDP).** Total population, total employment, and county GDP for all eight San Joaquin Valley counties, 1990–2025 — the basis for the regional growth figures on [Home](home.md) and throughout this site's current framing.

**U.S. Census Bureau, LEHD Quarterly Workforce Indicators (QWI).** Quarterly, NAICS-specific employment, hires, separations, and earnings — real flow data, not just stock counts. Used in [the synthetic-control check](synthetic-control.md) to test whether a closure's effect shows up at quarterly precision or in sector pay, after county-level annual data found nothing.

**U.S. Census Bureau, LEHD Job-to-Job Flows (J2J).** Quarterly origin-destination worker-flow data — separations, hires, earnings of job changers, and industry of destination — pulled for the four single-county metro areas this project tracks (Hanford-Corcoran, Visalia-Porterville, Modesto, and Fresno; the Fresno metro area, confirmed directly, actually covers Fresno and Madera counties combined, not Fresno County alone). A step closer than QWI toward seeing where a displaced worker actually went, though J2J's own industry detail tops out at 2-digit NAICS sector — it can't isolate food manufacturing specifically the way QWI can. Acquired; not yet run through this project's synthetic-control pipeline.

**Internal Revenue Service, Statistics of Income (SOI), County-to-County Migration Data.** Annual, county-level gross and net migration built from consecutive-year tax-return address changes, 2007-08 through 2022-23 (2023-24 not yet published). Used in [the synthetic-control check](synthetic-control.md) as a direct residential-mobility measure — the one outcome in that check that doesn't depend on what industry, if any, a displaced worker was reemployed in.

## Trade

**U.S. Census Bureau, state exports and imports by NAICS code.** Monthly, state-level, international trade data for California's food-manufacturing sector, 2010–present — the basis for the real trade adjustment described in [Methodology](methodology.md). Extended to Texas's own NAICS 311 export series and to U.S. NAICS 311 imports from Mexico specifically, for the trade cross-walk in [Same Land, Different Crop](mechanization.md).

**U.S. Census Bureau, international trade data by HS commodity code.** Used in an attempted, so-far-incomplete pull of almond-specific export data to independently check the standard trade-press account of a 2021-2023 export disruption — see [Same Land, Different Crop](mechanization.md) for what was and wasn't retrieved.

## Output

**U.S. Bureau of Economic Analysis, Regional Economic Accounts (SAGDP2).** State-level GDP by industry, used as the output denominator for the trade adjustment.

## Closures and layoffs

**California Employment Development Department, WARN Act filings** — the formal notices employers are required to file ahead of mass layoffs, 2014–present. Paired with original news reporting and, where available, company records, for the specific closures in our [case studies](case-studies.md).

## Land and water

**California Department of Water Resources / Land IQ, Statewide Crop Mapping.** Field-level crop and idle/fallow land classification, 2014–2024. **DWR SGMA groundwater level measurements** for the Kings and Tulare Lake subbasins, and separately for the Kaweah and Tule subbasins — confirmed by direct spatial overlap to be the ones that actually underlie Tulare County, distinct from the first two. Used to document the structural land- and water-use pressure behind the closures we study, and, in [Same Land, Different Crop](mechanization.md), to measure the acreage shift from stone fruit, grapes, and tomatoes into almonds and pistachios, and the resulting change in applied water demand.

## Agricultural statistics

**USDA Census of Agriculture** (county-level, every five years, 1974–2022) and **county Agricultural Commissioner annual crop reports**, for the longest available run of farm counts, acreage, and labor figures in each county we track. Fresno and Tulare's own annual reports break grape acreage out by variety (raisin/table/wine), which Land IQ's satellite classification can't — the basis for identifying which grape type actually accounts for the acreage loss in [Same Land, Different Crop](mechanization.md).

**Real estate press coverage with attributed per-acre land-value figures** (Farm Progress, The Business Journal, Our Valley Voice) — illustrative, press-sourced anchors for recent almond and pistachio land values in [Same Land, Different Crop](mechanization.md), used because no free, public, transaction-based land-value dataset exists at the crop-specific, county level; the one source built for that purpose (the California Chapter of ASFMRA's annual land-value survey) is a paid report this project doesn't have access to.

**USDA NASS Quick Stats, grower price received.** Annual, California state-level, for almonds, pistachios, English walnuts, clingstone peaches, raisin-type grapes, and wine-type grapes — used in [Same Land, Different Crop](mechanization.md) to test whether crop-price collapses, not just labor costs, explain the timing of the acreage shift into tree nuts.

**UC Davis / UC Cooperative Extension, Sample Costs to Produce studies.** California-region-specific, per-acre cost-of-production budgets, including itemized labor hours and dollars for cultural practices and harvest, and applied-water figures — the source for the per-acre labor-cost comparison and the net water-demand calculation in [Same Land, Different Crop](mechanization.md), covering almonds, pistachios, processing peaches, processing tomatoes, and raisin- and wine-type grapes.

## Business establishments

**U.S. Census Bureau, County Business Patterns (CBP), 2023.** County-level establishment counts and employment by size class for food manufacturing (NAICS 311) in Kings, Fresno, Tulare, and Stanislaus counties — a real but imperfect local proxy for *scale*, used in [Consolidation](consolidation.md). Not a firm-level market-share measure; see that page for what this data can and can't show.

**U.S. EPA, Enforcement and Compliance History Online (ECHO).** Environmental-compliance facility registry, NAICS-filtered to food manufacturing — used in [Consolidation](consolidation.md) to build named-firm counts for Kings County's food processors and, separately, for Fresno's poultry/meat sector and Tulare's dairy sector, each cross-checked against CBP's establishment counts. A registry of regulated facilities, not a market-share or revenue dataset; see that page for what this data can and can't show.

## Food assistance

**California Department of Social Services, CalFresh Participation and Benefit Issuance Report (DFA 256, and its May 2024 successor CF 256).** Monthly, county-level CalFresh (SNAP) enrollment, November 2003–present, for all 58 California counties — a household-distress signal independent of labor-force status, used in [the synthetic-control check](synthetic-control.md) alongside the employment-based checks.

## Retail sales

**California Department of Tax and Fee Administration (CDTFA), Taxable Sales, by City.** Quarterly, city-level taxable sales transactions, 2009 Q1–present, via CDTFA's Open Data Portal — real economic activity tied to where spending physically happens, independent of any employer's payroll records. Used in [the synthetic-control check](synthetic-control.md) as a third, non-labor-market outcome variable.

## School enrollment

**California Department of Education, historical School Enrollment data files (1981-82 through 2022-23) and the Public Schools and Districts directory.** Annual, school-level enrollment by county, district, and grade, aggregated to the school-district level for this project's own checks. Used in [the synthetic-control check](synthetic-control.md) as a fourth, family-instability-focused outcome variable, independent of anyone's labor-force status or employer.

## Flood claims

**FEMA, OpenFEMA NFIP Redacted Claims dataset.** Paid National Flood Insurance Program claims with a 2023 date of loss in Kings and Tulare counties, used in [Environmental Impact](environmental-impact.md) alongside — not in place of — the larger, separate farmland-restoration cost estimate already on that page. Covers insured structures only; excludes growing crops and any uninsured property.

## Historical record

Primary and contemporaneous sourcing for Central Valley/Sacramento commodity-ag processing events going back to 1912 — cannery foundings, the 1966–67 United Farm Workers ownership precedent at Delano's Forty Acres, and documented plant closures from the early 1980s forward — used to test whether the current wave of closures is part of a genuinely continuous, decades-long pattern rather than a recent, isolated event. See [Case Studies](case-studies.md) for the timeline built from this record.

## Photographs

Historical photographs on this site are drawn from the Library of Congress's Farm Security Administration/Office of War Information Collection and Historic American Buildings Survey — U.S. government works, confirmed public domain on a per-item basis before use, not assumed from a collection's general reputation. Several other candidate images (1966 Delano UFW photographs, Sacramento cannery interior photographs) were identified and explicitly excluded after turning out to be under copyright. The two Lindsay, California citrus-worker housing photographs on the home page (Dorothea Lange, February 1939, LOC item IDs 2017771233 and 2017771273) were confirmed the same way: rights-advisory and rights statements checked individually against the FSA/OWI collection's public-domain terms before use, not inferred from the collection's reputation.

## A note on completeness

Several of the sources above have real, documented gaps — some county crop reports are missing for specific years, some historical events are more thinly sourced than others. We'd rather name a gap than imply completeness we don't have. As our methodology page notes, this is a working record, not a finished one, and we update it as the gaps close.
