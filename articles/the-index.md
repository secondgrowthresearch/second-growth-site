# The Sector Dependence Index

## The question we're trying to measure

Before you can document what happens when a single industry leaves a place, you need a plain way to say how dependent that place was on the industry in the first place. A county where one processing sector accounts for a sliver of local employment is a different story than a county where that same sector is a large share of how people earn a living. We needed a consistent way to tell those two situations apart, across counties and across time — not a one-off judgment call for each case.

That's what the **Sector Dependence Index (SDI)** is for: a measure of how concentrated a local economy is in a single industry, built so the same method applies to any county and any sector, and can be compared fairly across both.

It's built on **location quotients**, a standard, long-established tool in regional economics — not something invented for this project. See [Methodology](methodology.md) for the full calculation, the data sources, and the honest limitations of the current version.

### Why this number, not just a job count

"Del Monte's closure cost roughly 500 jobs" is true but incomplete — it doesn't say whether those 500 jobs were marginal to Kings County's economy or central to it. The SDI answers that question directly, the way an economist would build the answer, using public employment data rather than an impression.

### What a location quotient actually measures

The mechanic underneath the SDI is simple, even though the name isn't: a **location quotient** compares a sector's share of local employment to that same sector's share of the benchmark economy's employment. If food manufacturing is 4% of Kings County's jobs, and 2% of U.S. jobs, Kings County's location quotient for food manufacturing is 2.0 — twice as concentrated locally as nationally. A quotient at or below 1.0 means the county has no more of that sector than the national average would predict; well above 1.0 means the county is carrying more of it than a typical place its size would.

That ratio matters because of a specific, named idea in regional economics called **economic base theory**: a local economy's health rests disproportionately on its "basic" sector — the jobs that pull money in from *outside* the local economy, through sales to other regions or countries — because that inflow is what then gets re-spent locally on groceries, rent, and services, which is what supports the "non-basic" jobs that only serve local demand. A sector with a location quotient well above 1.0 is doing more of that work than the benchmark economy typically does — which is why a county like Kings, concentrated in food processing, loses more than just a headcount when a plant like Del Monte's closes: that sector was carrying disproportionate weight in the county's export base, and the job count alone doesn't capture how much outside money was flowing through it in the first place.

**A related but different idea, worth naming precisely so the two don't blur together:** economic base theory is about where money *enters* a local economy. A separate concept — **leakage**, and the local-multiplier methods (like LM3) built to measure it — asks what happens *after* money enters: how much of each dollar stays in local circulation, re-spent at other local businesses, before it leaks out to an outside owner, landlord, or supplier. The SDI measures the first question, not the second. We don't currently calculate a leakage or local-multiplier figure for any Central Valley sector — if and when this site does, it'll be presented as its own distinct measure, not folded into the SDI's own numbers. (The same is true of a *total economic impact* figure — direct, indirect, and induced jobs and income from a single closure, the kind of estimate tools like BEA's RIMS II multipliers produce. The SDI measures how concentrated a sector is, not how large its full ripple effect would be; we don't conflate the two.)

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
  <div id="cv-map-svg-container" style="min-height:360px; position:relative;">
    <div class="map-zoom-controls">
      <button type="button" class="map-zoom-btn" data-zoom="in" aria-label="Zoom in">+</button>
      <button type="button" class="map-zoom-btn" data-zoom="out" aria-label="Zoom out">&minus;</button>
      <button type="button" class="map-zoom-btn map-zoom-reset" data-zoom="reset" aria-label="Reset zoom">Reset</button>
    </div>
  </div>
  <div class="chart-legend map-legend" id="cv-map-legend"></div>
  <details class="chart-table-toggle">
    <summary>View as table (both factors)</summary>
    <table>
      <thead><tr><th>County</th><th>Employment SDI (2025)</th><th>Unemployment rate (Aug 2026, not seasonally adjusted)</th></tr></thead>
      <tbody>
        <tr><td><strong>Kings</strong> (Hanford closure)</td><td>0.150</td><td>8.5%</td></tr>
        <tr><td>Fresno</td><td>0.094</td><td>7.8%</td></tr>
        <tr><td>Tulare</td><td>0.116</td><td>10.4%</td></tr>
        <tr><td><strong>Stanislaus</strong> (Modesto/Hughson closure)</td><td>0.200</td><td>7.0%</td></tr>
      </tbody>
    </table>
  </details>
  <div class="research-note">
  <span class="research-note-label">A note on the unemployment layer</span>
  Central Valley unemployment has a real, large seasonal cycle tied to harvest timing — in an agriculture-dependent county, unemployment typically runs lowest during peak harvest and rises in the off-season. The August 2026 figures above are not seasonally adjusted, and August sits inside most of these counties' active harvest window, so the cross-county differences shown are partly a snapshot of where each county's harvest calendar happened to be that month, not purely a stable, year-round difference in labor-market health. BLS doesn't publish a seasonally adjusted series at the county level, which is why we show the raw rate rather than imply a precision the data doesn't have.
  </div>
  <p class="chart-source" id="cv-map-source">County and state boundaries: U.S. Census Bureau via us-atlas. Terrain: Natural Earth 1:50m Gray Earth. SDI: Second Growth calculation, see <a href="methodology.md">Methodology</a>.</p>
