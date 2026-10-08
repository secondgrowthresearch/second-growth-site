# The Sector Dependence Index

## The question we're trying to measure

Before you can document what happens when a single industry leaves a place, you need a plain way to say how dependent that place was on the industry in the first place. A county where one processing sector accounts for a sliver of local employment is a different story than a county where that same sector is a large share of how people earn a living. We needed a consistent way to tell those two situations apart, across counties and across time — not a one-off judgment call for each case.

That's what the **Sector Dependence Index (SDI)** is for: a measure of how concentrated a local economy is in a single industry, built so the same method applies to any county and any sector, and can be compared fairly across both.

It's built on **location quotients**, a standard, long-established tool in regional economics — not something invented for this project. See [Methodology](methodology.md) for the full calculation, the data sources, and the honest limitations of the current version.

## What it shows: California's Central Valley food-processing sector

Our first application: how dependent four Central Valley counties are on **food manufacturing** (NAICS 311) — the sector behind the Del Monte and Olam/OFI plant closures we document in our [case studies](case-studies.md).

<script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>
<div class="chart" id="sdi-map-chart">
  <p class="chart-title" id="cv-map-title">Food manufacturing dependence, by county</p>
  <p class="chart-subtitle" id="cv-map-subtitle">Employment SDI vs. the U.S. benchmark, 2025</p>
  <div class="layer-toggle" role="group" aria-label="Choose which factor the map shows">
    <button type="button" class="layer-toggle-btn active" data-layer="sdi">Food-processing dependence (SDI)</button>
    <button type="button" class="layer-toggle-btn" data-layer="unemployment">Unemployment rate</button>
  </div>
  <div id="cv-map-svg-container" style="min-height:360px"></div>
  <div class="chart-legend map-legend" id="cv-map-legend"></div>
  <details class="chart-table-toggle">
    <summary>View as table (both factors)</summary>
    <table>
      <thead><tr><th>County</th><th>Employment SDI (2025)</th><th>Unemployment rate (Aug 2026, not seasonally adjusted)</th></tr></thead>
      <tbody>
        <tr><td><strong>Kings</strong> (Hanford closure)</td><td>0.153</td><td>8.5%</td></tr>
        <tr><td>Fresno</td><td>0.100</td><td>7.8%</td></tr>
        <tr><td>Tulare</td><td>0.119</td><td>10.4%</td></tr>
        <tr><td><strong>Stanislaus</strong> (Modesto/Hughson closure)</td><td>0.205</td><td>7.0%</td></tr>
      </tbody>
    </table>
  </details>
  <p class="chart-source" id="cv-map-source">County boundaries: U.S. Census Bureau via us-atlas. SDI: Second Growth calculation, see <a href="methodology.md">Methodology</a>.</p>
