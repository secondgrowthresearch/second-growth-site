# Making the new load pay its own way

A large new electrical customer changes what a utility has to build to serve everyone — more generation, more transmission capacity, sometimes a whole new substation. The question this mechanism asks: who pays for that new capacity, the new customer who caused the need for it, or every existing ratepayer, spread across their bills?

<div class="stat-pair">
  <div class="stat-card stat-card--absence">
    <p class="stat-number" data-target="0" data-decimals="0">0</p>
    <p class="stat-label">Dollar figure found anywhere, after two independent search passes, for a California publicly owned utility charging a large new load the actual cost of the capacity it requires.</p>
  </div>
  <div class="stat-card">
    <p class="stat-number" data-target="2027" data-decimals="0">0</p>
    <p class="stat-label">The year most of California's new "data centers pay their own way" grid-cost law is set to take effect — a real, enacted framework, not yet an operating one.</p>
  </div>
</div>

<div class="chart">
  <p class="chart-title">What a cost-internalizing mechanism does to a market</p>
  <p class="chart-subtitle">Illustrative, not to scale — the general shape behind cost-causation ratemaking and CEQA leverage alike.</p>
  <svg viewBox="0 0 460 300" style="width:100%; height:auto; display:block;" role="img" aria-label="A cost diagram. The marginal social cost curve sits above the marginal private cost curve, because the private cost doesn't include the externality. A Pigouvian payment closes that gap, moving the market from its unregulated quantity to the more efficient, lower quantity.">
    <line x1="60" y1="30" x2="60" y2="250" stroke="var(--ink)" stroke-width="1.5"></line>
    <line x1="60" y1="250" x2="420" y2="250" stroke="var(--ink)" stroke-width="1.5"></line>
    <text x="65" y="40" font-size="11.5" fill="var(--chart-text-secondary)">Cost per unit</text>
    <text x="330" y="270" font-size="11.5" fill="var(--chart-text-secondary)">Quantity / scale of impact</text>

    <line x1="90" y1="70" x2="400" y2="235" stroke="var(--chart-cat-2)" stroke-width="2"></line>
    <text x="405" y="240" font-size="12" fill="var(--chart-cat-2)">D</text>

    <line x1="80" y1="230" x2="370" y2="80" stroke="var(--chart-cat-1)" stroke-width="2"></line>
    <text x="375" y="78" font-size="12" fill="var(--chart-cat-1)">MPC</text>

    <line x1="80" y1="190" x2="340" y2="35" stroke="var(--chart-cat-1)" stroke-width="2" stroke-dasharray="6 4"></line>
    <text x="345" y="38" font-size="12" fill="var(--chart-cat-1)">MSC</text>

    <circle cx="262" cy="145" r="5" fill="var(--ink)"></circle>
    <circle cx="210" cy="112" r="5" fill="var(--ink)"></circle>
    <line x1="262" y1="145" x2="262" y2="250" stroke="var(--chart-muted)" stroke-width="1" stroke-dasharray="3 3"></line>
    <line x1="210" y1="112" x2="210" y2="250" stroke="var(--chart-muted)" stroke-width="1" stroke-dasharray="3 3"></line>
    <text x="262" y="265" font-size="10" fill="var(--chart-muted)" text-anchor="middle">Q&#7707; (unregulated)</text>
    <text x="210" y="283" font-size="10" fill="var(--chart-muted)" text-anchor="middle">Q&#7779; (efficient)</text>

    <line x1="210" y1="112" x2="210" y2="148" stroke="var(--ink)" stroke-width="2"></line>
    <text x="150" y="130" font-size="10.5" fill="var(--chart-text-primary)" text-anchor="end">Pigouvian payment closes this gap</text>
  </svg>
</div>

## The principle

Economists call this cost-causation ratemaking — a real-world instance of what's generally known as Pigouvian cost internalization, named for economist Arthur Pigou: the idea that whoever causes a cost should be the one billed for it, rather than that cost being folded into everyone's rates equally. It's the same logic behind a developer paying for the sewer-line extension their own subdivision requires, applied to electrical grid capacity.

## What one local utility already tried

The Modesto Irrigation District (MID) already requires large-load developers to pay up front for a utility-commissioned study of the grid impact their project would cause, before connection — a real, concrete, cost-causation practice already in place locally, found in this project's research into the Riverbank/Stanislaus County data-center proposals. A MID board member, Janice Keating, separately proposed a punitive triple-rate electricity tier specifically for data centers, plus a ban on staff signing NDAs with data-center prospects being courted for the district's territory. **Her board colleagues did not adopt either proposal** — a real, named, rejected local accountability measure, logged here because a measure that was proposed and voted down is still a fact worth knowing, not a fact to quietly drop because it didn't pass.

## The new state law, and why it doesn't have a number yet