</div>
<script>
(function () {
  var layers = {
    sdi: {
      title: "Food manufacturing dependence, by county",
      subtitle: "Employment SDI vs. the U.S. benchmark, 2025, real trade adjustment applied",
      byFips: {
        "06031": {name: "Kings", value: 0.150, note: "Hanford closure"},
        "06019": {name: "Fresno", value: 0.094, note: null},
        "06107": {name: "Tulare", value: 0.116, note: null},
        "06099": {name: "Stanislaus", value: 0.200, note: "Modesto/Hughson closure"}
      },
      // Green family, light->dark -- trial replacement for the rust ramp,
      // lightness-monotonic and legibility-checked against both text colors.
      ramp: ["#e4ead6", "#a8c489", "#4f8534", "#2f5c1f", "#17370c"],
      domain: [0.09, 0.22],
      format: function (v) { return v.toFixed(3); },
      tooltipLabel: "Employment SDI",
      legendLow: "Lower dependence",
      legendHigh: "Higher dependence",
      source: 'County and state boundaries: U.S. Census Bureau via us-atlas. Terrain: Natural Earth 1:50m Gray Earth. SDI: Second Growth calculation, see <a href="methodology.md">Methodology</a>.'
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
      source: 'County and state boundaries: U.S. Census Bureau via us-atlas. Terrain: Natural Earth 1:50m Gray Earth. Unemployment: BLS Local Area Unemployment Statistics, see <a href="data.md">Data</a>. Not seasonally adjusted.'
    }
  };

  var container = document.getElementById("cv-map-svg-container");
  // California's true bounding-box aspect ratio (computed from the state
  // outline in true Mercator units) is close to 1.16 (taller than wide).
  // 1.1 leaves a little breathing room for padding without wasting space.
  var width = container.clientWidth || 700, height = Math.round(width * 1.1);
  var currentLayer = "sdi";
  var svg = null, zoomG = null, path = null, zoomBehavior = null;

  // Which counties are "in" the study is a fact about the data, not
  // something the map code should hardcode -- any county that shows up
  // in a layer's byFips gets full data treatment (own color, label,
  // tooltip); every other California county renders as neutral
  // reference geography. Add a county to a future layer and it becomes
  // a focus county automatically, no map-code change required.
  var focusFips = {};
  Object.keys(layers).forEach(function (lk) {
    Object.keys(layers[lk].byFips).forEach(function (fips) { focusFips[fips] = true; });
  });
  function isFocus(d) { return !!focusFips[d.id]; }

  // Natural Earth 1:50m Gray Earth (shaded relief + hypsography, public
  // domain), pre-warped from source Plate Carree into true Web Mercator
  // by assets/data/ca-terrain.png's build step so a straight two-corner
  // placement against any d3.geoMercator() projection is geometrically
  // exact, not an approximation. Bounds below are the image's own exact
  // crop corners (assets/data/ca-terrain-bounds.json).
  var TERRAIN = {
    url: "/assets/data/ca-terrain.png",
    lon0: -125.21666666667213, lon1: -113.48333333333997,
    lat0: 32.183333333339114, lat1: 42.51666666667141
  };

  function addTerrain(svg, projection) {
    var topLeft = projection([TERRAIN.lon0, TERRAIN.lat1]);
    var bottomRight = projection([TERRAIN.lon1, TERRAIN.lat0]);
    svg.append("image")
      .attr("class", "map-terrain")
      .attr("href", TERRAIN.url)
      .attr("x", topLeft[0]).attr("y", topLeft[1])
      .attr("width", bottomRight[0] - topLeft[0])
      .attr("height", bottomRight[1] - topLeft[1])
      .attr("preserveAspectRatio", "none");
  }

  // Shared zoom-button wiring: + / - step by a fixed factor, Reset
  // returns to the identity transform. Wheel-zoom is deliberately off
  // (see the zoom behavior's filter below) so scrolling past the map
  // scrolls the page, not the map -- these buttons, drag-to-pan, and
  // pinch-to-zoom on touch are the supported ways in.
  function setupZoomControls(container, svg, zoomBehavior) {
    var controls = container.querySelector(".map-zoom-controls");
    if (!controls) return;
    controls.querySelectorAll(".map-zoom-btn").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var action = btn.getAttribute("data-zoom");
        if (action === "in") svg.transition().duration(200).call(zoomBehavior.scaleBy, 1.5);
        else if (action === "out") svg.transition().duration(200).call(zoomBehavior.scaleBy, 1 / 1.5);
        else svg.transition().duration(200).call(zoomBehavior.transform, d3.zoomIdentity);
      });
    });
  }

  function colorFor(layer, v) {
    var t = Math.max(0, Math.min(1, (v - layer.domain[0]) / (layer.domain[1] - layer.domain[0])));
    var idx = Math.min(layer.ramp.length - 1, Math.floor(t * layer.ramp.length));
    return layer.ramp[idx];
  }

  // Kings County, at full-state zoom, is too small on screen to hold its
  // own two-line label -- the name and value just collide with Fresno
  // and Tulare's own labels next door. Below a pixel-size threshold,
  // pull the label out below the shape on a leader line instead of
  // centering it inside, the way a print atlas handles a small county
  // or island that can't hold its own name.
  function labelPlacement(d, path) {
    var bounds = path.bounds(d);
    var centroid = path.centroid(d);
    var w = bounds[1][0] - bounds[0][0], h = bounds[1][1] - bounds[0][1];
    // Thresholds scale with the map's own width (calibrated at a ~800px
    // desktop map) rather than fixed pixels -- otherwise every county
    // shrinks together on a narrow phone screen and ones that fit fine
    // on desktop (Tulare) start false-triggering the small-county path
    // alongside Kings, and their leader labels collide with each other.
    if (w >= width * 0.0725 && h >= width * 0.05) {
      return {nameX: centroid[0], nameY: centroid[1], valueX: centroid[0], valueY: centroid[1] + 16, leader: null};
    }
    var labelX = centroid[0] - 4, labelY = bounds[1][1] + 24;
    return {
      nameX: labelX, nameY: labelY, valueX: labelX, valueY: labelY + 14,
      leader: {x1: centroid[0], y1: centroid[1], x2: labelX, y2: labelY - 17}
    };
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
      .attr("fill", function (d) {
        var info = layer.byFips[d.id];
        return info ? colorFor(layer, info.value) : "var(--chart-surface)";
      })
      .attr("fill-opacity", function (d) { return isFocus(d) ? 1 : 0.55; })
      .attr("data-label", function (d) {
        var info = layer.byFips[d.id];
        if (!info) return null;
        return info.name + (info.note ? " (" + info.note + ")" : "");
      })
      .attr("data-value", function (d) {
        var info = layer.byFips[d.id];
        return info ? layer.tooltipLabel + " " + layer.format(info.value) : null;
      })
      .attr("data-key-color", function (d) {
        var info = layer.byFips[d.id];
        return info ? colorFor(layer, info.value) : null;
      });

    svg.selectAll("text.county-label")
      .style("fill", function (d) {
        if (labelPlacement(d, path).leader) return "var(--chart-text-primary)"; // outside the fill, on neutral ground
        var v = layer.byFips[d.id].value;
        var t = (v - layer.domain[0]) / (layer.domain[1] - layer.domain[0]);
        return t > 0.5 ? "#fff" : "var(--chart-text-primary)";
      })
      .text(function (d) { return layer.byFips[d.id].name; });

    svg.selectAll("text.county-value")
      .style("fill", function (d) {
        if (labelPlacement(d, path).leader) return "var(--chart-text-secondary)";
        var v = layer.byFips[d.id].value;
        var t = (v - layer.domain[0]) / (layer.domain[1] - layer.domain[0]);
        return t > 0.5 ? "#fff" : "var(--chart-text-secondary)";
      })
      .text(function (d) { return layer.format(layer.byFips[d.id].value); });

    var legend = document.getElementById("cv-map-legend");
    var swatches = "";
    for (var i = 0; i < layer.ramp.length; i++) {
      swatches += '<span style="display:inline-block;width:22px;height:14px;background:' + layer.ramp[i] + ';border:1px solid var(--ink);"></span>';
    }
    legend.innerHTML = '<span>' + layer.legendLow + '</span>' + swatches + '<span>' + layer.legendHigh + '</span>';
  }

  Promise.all([
    fetch("/assets/data/california-counties.geojson").then(function (r) { return r.json(); }),
    fetch("/assets/data/california-outline.geojson").then(function (r) { return r.json(); })
  ]).then(function (results) {
      var allCaCounties = results[0], caOutline = results[1];
      svg = d3.select(container).append("svg")
        .attr("viewBox", "0 0 " + width + " " + height)
        .attr("role", "img")
        .attr("aria-label", "Map of California, with Kings, Fresno, Tulare, and Stanislaus counties highlighted and shaded by a selectable factor. Scroll-wheel zoom is off; use the on-map zoom buttons, drag to pan, or pinch to zoom.");

      // Fit to the whole state, not just the focus counties, so the
      // viewer sees where in California this data sits, not just the
      // data itself.
      var projection = d3.geoMercator().fitExtent([[20, 20], [width - 20, height - 20]], caOutline);
      path = d3.geoPath(projection);

      zoomG = svg.append("g").attr("class", "zoom-g");

      addTerrain(zoomG, projection);

      var geoFeatures = allCaCounties.features;

      zoomG.selectAll("path.county")
        .data(geoFeatures)
        .enter()
        .append("path")
        .attr("class", function (d) { return isFocus(d) ? "county chart-hit" : "county"; })
        .attr("d", path)
        .attr("vector-effect", "non-scaling-stroke")
        .attr("stroke", function (d) { return isFocus(d) ? "var(--ink)" : "var(--chart-baseline)"; })
        .attr("stroke-width", function (d) { return isFocus(d) ? 2.5 : 0.75; });

      // The state border itself, bold, on top of every county.
      zoomG.append("path")
        .attr("class", "state-outline")
        .datum(caOutline.features[0])
        .attr("d", path)
        .attr("vector-effect", "non-scaling-stroke")
        .attr("fill", "none")
        .attr("stroke", "var(--ink)")
        .attr("stroke-width", 1.75);

      var focusFeatures = geoFeatures.filter(isFocus);
      var leaderData = focusFeatures.filter(function (d) { return labelPlacement(d, path).leader !== null; });

      zoomG.selectAll("line.county-leader")
        .data(leaderData)
        .enter()
        .append("line")
        .attr("class", "county-leader")
        .attr("x1", function (d) { return labelPlacement(d, path).leader.x1; })
        .attr("y1", function (d) { return labelPlacement(d, path).leader.y1; })
        .attr("x2", function (d) { return labelPlacement(d, path).leader.x2; })
        .attr("y2", function (d) { return labelPlacement(d, path).leader.y2; })
        .attr("vector-effect", "non-scaling-stroke")
        .attr("stroke", "var(--ink)")
        .attr("stroke-width", 1);

      zoomG.selectAll("circle.county-anchor")
        .data(leaderData)
        .enter()
        .append("circle")
        .attr("class", "county-anchor")
        .attr("cx", function (d) { return path.centroid(d)[0]; })
        .attr("cy", function (d) { return path.centroid(d)[1]; })
        .attr("r", 2.5)
        .attr("fill", "var(--ink)");

      zoomG.selectAll("text.county-label")
        .data(focusFeatures)
        .enter()
        .append("text")
        .attr("class", "county-label mark-label")
        .attr("x", function (d) { return labelPlacement(d, path).nameX; })
        .attr("y", function (d) { return labelPlacement(d, path).nameY; })
        .attr("text-anchor", "middle")
        .attr("font-size", 13);

      zoomG.selectAll("text.county-value")
        .data(focusFeatures)
        .enter()
        .append("text")
        .attr("class", "county-value")
        .attr("x", function (d) { return labelPlacement(d, path).valueX; })
        .attr("y", function (d) { return labelPlacement(d, path).valueY; })
        .attr("text-anchor", "middle")
        .attr("font-size", 11);

      svg.append("rect")
        .attr("class", "map-frame")
        .attr("x", 0.75).attr("y", 0.75)
        .attr("width", width - 1.5).attr("height", height - 1.5)
        .attr("fill", "none")
        .attr("stroke", "var(--map-frame)")
        .attr("stroke-width", 1.5);

      zoomBehavior = d3.zoom()
        .scaleExtent([1, 8])
        .translateExtent([[0, 0], [width, height]])
        .filter(function (event) { return event.type !== "wheel"; })
        .on("zoom", function (event) { zoomG.attr("transform", event.transform); });
      svg.call(zoomBehavior);

      setupZoomControls(container, svg, zoomBehavior);

      render("sdi");

      document.querySelectorAll("#sdi-map-chart .layer-toggle-btn").forEach(function (btn) {
        btn.addEventListener("click", function () { render(btn.getAttribute("data-layer")); });
      });
    });
})();
</script>