</div>
<script>
(function () {
  var layers = {
    sdi: {
      title: "Food manufacturing dependence, by county",
      subtitle: "Employment SDI vs. the U.S. benchmark, 2025",
      byFips: {
        "06031": {name: "Kings", value: 0.153, note: "Hanford closure"},
        "06019": {name: "Fresno", value: 0.100, note: null},
        "06107": {name: "Tulare", value: 0.119, note: null},
        "06099": {name: "Stanislaus", value: 0.205, note: "Modesto/Hughson closure"}
      },
      // Green family, light->dark -- trial replacement for the rust ramp,
      // lightness-monotonic and legibility-checked against both text colors.
      ramp: ["#e4ead6", "#a8c489", "#4f8534", "#2f5c1f", "#17370c"],
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
      byFips: {
        "06031": {name: "Kings", value: 8.5, note: null},
        "06019": {name: "Fresno", value: 7.8, note: null},
        "06107": {name: "Tulare", value: 10.4, note: null},
        "06099": {name: "Stanislaus", value: 7.0, note: null}
      },
      // Denim family, light->dark -- the project's second validated series hue,
      // used deliberately so switching layers is visually unmistakable.
      ramp: ["#e3f3f7", "#a9d6e2", "#0e86a8", "#0a5c73", "#053542"],
      domain: [6, 11],
      format: function (v) { return v.toFixed(1) + "%"; },
      tooltipLabel: "Unemployment rate",
      legendLow: "Lower unemployment",
      legendHigh: "Higher unemployment",
      source: 'County boundaries: U.S. Census Bureau via us-atlas. Unemployment: BLS Local Area Unemployment Statistics, see <a href="data.md">Data</a>. Not seasonally adjusted.'
    }
  };

  var container = document.getElementById("cv-map-svg-container");
  var width = container.clientWidth || 700, height = 360;
  var currentLayer = "sdi";
  var geoData = null;
  var svg = null, path = null;

  function colorFor(layer, v) {
    var t = Math.max(0, Math.min(1, (v - layer.domain[0]) / (layer.domain[1] - layer.domain[0])));
    var idx = Math.min(layer.ramp.length - 1, Math.floor(t * layer.ramp.length));
    return layer.ramp[idx];
  }

  function render(layerKey) {
    currentLayer = layerKey;
    var layer = layers[layerKey];
    document.getElementById("cv-map-title").textContent = layer.title;
    document.getElementById("cv-map-subtitle").textContent = layer.subtitle;
    document.getElementById("cv-map-source").innerHTML = layer.source;
    document.querySelectorAll("#sdi-map-chart .layer-toggle-btn").forEach(function (btn) {
      btn.classList.toggle("active", btn.getAttribute("data-layer") === layerKey);
      btn.setAttribute("aria-pressed", btn.getAttribute("data-layer") === layerKey ? "true" : "false");
    });

    svg.selectAll("path.county")
      .attr("fill", function (d) { return colorFor(layer, layer.byFips[d.properties.fips].value); })
      .attr("data-label", function (d) {
        var info = layer.byFips[d.properties.fips];
        return info.name + (info.note ? " (" + info.note + ")" : "");
      })
      .attr("data-value", function (d) { return layer.tooltipLabel + " " + layer.format(layer.byFips[d.properties.fips].value); })
      .attr("data-key-color", function (d) { return colorFor(layer, layer.byFips[d.properties.fips].value); });

    svg.selectAll("text.county-label")
      .style("fill", function (d) {
        var v = layer.byFips[d.properties.fips].value;
        var t = (v - layer.domain[0]) / (layer.domain[1] - layer.domain[0]);
        return t > 0.5 ? "#fff" : "var(--chart-text-primary)";
      })
      .text(function (d) { return layer.byFips[d.properties.fips].name; });

    svg.selectAll("text.county-value")
      .style("fill", function (d) {
        var v = layer.byFips[d.properties.fips].value;
        var t = (v - layer.domain[0]) / (layer.domain[1] - layer.domain[0]);
        return t > 0.5 ? "#fff" : "var(--chart-text-secondary)";
      })
      .text(function (d) { return layer.format(layer.byFips[d.properties.fips].value); });

    var legend = document.getElementById("cv-map-legend");
    var swatches = "";
    for (var i = 0; i < layer.ramp.length; i++) {
      swatches += '<span style="display:inline-block;width:22px;height:14px;background:' + layer.ramp[i] + ';border:1px solid var(--ink);"></span>';
    }
    legend.innerHTML = '<span>' + layer.legendLow + '</span>' + swatches + '<span>' + layer.legendHigh + '</span>';
  }

  fetch("/assets/data/central-valley-counties.geojson")
    .then(function (r) { return r.json(); })
    .then(function (geo) {
      geoData = geo;
      svg = d3.select(container).append("svg")
        .attr("viewBox", "0 0 " + width + " " + height)
        .attr("role", "img")
        .attr("aria-label", "Map of Kings, Fresno, Tulare, and Stanislaus counties, shaded by a selectable factor");

      svg.append("rect")
        .attr("class", "map-water-bg")
        .attr("x", 0).attr("y", 0)
        .attr("width", width).attr("height", height)
        .attr("fill", "var(--map-water)");

      var projection = d3.geoMercator().fitExtent([[20, 20], [width - 20, height - 20]], geo);
      path = d3.geoPath(projection);

      svg.selectAll("path.county")
        .data(geo.features)
        .enter()
        .append("path")
        .attr("class", "county chart-hit")
        .attr("d", path)
        .attr("stroke", "var(--ink)")
        .attr("stroke-width", 2.5);

      svg.selectAll("text.county-label")
        .data(geo.features)
        .enter()
        .append("text")
        .attr("class", "county-label mark-label")
        .attr("x", function (d) { return path.centroid(d)[0]; })
        .attr("y", function (d) { return path.centroid(d)[1]; })
        .attr("text-anchor", "middle")
        .attr("font-size", 13);

      svg.selectAll("text.county-value")
        .data(geo.features)
        .enter()
        .append("text")
        .attr("class", "county-value")
        .attr("x", function (d) { return path.centroid(d)[0]; })
        .attr("y", function (d) { return path.centroid(d)[1] + 16; })
        .attr("text-anchor", "middle")
        .attr("font-size", 11);

      svg.append("rect")
        .attr("class", "map-frame")
        .attr("x", 0.75).attr("y", 0.75)
        .attr("width", width - 1.5).attr("height", height - 1.5)
        .attr("fill", "none")
        .attr("stroke", "var(--map-frame)")
        .attr("stroke-width", 1.5);

      render("sdi");

      document.querySelectorAll("#sdi-map-chart .layer-toggle-btn").forEach(function (btn) {
        btn.addEventListener("click", function () { render(btn.getAttribute("data-layer")); });
      });
    });
})();
</script>

**Employment SDI, benchmarked against the United States, 2025:**

