# Case Studies

## California's Central Valley: the first case study

Second Growth's first body of research documents more than fifty years of commodity agriculture consolidation in California's Central Valley, and what it has meant for the people who did the work of growing and processing it. We're starting with four counties — **Kings, Fresno, Tulare, and Stanislaus** — where that pattern is long-running and well documented.

### Start here: the whole picture, one map

This research actually runs on two different geographies — county lines for the economic data, groundwater subbasins for the water data, because water doesn't follow county lines. Switch between them below before reading the section-by-section detail that follows.

<script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>
<div class="chart" id="explorer-chart">
  <p class="chart-title" id="explorer-title">Food manufacturing dependence, by county</p>
  <p class="chart-subtitle" id="explorer-subtitle">Employment SDI vs. the U.S. benchmark, 2025</p>

  <div class="layer-toggle" role="group" aria-label="Choose the map's base geography">
    <button type="button" class="layer-toggle-btn active" data-base="county">County boundaries</button>
    <button type="button" class="layer-toggle-btn" data-base="subbasin">Groundwater subbasins</button>
  </div>

  <div class="layer-toggle" role="group" aria-label="Choose which factor the map shows" id="explorer-county-layers">
    <button type="button" class="layer-toggle-btn active" data-layer="sdi">Food-processing dependence (SDI)</button>
    <button type="button" class="layer-toggle-btn" data-layer="unemployment">Unemployment rate</button>
  </div>
  <div class="layer-toggle" role="group" aria-label="Choose which groundwater measure the map shows" id="explorer-subbasin-layers" style="display:none">
    <button type="button" class="layer-toggle-btn active" data-layer="depth">Depth to groundwater (by year)</button>
    <button type="button" class="layer-toggle-btn" data-layer="change">Change since 2015</button>
  </div>
  <div class="time-slider" id="explorer-time-slider" style="display:none">
    <label for="explorer-year-range">Year: <strong id="explorer-year-label">2026</strong></label>
    <input type="range" id="explorer-year-range" min="1950" max="2026" step="1" value="2026">
    <div class="time-slider-ends"><span>1950</span><span>2026</span></div>
  </div>

  <div id="explorer-svg-container" style="min-height:360px"></div>
  <div class="chart-legend" id="explorer-legend"></div>
  <details class="chart-table-toggle">
    <summary>View as table (both geographies)</summary>
    <table>
      <thead><tr><th>Geography</th><th>Area</th><th>SDI (2025)</th><th>Unemployment (Aug 2026)</th><th>Groundwater depth (2026)</th><th>Change since 2015</th></tr></thead>
      <tbody>
        <tr><td>County</td><td>Kings</td><td>0.153</td><td>8.5%</td><td>—</td><td>—</td></tr>
        <tr><td>County</td><td>Fresno</td><td>0.100</td><td>7.8%</td><td>—</td><td>—</td></tr>
        <tr><td>County</td><td>Tulare</td><td>0.119</td><td>10.4%</td><td>—</td><td>—</td></tr>
        <tr><td>County</td><td>Stanislaus</td><td>0.205</td><td>7.0%</td><td>—</td><td>—</td></tr>
        <tr><td>Subbasin</td><td>Kings Subbasin</td><td>—</td><td>—</td><td>131.4 ft</td><td>−11.2 ft</td></tr>
        <tr><td>Subbasin</td><td>Tulare Lake Subbasin</td><td>—</td><td>—</td><td>173.2 ft</td><td>−2.6 ft</td></tr>
      </tbody>
    </table>
    <p class="chart-source">Counties and subbasins are genuinely different geographies, not a single table pivoted two ways — see the "—" cells above. Kings County alone spans both the Kings and Tulare Lake groundwater subbasins.</p>
  </details>
  <p class="chart-source" id="explorer-source">County boundaries: U.S. Census Bureau via us-atlas. SDI: Second Growth calculation, see <a href="methodology.md">Methodology</a>.</p>