**Employment SDI, benchmarked against the United States, 2025.** (Income SDI, charted alongside it below, reweights the same basic-employment figures by each sector's average QCEW payroll — it's a payroll-weighted variant of the employment measure, not a separate income dataset. Full definition and formula: [Methodology](methodology.md).)

<div class="chart">
  <p class="chart-title">Food manufacturing's share of each county's economic base</p>
  <p class="chart-subtitle">Employment and Income SDI by county, 2025, benchmarked against the U.S.</p>
  <svg viewBox="0 0 760 340" role="img" aria-labelledby="sdi-bar-title sdi-bar-desc">
    <title id="sdi-bar-title">Sector Dependence Index by county, 2025, real trade-adjusted U.S. benchmark</title>
    <desc id="sdi-bar-desc">Kings 0.150 employment / 0.192 income. Fresno 0.094 / 0.095. Tulare 0.116 / 0.178. Stanislaus 0.200 / 0.222.</desc>
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
      <rect class="mark-visible chart-hit" data-label="Kings — Employment SDI" data-value="0.150" data-key-color="var(--chart-cat-1)" x="112.25" y="120" width="22" height="150" rx="3" fill="var(--chart-cat-1)"></rect>
      <rect class="mark-visible chart-hit" data-label="Kings — Income SDI" data-value="0.192" data-key-color="var(--chart-cat-2)" x="138.25" y="78" width="22" height="192" rx="3" fill="var(--chart-cat-2)"></rect>
      <text class="mark-label" x="133.25" y="113" text-anchor="end">0.150</text>
      <text class="mark-label" x="139.25" y="71" text-anchor="start">0.192</text>
    </g>
    <text x="136.25" y="295" text-anchor="middle" font-size="13" font-weight="700" fill="var(--chart-text-primary)">Kings</text>
    <text x="136.25" y="311" text-anchor="middle" font-size="10.5">Hanford closure</text>

    <!-- Fresno -->
    <g class="mark-group">
      <rect class="mark-hit" x="272.5" y="20" width="48" height="250"></rect>
      <rect class="mark-visible chart-hit" data-label="Fresno — Employment SDI" data-value="0.094" data-key-color="var(--chart-cat-1)" x="284.75" y="176" width="22" height="94" rx="3" fill="var(--chart-cat-1)"></rect>
      <rect class="mark-visible chart-hit" data-label="Fresno — Income SDI" data-value="0.095" data-key-color="var(--chart-cat-2)" x="310.75" y="175" width="22" height="95" rx="3" fill="var(--chart-cat-2)"></rect>
      <text class="mark-label" x="305.75" y="169" text-anchor="end">0.094</text>
      <text class="mark-label" x="311.75" y="168" text-anchor="start">0.095</text>
    </g>
    <text x="308.75" y="295" text-anchor="middle" font-size="13" font-weight="700" fill="var(--chart-text-primary)">Fresno</text>

    <!-- Tulare -->
    <g class="mark-group">
      <rect class="mark-hit" x="445" y="20" width="48" height="250"></rect>
      <rect class="mark-visible chart-hit" data-label="Tulare — Employment SDI" data-value="0.116" data-key-color="var(--chart-cat-1)" x="457.25" y="154" width="22" height="116" rx="3" fill="var(--chart-cat-1)"></rect>
      <rect class="mark-visible chart-hit" data-label="Tulare — Income SDI" data-value="0.178" data-key-color="var(--chart-cat-2)" x="483.25" y="92" width="22" height="178" rx="3" fill="var(--chart-cat-2)"></rect>
      <text class="mark-label" x="478.25" y="147" text-anchor="end">0.116</text>
      <text class="mark-label" x="484.25" y="85" text-anchor="start">0.178</text>
    </g>
    <text x="481.25" y="295" text-anchor="middle" font-size="13" font-weight="700" fill="var(--chart-text-primary)">Tulare</text>

    <!-- Stanislaus -->
    <g class="mark-group">
      <rect class="mark-hit" x="617.5" y="20" width="48" height="250"></rect>
      <rect class="mark-visible chart-hit" data-label="Stanislaus — Employment SDI" data-value="0.200" data-key-color="var(--chart-cat-1)" x="629.75" y="70" width="22" height="200" rx="3" fill="var(--chart-cat-1)"></rect>
      <rect class="mark-visible chart-hit" data-label="Stanislaus — Income SDI" data-value="0.222" data-key-color="var(--chart-cat-2)" x="655.75" y="48" width="22" height="222" rx="3" fill="var(--chart-cat-2)"></rect>
      <text class="mark-label" x="650.75" y="63" text-anchor="end">0.200</text>
      <text class="mark-label" x="656.75" y="41" text-anchor="start">0.222</text>
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
        <tr><td><strong>Kings</strong> (Hanford closure)</td><td>0.150</td><td>0.192</td></tr>
        <tr><td>Fresno</td><td>0.094</td><td>0.095</td></tr>
        <tr><td>Tulare</td><td>0.116</td><td>0.178</td></tr>
        <tr><td><strong>Stanislaus</strong> (Modesto/Hughson closure)</td><td>0.200</td><td>0.222</td></tr>
      </tbody>
    </table>
  </details>
  <p class="chart-source">Source: BLS QCEW, 1990–2026; Second Growth Sector Dependence Index calculation. See <a href="methodology.md">Methodology</a>.</p>
