# THE DAILY ORBIT — Tuesday, 24 November 2026

Entry for the make.fun bounty **news-image-20261124**: one image that sums up
the world's news of **Tuesday, 24 November 2026**.

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/labibhanafi/news-image-20261124-entry-v2/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/labibhanafi/news-image-20261124-entry-v2/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

- Bounty: https://make.fun/bounty/news-image-20261124
- Referral: https://make.fun/r/3t7y0djc

## What it is

A dense three-column newspaper front page, drawn programmatically at
1024×1024: a big dated masthead, a lead story band (the fourth tanker to hit
a mine in the Strait of Hormuz, with fact chips and a market strip), and
47 verified stories across 8 regions — Middle East, Europe, East Asia,
South Asia & Pacific, North America, Africa, Latin America, and
Science & Sport. Every story happened, or was first reported, on
24 November 2026; each headline and figure was verified by live web
research at build time (see `SOURCES.md`). Unverified stories were dropped.

## Run it

```sh
mkdir -p output
MAKEFUN_OUTPUT_DIR=output python3 main.py
# writes output/entry.png (1024x1024 PNG, deterministic: same bytes every run)
```

`main.py` uses only the Python standard library plus PIL when available,
with a stdlib-only fallback renderer. No network is used at run time.

## License

MIT — see `LICENSE`.
