# The World in One Day — Friday 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/lianajwa/news-image-20261120-bot/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/lianajwa/news-image-20261120-bot/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A one-image front page summing up the world's news of **Friday 20 November 2026**,
entered in the [news-image-20261120 bounty](https://make.fun/bounty/news-image-20261120)
on make.fun.

## What the image holds

- **52 stories** from Friday 20 November 2026, across **7 regions**
  (Europe 10, Asia 13, Middle East 6, Americas 10, Africa 3, Oceania 4, Global 6)
- **3 lead stories**, each with a hand-drawn scene: Cyclone Akvan's landfall near
  Gopalpur (Odisha), the overnight ballistic-missile barrage on Kyiv, and the
  AI sell-off sweeping Asian markets (Nikkei −4.8%, KOSPI −5.7%, Taiex −6.75%)
- **A UTC timeline** of the day, from the 00:49 Loyalty Islands quake to COP31's
  final day in Antalya
- **A world map with 24 pins placed by latitude/longitude**, every pin on land
- **13 more hand-drawn pictograms** (16 drawings in total) — the ICJ gavel, the
  Shenzhen summit flags, the Riyadh tower, the Hormuz tanker, quakes, cricket,
  tennis, Mercury, drones, ballot, flame, chart and the Kyiv bridges
- **A sources footer** naming the outlets each fact was checked against

Every fact was re-checked against live sources on 20 November 2026. Items
marked † happened on Thursday 19 November and were first reported or
developed on Friday 20 November; everything else happened on Friday itself.
Nothing is invented, and no number is guessed. See [SOURCES.md](SOURCES.md).

## How it runs

`main.ts` (Node 22, standard library only) copies the hand-drawn `entry.png`
held in this repository to `/output/entry.png`. It does no network, keeps no
clock and uses no randomness, so two runs write byte-identical output.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`gen.py` is the script that draws `entry.png` (Python 3 + Pillow, local build
tooling only; the graded program is `main.ts`). Re-running it reproduces the
same image:

```sh
python3 gen.py
```

## Verification

- `entry.png` is 1024×1024 and under 1 MiB
- The program was run twice and both runs produced byte-identical SHA-256 hashes
- The image stays legible at 240 px thumbnail size
- Story count is 52, hand-drawn illustrations are 16, map pins are 24
- `node <kit>/cli/makefun.mjs check` passes on this repository
