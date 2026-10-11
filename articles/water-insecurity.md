# Water insecurity and farm labor occupy the same map

Our [case studies](case-studies.md) document what happens when the industry that built a place leaves. This page documents something that happens *while* it's still there: the same Central Valley communities that supply the region's farm labor are, disproportionately, the ones whose own drinking water isn't safe or reliable.

This isn't a coincidence we're asserting — it's a pattern we went and checked, town by town, the same way we built our closure record: pulling the public filings, news coverage, state water-board records, and legal filings behind each place, not a secondhand list.

<div class="stat-pair">
  <div class="stat-card">
    <p class="stat-number" data-target="20" data-decimals="0">0</p>
    <p class="stat-label">Communities across four counties where we've independently confirmed both a farm-labor economy and a documented water-insecurity problem.</p>
  </div>
  <div class="stat-card">
    <p class="stat-number" data-target="70" data-decimals="0">0</p>
    <p class="stat-label">Years one of those communities — Westley, in Stanislaus County — has gone without a public school able to provide its own students drinkable water.</p>
  </div>
</div>

<figure class="figure">
  <img src="/assets/photos/10-tulare-irrigation-pump-1938.jpg" alt="A butane-powered irrigation pump mounted on a wooden platform, Tulare County, California, 1938, with pipes, tanks, and a timber support structure.">
  <figcaption class="figure-caption"><strong>Tulare County, November 1938.</strong> A Farm Security Administration irrigation pump, part of a federal program to cut small farmers' water costs — the same water infrastructure this region has run on for nearly a century, and whose modern reliability this page documents town by town. <span class="figure-source">Dorothea Lange, Farm Security Administration. Public domain, Library of Congress.</span></figcaption>
</figure>

<script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>
<div class="chart" id="wi-map-chart">
  <p class="chart-title">Where these 20 communities sit</p>
  <p class="chart-subtitle">Real county boundaries and town locations — the same geographic data behind every map on this site, cropped to these four counties for readability.</p>
  <div id="wi-map-svg-container" style="min-height:420px; position:relative;"></div>
  <div class="chart-legend" id="wi-map-legend"></div>
  <p class="chart-source">County boundaries: U.S. Census Bureau via us-atlas. Town locations: OpenStreetMap contributors (ODbL), geocoded against each place's own name, 2026. One point — Cowan Tract, Stanislaus County — is an approximate match to a street in the subdivision's area, not a confirmed town centroid; it's marked accordingly on hover.</p>