</div>

In plain terms: in Kings County, food processing accounts for about 15% of the county's entire *basic* economy — every export-driven job in every sector, not just food processing. That share has risen steadily since 1990, when it was closer to 7% — though not in a straight line. See the full trajectory below.

**A second benchmark, same underlying method, both now real trade-adjusted.** The chart above benchmarks each county against the *United States*. Benchmarked against *California* instead, the picture is higher in two of the four counties:

<div class="table-scroll">
<table>
  <thead><tr><th>County</th><th>Employment SDI (US benchmark)</th><th>Employment SDI (CA benchmark)</th><th>Income SDI (US benchmark)</th><th>Income SDI (CA benchmark)</th></tr></thead>
  <tbody>
    <tr><td>Kings</td><td>0.150</td><td><strong>0.339</strong></td><td>0.192</td><td><strong>0.365</strong></td></tr>
    <tr><td>Fresno</td><td>0.094</td><td>0.108</td><td>0.095</td><td>0.108</td></tr>
    <tr><td>Tulare</td><td>0.116</td><td>0.121</td><td>0.178</td><td>0.187</td></tr>
    <tr><td>Stanislaus</td><td>0.200</td><td><strong>0.312</strong></td><td>0.222</td><td><strong>0.338</strong></td></tr>
  </tbody>