</div>
<script>
(function () {
  var countyLayers = {
    sdi: {
      title: "Food manufacturing dependence, by county",
      subtitle: "Employment SDI vs. the U.S. benchmark, 2025",
      byKey: {
        "06031": {name: "Kings", value: 0.153, note: "Hanford closure"},
        "06019": {name: "Fresno", value: 0.100, note: null},
        "06107": {name: "Tulare", value: 0.119, note: null},
        "06099": {name: "Stanislaus", value: 0.205, note: "Modesto/Hughson closure"}
      },
      diverging: false,
      ramp: ["#f8e2d8", "#e3a88f", "#c23b1f", "#8a2414", "#5c160c"],
      domain: [0.09, 0.22],
      format: function (v) { return v.toFixed(3); },
      tooltipLabel: "Employment SDI",
      legendLow: "Lower dependence",
      legendHigh: "Higher dependence",
      source: 'County boundaries: U.S. Census Bureau via us-atlas. SDI: Second Growth calculation, see <a href="methodology.md">Methodology</a>.'
    },
    unemployment: {
      title: "Unemployment rate, by county",
      subtitle: "August 2026, not seasonally adjusted (Central Valley unemployment has a real seasonal cycle — see note below)",
      byKey: {
        "06031": {name: "Kings", value: 8.5, note: null},
        "06019": {name: "Fresno", value: 7.8, note: null},
        "06107": {name: "Tulare", value: 10.4, note: null},
        "06099": {name: "Stanislaus", value: 7.0, note: null}
      },
      diverging: false,
      ramp: ["#e3f3f7", "#a9d6e2", "#0e86a8", "#0a5c73", "#053542"],
      domain: [6, 11],
      format: function (v) { return v.toFixed(1) + "%"; },
      tooltipLabel: "Unemployment rate",
      legendLow: "Lower unemployment",
      legendHigh: "Higher unemployment",
      source: 'County boundaries: U.S. Census Bureau via us-atlas. Unemployment: BLS Local Area Unemployment Statistics, see <a href="data.md">Data</a>. Not seasonally adjusted.'
    }
  };

  var subbasinLayers = {
    depth: {
      title: "Depth to groundwater, by subbasin",
      subtitle: "Annual average, by year selected below",
      byKey: {
        "5-022.08": {name: "Kings Subbasin", note: "Hanford", value: 131.4},
        "5-022.12": {name: "Tulare Lake Subbasin", note: "Corcoran", value: 173.2}
      },
      diverging: false,
      ramp: ["#f9ecd2", "#e8c87a", "#c9960f", "#9a7108", "#6b4e05"],
      domain: [30, 235],
      format: function (v) { return v.toFixed(1) + " ft"; },
      tooltipLabel: "Depth to groundwater",
      legendLow: "Shallower",
      legendHigh: "Deeper",
      source: 'Subbasin boundaries: DWR Bulletin 118, via CA GIS open-data portal. Groundwater: DWR periodic groundwater level measurements, annual average by well. See <a href="data.md">Data</a>.'
    },
    change: {
      title: "Change in groundwater depth since 2015, by subbasin",
      subtitle: "Paired per-well comparison, 2015 vs. most recent reading since 2023 — negative = shallower = recovery",
      byKey: {
        "5-022.08": {name: "Kings Subbasin", note: "Hanford", value: -11.2},
        "5-022.12": {name: "Tulare Lake Subbasin", note: "Corcoran", value: -2.6}
      },
      diverging: true,
      ramp: ["#7a2415", "#c23b1f", "#ece6d6", "#0e86a8", "#0a5c73"],
      domain: [-15, 15],
      format: function (v) { return (v > 0 ? "+" : "−") + Math.abs(v).toFixed(1) + " ft"; },
      tooltipLabel: "Change since 2015",
      legendLow: "Decline (deeper)",
      legendHigh: "Recovery (shallower)",
      source: 'Subbasin boundaries: DWR Bulletin 118, via CA GIS open-data portal. Groundwater: DWR periodic groundwater level measurements, paired per-well comparison. See <a href="data.md">Data</a>.'
    }
  };

  var container = document.getElementById("explorer-svg-container");
  var width = container.clientWidth || 700;
  var countyHeight = 360, subbasinHeight = 300;
  var currentBase = "county";
  var currentCountyLayer = "sdi";
  var currentSubbasinLayer = "depth";
  var countyGeo = null, subbasinGeo = null, subbasinAnnual = null;
  var svg = null, path = null;

  function colorFor(layer, v) {
    if (layer.diverging) {
      var half = Math.max(Math.abs(layer.domain[0]), Math.abs(layer.domain[1]));
      var t = Math.max(-1, Math.min(1, v / half));
      var idx = Math.round((1 - t) / 2 * (layer.ramp.length - 1));
      return layer.ramp[idx];
    }
    var t2 = Math.max(0, Math.min(1, (v - layer.domain[0]) / (layer.domain[1] - layer.domain[0])));
    var idx2 = Math.min(layer.ramp.length - 1, Math.floor(t2 * layer.ramp.length));
    return layer.ramp[idx2];
  }

  function textColorFor(layer, v) {
    var t = layer.diverging
      ? Math.abs(v) / Math.max(Math.abs(layer.domain[0]), Math.abs(layer.domain[1]))
      : (v - layer.domain[0]) / (layer.domain[1] - layer.domain[0]);
    return t > 0.55 ? "#fff" : null;
  }

  function idPropFor(base) { return base === "county" ? "fips" : "Basin_Subbasin_Number"; }

  function render() {
    var base = currentBase;
    var layers = base === "county" ? countyLayers : subbasinLayers;
    var layerKey = base === "county" ? currentCountyLayer : currentSubbasinLayer;
    var layer = layers[layerKey];
    var idProp = idPropFor(base);

    document.getElementById("explorer-title").textContent = layer.title;
    document.getElementById("explorer-subtitle").textContent = layer.subtitle;
    document.getElementById("explorer-source").innerHTML = layer.source;

    var btnGroupSel = base === "county" ? "#explorer-county-layers" : "#explorer-subbasin-layers";
    document.querySelectorAll(btnGroupSel + " .layer-toggle-btn").forEach(function (btn) {
      btn.classList.toggle("active", btn.getAttribute("data-layer") === layerKey);
      btn.setAttribute("aria-pressed", btn.getAttribute("data-layer") === layerKey ? "true" : "false");
    });

    svg.selectAll("path.feature")
      .attr("fill", function (d) { return colorFor(layer, layer.byKey[d.properties[idProp]].value); })
      .attr("data-label", function (d) {
        var info = layer.byKey[d.properties[idProp]];
        return info.name + (info.note ? " (" + info.note + ")" : "");
      })
      .attr("data-value", function (d) { return layer.tooltipLabel + ": " + layer.format(layer.byKey[d.properties[idProp]].value); })
      .attr("data-key-color", function (d) { return colorFor(layer, layer.byKey[d.properties[idProp]].value); });

    svg.selectAll("text.feature-label")
      .attr("fill", function (d) { return textColorFor(layer, layer.byKey[d.properties[idProp]].value) || "var(--chart-text-primary)"; })
      .text(function (d) { return layer.byKey[d.properties[idProp]].name; });

    svg.selectAll("text.feature-value")
      .attr("fill", function (d) { return textColorFor(layer, layer.byKey[d.properties[idProp]].value) || "var(--chart-text-secondary)"; })
      .text(function (d) { return layer.format(layer.byKey[d.properties[idProp]].value); });

    var legend = document.getElementById("explorer-legend");
    var swatches = "";
    for (var i = 0; i < layer.ramp.length; i++) {
      swatches += '<span style="display:inline-block;width:22px;height:14px;background:' + layer.ramp[i] + ';"></span>';
    }
    legend.innerHTML = '<span>' + layer.legendLow + '</span>' + swatches + '<span>' + layer.legendHigh + '</span>';
  }

  function applyYear(year) {
    if (!subbasinAnnual) return;
    var idByKey = {"kings": "5-022.08", "tulare-lake": "5-022.12"};
    Object.keys(idByKey).forEach(function (key) {
      var rec = subbasinAnnual[key] && subbasinAnnual[key][year];
      if (rec) subbasinLayers.depth.byKey[idByKey[key]].value = rec.depth;
    });
    subbasinLayers.depth.subtitle = "Annual average, " + year;
    document.getElementById("explorer-year-label").textContent = year;
  }

  function buildSvg(base) {
    var geo = base === "county" ? countyGeo : subbasinGeo;
    var height = base === "county" ? countyHeight : subbasinHeight;
    d3.select(container).selectAll("svg").remove();

    svg = d3.select(container).append("svg")
      .attr("viewBox", "0 0 " + width + " " + height)
      .attr("role", "img")
      .attr("aria-label", base === "county"
        ? "Map of Kings, Fresno, Tulare, and Stanislaus counties, shaded by a selectable factor"
        : "Map of the Kings and Tulare Lake groundwater subbasins, shaded by a selectable groundwater measure");

    var projection = d3.geoMercator().fitExtent([[20, 20], [width - 20, height - 20]], geo);
    path = d3.geoPath(projection);

    svg.selectAll("path.feature")
      .data(geo.features)
      .enter()
      .append("path")
      .attr("class", "feature chart-hit")
      .attr("d", path)
      .attr("stroke", "#fff")
      .attr("stroke-width", 2);

    svg.selectAll("text.feature-label")
      .data(geo.features)
      .enter()
      .append("text")
      .attr("class", "feature-label mark-label")
      .attr("x", function (d) { return path.centroid(d)[0]; })
      .attr("y", function (d) { return path.centroid(d)[1]; })
      .attr("text-anchor", "middle")
      .attr("font-size", 13);

    svg.selectAll("text.feature-value")
      .data(geo.features)
      .enter()
      .append("text")
      .attr("class", "feature-value")
      .attr("x", function (d) { return path.centroid(d)[0]; })
      .attr("y", function (d) { return path.centroid(d)[1] + 16; })
      .attr("text-anchor", "middle")
      .attr("font-size", 11);

    render();
  }

  function switchBase(base) {
    currentBase = base;
    document.getElementById("explorer-county-layers").style.display = base === "county" ? "" : "none";
    document.getElementById("explorer-subbasin-layers").style.display = base === "subbasin" ? "" : "none";
    document.getElementById("explorer-time-slider").style.display = (base === "subbasin" && currentSubbasinLayer === "depth") ? "" : "none";
    buildSvg(base);
  }

  Promise.all([
    fetch("/assets/data/central-valley-counties.geojson").then(function (r) { return r.json(); }),
    fetch("/assets/data/kings-tulare-lake-subbasins.geojson").then(function (r) { return r.json(); }),
    fetch("/assets/data/subbasin_annual_depth_to_groundwater.json").then(function (r) { return r.json(); })
  ]).then(function (results) {
    countyGeo = results[0];
    subbasinGeo = results[1];
    subbasinAnnual = results[2];
    applyYear(document.getElementById("explorer-year-range").value);

    buildSvg("county");

    document.querySelectorAll("#explorer-chart [data-base]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        document.querySelectorAll("#explorer-chart [data-base]").forEach(function (b) {
          b.classList.toggle("active", b === btn);
        });
        switchBase(btn.getAttribute("data-base"));
      });
    });

    document.querySelectorAll("#explorer-county-layers .layer-toggle-btn").forEach(function (btn) {
      btn.addEventListener("click", function () {
        currentCountyLayer = btn.getAttribute("data-layer");
        render();
      });
    });

    var yearSlider = document.getElementById("explorer-year-range");
    yearSlider.addEventListener("input", function () {
      applyYear(yearSlider.value);
      render();
    });

    document.querySelectorAll("#explorer-subbasin-layers .layer-toggle-btn").forEach(function (btn) {
      btn.addEventListener("click", function () {
        currentSubbasinLayer = btn.getAttribute("data-layer");
        document.getElementById("explorer-time-slider").style.display = currentSubbasinLayer === "depth" ? "" : "none";
        if (currentSubbasinLayer === "depth") applyYear(yearSlider.value);
        render();
      });
    });
  });
})();
</script>

