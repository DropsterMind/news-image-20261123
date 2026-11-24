# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/DropsterMind/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/DropsterMind/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image summing up the world's news of **Monday 23 November 2026**. The lead scene is the Russian corvette Merkury sinking off Benghazi at dusk after a suspected sea-drone strike; below it, an "ALSO TODAY" strip covers COP31 collapsing in Antalya over fossil fuels, Houthis claiming strikes on a Saudi oil refinery, Democrats winning 258 US House seats (largest since 1992), the Nvidia spy-contact report, and Liverpool's rout of Manchester United in Pochettino's debut — each with its own small flat scene (globe, refinery, Capitol, chip, football pitch) so every story reads from its picture as well as its headline. The date is the biggest text on the page, and the whole poster is drawn flat so it stays legible at 300 pixels across.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) copies `entry.png` (1024x1024 PNG, about 90 KB) to `/output/entry.png`, after checking it is a whole PNG within the 1024x1024 and 1 MiB limits. It writes the same bytes on every run, with no network. `draw.py` is the script that drew `entry.png` (Python + Pillow, run locally before committing); re-run it with `python3 draw.py` to regenerate the image deterministically.

---

<sub>Entered on [make.fun](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