</div>
<script>
(function () {
  var TOWNS = [
    {name: "Kettleman City", county: "Kings", lon: -119.9626738, lat: 36.0087178},
    {name: "Stratford", county: "Kings", lon: -119.8215654, lat: 36.19057},
    {name: "Corcoran", county: "Kings", lon: -119.5603728, lat: 36.0981045},
    {name: "Armona", county: "Kings", lon: -119.7024315, lat: 36.315894},
    {name: "Avenal", county: "Kings", lon: -120.1290272, lat: 36.0041223},
    {name: "Lanare", county: "Fresno", lon: -119.9321826, lat: 36.4381935},
    {name: "Cantua Creek", county: "Fresno", lon: -120.316113, lat: 36.5011795},
    {name: "Shady Lakes MHP", county: "Fresno", lon: -119.7368542, lat: 36.6537561},
    {name: "Caruthers", county: "Fresno", lon: -119.8450189, lat: 36.539914},
    {name: "Allensworth", county: "Tulare", lon: -119.3905252, lat: 35.8635518},
    {name: "East Porterville", county: "Tulare", lon: -118.9792538, lat: 36.0577505},
    {name: "Tooleville", county: "Tulare", lon: -119.1154395, lat: 36.2878269},
    {name: "Earlimart", county: "Tulare", lon: -119.2725961, lat: 35.8799715},
    {name: "Strathmore", county: "Tulare", lon: -119.0598476, lat: 36.141569},
    {name: "Richgrove", county: "Tulare", lon: -119.1066216, lat: 35.7968056},
    {name: "Plainview", county: "Tulare", lon: -119.1386712, lat: 36.1403117},
    {name: "Westley / Grayson", county: "Stanislaus", lon: -121.1864612, lat: 37.579063},
    {name: "Keyes", county: "Stanislaus", lon: -120.9072329, lat: 37.5604628},
    {name: "Cowan Tract (approximate)", county: "Stanislaus", lon: -120.989715, lat: 37.5603986},
    {name: "Salida", county: "Stanislaus", lon: -121.0866771, lat: 37.7151375}
  ];
  var COUNTY_FIPS = {"06031": "Kings", "06019": "Fresno", "06107": "Tulare", "06099": "Stanislaus"};
  var COUNTY_COLOR = {Kings: "var(--chart-cat-1)", Fresno: "var(--chart-cat-2)", Tulare: "var(--chart-cat-3)", Stanislaus: "var(--chart-cat-4)"};

  var container = document.getElementById("wi-map-svg-container");
  var width = container.clientWidth || 700, height = Math.round(width * 0.9);

  function isFocus(d) { return !!COUNTY_FIPS[d.id]; }

  Promise.all([
    fetch("/assets/data/california-counties.geojson").then(function (r) { return r.json(); })
  ]).then(function (results) {
    var allCounties = results[0];
    var focusFeatures = allCounties.features.filter(isFocus);
    var focusCollection = {type: "FeatureCollection", features: focusFeatures};

    var svg = d3.select(container).append("svg")
      .attr("viewBox", "0 0 " + width + " " + height)
      .attr("role", "img")
      .attr("aria-label", "A map of Kings, Fresno, Tulare, and Stanislaus counties with 20 communities marked by real location, color-coded by county. Hover or tap a point for its name.");

    // Fit tightly to just these four counties, not the whole state --
    // this map's job is distinguishing 20 close-together towns, not
    // showing where in California they sit (the-index.md's map already
    // does that job at state scale).
    var projection = d3.geoMercator().fitExtent([[20, 20], [width - 20, height - 20]], focusCollection);
    var path = d3.geoPath(projection);

    svg.selectAll("path.county")
      .data(allCounties.features)
      .enter()
      .append("path")
      .attr("class", "county")
      .attr("d", path)
      .attr("vector-effect", "non-scaling-stroke")
      .attr("fill", "var(--chart-surface)")
      .attr("stroke", function (d) { return isFocus(d) ? "var(--ink)" : "var(--chart-baseline)"; })
      .attr("stroke-width", function (d) { return isFocus(d) ? 2 : 0.75; });

    svg.selectAll("circle.town")
      .data(TOWNS)
      .enter()
      .append("circle")
      .attr("class", "town")
      .attr("cx", function (d) { return projection([d.lon, d.lat])[0]; })
      .attr("cy", function (d) { return projection([d.lon, d.lat])[1]; })
      .attr("r", 6)
      .attr("fill", function (d) { return COUNTY_COLOR[d.county]; })
      .attr("stroke", "var(--ink)")
      .attr("stroke-width", 1.25)
      .append("title")
      .text(function (d) { return d.name + " (" + d.county + " County)"; });

    var legend = document.getElementById("wi-map-legend");
    ["Kings", "Fresno", "Tulare", "Stanislaus"].forEach(function (c) {
      legend.innerHTML += '<span class="chart-legend-item"><span class="chart-legend-swatch" style="background:' + COUNTY_COLOR[c] + '"></span>' + c + '</span>';
    });
  });
})();
</script>

## What we found, county by county

### Kings County

- [Kettleman City](case-studies/kings-kettleman-city.md) — a birth-defect rate spike next to the western U.S.'s largest hazardous-waste landfill, plus a separate, unrelated arsenic problem in the town's groundwater.
- [Stratford](case-studies/kings-stratford.md) — recurring well failures and discolored water, going back to at least 2014.
- [Corcoran](case-studies/kings-corcoran.md) — the self-proclaimed "Dairy Capital of the World" suing one of its own dairies for $65 million over nitrate contamination.
- [Armona](case-studies/kings-armona.md) — arsenic took two of three wells offline; a new well and treatment plant fixed it, but single-point-of-failure risk remains.
- [Avenal](case-studies/kings-avenal.md) — not contamination, but infrastructure: an imported-water pipeline that's failed outright twice, cutting off the town for up to 12 days.

