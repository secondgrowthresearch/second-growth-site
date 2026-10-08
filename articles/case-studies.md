# Case Studies

## California's Central Valley: the first case study

Second Growth's first body of research documents more than fifty years of commodity agriculture consolidation in California's Central Valley, and what it has meant for the people who did the work of growing and processing it. We're starting with four counties — **Kings, Fresno, Tulare, and Stanislaus** — where that pattern is long-running and well documented.

### The pattern we're tracking

Commodity food processing has been a defining industry across these counties for generations — the kind of industry a region's labor market, tax base, and civic life organize around. Over the past two years alone, plant closures and mass layoffs tied to major processors have removed well over two thousand documented jobs across Stanislaus, Kings, and Fresno counties, and that period sits inside a far longer pattern of consolidation that goes back decades. Reporting around one recent closure placed it among roughly sixty Central Valley plant closures or mass layoffs in a single year.

These aren't isolated business decisions happening in a vacuum. They track a structural pressure on the region: California's Sustainable Groundwater Management Act is expected to push a significant share of San Joaquin Valley irrigated farmland out of production over the next two decades as groundwater use is brought into balance. Processing capacity and the water-constrained supply it depends on are moving in the same direction, in the same places, at the same time.

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