<div class="chart">
  <p class="chart-title">Food manufacturing's share of each county's economic base</p>
  <p class="chart-subtitle">Employment and Income SDI by county, 2025, benchmarked against the U.S.</p>
  <svg viewBox="0 0 760 340" role="img" aria-labelledby="sdi-bar-title sdi-bar-desc">
    <title id="sdi-bar-title">Sector Dependence Index by county, 2025</title>
    <desc id="sdi-bar-desc">Kings 0.153 employment / 0.195 income. Fresno 0.100 / 0.101. Tulare 0.119 / 0.184. Stanislaus 0.205 / 0.227.</desc>
    <line class="gridline" x1="50" y1="220" x2="740" y2="220"></line>
    <line class="gridline" x1="50" y1="170" x2="740" y2="170"></line>
    <line class="gridline" x1="50" y1="120" x2="740" y2="120"></line>
    <line class="gridline" x1="50" y1="70"  x2="740" y2="70"></line>
    <text x="44" y="274" text-anchor="end" font-size="12">0</text>
    <text x="44" y="224" text-anchor="end" font-size="12">0.05</text>
    <text x="44" y="174" text-anchor="end" font-size="12">0.10</text>
    <text x="44" y="124" text-anchor="end" font-size="12">0.15</text>
    <text x="44" y="74"  text-anchor="end" font-size="12">0.20</text>
    <text x="44" y="24"  text-anchor="end" font-size="12">0.25</text>

    <!-- Kings -->
    <g class="mark-group">
      <rect class="mark-hit" x="100" y="20" width="48" height="250"></rect>
      <rect class="mark-visible chart-hit" data-label="Kings — Employment SDI" data-value="0.153" data-key-color="var(--chart-cat-1)" x="112.25" y="117" width="22" height="153" rx="3" fill="var(--chart-cat-1)"></rect>
      <rect class="mark-visible chart-hit" data-label="Kings — Income SDI" data-value="0.195" data-key-color="var(--chart-cat-2)" x="138.25" y="75" width="22" height="195" rx="3" fill="var(--chart-cat-2)"></rect>
      <text class="mark-label" x="133.25" y="110" text-anchor="end">0.153</text>
      <text class="mark-label" x="139.25" y="68" text-anchor="start">0.195</text>
    </g>
    <text x="136.25" y="295" text-anchor="middle" font-size="13" font-weight="700" fill="var(--chart-text-primary)">Kings</text>
    <text x="136.25" y="311" text-anchor="middle" font-size="10.5">Hanford closure</text>

    <!-- Fresno -->
    <g class="mark-group">
      <rect class="mark-hit" x="272.5" y="20" width="48" height="250"></rect>
      <rect class="mark-visible chart-hit" data-label="Fresno — Employment SDI" data-value="0.100" data-key-color="var(--chart-cat-1)" x="284.75" y="170" width="22" height="100" rx="3" fill="var(--chart-cat-1)"></rect>
      <rect class="mark-visible chart-hit" data-label="Fresno — Income SDI" data-value="0.101" data-key-color="var(--chart-cat-2)" x="310.75" y="169" width="22" height="101" rx="3" fill="var(--chart-cat-2)"></rect>
      <text class="mark-label" x="305.75" y="163" text-anchor="end">0.100</text>
      <text class="mark-label" x="311.75" y="162" text-anchor="start">0.101</text>
    </g>
    <text x="308.75" y="295" text-anchor="middle" font-size="13" font-weight="700" fill="var(--chart-text-primary)">Fresno</text>

    <!-- Tulare -->
    <g class="mark-group">
      <rect class="mark-hit" x="445" y="20" width="48" height="250"></rect>
      <rect class="mark-visible chart-hit" data-label="Tulare — Employment SDI" data-value="0.119" data-key-color="var(--chart-cat-1)" x="457.25" y="151" width="22" height="119" rx="3" fill="var(--chart-cat-1)"></rect>
      <rect class="mark-visible chart-hit" data-label="Tulare — Income SDI" data-value="0.184" data-key-color="var(--chart-cat-2)" x="483.25" y="86" width="22" height="184" rx="3" fill="var(--chart-cat-2)"></rect>
      <text class="mark-label" x="478.25" y="144" text-anchor="end">0.119</text>
      <text class="mark-label" x="484.25" y="79" text-anchor="start">0.184</text>
    </g>
    <text x="481.25" y="295" text-anchor="middle" font-size="13" font-weight="700" fill="var(--chart-text-primary)">Tulare</text>

    <!-- Stanislaus -->
    <g class="mark-group">
      <rect class="mark-hit" x="617.5" y="20" width="48" height="250"></rect>
      <rect class="mark-visible chart-hit" data-label="Stanislaus — Employment SDI" data-value="0.205" data-key-color="var(--chart-cat-1)" x="629.75" y="65" width="22" height="205" rx="3" fill="var(--chart-cat-1)"></rect>
      <rect class="mark-visible chart-hit" data-label="Stanislaus — Income SDI" data-value="0.227" data-key-color="var(--chart-cat-2)" x="655.75" y="43" width="22" height="227" rx="3" fill="var(--chart-cat-2)"></rect>
      <text class="mark-label" x="650.75" y="58" text-anchor="end">0.205</text>
      <text class="mark-label" x="656.75" y="36" text-anchor="start">0.227</text>
    </g>
    <text x="653.75" y="295" text-anchor="middle" font-size="13" font-weight="700" fill="var(--chart-text-primary)">Stanislaus</text>
    <text x="653.75" y="311" text-anchor="middle" font-size="10.5">Modesto/Hughson closure</text>

    <line class="axis-line" x1="50" y1="270" x2="740" y2="270"></line>
  </svg>
  <div class="chart-legend">
    <span class="chart-legend-item"><span class="chart-legend-swatch" style="background:var(--chart-cat-1)"></span>Employment SDI</span>
    <span class="chart-legend-item"><span class="chart-legend-swatch" style="background:var(--chart-cat-2)"></span>Income SDI</span>
  </div>
  <details class="chart-table-toggle">
    <summary>View as table</summary>
    <table>
      <thead><tr><th>County</th><th>Employment SDI</th><th>Income SDI</th></tr></thead>
      <tbody>
        <tr><td><strong>Kings</strong> (Hanford closure)</td><td>0.153</td><td>0.195</td></tr>
        <tr><td>Fresno</td><td>0.100</td><td>0.101</td></tr>
        <tr><td>Tulare</td><td>0.119</td><td>0.184</td></tr>
        <tr><td><strong>Stanislaus</strong> (Modesto/Hughson closure)</td><td>0.205</td><td>0.227</td></tr>
      </tbody>
    </table>
  </details>
  <p class="chart-source">Source: BLS QCEW, 1990–2026; Second Growth Sector Dependence Index calculation. See <a href="methodology.md">Methodology</a>.</p>