</table>
</div>

**Both columns now carry a real, year-specific trade adjustment** — the U.S. column was unadjusted (factor = 1.0) until this page's own 2026-10-12 update; it no longer is. The gap that remains between the two columns is a benchmark-choice question, not an adjustment-presence one: comparing Kings to the *entire United States'* food-processing footprint is a different question than comparing it to *California's own*, and the two economies don't carry the same share of the sector, so the same county reads as more specialized against one than the other. We lead with the U.S.-benchmark chart above because it's the more familiar comparison point; neither column is "more correct" than the other now that both are real — they're answering two different, both-legitimate questions. See [Methodology](methodology.md) for how the trade adjustment itself is calculated for each benchmark.

**A separate question the SDI alone can't answer: were these above- or below-average-wage jobs?** Food manufacturing's own average annual pay, against each county's overall average pay across every sector, 2025 (same BLS QCEW data as the SDI itself):

<div class="table-scroll">
<table>
  <thead><tr><th>County</th><th>Food-manufacturing avg. pay</th><th>County-wide avg. pay, all sectors</th><th>Difference</th></tr></thead>
  <tbody>
    <tr><td>Tulare</td><td>$74,031</td><td>$54,792</td><td><strong>35% above</strong> county average</td></tr>
    <tr><td>Kings</td><td>$73,345</td><td>$57,329</td><td><strong>28% above</strong> county average</td></tr>
    <tr><td>Stanislaus</td><td>$71,151</td><td>$64,812</td><td><strong>10% above</strong> county average</td></tr>
    <tr><td>Fresno</td><td>$56,987</td><td>$60,417</td><td>6% <em>below</em> county average</td></tr>
  </tbody>
</table>
</div>

In three of the four counties this project tracks, the food-manufacturing jobs lost to the closures in our [case studies](case-studies.md) paid *above* the county's own average — not marginal, low-wage work, but some of the better-paying jobs locally available. Fresno is the one exception. This is a different measure than the SDI (which asks how *concentrated* a sector is, not how well it pays) — we're showing it alongside, not folding it in.

**What "average pay" doesn't quite capture, for a seasonal sector:** QCEW's avg. pay divides total wages paid by a *smoothed* average employment count, not a headcount of unique workers — so for a seasonal sector like food processing, someone who works a single quarter still pulls the wage total up without fully registering in the employment denominator. It's a real, standard, correctly-computed figure, and still the best available proxy for what these jobs paid — just not the same thing as "what a typical individual processing worker took home in a year," which this data can't directly give.