### The pattern we're tracking

Commodity food processing has been a defining industry across these counties for generations — the kind of industry a region's labor market, tax base, and civic life organize around. Over the past two years alone, plant closures and mass layoffs tied to major processors have removed well over two thousand documented jobs across Stanislaus, Kings, and Fresno counties, and that period sits inside a far longer pattern of consolidation that goes back decades. Reporting around one recent closure placed it among roughly sixty Central Valley plant closures or mass layoffs in a single year.

These aren't isolated business decisions happening in a vacuum. They track a structural pressure on the region: California's Sustainable Groundwater Management Act is expected to push a significant share of San Joaquin Valley irrigated farmland out of production over the next two decades as groundwater use is brought into balance. Processing capacity and the water-constrained supply it depends on are moving in the same direction, in the same places, at the same time.

### The long arc, in one timeline

"Fifty years" and "sixty closures in a single year" are two very different kinds of claim — one about a slow multi-generational pattern, one about a sudden acceleration. Both are true, and the gap between them is itself worth seeing: the first eight events below are spread across more than a century; the last five happened within about two years. The zoomed-in panel isn't a different chart — it's the same spine, broken and magnified so the recent cluster doesn't collapse into a single dot.

<div class="chart" id="timeline-chart">
  <p class="chart-title">Central Valley/Sacramento commodity-ag processing, 1912–2026</p>
  <p class="chart-subtitle">Founding and ownership milestones, bankruptcy filings and policy, and plant closures — sourced to original reporting, company filings, and public records. See <a href="data.md">Data</a> for full citations, including the two events flagged below as thinly sourced.</p>
  <div class="layer-toggle" role="group" aria-label="Filter the timeline by category">
    <button type="button" class="layer-toggle-btn active" data-category="all">All events</button>
    <button type="button" class="layer-toggle-btn" data-category="founding">Founding / ownership</button>
    <button type="button" class="layer-toggle-btn" data-category="bankruptcy">Bankruptcy / policy</button>
    <button type="button" class="layer-toggle-btn" data-category="closure">Closures</button>
  </div>
  <svg viewBox="0 0 780 560" role="img" aria-labelledby="tl-title tl-desc">
    <title id="tl-title">Timeline of Central Valley and Sacramento commodity-ag processing events, 1912 to 2026</title>
    <desc id="tl-desc">Thirteen events from 1912 to 2026: cannery foundings, the 1966-67 UFW Forty Acres ownership precedent, cannery closures in the early 1980s and 1993, the 2000 Tri Valley Growers bankruptcy, the 2012-13 Campbell Soup closure, the 2014 Sustainable Groundwater Management Act, and a cluster of five bankruptcy and closure events in 2024-2026, shown in a zoomed inset because they fall within about two years of each other. Click or tap any point to pin its full description and sourcing below the chart; the table below the chart also has full text and sourcing notes.</desc>

    <!-- Track 1: 1912-2020, main spine at y=150 -->
    <line class="axis-line" x1="70" y1="150" x2="740" y2="150"></line>

    <!-- 1912 Libby built (above, gold, anchor start) -->
    <g class="tl-event" data-category="founding">
    <line x1="70" y1="150" x2="70" y2="135" class="axis-line"></line>
    <circle class="chart-hit" tabindex="0" role="button" data-label="1912 — Libby, McNeill &amp; Libby cannery built, Sacramento" data-value="Founding" data-key-color="var(--chart-cat-3)" data-sourcing="Well documented." cx="70" cy="150" r="6" fill="var(--chart-cat-3)" stroke="#fff" stroke-width="2"></circle>
    <text x="70" y="108" text-anchor="start" font-size="10">Libby built</text>
    <text class="mark-label" x="70" y="125" text-anchor="start" fill="var(--chart-cat-3)" font-size="12">1912</text>
    </g>

    <!-- 1931 Bercut-Richards founded (below, gold, middle) -->
    <g class="tl-event" data-category="founding">
    <line x1="187.9" y1="150" x2="187.9" y2="165" class="axis-line"></line>
    <circle class="chart-hit" tabindex="0" role="button" data-label="1931 — Bercut-Richards cannery founded, Sacramento" data-value="Founding" data-key-color="var(--chart-cat-3)" data-sourcing="Well documented." cx="187.9" cy="150" r="6" fill="var(--chart-cat-3)" stroke="#fff" stroke-width="2"></circle>
    <text class="mark-label" x="187.9" y="180" text-anchor="middle" fill="var(--chart-cat-3)" font-size="12">1931</text>
    <text x="187.9" y="196" text-anchor="middle" font-size="10">Bercut-Richards</text>
    </g>

    <!-- 1966-67 Forty Acres / UFW (above, gold, middle) -->
    <g class="tl-event" data-category="founding">
    <line x1="408.1" y1="150" x2="408.1" y2="135" class="axis-line"></line>
    <circle class="chart-hit" tabindex="0" role="button" data-label="1966–67 — Forty Acres becomes UFW headquarters; Farm Worker Cooperative founded, Delano" data-value="Ownership precedent" data-key-color="var(--chart-cat-3)" data-sourcing="NPS National Historic Landmark nomination (2008)." data-photo-id="photo-forty-acres" cx="408.1" cy="150" r="6" fill="var(--chart-cat-3)" stroke="#fff" stroke-width="2"></circle>
    <text x="408.1" y="108" text-anchor="middle" font-size="10">Forty Acres (UFW)</text>
    <text class="mark-label" x="408.1" y="125" text-anchor="middle" fill="var(--chart-cat-3)" font-size="12">1966–67</text>
    </g>

    <!-- ~1982 Libby closes (below, rust, middle, uncertain date = dashed) -->
    <g class="tl-event" data-category="closure">
    <line x1="504.3" y1="150" x2="504.3" y2="165" class="axis-line"></line>
    <circle class="chart-hit" tabindex="0" role="button" data-label="~1982 — Libby, McNeill &amp; Libby cannery closes, Sacramento (closure date not firmly confirmed)" data-value="Closure" data-key-color="var(--chart-cat-1)" data-sourcing="Thin. No contemporaneous news source located; exact year unconfirmed (early-1980s range, building NRHP-listed March 1982)." cx="504.3" cy="150" r="6" fill="var(--chart-cat-1)" stroke="#fff" stroke-width="2" stroke-dasharray="2,1.5"></circle>
    <text class="mark-label" x="504.3" y="180" text-anchor="middle" fill="var(--chart-cat-1)" font-size="12">~1982</text>
    <text x="504.3" y="196" text-anchor="middle" font-size="10">Libby closes*</text>
    </g>

    <!-- 1993 Bercut-Richards closes (above, rust, middle, uncertain = dashed) -->
    <g class="tl-event" data-category="closure">
    <line x1="572.5" y1="150" x2="572.5" y2="135" class="axis-line"></line>
    <circle class="chart-hit" tabindex="0" role="button" data-label="1993 — Bercut-Richards cannery closes, Sacramento (no contemporaneous source located)" data-value="Closure" data-key-color="var(--chart-cat-1)" data-sourcing="Thin. No contemporaneous 1993 news source located; drawn from retrospective secondary sources." cx="572.5" cy="150" r="6" fill="var(--chart-cat-1)" stroke="#fff" stroke-width="2" stroke-dasharray="2,1.5"></circle>
    <text x="572.5" y="108" text-anchor="middle" font-size="10">Bercut-Richards*</text>
    <text class="mark-label" x="572.5" y="125" text-anchor="middle" fill="var(--chart-cat-1)" font-size="12">1993</text>
    </g>

    <!-- 2000 Tri Valley Growers bankruptcy (below, denim, middle) -->
    <g class="tl-event" data-category="bankruptcy">
    <line x1="615.9" y1="150" x2="615.9" y2="165" class="axis-line"></line>
    <circle class="chart-hit" tabindex="0" role="button" data-label="2000 — Tri Valley Growers files Chapter 11; roughly 11,000 Central Valley jobs lost" data-value="Bankruptcy" data-key-color="var(--chart-cat-2)" data-sourcing="UC Davis Giannini Foundation (2004), Journal of Cooperatives (2009), cross-verified job figure." cx="615.9" cy="150" r="6" fill="var(--chart-cat-2)" stroke="#fff" stroke-width="2"></circle>
    <text class="mark-label" x="615.9" y="180" text-anchor="middle" fill="var(--chart-cat-2)" font-size="12">2000</text>
    <text x="615.9" y="196" text-anchor="middle" font-size="10">TVG</text>
    </g>

    <!-- 2012-13 Campbell Soup closes Sacramento (above, rust, end-anchor) -->
    <g class="tl-event" data-category="closure">
    <line x1="693.5" y1="150" x2="693.5" y2="135" class="axis-line"></line>
    <circle class="chart-hit" tabindex="0" role="button" data-label="2012–13 — Campbell Soup closes Sacramento plant; 700 jobs" data-value="Closure" data-key-color="var(--chart-cat-1)" data-sourcing="Company press release plus three independent local-news outlets." cx="693.5" cy="150" r="6" fill="var(--chart-cat-1)" stroke="#fff" stroke-width="2"></circle>
    <text x="693.5" y="108" text-anchor="end" font-size="10">Campbell</text>
    <text class="mark-label" x="693.5" y="125" text-anchor="end" fill="var(--chart-cat-1)" font-size="12">2012–13</text>
    </g>

    <!-- 2014 SGMA signed (below, denim, end-anchor) -->
    <g class="tl-event" data-category="bankruptcy">
    <line x1="702.8" y1="150" x2="702.8" y2="165" class="axis-line"></line>
    <circle class="chart-hit" tabindex="0" role="button" data-label="2014 — California's Sustainable Groundwater Management Act (SGMA) signed into law" data-value="Policy" data-key-color="var(--chart-cat-2)" data-sourcing="Public legislative record." cx="702.8" cy="150" r="6" fill="var(--chart-cat-2)" stroke="#fff" stroke-width="2"></circle>
    <text class="mark-label" x="702.8" y="180" text-anchor="end" fill="var(--chart-cat-2)" font-size="12">2014</text>
    <text x="702.8" y="196" text-anchor="end" font-size="10">SGMA</text>
    </g>

    <text x="70" y="222" text-anchor="start" font-size="10" fill="var(--chart-muted)">1912</text>
    <text x="740" y="222" text-anchor="end" font-size="10" fill="var(--chart-muted)">2020</text>

    <!-- Break / zoom annotation -->
    <line x1="715" y1="140" x2="725" y2="160" stroke="var(--chart-muted)" stroke-width="2"></line>
    <line x1="725" y1="140" x2="735" y2="160" stroke="var(--chart-muted)" stroke-width="2"></line>
    <text x="405" y="250" text-anchor="middle" font-size="12" font-weight="700" fill="var(--chart-text-secondary)">↓ zoomed in below: 2024–2026 (five events in about two years) ↓</text>
    <line x1="65" y1="290" x2="75" y2="310" stroke="var(--chart-muted)" stroke-width="2"></line>
    <line x1="75" y1="290" x2="85" y2="310" stroke="var(--chart-muted)" stroke-width="2"></line>

    <!-- Track 2: zoomed inset, 2023.7-2026.6, spine at y=330 -->
    <line class="axis-line" x1="70" y1="330" x2="740" y2="330"></line>

    <!-- 2024 Olam/OFI Firebaugh (above, rust, middle) -->
    <g class="tl-event" data-category="closure">
    <line x1="208.6" y1="330" x2="208.6" y2="315" class="axis-line"></line>
    <circle class="chart-hit" tabindex="0" role="button" data-label="2024 — Olam/OFI closes Firebaugh plant (dried onion/parsley), western Fresno County; 275 jobs" data-value="Closure" data-key-color="var(--chart-cat-1)" data-sourcing="WARN filing plus local/trade-press reporting." cx="208.6" cy="330" r="6" fill="var(--chart-cat-1)" stroke="#fff" stroke-width="2"></circle>
    <text x="208.6" y="288" text-anchor="middle" font-size="10">Firebaugh</text>
    <text class="mark-label" x="208.6" y="305" text-anchor="middle" fill="var(--chart-cat-1)" font-size="12">2024</text>
    </g>

    <!-- 2024 Olam/OFI Lemoore (below, rust, middle, disputed job count) -->
    <g class="tl-event" data-category="closure">
    <line x1="277.9" y1="330" x2="277.9" y2="345" class="axis-line"></line>
    <circle class="chart-hit" tabindex="0" role="button" data-label="2024 — Olam/OFI closes Lemoore tomato plant; reported job count ranges from 250 to 567 across sources, unresolved" data-value="Closure" data-key-color="var(--chart-cat-1)" data-sourcing="Disputed. Reported job counts range from 250 to 567 across sources; not yet resolved with an independent primary source." cx="277.9" cy="330" r="6" fill="var(--chart-cat-1)" stroke="#fff" stroke-width="2" stroke-dasharray="2,1.5"></circle>
    <text class="mark-label" x="277.9" y="360" text-anchor="middle" fill="var(--chart-cat-1)" font-size="12">2024</text>
    <text x="277.9" y="376" text-anchor="middle" font-size="10">Lemoore*</text>
    </g>

    <!-- 2025 Del Monte Chapter 11 (above, denim, middle) -->
    <g class="tl-event" data-category="bankruptcy">
    <line x1="439.7" y1="330" x2="439.7" y2="315" class="axis-line"></line>
    <circle class="chart-hit" tabindex="0" role="button" data-label="2025 — Del Monte Foods files Chapter 11" data-value="Bankruptcy" data-key-color="var(--chart-cat-2)" data-sourcing="Company bankruptcy filing, July 2025." cx="439.7" cy="330" r="6" fill="var(--chart-cat-2)" stroke="#fff" stroke-width="2"></circle>
    <text x="439.7" y="288" text-anchor="middle" font-size="10">Del Monte Ch. 11</text>
    <text class="mark-label" x="439.7" y="305" text-anchor="middle" fill="var(--chart-cat-2)" font-size="12">2025</text>
    </g>

    <!-- 2026 Del Monte Hanford (below, rust, end-anchor) -->
    <g class="tl-event" data-category="closure">
    <line x1="624.5" y1="330" x2="624.5" y2="345" class="axis-line"></line>
    <circle class="chart-hit" tabindex="0" role="button" data-label="2026 — Del Monte closes Hanford tomato plant, Kings County; 378–500+ jobs" data-value="Closure" data-key-color="var(--chart-cat-1)" data-sourcing="WARN filing plus local/trade-press reporting." cx="624.5" cy="330" r="6" fill="var(--chart-cat-1)" stroke="#fff" stroke-width="2"></circle>
    <text class="mark-label" x="624.5" y="360" text-anchor="end" fill="var(--chart-cat-1)" font-size="12">2026</text>
    <text x="624.5" y="376" text-anchor="end" font-size="10">Hanford</text>
    </g>

    <!-- 2026 Del Monte Modesto/Hughson (above, rust, end-anchor) -->
    <g class="tl-event" data-category="closure">
    <line x1="670.7" y1="330" x2="670.7" y2="315" class="axis-line"></line>
    <circle class="chart-hit" tabindex="0" role="button" data-label="2026 — Del Monte closes Modesto/Hughson canneries, Stanislaus County; 765 jobs" data-value="Closure" data-key-color="var(--chart-cat-1)" data-sourcing="Multiple independent news outlets, federal aid records." cx="670.7" cy="330" r="6" fill="var(--chart-cat-1)" stroke="#fff" stroke-width="2"></circle>
    <text x="670.7" y="288" text-anchor="end" font-size="10">Modesto/Hughson</text>
    <text class="mark-label" x="670.7" y="305" text-anchor="end" fill="var(--chart-cat-1)" font-size="12">2026</text>
    </g>

    <text x="70" y="402" text-anchor="start" font-size="10" fill="var(--chart-muted)">2024</text>
    <text x="740" y="402" text-anchor="end" font-size="10" fill="var(--chart-muted)">2026</text>
  </svg>
  <div class="chart-legend">
    <span class="chart-legend-item"><span class="chart-legend-swatch" style="background:var(--chart-cat-3)"></span>Founding / ownership precedent</span>
    <span class="chart-legend-item"><span class="chart-legend-swatch" style="background:var(--chart-cat-2)"></span>Bankruptcy filing / policy</span>
    <span class="chart-legend-item"><span class="chart-legend-swatch" style="background:var(--chart-cat-1)"></span>Plant closure / mass layoff</span>
  </div>
  <div class="tl-detail" id="tl-detail">
    <p class="tl-detail-empty">Click or tap any point on the timeline above for its full description and sourcing.</p>
  </div>
  <details class="chart-table-toggle">
    <summary>View as table, with sourcing notes</summary>
    <table>
      <thead><tr><th>Year</th><th>Event</th><th>Sourcing</th></tr></thead>
      <tbody>
        <tr><td>1912</td><td>Libby, McNeill &amp; Libby cannery built, Sacramento</td><td>Well documented</td></tr>
        <tr><td>1931</td><td>Bercut-Richards cannery founded, Sacramento</td><td>Well documented</td></tr>
        <tr><td>1966–67</td><td>Forty Acres becomes UFW headquarters; Farm Worker Cooperative founded, Delano</td><td>NPS National Historic Landmark nomination (2008)</td></tr>
        <tr><td>~1982</td><td>Libby cannery closes, Sacramento</td><td><strong>Thin.</strong> No contemporaneous news source located; exact year unconfirmed (early-1980s range, building NRHP-listed March 1982)</td></tr>
        <tr><td>1993</td><td>Bercut-Richards cannery closes, Sacramento</td><td><strong>Thin.</strong> No contemporaneous 1993 news source located; drawn from retrospective secondary sources</td></tr>
        <tr><td>2000</td><td>Tri Valley Growers files Chapter 11; ~11,000 Central Valley jobs lost</td><td>UC Davis Giannini Foundation (2004), Journal of Cooperatives (2009), cross-verified job figure</td></tr>
        <tr><td>2012–13</td><td>Campbell Soup closes Sacramento plant; 700 jobs</td><td>Company press release plus three independent local-news outlets</td></tr>
        <tr><td>2014</td><td>California's Sustainable Groundwater Management Act (SGMA) signed into law</td><td>Public legislative record</td></tr>
        <tr><td>2024</td><td>Olam/OFI closes Firebaugh plant; 275 jobs</td><td>WARN filing plus local/trade-press reporting</td></tr>
        <tr><td>2024</td><td>Olam/OFI closes Lemoore tomato plant</td><td><strong>Disputed.</strong> Reported job counts range from 250 to 567 across sources; not yet resolved with an independent primary source</td></tr>
        <tr><td>2025</td><td>Del Monte Foods files Chapter 11</td><td>Company bankruptcy filing, July 2025</td></tr>
        <tr><td>2026</td><td>Del Monte closes Hanford tomato plant, Kings County; 378–500+ jobs</td><td>WARN filing plus local/trade-press reporting</td></tr>
        <tr><td>2026</td><td>Del Monte closes Modesto/Hughson canneries, Stanislaus County; 765 jobs</td><td>Multiple independent news outlets, federal aid records</td></tr>
      </tbody>
    </table>
    <p class="chart-source">* Flagged in our sourcing notes as thinly documented — see <a href="data.md">Data</a> for the full access-limitations writeup (pre-1995 regional newspaper archives are not freely web-indexed, which is the single biggest limiting factor for the two earliest closures above).</p>
  </details>
  <p class="chart-source">Sources: UC Davis Giannini Foundation of Agricultural Economics; company press releases and SEC filings; WARN Act filings; Modesto Focus, KTLA, ABC30, San Joaquin Valley Sun, and other local/trade reporting; National Park Service NHL nomination records. See <a href="data.md">Data</a> for the full citation list.</p>