</div>

In plain terms: in Kings County, food processing accounts for about 15% of the county's entire *basic* economy — every export-driven job in every sector, not just food processing. That share has risen steadily since 1990, when it was closer to 7% — though not in a straight line. See the full trajectory below.

<div class="chart">
  <p class="chart-title">Kings County's dependence on food manufacturing, 1990–2025</p>
  <p class="chart-subtitle">Employment SDI vs. the U.S. benchmark, unadjusted for trade</p>
  <svg viewBox="0 0 760 300" role="img" aria-labelledby="kings-line-title kings-line-desc">
    <title id="kings-line-title">Kings County Employment SDI, 1990 to 2025</title>
    <desc id="kings-line-desc">Rose from 0.070 in 1990 to a peak of 0.419 in 2017, held near 0.40 through 2021, then fell back to 0.153 by 2025.</desc>
    <line class="gridline" x1="50" y1="214.4" x2="740" y2="214.4"></line>
    <line class="gridline" x1="50" y1="158.9" x2="740" y2="158.9"></line>
    <line class="gridline" x1="50" y1="103.3" x2="740" y2="103.3"></line>
    <line class="gridline" x1="50" y1="47.8"  x2="740" y2="47.8"></line>
    <text x="44" y="274" text-anchor="end" font-size="12">0</text>
    <text x="44" y="218.4" text-anchor="end" font-size="12">0.10</text>
    <text x="44" y="162.9" text-anchor="end" font-size="12">0.20</text>
    <text x="44" y="107.3" text-anchor="end" font-size="12">0.30</text>
    <text x="44" y="51.8"  text-anchor="end" font-size="12">0.40</text>

    <path fill="none" stroke="var(--chart-cat-1)" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"
      d="M50.0,231.1 69.7,210.7 89.4,225.8 109.1,224.8 128.9,224.9 148.6,224.0 168.3,225.3 188.0,222.5 207.7,222.2 227.4,211.3 247.1,215.3 266.9,212.8 286.6,204.1 306.3,175.5 326.0,166.9 345.7,169.9 365.4,172.7 385.1,194.1 404.9,169.8 424.6,182.8 444.3,179.4 464.0,172.4 483.7,169.4 503.4,169.4 523.1,171.8 542.9,152.6 562.6,156.2 582.3,37.4 602.0,44.5 621.7,49.1 641.4,46.9 661.1,53.3 680.9,153.6 700.6,168.5 720.3,165.1 740.0,185.1"></path>

    <circle class="chart-hit" data-label="Peak, 2017" data-value="0.419" data-key-color="var(--chart-cat-1)" cx="582.3" cy="37.4" r="6" fill="var(--chart-cat-1)" stroke="#fff" stroke-width="2"></circle>
    <text class="mark-label" x="582.3" y="25" text-anchor="middle">0.419</text>
    <text x="582.3" y="290" text-anchor="middle" font-size="10.5">2017</text>

    <circle class="chart-hit" data-label="Start, 1990" data-value="0.070" data-key-color="var(--chart-cat-1)" cx="50" cy="231.1" r="6" fill="var(--chart-cat-1)" stroke="#fff" stroke-width="2"></circle>
    <text x="50" y="290" text-anchor="middle" font-size="10.5">1990</text>

    <circle class="chart-hit" data-label="2025 (most recent)" data-value="0.153" data-key-color="var(--chart-cat-1)" cx="740" cy="185.1" r="6" fill="var(--chart-cat-1)" stroke="#fff" stroke-width="2"></circle>
    <text class="mark-label" x="700" y="175" text-anchor="middle">0.153</text>
    <text x="740" y="290" text-anchor="end" font-size="10.5">2025</text>

    <line class="axis-line" x1="50" y1="270" x2="740" y2="270"></line>
  </svg>
  <details class="chart-table-toggle">
    <summary>View as table (all 36 years)</summary>
    <table>
      <thead><tr><th>Year</th><th>Employment SDI</th></tr></thead>
      <tbody>
        <tr><td>1990</td><td>0.070</td></tr><tr><td>1995</td><td>0.083</td></tr><tr><td>2000</td><td>0.098</td></tr>
        <tr><td>2005</td><td>0.180</td></tr><tr><td>2010</td><td>0.163</td></tr><tr><td>2015</td><td>0.211</td></tr>
        <tr><td>2016</td><td>0.205</td></tr><tr><td><strong>2017</strong></td><td><strong>0.419 (peak)</strong></td></tr>
        <tr><td>2018</td><td>0.406</td></tr><tr><td>2019</td><td>0.398</td></tr><tr><td>2020</td><td>0.402</td></tr>
        <tr><td>2021</td><td>0.390</td></tr><tr><td>2022</td><td>0.210</td></tr><tr><td>2023</td><td>0.183</td></tr>
        <tr><td>2024</td><td>0.189</td></tr><tr><td>2025</td><td>0.153</td></tr>
      </tbody>
    </table>
    <p class="chart-source">Full year-by-year data (all 36 years) is in the project repository's methodology output.</p>
  </details>
  <p class="chart-source">Source: BLS QCEW. Not yet trade-adjusted for the US benchmark — see <a href="methodology.md">Methodology</a>.</p>
