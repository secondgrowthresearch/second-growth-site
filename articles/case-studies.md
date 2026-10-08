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
  <label class="explorer-marker-toggle">
    <input type="checkbox" id="explorer-marker-checkbox" checked>
    Show closure &amp; photo locations
  </label>

  <div id="explorer-svg-container" style="min-height:360px"></div>
  <div class="chart-legend map-legend" id="explorer-legend"></div>
  <div class="tl-detail" id="explorer-detail">
    <p class="tl-detail-empty">Click a county or subbasin for its full detail, or a marker for what happened at that specific location.</p>
  </div>
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

  // Point markers: real closure/historical-photo locations within the four
  // counties this map actually depicts. Deliberately excludes timeline
  // events with no specific in-area location (Tri Valley Growers was
  // headquartered in San Ramon, outside this map; SGMA is a statewide law,
  // not a place; Del Monte's Chapter 11 filing isn't tied to one site) --
  // not forcing a fake pin rather than leaving them off. Coordinates are
  // standard city-center points, not sourced to a specific dataset -- fine
  // at this map's scale (county/subbasin level), not claimed as precise.
  var markers = [
    {
      name: "Hanford", lon: -119.6457, lat: 36.3274, bases: ["county", "subbasin"],
      county: "06031", subbasin: "5-022.08",
      events: [{label: "2026 — Del Monte closes Hanford tomato plant, Kings County; 378–500+ jobs", sourcing: "WARN filing plus local/trade-press reporting."}],
      photos: []
    },
    {
      name: "Corcoran", lon: -119.5604, lat: 36.0980, bases: ["county", "subbasin"],
      county: "06031", subbasin: "5-022.12",
      events: [],
      photos: [
        {id: "photo-corcoran-picket-line", label: "Photo: 1933 cotton strike picket line"},
        {id: "photo-corcoran-housing-sjv", label: "Photo: company housing, 1936"},
        {id: "photo-corcoran-housing-kings", label: "Photo: company housing, 1936 (Kings County section)"}
      ]
    },
    {
      name: "Firebaugh", lon: -120.4569, lat: 36.8597, bases: ["county"],
      county: "06019", subbasin: null,
      events: [{label: "2024 — Olam/OFI closes Firebaugh plant (dried onion/parsley), western Fresno County; 275 jobs", sourcing: "WARN filing plus local/trade-press reporting."}],
      photos: []
    },
    {
      name: "Lemoore", lon: -119.7811, lat: 36.3002, bases: ["county"],
      county: "06031", subbasin: null,
      events: [{label: "2024 — Olam/OFI closes Lemoore tomato plant; reported job count ranges from 250 to 567 across sources, unresolved", sourcing: "Disputed. Not yet resolved with an independent primary source."}],
      photos: []
    },
    {
      name: "Modesto/Hughson", lon: -120.9969, lat: 37.6391, bases: ["county"],
      county: "06099", subbasin: null,
      events: [{label: "2026 — Del Monte closes Modesto/Hughson canneries, Stanislaus County; 765 jobs", sourcing: "Multiple independent news outlets, federal aid records."}],
      photos: []
    }
  ];

  // Full 1990-2025 Employment SDI series per county, US benchmark -- same
  // verified data as the 4-county comparison chart on The Index page
  // (methodology/output/*_county_naics311_sdi.csv). Tulare's 2019 omitted:
  // confirmed data-pipeline artifact, see that chart's own documentation
  // and methodology/README.md for the full writeup.
  var countySdiSeries = {
    "06031": {1990:0.0701,1991:0.1067,1992:0.0796,1993:0.0813,1994:0.0812,1995:0.0828,1996:0.0805,1997:0.0855,1998:0.086,1999:0.1056,2000:0.0984,2001:0.103,2002:0.1186,2003:0.1701,2004:0.1855,2005:0.1802,2006:0.1751,2007:0.1367,2008:0.1803,2009:0.1569,2010:0.1631,2011:0.1757,2012:0.1811,2013:0.1811,2014:0.1768,2015:0.2114,2016:0.2048,2017:0.4187,2018:0.4059,2019:0.3976,2020:0.4016,2021:0.3901,2022:0.2095,2023:0.1827,2024:0.1889,2025:0.1529},
    "06019": {1990:0.0861,1991:0.0962,1992:0.0897,1993:0.0852,1994:0.0868,1995:0.0949,1996:0.0847,1997:0.0929,1998:0.0925,1999:0.0919,2000:0.0975,2001:0.113,2002:0.1117,2003:0.1294,2004:0.1405,2005:0.1281,2006:0.1233,2007:0.1164,2008:0.1151,2009:0.1238,2010:0.1232,2011:0.1178,2012:0.1117,2013:0.1177,2014:0.113,2015:0.1278,2016:0.1218,2017:0.1295,2018:0.1201,2019:0.1181,2020:0.1327,2021:0.1183,2022:0.1141,2023:0.1113,2024:0.105,2025:0.0995},
    "06107": {1990:0.0793,1991:0.1309,1992:0.091,1993:0.0735,1994:0.0667,1995:0.0724,1996:0.0483,1997:0.0537,1998:0.0494,1999:0.0583,2000:0.0596,2001:0.0653,2002:0.0712,2003:0.0793,2004:0.0935,2005:0.0951,2006:0.1048,2007:0.1107,2008:0.1058,2009:0.1081,2010:0.0947,2011:0.1086,2012:0.1169,2013:0.114,2014:0.1175,2015:0.1053,2016:0.1163,2017:0.1187,2018:0.1163,2020:0.1209,2021:0.126,2022:0.1196,2023:0.125,2024:0.118,2025:0.1195},
    "06099": {1990:0.2769,1991:0.2465,1992:0.2484,1993:0.2568,1994:0.2497,1995:0.2348,1996:0.2264,1997:0.2208,1998:0.2146,1999:0.202,2000:0.2063,2001:0.2129,2002:0.2049,2003:0.2952,2004:0.3064,2005:0.2978,2006:0.2865,2007:0.1671,2008:0.2501,2009:0.2576,2010:0.2586,2011:0.2401,2012:0.2653,2013:0.1979,2014:0.1986,2015:0.1899,2016:0.1918,2017:0.2346,2018:0.2335,2019:0.2227,2020:0.2273,2021:0.3616,2022:0.2211,2023:0.2438,2024:0.2227,2025:0.2046}
  };

  var container = document.getElementById("explorer-svg-container");
  var width = container.clientWidth || 700;
  var countyHeight = 360, subbasinHeight = 300;
  var currentBase = "county";
  var currentCountyLayer = "sdi";
  var currentSubbasinLayer = "depth";
  var countyGeo = null, subbasinGeo = null, subbasinAnnual = null;
  var svg = null, path = null, projection = null;

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
      .style("fill", function (d) { return textColorFor(layer, layer.byKey[d.properties[idProp]].value) || "var(--chart-text-primary)"; })
      .text(function (d) { return layer.byKey[d.properties[idProp]].name; });

    svg.selectAll("text.feature-value")
      .style("fill", function (d) { return textColorFor(layer, layer.byKey[d.properties[idProp]].value) || "var(--chart-text-secondary)"; })
      .text(function (d) { return layer.format(layer.byKey[d.properties[idProp]].value); });

    var legend = document.getElementById("explorer-legend");
    var swatches = "";
    for (var i = 0; i < layer.ramp.length; i++) {
      swatches += '<span style="display:inline-block;width:22px;height:14px;background:' + layer.ramp[i] + ';border:1px solid var(--ink);"></span>';
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

    projection = d3.geoMercator().fitExtent([[20, 20], [width - 20, height - 20]], geo);
    path = d3.geoPath(projection);

    svg.selectAll("path.feature")
      .data(geo.features)
      .enter()
      .append("path")
      .attr("class", "feature chart-hit")
      .attr("d", path)
      .attr("stroke", "var(--ink)")
      .attr("stroke-width", 2)
      .on("click", function (event, d) { selectFeature(base, d); });

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
    renderMarkers(base);
  }

  function selectMarker(marker) {
    var detail = document.getElementById("explorer-detail");
    detail.innerHTML = "";
    detail.style.borderLeftColor = "var(--ink)";

    var nameP = document.createElement("p");
    nameP.className = "tl-detail-event";
    nameP.textContent = marker.name;
    detail.appendChild(nameP);

    if (marker.events.length === 0 && marker.photos.length === 0) {
      var noneP = document.createElement("p");
      noneP.className = "tl-detail-sourcing";
      noneP.textContent = "No documented event at this location yet.";
      detail.appendChild(noneP);
    }

    marker.events.forEach(function (ev) {
      var evP = document.createElement("p");
      evP.className = "tl-detail-sourcing";
      var strong = document.createElement("strong");
      strong.textContent = ev.label + " ";
      evP.appendChild(strong);
      evP.appendChild(document.createTextNode("(" + ev.sourcing + ") See the timeline above for full sourcing."));
      detail.appendChild(evP);
    });

    marker.photos.forEach(function (ph) {
      var link = document.createElement("a");
      link.className = "tl-detail-photo";
      link.href = "#" + ph.id;
      link.textContent = ph.label + " ↓";
      link.style.display = "block";
      detail.appendChild(link);
    });
  }

  function buildSparkline(series) {
    var years = Object.keys(series).map(Number).sort(function (a, b) { return a - b; });
    if (years.length < 2) return null;
    var values = years.map(function (yr) { return series[yr]; });
    var w = 240, h = 46, pad = 4;
    var minV = Math.min.apply(null, values), maxV = Math.max.apply(null, values);
    var span = maxV - minV || 1;

    function x(i) { return pad + i * (w - 2 * pad) / (years.length - 1); }
    function y(v) { return h - pad - (v - minV) / span * (h - 2 * pad); }

    // Break into contiguous segments so a gap year (e.g. Tulare's excluded
    // 2019) shows as a visible break, not a false straight line across it.
    var segments = [];
    var current = [];
    for (var i = 0; i < years.length; i++) {
      if (i > 0 && years[i] !== years[i - 1] + 1) {
        segments.push(current);
        current = [];
      }
      current.push(i);
    }
    segments.push(current);

    var svgNS = "http://www.w3.org/2000/svg";
    var wrap = document.createElement("div");
    wrap.style.marginTop = "0.6em";
    var svgEl = document.createElementNS(svgNS, "svg");
    svgEl.setAttribute("viewBox", "0 0 " + w + " " + h);
    svgEl.setAttribute("width", w);
    svgEl.setAttribute("height", h);
    svgEl.setAttribute("aria-hidden", "true");
    svgEl.style.display = "block";

    segments.forEach(function (seg) {
      var pts = seg.map(function (i) { return x(i) + "," + y(values[i]); }).join(" ");
      var poly = document.createElementNS(svgNS, "polyline");
      poly.setAttribute("points", pts);
      poly.setAttribute("fill", "none");
      poly.setAttribute("stroke", "var(--chart-cat-1)");
      poly.setAttribute("stroke-width", "2");
      poly.setAttribute("stroke-linejoin", "round");
      poly.setAttribute("stroke-linecap", "round");
      svgEl.appendChild(poly);
    });

    var lastI = years.length - 1;
    var dot = document.createElementNS(svgNS, "circle");
    dot.setAttribute("cx", x(lastI));
    dot.setAttribute("cy", y(values[lastI]));
    dot.setAttribute("r", "3");
    dot.setAttribute("fill", "var(--chart-cat-1)");
    svgEl.appendChild(dot);

    wrap.appendChild(svgEl);
    var caption = document.createElement("p");
    caption.style.fontSize = "0.78em";
    caption.style.color = "var(--chart-muted)";
    caption.style.margin = "0.3em 0 0 0";
    caption.textContent = "Employment SDI, " + years[0] + "–" + years[lastI] + " (sparkline — see The Index for the full chart)";
    wrap.appendChild(caption);
    return wrap;
  }

  function selectFeature(base, d) {
    var idProp = idPropFor(base);
    var key = d.properties[idProp];
    var detail = document.getElementById("explorer-detail");
    detail.innerHTML = "";
    detail.style.borderLeftColor = "var(--ink)";

    var name = base === "county" ? countyLayers.sdi.byKey[key].name : subbasinLayers.depth.byKey[key].name;
    var nameP = document.createElement("p");
    nameP.className = "tl-detail-event";
    nameP.textContent = name;
    detail.appendChild(nameP);

    var statsP = document.createElement("p");
    statsP.className = "tl-detail-sourcing";
    if (base === "county") {
      var sdiVal = countyLayers.sdi.byKey[key].value;
      var unempVal = countyLayers.unemployment.byKey[key].value;
      statsP.innerHTML = "<span style=\"display:inline-block; white-space:nowrap; margin-right:1em;\"><strong>Employment SDI (2025):</strong> " + sdiVal.toFixed(3) + "</span><span style=\"display:inline-block; white-space:nowrap;\"><strong>Unemployment (Aug 2026):</strong> " + unempVal.toFixed(1) + "%</span>";
    } else {
      var depthVal = subbasinLayers.depth.byKey[key].value;
      var changeVal = subbasinLayers.change.byKey[key].value;
      statsP.innerHTML = "<span style=\"display:inline-block; white-space:nowrap; margin-right:1em;\"><strong>Depth to groundwater:</strong> " + depthVal.toFixed(1) + " ft</span><span style=\"display:inline-block; white-space:nowrap;\"><strong>Change since 2015:</strong> " + (changeVal > 0 ? "+" : "−") + Math.abs(changeVal).toFixed(1) + " ft</span>";
    }
    detail.appendChild(statsP);

    if (base === "county" && countySdiSeries[key]) {
      var spark = buildSparkline(countySdiSeries[key]);
      if (spark) detail.appendChild(spark);
    }

    var related = markers.filter(function (m) {
      return base === "county" ? m.county === key : m.subbasin === key;
    });

    var relHeader = document.createElement("p");
    relHeader.className = "tl-detail-sourcing";
    relHeader.style.marginTop = "0.7em";
    relHeader.innerHTML = "<strong>Documented here:</strong>";
    detail.appendChild(relHeader);

    if (related.length === 0) {
      var noneP = document.createElement("p");
      noneP.className = "tl-detail-sourcing";
      noneP.textContent = "No documented closures or photos yet.";
      detail.appendChild(noneP);
    } else {
      related.forEach(function (m) {
        m.events.forEach(function (ev) {
          var p = document.createElement("p");
          p.className = "tl-detail-sourcing";
          p.style.marginLeft = "1em";
          p.textContent = m.name + ": " + ev.label;
          detail.appendChild(p);
        });
        m.photos.forEach(function (ph) {
          var link = document.createElement("a");
          link.className = "tl-detail-photo";
          link.href = "#" + ph.id;
          link.textContent = m.name + " — " + ph.label + " ↓";
          link.style.display = "block";
          link.style.marginLeft = "1em";
          detail.appendChild(link);
        });
      });
    }
  }

  function renderMarkers(base) {
    svg.selectAll("g.explorer-marker").remove();
    var checkbox = document.getElementById("explorer-marker-checkbox");
    if (!checkbox.checked) return;

    var visible = markers.filter(function (m) { return m.bases.indexOf(base) !== -1; });

    var markerGroups = svg.selectAll("g.explorer-marker")
      .data(visible)
      .enter()
      .append("g")
      .attr("class", "explorer-marker")
      .attr("transform", function (d) {
        var p = projection([d.lon, d.lat]);
        return "translate(" + p[0] + "," + p[1] + ")";
      })
      .style("cursor", "pointer")
      .on("click", function (event, d) { selectMarker(d); });

    markerGroups.append("circle")
      .attr("class", "chart-hit")
      .attr("r", 7)
      .attr("fill", "var(--ink)")
      .attr("stroke", "#fff")
      .attr("stroke-width", 2)
      .attr("tabindex", 0)
      .attr("role", "button")
      .attr("data-label", function (d) { return d.name; })
      .attr("data-value", function (d) {
        var n = d.events.length + d.photos.length;
        return n + (n === 1 ? " item" : " items") + " — click to see on the map";
      })
      .attr("data-key-color", "var(--ink)");

    markerGroups.append("text")
      .attr("x", 0)
      .attr("y", -11)
      .attr("text-anchor", "middle")
      .attr("font-size", 10.5)
      .attr("font-weight", 700)
      .attr("fill", "var(--chart-text-primary)")
      .attr("stroke", "#fff")
      .attr("stroke-width", 3)
      .attr("paint-order", "stroke")
      .text(function (d) { return d.name; });
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

    document.getElementById("explorer-marker-checkbox").addEventListener("change", function () {
      renderMarkers(currentBase);
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
  <div class="chart-legend map-legend" id="gw-map-legend"></div>
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
  <figure class="figure" id="photo-corcoran-picket-line">
    <img src="/assets/photos/01-corcoran-picket-line-1933.jpg" alt="Trucks loaded with striking cotton workers in a 1933 picket line near Corcoran, California, one truck marked with a hand-lettered DON'T SCAB sign.">
    <figcaption class="figure-caption"><strong>Corcoran, California, October 1933.</strong> A picket line during that year's statewide cotton strike — the same town this section's Tulare Lake Subbasin map is named for. <span class="figure-source">Farm Security Administration. Public domain, Library of Congress.</span></figcaption>
  </figure>
  <figure class="figure" id="photo-corcoran-housing-sjv">
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
      .style("fill", function (d) { return textColorFor(d) || "var(--chart-text-primary)"; })
      .text(function (d) { return layer.byId[d.properties.Basin_Subbasin_Number].name; });

    gwSvg.selectAll("text.subbasin-value")
      .style("fill", function (d) { return textColorFor(d) || "var(--chart-text-secondary)"; })
      .text(function (d) { return layer.format(layer.byId[d.properties.Basin_Subbasin_Number].value); });

    var legend = document.getElementById("gw-map-legend");
    var swatches = "";
    for (var i = 0; i < layer.ramp.length; i++) {
      swatches += '<span style="display:inline-block;width:22px;height:14px;background:' + layer.ramp[i] + ';border:1px solid var(--ink);"></span>';
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
        .attr("stroke", "var(--ink)")
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

<figure class="figure" id="photo-corcoran-housing-kings">
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
