# news-image-23nov2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Brooo-ui/news-image-23nov2026/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Brooo-ui/news-image-23nov2026/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One newspaper front page summing up the world's news of Monday 23 November 2026: 64 stories from 9 regions, three lead stories with drawn scenes (COP31 collapses with no deal, Iran's strikes on US bases in Bahrain and the Hormuz tanker war, NATO's emergency session on the Poland missiles), the day in twenty, 41 more stories, and a date check that names what was left out on purpose. Every story was verified against the day's wires (Reuters, CNN, The Times, FT, Al Jazeera, AFP, IANS, ANI, ESPNcricinfo, Cricbuzz, ESA, Finnhub, Cinepals); single-source items are labelled REPORTED, one side's claims CLAIM.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

That writes `out/entry.png` (1024x1024, under 1 MiB). `main.py` is standard library only and copies the vendored `entry.png`; `draw.py` is the Pillow program that drew the page (run `python3 draw.py` to regenerate it).

---

<sub>Entered on [make.fun](https://make.fun/?ref=suroto&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
