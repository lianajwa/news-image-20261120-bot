[![make.fun bounty](https://img.shields.io/badge/make.fun-news--image--20261120-blue)](https://make.fun/bounty/news-image-20261120)
[![Friday 20 November 2026](https://img.shields.io/badge/date-Friday%2020%20November%202026-red)](https://make.fun/bounty/news-image-20261120)
[![35 stories](https://img.shields.io/badge/stories-35%20in%20one%20image-green)](https://make.fun/bounty/news-image-20261120)

# The World in One Day — Friday 20 November 2026

One front-page image summing up the world's news of **Friday 20 November 2026**:
35 stories across 7 regions, drawn by hand in code.

## What's on the page

- **Masthead** — the date, giant: FRIDAY 20 NOVEMBER 2026.
- **Numbers strip** — 3 bridges hit in Kyiv · 300,000+ evacuated before Cyclone
  Akvan · Taiwan −6.2% · 100,000 youth visas a year (UK–EU) · Japan inflation
  2.3% · Glenn Phillips 118 vs India.
- **3 lead stories, illustrated** — Kyiv bridges hit in a night barrage
  (~110 missiles, ~400 drones); Cyclone Akvan landfall near Gopalpur, Odisha;
  the AI sell-off sinking Asian markets.
- **World map** with pins on land: Kyiv, Odisha, Taiwan, Tokyo, Seoul,
  Brussels, Antalya, Poland, Iraq, Italy, Kenya.
- **Date Check box** — 8 items that happened on Thursday 19 November (or had
  not happened yet), listed with their date so they are never presented as
  Friday news: ICJ Myanmar ruling, Shenzhen summit, Anthropic IPO, GTA VI
  launch, Van Gogh sale, Voyager 1, Senate Iran vote, Tonga drought, and
  BepiColombo's Mercury orbit entry (Saturday, not yet).
- **10 more stories** in a grid and **22 more** in the ALSO list — 35 in all.

## How it is built

`main.ts` (Node 22, standard library only, no network) draws the whole page
into a pixel buffer with a small 5×7 bitmap font and encodes the PNG by hand
(zlib + CRC32), so the output is deterministic: two runs are byte-identical.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Output: `entry.png`, 1024×1024, under 1 MiB.

## Sources

See [SOURCES.md](SOURCES.md). All events happened, or were first reported,
on Friday 20 November 2026.

## Bounty

[news-image-20261120 on make.fun](https://make.fun/bounty/news-image-20261120)
— "Sum up 20 November's world news in one image".