</div>

**The real shape of this trend is sharper than a two-point summary suggests.** Kings County's food-processing dependence didn't rise steadily — it climbed through the 2000s, then **spiked to 0.419 in 2017** and held near 0.40 for five straight years (2017–2021), before falling back to 0.153 by 2025. We haven't yet researched what drove the 2017–2021 plateau specifically; it's a real, open question, not explained here.

Stanislaus County — home to the larger Modesto/Hughson closure — tells a different story: it started the most dependent of the four counties in 1990, and has been diversifying *away* from food processing over the long run (Employment SDI: 0.277 → 0.205), without the dramatic mid-2010s spike Kings shows. We haven't drawn conclusions from that contrast yet — it's a real, open question for further research, not yet explained here.

**All four counties have this same full 36-year trajectory computed — not just Kings.** Seeing them together is more informative than reading two endpoint numbers in prose.

<div class="chart" id="compare-counties-chart">
  <p class="chart-title">Food-processing dependence, all four counties, 1990–2025</p>
  <p class="chart-subtitle">Employment SDI vs. the U.S. benchmark, not yet trade-adjusted. Click a county below to isolate its line.</p>
  <div class="layer-toggle" role="group" aria-label="Highlight one county's line">
    <button type="button" class="layer-toggle-btn active" data-county="all">All counties</button>
    <button type="button" class="layer-toggle-btn" data-county="kings">Kings</button>
    <button type="button" class="layer-toggle-btn" data-county="fresno">Fresno</button>
    <button type="button" class="layer-toggle-btn" data-county="tulare">Tulare</button>
    <button type="button" class="layer-toggle-btn" data-county="stanislaus">Stanislaus</button>
  </div>
  <svg viewBox="0 0 830 300" role="img" aria-labelledby="cmp-title cmp-desc">
    <title id="cmp-title">Employment SDI, all four counties, 1990 to 2025</title>
    <desc id="cmp-desc">Kings rises from 0.070 to a 2017 peak of 0.419 then falls to 0.153. Fresno stays roughly flat, 0.086 to 0.100. Tulare rises gradually from 0.079 to 0.120, with 2019 excluded as a confirmed data artifact. Stanislaus starts highest at 0.277 and falls to 0.205, with a 2021 spike to 0.362.</desc>
    <line class="gridline" x1="50" y1="214.4" x2="740" y2="214.4"></line>
    <line class="gridline" x1="50" y1="158.9" x2="740" y2="158.9"></line>
    <line class="gridline" x1="50" y1="103.3" x2="740" y2="103.3"></line>
    <line class="gridline" x1="50" y1="47.8"  x2="740" y2="47.8"></line>
    <text x="44" y="274" text-anchor="end" font-size="12">0</text>
    <text x="44" y="218.4" text-anchor="end" font-size="12">0.10</text>
    <text x="44" y="162.9" text-anchor="end" font-size="12">0.20</text>
    <text x="44" y="107.3" text-anchor="end" font-size="12">0.30</text>
    <text x="44" y="51.8"  text-anchor="end" font-size="12">0.40</text>

    <g class="compare-line" data-county="fresno">
      <path fill="none" stroke="var(--chart-cat-3)" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"
        d="M50.0,222.1 69.7,216.5 89.4,220.1 109.1,222.6 128.9,221.7 148.6,217.2 168.3,222.9 188.0,218.3 207.7,218.6 227.4,218.9 247.1,215.8 266.9,207.2 286.6,207.9 306.3,198.1 326.0,191.9 345.7,198.8 365.4,201.5 385.1,205.3 404.9,206.0 424.6,201.2 444.3,201.5 464.0,204.5 483.7,207.9 503.4,204.6 523.1,207.2 542.9,199.0 562.6,202.3 582.3,198.0 602.0,203.2 621.7,204.3 641.4,196.2 661.1,204.2 680.9,206.6 700.6,208.1 720.3,211.6 740.0,214.7"></path>
      <circle class="chart-hit" data-label="Fresno, 2025" data-value="0.100" data-key-color="var(--chart-cat-3)" cx="740.0" cy="214.7" r="5" fill="var(--chart-cat-3)" stroke="#fff" stroke-width="1.5"></circle>
      <text x="745" y="218" text-anchor="start" font-size="11" font-weight="700" fill="var(--chart-cat-3)">Fresno</text>
    </g>

    <g class="compare-line" data-county="tulare">
      <path fill="none" stroke="var(--chart-cat-4)" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"
        d="M50.0,225.9 69.7,197.2 89.4,219.4 109.1,229.1 128.9,232.9 148.6,229.7 168.3,243.1 188.0,240.1 207.7,242.5 227.4,237.6 247.1,236.8 266.9,233.7 286.6,230.4 306.3,225.9 326.0,218.0 345.7,217.1 365.4,211.7 385.1,208.5 404.9,211.2 424.6,209.9 444.3,217.3 464.0,209.6 483.7,205.0 503.4,206.6 523.1,204.7 542.9,211.5 562.6,205.3 582.3,204.0 602.0,205.3"></path>
      <path fill="none" stroke="var(--chart-cat-4)" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" stroke-dasharray="3,2.5" opacity="0.6"
        d="M602.0,205.3 621.7,203.2"></path>
      <path fill="none" stroke="var(--chart-cat-4)" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"
        d="M641.4,202.8 661.1,200.0 680.9,203.5 700.6,200.5 720.3,204.4 740.0,203.6"></path>
      <circle class="chart-hit" data-label="Tulare, 2025" data-value="0.120" data-key-color="var(--chart-cat-4)" cx="740.0" cy="203.6" r="5" fill="var(--chart-cat-4)" stroke="#fff" stroke-width="1.5"></circle>
      <text x="745" y="200" text-anchor="start" font-size="11" font-weight="700" fill="var(--chart-cat-4)">Tulare</text>
    </g>

    <g class="compare-line" data-county="stanislaus">
      <path fill="none" stroke="var(--chart-cat-2)" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"
        d="M50.0,116.2 69.7,133.0 89.4,132.0 109.1,127.3 128.9,131.3 148.6,139.5 168.3,144.2 188.0,147.3 207.7,150.8 227.4,157.8 247.1,155.4 266.9,151.7 286.6,156.1 306.3,106.0 326.0,99.8 345.7,104.6 365.4,110.8 385.1,177.1 404.9,131.0 424.6,126.9 444.3,126.3 464.0,136.6 483.7,122.6 503.4,160.0 523.1,159.6 542.9,164.5 562.6,163.4 582.3,139.6 602.0,140.3 621.7,146.3 641.4,143.7 661.1,69.1 680.9,147.1 700.6,134.5 720.3,146.3 740.0,156.3"></path>
      <circle class="chart-hit" data-label="Stanislaus, 2025" data-value="0.205" data-key-color="var(--chart-cat-2)" cx="740.0" cy="156.3" r="5" fill="var(--chart-cat-2)" stroke="#fff" stroke-width="1.5"></circle>
      <text x="745" y="152" text-anchor="start" font-size="11" font-weight="700" fill="var(--chart-cat-2)">Stanislaus</text>
    </g>

    <g class="compare-line" data-county="kings">
      <path fill="none" stroke="var(--chart-cat-1)" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"
        d="M50.0,231.1 69.7,210.7 89.4,225.8 109.1,224.8 128.9,224.9 148.6,224.0 168.3,225.3 188.0,222.5 207.7,222.2 227.4,211.3 247.1,215.3 266.9,212.8 286.6,204.1 306.3,175.5 326.0,166.9 345.7,169.9 365.4,172.7 385.1,194.1 404.9,169.8 424.6,182.8 444.3,179.4 464.0,172.4 483.7,169.4 503.4,169.4 523.1,171.8 542.9,152.6 562.6,156.2 582.3,37.4 602.0,44.5 621.7,49.1 641.4,46.9 661.1,53.3 680.9,153.6 700.6,168.5 720.3,165.1 740.0,185.1"></path>
      <circle class="chart-hit" data-label="Kings, 2025" data-value="0.153" data-key-color="var(--chart-cat-1)" cx="740.0" cy="185.1" r="5" fill="var(--chart-cat-1)" stroke="#fff" stroke-width="1.5"></circle>
      <text x="745" y="189" text-anchor="start" font-size="11" font-weight="700" fill="var(--chart-cat-1)">Kings</text>
    </g>

    <text x="50" y="290" text-anchor="start" font-size="10.5">1990</text>
    <text x="395" y="290" text-anchor="middle" font-size="10.5">2007</text>
    <text x="740" y="290" text-anchor="end" font-size="10.5">2025</text>
    <line class="axis-line" x1="50" y1="270" x2="740" y2="270"></line>
  </svg>
  <p style="font-size:0.82em; color:var(--chart-muted); margin:0.6em 0 0 0;">Tulare's 2019 point (dashed gap above) is excluded: a confirmed error in the underlying calculation, not a real one-year collapse — see the table below.</p>
  <details class="chart-table-toggle">
    <summary>View as table (all four counties, 36 years)</summary>
    <table>
      <thead><tr><th>Year</th><th>Kings</th><th>Fresno</th><th>Tulare</th><th>Stanislaus</th></tr></thead>
      <tbody>
        <tr><td>1990</td><td>0.070</td><td>0.086</td><td>0.079</td><td>0.277</td></tr>
        <tr><td>1995</td><td>0.083</td><td>0.095</td><td>0.072</td><td>0.235</td></tr>
        <tr><td>2000</td><td>0.098</td><td>0.098</td><td>0.060</td><td>0.206</td></tr>
        <tr><td>2005</td><td>0.180</td><td>0.128</td><td>0.095</td><td>0.298</td></tr>
        <tr><td>2010</td><td>0.163</td><td>0.123</td><td>0.095</td><td>0.259</td></tr>
        <tr><td>2015</td><td>0.211</td><td>0.128</td><td>0.105</td><td>0.190</td></tr>
        <tr><td>2016</td><td>0.205</td><td>0.122</td><td>0.116</td><td>0.192</td></tr>
        <tr><td><strong>2017</strong></td><td><strong>0.419 (Kings peak)</strong></td><td>0.130</td><td>0.119</td><td>0.235</td></tr>
        <tr><td>2018</td><td>0.406</td><td>0.120</td><td>0.116</td><td>0.234</td></tr>
        <tr><td>2019</td><td>0.398</td><td>0.118</td><td>excluded*</td><td>0.223</td></tr>
        <tr><td>2020</td><td>0.402</td><td>0.133</td><td>0.121</td><td>0.227</td></tr>
        <tr><td><strong>2021</strong></td><td>0.390</td><td>0.118</td><td>0.126</td><td><strong>0.362 (Stanislaus peak)</strong></td></tr>
        <tr><td>2022</td><td>0.210</td><td>0.114</td><td>0.120</td><td>0.221</td></tr>
        <tr><td>2023</td><td>0.183</td><td>0.111</td><td>0.125</td><td>0.244</td></tr>
        <tr><td>2024</td><td>0.189</td><td>0.105</td><td>0.118</td><td>0.223</td></tr>
        <tr><td>2025</td><td>0.153</td><td>0.100</td><td>0.120</td><td>0.205</td></tr>
      </tbody>
    </table>
    <p class="chart-source">* Tulare 2019: the underlying calculation's "total basic jobs, all sectors" denominator collapsed to 4,809 that year (vs. ~42,000 in 2018 and ~38,000 in 2020) — nearly equal to sector 311's own basic employment alone, meaning every other sector was silently dropped from the sum for that one county-year. A confirmed data-pipeline bug, not a real economic event. Flagged for a fix in the underlying calculation; excluded here rather than shown as a false 0.99 spike. Full 16-year subset shown; all 36 years are in the downloadable CSV.</p>
  </details>
  <p class="chart-source">Source: BLS QCEW, 1990–2026; Second Growth Sector Dependence Index calculation. See <a href="methodology.md">Methodology</a>.</p>