</div>
<script>
(function () {
  var chart = document.getElementById("timeline-chart");
  var detail = document.getElementById("tl-detail");

  // Category filter: dim non-matching events rather than hiding them, so
  // the overall shape of the 114-year span stays visible.
  var filterBtns = chart.querySelectorAll(".layer-toggle-btn");
  var events = chart.querySelectorAll(".tl-event");
  filterBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      filterBtns.forEach(function (b) {
        b.classList.toggle("active", b === btn);
        b.setAttribute("aria-pressed", b === btn ? "true" : "false");
      });
      var cat = btn.getAttribute("data-category");
      events.forEach(function (g) {
        var match = cat === "all" || g.getAttribute("data-category") === cat;
        g.classList.toggle("tl-dimmed", !match);
      });
    });
  });

  // Click-to-pin: hover already shows a quick tooltip (shared site-wide
  // script); clicking pins the full description, sourcing confidence, and
  // a jump-link to the matching photo where one exists on this page.
  function selectEvent(circle) {
    chart.querySelectorAll(".chart-hit").forEach(function (c) {
      c.classList.remove("tl-selected");
    });
    circle.classList.add("tl-selected");

    var label = circle.getAttribute("data-label");
    var sourcing = circle.getAttribute("data-sourcing");
    var photoId = circle.getAttribute("data-photo-id");
    var color = circle.getAttribute("data-key-color");

    detail.innerHTML = "";
    detail.style.borderLeftColor = color;

    var eventP = document.createElement("p");
    eventP.className = "tl-detail-event";
    eventP.textContent = label;
    detail.appendChild(eventP);

    var sourcingP = document.createElement("p");
    sourcingP.className = "tl-detail-sourcing";
    var strong = document.createElement("strong");
    strong.textContent = "Sourcing: ";
    sourcingP.appendChild(strong);
    sourcingP.appendChild(document.createTextNode(sourcing));
    detail.appendChild(sourcingP);

    if (photoId) {
      var link = document.createElement("a");
      link.className = "tl-detail-photo";
      link.href = "#" + photoId;
      link.textContent = "See the photograph ↓";
      detail.appendChild(link);
    }
  }

  chart.querySelectorAll(".chart-hit").forEach(function (circle) {
    circle.addEventListener("click", function () { selectEvent(circle); });
    circle.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        selectEvent(circle);
      }
    });
  });
})();
</script>