California enacted a seven-bill package in September 2026 addressing data-center energy and water use. Three of the seven bear directly on this mechanism: AB 2383 and SB 886 direct the CPUC to design new tariffs making data centers cover the generation and transmission costs tied specifically to their own new load, with a 10-year minimum payment structure meant to prevent those costs from being shifted onto other ratepayers; SB 1168 separately directs the CPUC to evaluate rate structures ensuring data centers pay their "reasonable share" of distribution infrastructure costs. **None of the three bills sets an actual dollar figure.** They order the CPUC to design the tariff mechanism that eventually will, and most of the package doesn't take effect until January 1, 2027. The other four bills in the same package govern water-use and reporting disclosure, not grid costs, and shouldn't be conflated with these three.

## Who regulates this, really

<div class="chart">
  <p class="chart-title">Where the money actually goes</p>
  <svg viewBox="0 0 560 160" style="width:100%; height:auto; display:block;" role="img" aria-label="Flow diagram: DOE grid-infrastructure funding, through GRIP and SPARK, is the real federal angle for capital -- but rate-setting itself runs through the Modesto Irrigation District's own board, which already requires a grid-impact study before connection.">
    <rect x="10" y="30" width="160" height="80" rx="6" fill="var(--chart-surface)" stroke="var(--ink)" stroke-width="1.5"></rect>
    <text x="90" y="65" font-size="10.5" text-anchor="middle" fill="var(--chart-text-primary)">DOE grid-infrastructure</text>
    <text x="90" y="79" font-size="10.5" text-anchor="middle" fill="var(--chart-text-primary)">funding (GRIP / SPARK)</text>

    <line x1="172" y1="70" x2="192" y2="70" stroke="var(--ink)" stroke-width="1.5"></line>
    <polygon points="192,64 192,76 202,70" fill="var(--ink)"></polygon>

    <rect x="200" y="30" width="160" height="80" rx="6" fill="var(--chart-surface)" stroke="var(--ink)" stroke-width="1.5"></rect>
    <text x="280" y="65" font-size="10.5" text-anchor="middle" fill="var(--chart-text-primary)">Modesto Irrigation</text>
    <text x="280" y="79" font-size="10.5" text-anchor="middle" fill="var(--chart-text-primary)">District board</text>

    <line x1="362" y1="70" x2="382" y2="70" stroke="var(--ink)" stroke-width="1.5"></line>
    <polygon points="382,64 382,76 392,70" fill="var(--ink)"></polygon>

    <rect x="390" y="30" width="160" height="80" rx="6" fill="var(--chart-surface)" stroke="var(--ink)" stroke-width="1.5"></rect>
    <text x="470" y="65" font-size="10.5" text-anchor="middle" fill="var(--chart-text-primary)">Grid-impact-study</text>
    <text x="470" y="79" font-size="10.5" text-anchor="middle" fill="var(--chart-text-primary)">requirement</text>
  </svg>
</div>

This is not a FERC matter for a publicly owned utility like an irrigation district — confirmed directly against the statute, not assumed: 16 U.S.C. § 824(f), Section 201(f) of the Federal Power Act, exempts "the United States, a State, or any political subdivision of a State... or any agency, authority, or instrumentality" of one from Part II of the Act — the part that gives FERC its ratemaking authority — unless a specific provision names them. An irrigation district is a political subdivision under the Act's own definition. MID's own board, not any federal regulator, sets its rates. The real federal angle for this mechanism isn't rate regulation at all — it's capital funding for grid infrastructure, through the Department of Energy's Grid Resilience and Innovation Partnerships program, whose current (third) funding round was explicitly renamed and rescoped in March 2026 around a different policy emphasis ("Speed to Power," prioritizing rapid-deployment infrastructure) than its first two rounds.

## What we don't know

- Whether any of the five data-center proposals in this project's four counties has actually commissioned or paid for a MID-style grid-impact study yet — this research found that the mechanism exists, not that it's been applied to any specific named proposal here.
- What the CPUC's eventual tariff design under AB 2383/SB 886 will actually charge, once the rulemaking concludes — the bills order a process, not a number, and that process hadn't produced one as of this research.
- Whether DOE's SPARK funding opportunity has closed applications or made any award, and whether any California utility has applied.

## Sources

- The Modesto Focus, ["Officials with MID... say they'll protect customers, but no consensus yet on how"](https://themodestofocus.org/officials-with-mid-which-would-power-any-potential-data-center-say-theyll-protect-customers-but-no-consensus-yet-on-how/).
- Holland & Knight, ["California's 2026 Data Center Laws: What You Need to Know"](https://www.hklaw.com/en/insights/publications/2026/10/californias-2026-data-center-laws-what-you-need-to-know).
- CalMatters, [on the September 2026 data-center bill signing](https://calmatters.org/economy/technology/2026/09/new-california-laws-data-centers/).
- [16 U.S.C. § 824(f)](https://www.law.cornell.edu/uscode/text/16/824), Federal Power Act Section 201(f) — Cornell Legal Information Institute.
- DOE Office of Electricity, [Grid Resilience and Innovation Partnerships (GRIP) Program](https://www.energy.gov/oe/grid-resilience-and-innovation-partnerships-grip-program); [SPARK NOFO announcement](https://www.energy.gov/oe/speed-power-through-accelerated-reconductoring-and-other-key-advanced-transmission-technology).

Back to [Mechanisms](../mechanisms.md).