</div>
<script>
(function () {
  var chart = document.getElementById("compare-counties-chart");
  var btns = chart.querySelectorAll(".layer-toggle-btn");
  var lines = chart.querySelectorAll(".compare-line");
  btns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      btns.forEach(function (b) {
        b.classList.toggle("active", b === btn);
        b.setAttribute("aria-pressed", b === btn ? "true" : "false");
      });
      var county = btn.getAttribute("data-county");
      lines.forEach(function (g) {
        var match = county === "all" || g.getAttribute("data-county") === county;
        g.classList.toggle("compare-dimmed", !match);
      });
    });
  });
})();
</script>

## Why this number, not just a job count

"Del Monte's closure cost roughly 500 jobs" is true but incomplete — it doesn't say whether those 500 jobs were marginal to Kings County's economy or central to it. The SDI answers that question directly, the way an economist would build the answer, using public employment data rather than an impression.

## A real refinement, not a finished number

The location-quotient calculation above assumes the benchmark economy (the US, or California) is roughly self-sufficient in food processing — neither a meaningful net importer nor exporter. We checked that assumption against real trade data rather than assuming it, and it turned out to matter: **California's international trade balance in this sector has flipped from a small surplus in 2010 to an $11.4 billion deficit in 2025.**

<div class="chart">
  <p class="chart-title">California's food-manufacturing trade balance, 2010–2025</p>
  <p class="chart-subtitle">Net exports (NAICS 311, international trade only)</p>
  <svg viewBox="0 0 730 340" role="img" aria-labelledby="trade-div-title trade-div-desc">
    <title id="trade-div-title">California NAICS 311 net exports, 2010 to 2025</title>
    <desc id="trade-div-desc">A small surplus of $129 million in 2010 flips to a deficit by 2012 and worsens almost every year, reaching an $11.4 billion deficit in 2025.</desc>
    <rect x="60" y="20" width="610" height="20" fill="var(--chart-div-pos-300)" opacity="0.35"></rect>
    <rect x="60" y="40" width="610" height="240" fill="var(--chart-div-neg-300)" opacity="0.35"></rect>
    <line class="gridline" x1="60" y1="20"  x2="670" y2="20"></line>
    <line class="gridline" x1="60" y1="80"  x2="670" y2="80"></line>
    <line class="gridline" x1="60" y1="120" x2="670" y2="120"></line>
    <line class="gridline" x1="60" y1="160" x2="670" y2="160"></line>
    <line class="gridline" x1="60" y1="200" x2="670" y2="200"></line>
    <line class="gridline" x1="60" y1="240" x2="670" y2="240"></line>
    <text x="54" y="24"  text-anchor="end" font-size="12">+$1B</text>
    <text x="54" y="44"  text-anchor="end" font-size="12">$0</text>
    <text x="54" y="84"  text-anchor="end" font-size="12">−$2B</text>
    <text x="54" y="124" text-anchor="end" font-size="12">−$4B</text>
    <text x="54" y="164" text-anchor="end" font-size="12">−$6B</text>
    <text x="54" y="204" text-anchor="end" font-size="12">−$8B</text>
    <text x="54" y="244" text-anchor="end" font-size="12">−$10B</text>

    <path fill="none" stroke="var(--chart-cat-1)" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"
      d="M60.0,37.4 100.7,36.7 141.3,48.8 182.0,31.1 222.7,41.6 263.3,71.5 304.0,85.6 344.7,100.5 385.3,120.7 426.0,117.4 466.7,131.1 507.3,152.8 548.0,178.4 588.7,197.0 629.3,244.8 670.0,267.5"></path>

    <circle class="chart-hit" data-label="2010" data-value="+$129M surplus" data-key-color="var(--chart-cat-1)" cx="60" cy="37.4" r="6" fill="var(--chart-cat-2)" stroke="#fff" stroke-width="2"></circle>
    <text class="mark-label" x="60" y="15" text-anchor="start" fill="var(--denim-dark)">+$129M</text>

    <circle class="chart-hit" data-label="2025" data-value="−$11.4B deficit" data-key-color="var(--chart-cat-1)" cx="670" cy="267.5" r="6" fill="var(--chart-cat-1)" stroke="#fff" stroke-width="2"></circle>
    <text class="mark-label" x="670" y="296" text-anchor="end" font-size="15" fill="var(--chart-cat-1)">−$11.4B</text>

    <text x="60" y="313" text-anchor="start" font-size="10.5">2010</text>
    <text x="263.3" y="313" text-anchor="middle" font-size="10.5">2015</text>
    <text x="466.7" y="313" text-anchor="middle" font-size="10.5">2020</text>
    <text x="629.3" y="313" text-anchor="end" font-size="10.5">2024</text>

    <line class="axis-line" x1="60" y1="40" x2="670" y2="40"></line>
  </svg>
  <div class="chart-legend">
    <span class="chart-legend-item"><span class="chart-legend-swatch" style="background:var(--chart-div-pos-500)"></span>Surplus (exports &gt; imports)</span>
    <span class="chart-legend-item"><span class="chart-legend-swatch" style="background:var(--chart-div-neg-500)"></span>Deficit (imports &gt; exports)</span>
  </div>
  <details class="chart-table-toggle">
    <summary>View as table</summary>
    <table>
      <thead><tr><th>Year</th><th>Net exports</th></tr></thead>
      <tbody>
        <tr><td>2010</td><td>+$129M</td></tr><tr><td>2011</td><td>+$167M</td></tr>
        <tr><td>2012</td><td>−$440M</td></tr><tr><td>2013</td><td>+$446M</td></tr>
        <tr><td>2014</td><td>−$81M</td></tr><tr><td>2015</td><td>−$1.6B</td></tr>
        <tr><td>2016</td><td>−$2.3B</td></tr><tr><td>2017</td><td>−$3.0B</td></tr>
        <tr><td>2018</td><td>−$4.0B</td></tr><tr><td>2019</td><td>−$3.9B</td></tr>
        <tr><td>2020</td><td>−$4.6B</td></tr><tr><td>2021</td><td>−$5.6B</td></tr>
        <tr><td>2022</td><td>−$6.9B</td></tr><tr><td>2023</td><td>−$7.9B</td></tr>
        <tr><td>2024</td><td>−$10.2B</td></tr><tr><td><strong>2025</strong></td><td><strong>−$11.4B</strong></td></tr>
      </tbody>
    </table>
  </details>
  <p class="chart-source">Source: U.S. Census Bureau, state exports/imports by NAICS (bulk files, international trade only). See <a href="data.md">Data</a>.</p>
</div>

Where we have the data to correct for this (California benchmark, 2010–2025), we do. Full detail, including what's still unadjusted and why, is in [Methodology](methodology.md).