<div class="figure-pair">
  <figure class="figure">
    <img src="/assets/photos/04-sacramento-cannery-family-1936.jpg" alt="A Tennessee migrant family's camp on the American River near Sacramento, 1936. The mother worked in a fruit cannery.">
    <figcaption class="figure-caption"><strong>American River camp, Sacramento, 1936.</strong> A Tennessee family who came to California in 1935 — the mother worked in a fruit cannery alongside walnut, tomato, and peach work. <span class="figure-source">Dorothea Lange, Farm Security Administration. Public domain, Library of Congress.</span></figcaption>
  </figure>
  <figure class="figure">
    <img src="/assets/photos/05-shafter-cannery-union-1938.jpg" alt="A night street meeting in Shafter, California, 1938, where an organizer for the United Cannery Agricultural Packing and Allied Workers of America addresses a crowd.">
    <figcaption class="figure-caption"><strong>Shafter, California, 1938.</strong> A cannery and agricultural workers' union organizer addresses a night street meeting — nearly three decades before the UFW's own Delano organizing a few miles away. The strike this meeting was part of failed. <span class="figure-source">Dorothea Lange, Farm Security Administration. Public domain, Library of Congress.</span></figcaption>
  </figure>
</div>

<figure class="figure" id="photo-forty-acres">
  <img src="/assets/photos/07-forty-acres-clinic-habs.jpg" alt="The Rodrigo Terronez Memorial Clinic building at the Forty Acres site in Delano, California, mission-style architecture with a red tile roof.">
  <figcaption class="figure-caption"><strong>Forty Acres, Delano — the Rodrigo Terronez Memorial Clinic.</strong> No public-domain photo of the 1966–67 opening itself survives in the archives we checked (the only images we found were rights-restricted). This federal historic-documentation photo of the site itself is the substitute: the building the United Farm Workers raised as an explicit attempt at cooperative economic ownership, not just collective bargaining. <span class="figure-source">Historic American Buildings Survey, National Park Service. Public domain, Library of Congress.</span></figcaption>