<div class="chart">
  <p class="chart-title">Kings County's dependence on food manufacturing, 1990–2025</p>
  <p class="chart-subtitle">Employment SDI vs. the U.S. benchmark, real trade adjustment applied</p>
  <svg viewBox="0 0 760 300" role="img" aria-labelledby="kings-line-title kings-line-desc">
    <title id="kings-line-title">Kings County Employment SDI, 1990 to 2025</title>
    <desc id="kings-line-desc">Rose from 0.070 in 1990 to a peak of 0.419 in 2017, held near 0.40 through 2021, then fell back to 0.150 by 2025.</desc>
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
      d="M50.0,231.0 69.7,210.7 89.4,225.7 109.1,224.8 128.9,224.9 148.6,224.0 168.3,225.2 188.0,222.5 207.7,222.2 227.4,211.3 247.1,215.3 266.9,212.7 286.6,204.1 306.3,175.4 326.0,166.9 345.7,169.8 365.4,172.6 385.1,194.0 404.9,169.8 424.6,182.8 444.3,178.8 464.0,171.8 483.7,168.8 503.4,168.5 523.1,171.1 542.9,152.2 562.6,156.0 582.3,37.0 602.0,44.4 621.7,49.0 641.4,47.1 661.1,53.7 680.9,154.5 700.6,169.4 720.3,166.2 740.0,186.4"></path>

    <circle class="chart-hit" data-label="Peak, 2017" data-value="0.419" data-key-color="var(--chart-cat-1)" cx="582.3" cy="37.0" r="6" fill="var(--chart-cat-1)" stroke="#fff" stroke-width="2"></circle>
    <text class="mark-label" x="582.3" y="25" text-anchor="middle">0.419</text>
    <text x="582.3" y="290" text-anchor="middle" font-size="10.5">2017</text>

    <circle class="chart-hit" data-label="Start, 1990" data-value="0.070" data-key-color="var(--chart-cat-1)" cx="50" cy="231.0" r="6" fill="var(--chart-cat-1)" stroke="#fff" stroke-width="2"></circle>
    <text x="50" y="290" text-anchor="middle" font-size="10.5">1990</text>

    <circle class="chart-hit" data-label="2025 (most recent)" data-value="0.150" data-key-color="var(--chart-cat-1)" cx="740" cy="186.4" r="6" fill="var(--chart-cat-1)" stroke="#fff" stroke-width="2"></circle>
    <text class="mark-label" x="700" y="176" text-anchor="middle">0.150</text>
    <text x="740" y="290" text-anchor="end" font-size="10.5">2025</text>

    <line class="axis-line" x1="50" y1="270" x2="740" y2="270"></line>
  </svg>
  <details class="chart-table-toggle">
    <summary>View as table (all 36 years)</summary>
    <table>
      <thead><tr><th>Year</th><th>Employment SDI</th></tr></thead>
      <tbody>
        <tr><td>1990</td><td>0.070</td></tr><tr><td>1995</td><td>0.083</td></tr><tr><td>2000</td><td>0.098</td></tr>
        <tr><td>2005</td><td>0.180</td></tr><tr><td>2010</td><td>0.164</td></tr><tr><td>2015</td><td>0.212</td></tr>
        <tr><td>2016</td><td>0.205</td></tr><tr><td><strong>2017</strong></td><td><strong>0.419 (peak)</strong></td></tr>
        <tr><td>2018</td><td>0.406</td></tr><tr><td>2019</td><td>0.397</td></tr><tr><td>2020</td><td>0.401</td></tr>
        <tr><td>2021</td><td>0.389</td></tr><tr><td>2022</td><td>0.208</td></tr><tr><td>2023</td><td>0.181</td></tr>
        <tr><td>2024</td><td>0.187</td></tr><tr><td>2025</td><td>0.150</td></tr>
      </tbody>
    </table>
    <p class="chart-source">Full year-by-year data (all 36 years) is in the project repository's methodology output.</p>
  </details>
  <p class="chart-source">Source: BLS QCEW. Real, year-by-year trade adjustment applied to the US benchmark as of 2026-10-12 — see <a href="methodology.md">Methodology</a>.</p>
</div>

**The real shape of this trend is sharper than a two-point summary suggests.** Kings County's food-processing dependence didn't rise steadily — it climbed through the 2000s, then **spiked to 0.419 in 2017** and held near 0.40 for five straight years (2017–2021), before falling back to 0.150 by 2025.

<div class="research-note">
<span class="research-note-label">What we found</span>
Checked directly against the underlying data rather than left unexplained: this plateau is very likely a data artifact, not a real five-year economic shift. Sector 311's own employment barely moved during this window — 3,415 to 3,784 jobs throughout, no real growth. What moved was the <em>denominator</em>: total basic employment summed across every other sector, which roughly halved for exactly these five years and recovered by 2022. The same pattern shows up, much fainter, in Stanislaus County for 2021 alone, and not at all in Fresno — the largest, most diversified of the four counties — which is the signature of smaller counties having more sectors suppressed from public disclosure in any given year, not a real economic swing. Not yet traced to the specific missing data.
</div>

<div class="research-note research-note--open">
<span class="research-note-label">A systematic audit, not just these two windows</span>
This Kings plateau and Tulare's 2019 collapse (below) were both found by inspection — which raised an obvious question: are there more, smaller versions of the same issue hiding elsewhere in 36 years × 4 counties × 2 benchmarks of this calculation? A systematic check applying the same diagnostic logic to every row found <strong>16 additional flagged county-years</strong> beyond these two. Spot-checking two of them directly against the underlying data shows they are not all the same finding: one (Kings, 2022) turns out <em>not</em> to be a disclosure-suppression artifact at all — the same number of sectors were disclosed both years, with no unusual suppression — but a different, newly-identified property of the method itself, where a sector's location quotient crossing 1.0 between two years flips its entire contribution to the denominator between zero and a real number, a real source of year-to-year volatility distinct from data suppression. The other 14 flagged rows have not yet been individually classified the same way. We're naming this precisely rather than letting the two already-found artifacts stand as if they were the whole story — the series is noisier than this page previously stated, in at least two distinct ways, and most of that noise hasn't been traced to a specific cause yet.
</div>

Stanislaus County — home to the larger Modesto/Hughson closure — tells a different story: it started the most dependent of the four counties in 1990, and has been diversifying *away* from food processing over the long run (Employment SDI: 0.277 → 0.200). It shows a much smaller, single-year version of the same denominator artifact in 2021 (see above), but not the sustained multi-year pattern Kings shows.