### Fresno County

- [Lanare](case-studies/fresno-lanare.md) — thirteen years of arsenic, including nine years paying off a state-funded treatment plant that never worked.
- [Cantua Creek](case-studies/fresno-cantua-creek.md) — a majority farm-worker town of fewer than 500 people, paying for water they won't drink.
- [Shady Lakes Mobile Home Park](case-studies/fresno-shady-lakes-mhp.md) — a lawsuit against the park's owner, settled for $200,000.
- [Caruthers](case-studies/fresno-caruthers.md) — a quieter, ongoing, state-funded arsenic-treatment project.

### Tulare County

- [Allensworth](case-studies/tulare-allensworth.md) — California's first Black-founded town, still working through an arsenic fix twelve years after the problem was identified.
- [East Porterville](case-studies/tulare-east-porterville.md) — roughly 1,000 household wells ran dry in the 2012–2016 drought, in a community about 75% Latino.
- [Tooleville](case-studies/tulare-tooleville.md) — bottled water since 2014 for hexavalent chromium; now the wells are failing outright too.
- [Earlimart](case-studies/tulare-earlimart.md) — a $5.7 million settlement against Dow, Shell, and Wilbur-Ellis over TCP contamination — money that sat unspent for years.
- [Strathmore](case-studies/tulare-strathmore.md) — nitrate-removal project filings dating back to 1986, the longest documented history in this record.
- [Richgrove](case-studies/tulare-richgrove.md) — arsenic, nitrates, and the legacy fumigant DBCP, all at once; farmworker housing residents rationed to 20 gallons a month.
- [Plainview](case-studies/tulare-plainview.md) — a state "Nitrate Relief Project" we could document only through official filings, not independent reporting.

### Stanislaus County

- [Westley / Grayson Elementary](case-studies/stanislaus-westley-grayson.md) — a public school that has never, in 70 years, had reliably drinkable water.
- [Keyes](case-studies/stanislaus-keyes.md) — four wells, four arsenic violations, resolved by a 2019 multi-system consolidation; a new TCP problem has since emerged.
- [Cowan Tract](case-studies/stanislaus-cowan-tract.md) — no public water system at all; private wells in the worst 4% of the state for water-quality hazard.
- [Salida](case-studies/stanislaus-salida.md) — part of a regional, polluter-funded bottled-water program covering an estimated 50,000 households.

## Who else is doing this work

This is a documentation project, not a remediation one. Our own contribution is narrower than full resolution: establishing, with sources, that the places carrying this region's water burden are overwhelmingly the same places carrying its farm-labor burden — and that the overlap is not incidental to how this region's economy was built. For readers looking to act on what's documented here, or to work with the underlying data directly, these organizations are already doing that work:

- **Leadership Counsel for Justice and Accountability** and **California Rural Legal Assistance** — litigation, advocacy, and state-complaint processes, active in several of the communities on this page.
- **The California Water Data Consortium** — the state's own open water-data infrastructure, built under California's Open and Transparent Water Data Act, for readers who want the underlying datasets rather than our summary of them.
- **Fresno State's WET Center** (Water, Energy, and Technology) — regional water and agricultural-technology research, incubation, and workforce development, based in the same San Joaquin Valley geography this page documents.

## The honest limitation

Several communities we researched for this pass — including Coalinga, Raisin City, Tranquillity, Biola, Riverdale, and Armona's neighbor towns of Home Garden and Kingston — turned up no town-specific water-crisis story despite repeated searches, even though some appear on official disadvantaged-community lists. We're not treating an official designation as proof of an undocumented crisis, and we're not filling those gaps with inference. They remain open questions, not findings.

Full citation detail and source archive: [Data](data.md). See [Case Studies](case-studies.md) for the plant-closure side of this project's record, and [the Index](the-index.md) for the economic-dependence measure behind our overall thesis.