</figure>

### Groundwater: a different geography

Hanford and Corcoran are both Kings County — but they sit in two different **groundwater subbasins**, which follow hydrology, not county lines. A water map of this region has to use its own geography, not the county map above.

<script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>
<div class="chart" id="gw-map-chart">
  <p class="chart-title" id="gw-map-title">Depth to groundwater, by subbasin</p>
  <p class="chart-subtitle" id="gw-map-subtitle">Most recent reading, averaged across all wells with data since 2023</p>
  <div class="layer-toggle" role="group" aria-label="Choose which groundwater measure the map shows">
    <button type="button" class="layer-toggle-btn active" data-layer="depth">Depth to groundwater (by year)</button>
    <button type="button" class="layer-toggle-btn" data-layer="change">Change since 2015</button>
  </div>
  <div class="time-slider" id="gw-time-slider">
    <label for="gw-year-range">Year: <strong id="gw-year-label">2026</strong></label>
    <input type="range" id="gw-year-range" min="1950" max="2026" step="1" value="2026">
    <div class="time-slider-ends"><span>1950</span><span>2026</span></div>
  </div>
  <div id="gw-map-svg-container" style="min-height:300px"></div>
  <div class="chart-legend" id="gw-map-legend"></div>
  <details class="chart-table-toggle">
    <summary>View as table</summary>
    <table>
      <thead><tr><th>Subbasin</th><th>Current depth to groundwater</th><th>Wells</th><th>Change since 2015</th><th>Paired wells</th></tr></thead>
      <tbody>
        <tr><td><strong>Kings Subbasin</strong> (Hanford)</td><td>131.0 ft</td><td>229</td><td>−11.2 ft (shallower)</td><td>71</td></tr>
        <tr><td><strong>Tulare Lake Subbasin</strong> (Corcoran)</td><td>176.6 ft</td><td>73</td><td>−2.6 ft (shallower)</td><td>23</td></tr>
      </tbody>
    </table>
  </details>
  <p class="chart-source" id="gw-map-source">Subbasin boundaries: DWR Bulletin 118, via CA GIS open-data portal. Groundwater: DWR periodic groundwater level measurements. See <a href="data.md">Data</a>.</p>
</div>

**The long arc, scrub the slider to see it**: both subbasins have gotten dramatically deeper since 1950 — Kings Subbasin from 38 ft to 131 ft (roughly 3.4x), Tulare Lake Subbasin from 38 ft to 173 ft (roughly 4.6x) — a real, 76-year decline consistent with the broader SGMA story this section opened with.