<div class="research-note">
<span class="research-note-label">What we found</span>
A direct check of what Stanislaus actually diversified into, and a correction to this page's own earlier premise. NAICS 311 employment there did <em>not</em> stay "roughly flat" over the full 1990-2025 window — it fell 25.4% (14,475 to 10,792 jobs), concentrated in the 1990s plus one sharp, unexplained one-year drop in 2003; "roughly flat" only holds for the 2003-2025 sub-window. What filled the gap: Health Care/Social Assistance and Educational Services combined, rising from 18.9% to 31.4% of county total employment — nearly doubling in headcount, 26,101 to 62,515 jobs. No other sector comes remotely close (the next-largest gainer, Accommodation/Food Services, managed +2.7 points). Manufacturing broadly, not just food processing, lost 8 points of share county-wide — Stanislaus's falling SDI is one piece of a county-wide shift into "eds and meds," not an isolated food-processing story. A real BLS data-quality issue surfaced while computing this: the 1990 county file misfiled 13,852 real jobs — 10% of that year's total county employment — under a retired aggregate code instead of the standard sector rows this calculation reads; corrected explicitly using BLS's own more granular disclosed figures, documented in the project's methodology output rather than silently patched over.
</div>

**All four counties have this same full 36-year trajectory computed — not just Kings.** Seeing them together is more informative than reading two endpoint numbers in prose.

