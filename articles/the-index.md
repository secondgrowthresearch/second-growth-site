# The Sector Dependence Index

## The question we're trying to measure

Before you can document what happens when a single industry leaves a place, you need a plain way to say how dependent that place was on the industry in the first place. A county where one processing sector accounts for a sliver of local employment is a different story than a county where that same sector is a large share of how people earn a living. We needed a consistent way to tell those two situations apart, across counties and across time — not a one-off judgment call for each case.

That's what the **Sector Dependence Index (SDI)** is for: a measure of how concentrated a local economy is in a single industry, built so the same method applies to any county and any sector, and can be compared fairly across both.

It's built on **location quotients**, a standard, long-established tool in regional economics — not something invented for this project. See [Methodology](methodology.md) for the full calculation, the data sources, and the honest limitations of the current version.

## What it shows: California's Central Valley food-processing sector

Our first application: how dependent four Central Valley counties are on **food manufacturing** (NAICS 311) — the sector behind the Del Monte and Olam/OFI plant closures we document in our [case studies](case-studies.md).

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