**An honest complication, not smoothed over**: the "Change since 2015" layer (a careful, same-well paired comparison) shows both subbasins getting *shallower* in just the last decade, not deeper — and a simpler year-to-year average comparison using the slider above disagrees with that paired method about Kings Subbasin's recent *direction* entirely. The two methods use different, non-identical sets of wells (the monitoring network itself has shrunk over time — Kings Subbasin alone went from 544 reporting wells in 1950 to 193 in 2026), and we don't have a confident answer for which is closer to the truth. We'd rather show you the disagreement than quietly pick the number that fits the narrative. Full method and the real numbers behind both claims: [Data](data.md).

<div class="figure-pair">
  <figure class="figure">
    <img src="/assets/photos/01-corcoran-picket-line-1933.jpg" alt="Trucks loaded with striking cotton workers in a 1933 picket line near Corcoran, California, one truck marked with a hand-lettered DON'T SCAB sign.">
    <figcaption class="figure-caption"><strong>Corcoran, California, October 1933.</strong> A picket line during that year's statewide cotton strike — the same town this section's Tulare Lake Subbasin map is named for. <span class="figure-source">Farm Security Administration. Public domain, Library of Congress.</span></figcaption>
  </figure>
  <figure class="figure">
    <img src="/assets/photos/02-corcoran-cotton-housing-sjv-bg-1936.jpg" alt="Rows of wooden company housing for cotton pickers south of Corcoran, California, with the open San Joaquin Valley in the background, 1936.">
    <figcaption class="figure-caption"><strong>South of Corcoran, 1936.</strong> Company housing for cotton pickers, the San Joaquin Valley's open land running to the horizon behind it — the same land this groundwater map now tracks by the foot. <span class="figure-source">Dorothea Lange, Farm Security Administration. Public domain, Library of Congress.</span></figcaption>
  </figure>
</div>

<script>
(function () {
  var gwLayers = {
    depth: {
      title: "Depth to groundwater, by subbasin",
      subtitle: "Annual average, by year selected below",
      byId: {
        "5-022.08": {name: "Kings Subbasin", note: "Hanford", value: 131.4},
        "5-022.12": {name: "Tulare Lake Subbasin", note: "Corcoran", value: 173.2}
      },
      diverging: false,
      // Gold family, light->dark -- the project's third validated series hue.
      ramp: ["#f9ecd2", "#e8c87a", "#c9960f", "#9a7108", "#6b4e05"],
      domain: [30, 235],
      format: function (v) { return v.toFixed(1) + " ft"; },
      tooltipLabel: "Depth to groundwater",
      legendLow: "Shallower",
      legendHigh: "Deeper",
      source: 'Subbasin boundaries: DWR Bulletin 118, via CA GIS open-data portal. Groundwater: DWR periodic groundwater level measurements, annual average by well. See <a href="data.md">Data</a>.'
    },
    change: {
      title: "Change in groundwater depth since 2015, by subbasin",
      subtitle: "Paired per-well comparison, 2015 vs. most recent reading since 2023 — negative = shallower = recovery",
      byId: {
        "5-022.08": {name: "Kings Subbasin", note: "Hanford", value: -11.2},
        "5-022.12": {name: "Tulare Lake Subbasin", note: "Corcoran", value: -2.6}
      },
      diverging: true,
      // Diverging: rust (decline) <-> neutral <-> denim (recovery) -- the
      // project's validated diverging pair.
      ramp: ["#7a2415", "#c23b1f", "#ece6d6", "#0e86a8", "#0a5c73"],
      domain: [-15, 15],
      format: function (v) { return (v > 0 ? "+" : "−") + Math.abs(v).toFixed(1) + " ft"; },
      tooltipLabel: "Change since 2015",
      legendLow: "Decline (deeper)",
      legendHigh: "Recovery (shallower)",
      source: 'Subbasin boundaries: DWR Bulletin 118, via CA GIS open-data portal. Groundwater: DWR periodic groundwater level measurements, paired per-well comparison. See <a href="data.md">Data</a>.'
    }
  };

  var gwContainer = document.getElementById("gw-map-svg-container");
  var gwWidth = gwContainer.clientWidth || 700, gwHeight = 300;
  var gwSvg = null, gwPath = null;

  function gwColorFor(layer, v) {
    if (layer.diverging) {
      var half = Math.max(Math.abs(layer.domain[0]), Math.abs(layer.domain[1]));
      var t = Math.max(-1, Math.min(1, v / half));
      var idx = Math.round((1 - t) / 2 * (layer.ramp.length - 1));
      return layer.ramp[idx];
    }
    var t2 = Math.max(0, Math.min(1, (v - layer.domain[0]) / (layer.domain[1] - layer.domain[0])));
    var idx2 = Math.min(layer.ramp.length - 1, Math.floor(t2 * layer.ramp.length));
    return layer.ramp[idx2];
  }

  function gwRender(layerKey) {
    var layer = gwLayers[layerKey];
    document.getElementById("gw-map-title").textContent = layer.title;
    document.getElementById("gw-map-subtitle").textContent = layer.subtitle;
    document.getElementById("gw-map-source").innerHTML = layer.source;
    document.querySelectorAll("#gw-map-chart .layer-toggle-btn").forEach(function (btn) {
      btn.classList.toggle("active", btn.getAttribute("data-layer") === layerKey);
      btn.setAttribute("aria-pressed", btn.getAttribute("data-layer") === layerKey ? "true" : "false");
    });

    gwSvg.selectAll("path.subbasin")
      .attr("fill", function (d) { return gwColorFor(layer, layer.byId[d.properties.Basin_Subbasin_Number].value); })
      .attr("data-label", function (d) {
        var info = layer.byId[d.properties.Basin_Subbasin_Number];
        return info.name + " (" + info.note + ")";
      })
      .attr("data-value", function (d) { return layer.tooltipLabel + ": " + layer.format(layer.byId[d.properties.Basin_Subbasin_Number].value); })
      .attr("data-key-color", function (d) { return gwColorFor(layer, layer.byId[d.properties.Basin_Subbasin_Number].value); });

    function textColorFor(d) {
      var v = layer.byId[d.properties.Basin_Subbasin_Number].value;
      var t = layer.diverging
        ? Math.abs(v) / Math.max(Math.abs(layer.domain[0]), Math.abs(layer.domain[1]))
        : (v - layer.domain[0]) / (layer.domain[1] - layer.domain[0]);
      return t > 0.55 ? "#fff" : null; // null -> fall back to the CSS default (ink)
    }

    gwSvg.selectAll("text.subbasin-label")
      .attr("fill", function (d) { return textColorFor(d) || "var(--chart-text-primary)"; })
      .text(function (d) { return layer.byId[d.properties.Basin_Subbasin_Number].name; });

    gwSvg.selectAll("text.subbasin-value")
      .attr("fill", function (d) { return textColorFor(d) || "var(--chart-text-secondary)"; })
      .text(function (d) { return layer.format(layer.byId[d.properties.Basin_Subbasin_Number].value); });

    var legend = document.getElementById("gw-map-legend");
    var swatches = "";
    for (var i = 0; i < layer.ramp.length; i++) {
      swatches += '<span style="display:inline-block;width:22px;height:14px;background:' + layer.ramp[i] + ';"></span>';
    }
    legend.innerHTML = '<span>' + layer.legendLow + '</span>' + swatches + '<span>' + layer.legendHigh + '</span>';
  }

  var gwAnnual = null; // {subbasin: {year: {depth, wells}}}, loaded below

  function gwApplyYear(year) {
    if (!gwAnnual) return;
    var idByKey = {"kings": "5-022.08", "tulare-lake": "5-022.12"};
    Object.keys(idByKey).forEach(function (key) {
      var rec = gwAnnual[key] && gwAnnual[key][year];
      if (rec) gwLayers.depth.byId[idByKey[key]].value = rec.depth;
    });
    gwLayers.depth.subtitle = "Annual average, " + year;
    document.getElementById("gw-year-label").textContent = year;
  }

  Promise.all([
    fetch("/assets/data/kings-tulare-lake-subbasins.geojson").then(function (r) { return r.json(); }),
    fetch("/assets/data/subbasin_annual_depth_to_groundwater.json").then(function (r) { return r.json(); })
  ])
    .then(function (results) {
      var geo = results[0];
      gwAnnual = results[1];
      gwApplyYear(document.getElementById("gw-year-range").value);

      gwSvg = d3.select(gwContainer).append("svg")
        .attr("viewBox", "0 0 " + gwWidth + " " + gwHeight)
        .attr("role", "img")
        .attr("aria-label", "Map of the Kings and Tulare Lake groundwater subbasins, shaded by a selectable groundwater measure");

      var gwProjection = d3.geoMercator().fitExtent([[20, 20], [gwWidth - 20, gwHeight - 20]], geo);
      gwPath = d3.geoPath(gwProjection);

      gwSvg.selectAll("path.subbasin")
        .data(geo.features)
        .enter()
        .append("path")
        .attr("class", "subbasin chart-hit")
        .attr("d", gwPath)
        .attr("stroke", "#fff")
        .attr("stroke-width", 2);

      gwSvg.selectAll("text.subbasin-label")
        .data(geo.features)
        .enter()
        .append("text")
        .attr("class", "subbasin-label mark-label")
        .attr("x", function (d) { return gwPath.centroid(d)[0]; })
        .attr("y", function (d) { return gwPath.centroid(d)[1]; })
        .attr("text-anchor", "middle")
        .attr("font-size", 13)
        .attr("fill", "var(--chart-text-primary)");

      gwSvg.selectAll("text.subbasin-value")
        .data(geo.features)
        .enter()
        .append("text")
        .attr("class", "subbasin-value")
        .attr("x", function (d) { return gwPath.centroid(d)[0]; })
        .attr("y", function (d) { return gwPath.centroid(d)[1] + 16; })
        .attr("text-anchor", "middle")
        .attr("font-size", 11)
        .attr("fill", "var(--chart-text-secondary)");

      gwRender("depth");

      var slider = document.getElementById("gw-year-range");
      slider.addEventListener("input", function () {
        gwApplyYear(slider.value);
        gwRender("depth");
      });

      document.querySelectorAll("#gw-map-chart .layer-toggle-btn").forEach(function (btn) {
        btn.addEventListener("click", function () {
          var layerKey = btn.getAttribute("data-layer");
          document.getElementById("gw-time-slider").style.display = layerKey === "depth" ? "" : "none";
          if (layerKey === "depth") gwApplyYear(slider.value);
          gwRender(layerKey);
        });
      });
    });
})();
</script>