<div class="chart" id="compare-counties-chart">
  <p class="chart-title">Food-processing dependence, all four counties, 1990–2025</p>
  <p class="chart-subtitle">Employment SDI vs. the U.S. benchmark, real trade adjustment applied. Click a county below to isolate its line.</p>
  <div class="layer-toggle" role="group" aria-label="Highlight one county's line">
    <button type="button" class="layer-toggle-btn active" data-county="all">All counties</button>
    <button type="button" class="layer-toggle-btn" data-county="kings">Kings</button>
    <button type="button" class="layer-toggle-btn" data-county="fresno">Fresno</button>
    <button type="button" class="layer-toggle-btn" data-county="tulare">Tulare</button>
    <button type="button" class="layer-toggle-btn" data-county="stanislaus">Stanislaus</button>
  </div>
  <svg viewBox="0 0 830 300" role="img" aria-labelledby="cmp-title cmp-desc">
    <title id="cmp-title">Employment SDI, all four counties, 1990 to 2025</title>
    <desc id="cmp-desc">Kings rises from 0.070 to a 2017 peak of 0.419 then falls to 0.150. Fresno stays roughly flat, 0.086 to 0.094. Tulare rises gradually from 0.079 to 0.116, with 2019 excluded as a confirmed data artifact. Stanislaus starts highest at 0.277 and falls to 0.200, with a 2021 spike to 0.360.</desc>
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
        d="M50.0,222.1 69.7,216.5 89.4,220.1 109.1,222.6 128.9,221.7 148.6,217.2 168.3,222.9 188.0,218.3 207.7,218.6 227.4,218.9 247.1,215.8 266.9,207.2 286.6,207.9 306.3,198.1 326.0,191.9 345.7,198.8 365.4,201.4 385.1,205.3 404.9,206.0 424.6,201.2 444.3,200.3 464.0,203.3 483.7,206.7 503.4,202.6 523.1,205.6 542.9,198.4 562.6,201.9 582.3,197.7 602.0,203.3 621.7,204.6 641.4,196.9 661.1,205.2 680.9,208.8 700.6,210.2 720.3,214.2 740.0,217.7"></path>
      <circle class="chart-hit" data-label="Fresno, 2025" data-value="0.094" data-key-color="var(--chart-cat-3)" cx="740.0" cy="217.7" r="5" fill="var(--chart-cat-3)" stroke="#fff" stroke-width="1.5"></circle>
      <text x="745" y="221" text-anchor="start" font-size="11" font-weight="700" fill="var(--chart-cat-3)">Fresno</text>
    </g>

    <g class="compare-line" data-county="tulare">
      <path fill="none" stroke="var(--chart-cat-4)" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"
        d="M50.0,225.9 69.7,197.2 89.4,219.4 109.1,229.1 128.9,232.9 148.6,229.7 168.3,243.1 188.0,240.1 207.7,242.5 227.4,237.6 247.1,236.9 266.9,233.7 286.6,230.4 306.3,225.9 326.0,218.0 345.7,217.1 365.4,211.7 385.1,208.5 404.9,211.2 424.6,209.9 444.3,216.5 464.0,208.8 483.7,204.1 503.4,205.3 523.1,203.6 542.9,211.1 562.6,205.1 582.3,203.7 602.0,205.4"></path>
      <path fill="none" stroke="var(--chart-cat-4)" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" stroke-dasharray="3,2.5" opacity="0.6"
        d="M602.0,205.4 621.7,204.3"></path>
      <path fill="none" stroke="var(--chart-cat-4)" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"
        d="M641.4,203.2 661.1,200.6 680.9,205.0 700.6,201.9 720.3,206.3 740.0,205.8"></path>
      <circle class="chart-hit" data-label="Tulare, 2025" data-value="0.116" data-key-color="var(--chart-cat-4)" cx="740.0" cy="205.8" r="5" fill="var(--chart-cat-4)" stroke="#fff" stroke-width="1.5"></circle>
      <text x="745" y="202" text-anchor="start" font-size="11" font-weight="700" fill="var(--chart-cat-4)">Tulare</text>
    </g>

    <g class="compare-line" data-county="stanislaus">
      <path fill="none" stroke="var(--chart-cat-2)" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"
        d="M50.0,116.0 69.7,132.9 89.4,131.9 109.1,127.2 128.9,131.2 148.6,139.5 168.3,144.1 188.0,147.2 207.7,150.7 227.4,157.7 247.1,155.3 266.9,151.6 286.6,156.1 306.3,105.9 326.0,99.6 345.7,104.4 365.4,110.7 385.1,177.1 404.9,130.9 424.6,126.8 444.3,125.1 464.0,135.5 483.7,121.2 503.4,158.4 523.1,158.3 542.9,164.0 562.6,163.0 582.3,139.2 602.0,140.3 621.7,146.4 641.4,144.2 661.1,70.0 680.9,148.9 700.6,136.2 720.3,148.3 740.0,158.6"></path>
      <circle class="chart-hit" data-label="Stanislaus, 2025" data-value="0.200" data-key-color="var(--chart-cat-2)" cx="740.0" cy="158.6" r="5" fill="var(--chart-cat-2)" stroke="#fff" stroke-width="1.5"></circle>
      <text x="745" y="154" text-anchor="start" font-size="11" font-weight="700" fill="var(--chart-cat-2)">Stanislaus</text>
    </g>

    <g class="compare-line" data-county="kings">
      <path fill="none" stroke="var(--chart-cat-1)" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"
        d="M50.0,231.0 69.7,210.7 89.4,225.7 109.1,224.8 128.9,224.9 148.6,224.0 168.3,225.2 188.0,222.5 207.7,222.2 227.4,211.3 247.1,215.3 266.9,212.7 286.6,204.1 306.3,175.4 326.0,166.9 345.7,169.8 365.4,172.6 385.1,194.0 404.9,169.8 424.6,182.8 444.3,178.8 464.0,171.8 483.7,168.8 503.4,168.5 523.1,171.1 542.9,152.2 562.6,156.0 582.3,37.0 602.0,44.4 621.7,49.0 641.4,47.1 661.1,53.7 680.9,154.5 700.6,169.4 720.3,166.2 740.0,186.4"></path>
      <circle class="chart-hit" data-label="Kings, 2025" data-value="0.150" data-key-color="var(--chart-cat-1)" cx="740.0" cy="186.4" r="5" fill="var(--chart-cat-1)" stroke="#fff" stroke-width="1.5"></circle>
      <text x="745" y="190" text-anchor="start" font-size="11" font-weight="700" fill="var(--chart-cat-1)">Kings</text>
    </g>

    <text x="50" y="290" text-anchor="start" font-size="10.5">1990</text>
    <text x="395" y="290" text-anchor="middle" font-size="10.5">2007</text>
    <text x="740" y="290" text-anchor="end" font-size="10.5">2025</text>
    <line class="axis-line" x1="50" y1="270" x2="740" y2="270"></line>
  </svg>
  <div class="research-note" style="margin-top:0.8em;">
  <span class="research-note-label">What we found</span>
  <p style="font-size:0.92em;">Tulare's 2019 point (dashed gap above) is excluded, not interpolated or smoothed: that year's calculation collapsed to 0.9901 — a confirmed pipeline error, not a real one-year collapse in the underlying economy. Sector 311's own employment was normal that year; the denominator (total basic employment across every other sector) silently dropped every sector except food manufacturing from the sum. See the table below for the real excluded value, and the methodology repository for the full diagnosis.</p>
  </div>
  <details class="chart-table-toggle">
    <summary>View as table (all four counties, 36 years)</summary>
    <table>
      <thead><tr><th>Year</th><th>Kings</th><th>Fresno</th><th>Tulare</th><th>Stanislaus</th></tr></thead>
      <tbody>
        <tr><td>1990</td><td>0.070</td><td>0.086</td><td>0.079</td><td>0.277</td></tr>
        <tr><td>1995</td><td>0.083</td><td>0.095</td><td>0.072</td><td>0.235</td></tr>
        <tr><td>2000</td><td>0.098</td><td>0.098</td><td>0.060</td><td>0.206</td></tr>
        <tr><td>2005</td><td>0.180</td><td>0.128</td><td>0.095</td><td>0.298</td></tr>
        <tr><td>2010</td><td>0.164</td><td>0.125</td><td>0.096</td><td>0.261</td></tr>
        <tr><td>2015</td><td>0.212</td><td>0.129</td><td>0.106</td><td>0.191</td></tr>
        <tr><td>2016</td><td>0.205</td><td>0.122</td><td>0.117</td><td>0.192</td></tr>
        <tr><td><strong>2017</strong></td><td><strong>0.419 (Kings peak)</strong></td><td>0.130</td><td>0.119</td><td>0.235</td></tr>
        <tr><td>2018</td><td>0.406</td><td>0.120</td><td>0.116</td><td>0.233</td></tr>
        <tr><td>2019</td><td>0.397</td><td>0.118</td><td>excluded*</td><td>0.222</td></tr>
        <tr><td>2020</td><td>0.401</td><td>0.132</td><td>0.120</td><td>0.226</td></tr>
        <tr><td><strong>2021</strong></td><td>0.389</td><td>0.117</td><td>0.125</td><td><strong>0.360 (Stanislaus peak)</strong></td></tr>
        <tr><td>2022</td><td>0.208</td><td>0.110</td><td>0.117</td><td>0.218</td></tr>
        <tr><td>2023</td><td>0.181</td><td>0.107</td><td>0.122</td><td>0.241</td></tr>
        <tr><td>2024</td><td>0.187</td><td>0.100</td><td>0.115</td><td>0.219</td></tr>
        <tr><td>2025</td><td>0.150</td><td>0.094</td><td>0.116</td><td>0.200</td></tr>
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