## Kings County: the flagship case study

In March 2026, Del Monte closed its Hanford tomato-processing plant — the only tomato-processing facility in the company's entire ten-plant U.S./Mexico roster — eliminating 378 to 500-plus jobs.

Food manufacturing wasn't a marginal part of Kings County's economy when that plant closed. By our [Sector Dependence Index](the-index.md), the sector's share of the county's entire export-driven economic base **more than doubled between 1990 and 2025** (Employment SDI: 0.070 → 0.153 against the U.S. benchmark) — meaning the closure landed on a *growing*, increasingly central pillar of the county's economy, not a shrinking, marginal one. That's a measurable claim, not an impression — see [the Index](the-index.md) for the full numbers and [Methodology](methodology.md) for how we calculated them.

<figure class="figure">
  <img src="/assets/photos/03-corcoran-cotton-housing-1936.jpg" alt="Company housing for cotton workers near Corcoran, Kings County, California, 1936.">
  <figcaption class="figure-caption"><strong>Company housing for cotton workers near Corcoran, Kings County, 1936.</strong> Ninety years before the Hanford closure, this county's economy already ran on a single crop's hired labor, housed by the company that employed it. <span class="figure-source">Dorothea Lange, Farm Security Administration. Public domain, Library of Congress.</span></figcaption>
</figure>

## Stanislaus County: the larger, older closure

Del Monte's Modesto/Hughson canneries closed in April 2026, eliminating 765 permanent jobs and ending 20-year supply contracts with roughly 70 California peach growers — a closure substantial enough that growers are now removing an estimated 420,000 clingstone peach trees. Stanislaus has the *highest* food-processing dependence of the four counties we track (Employment SDI 0.205 in 2025), but — unlike Kings — that dependence has been *declining* since 1990 (from 0.277), not rising. We haven't yet explained why these two flagship closures sit on opposite economic trajectories; it's a real open question for further research, not glossed over here.

## Fresno and Tulare Counties

Both counties carry real, continuing exposure to the same sector — Olam/OFI's Firebaugh closure (275 jobs, 2024) sits in western Fresno County, and the broader closure wave has touched Tulare as well — but at this stage their Sector Dependence Index figures (Fresno: 0.100; Tulare: 0.119, 2025) are lower than Kings' or Stanislaus', and the narrative case-study work for each is still being built out. We're publishing their numbers now rather than waiting for the full narrative, consistent with our commitment to a checkable record over a polished one.

## What we're documenting

- **The closures themselves** — company, location, job counts, and timing, sourced to original reporting and public filings wherever we can get a primary source rather than a secondhand account.
- **The longer arc** — how this round of closures fits into a pattern of commodity-processing consolidation that has been displacing Central Valley farmworkers for more than fifty years, not a single recent shock.
- **The structural drivers** — the groundwater and land-use pressures that are reshaping what can be grown, and processed, in the affected counties going forward.
- **Precedent** — real examples, in this region's own history and elsewhere, of worker- and community-ownership structures that changed who held the cost when an industry contracted.

## An honest limitation

This research documents industry exit and its effect on displaced labor. It does not, by itself, resolve separate infrastructure problems — like drinking-water contamination in some unincorporated Central Valley communities — that sit on the same groundwater basins but require their own distinct remedies. We try to be precise about what our research does and doesn't address, rather than overstating its reach.

## Where this is going

This is the first of what we expect to be several regional case studies. The underlying question is the same wherever we look: when a single industry that organized a place for generations exits, who bears the cost, and what form of ownership might have changed that outcome.
