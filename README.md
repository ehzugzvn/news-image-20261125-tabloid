# The World in One Day — TABLOID

One image summing up Wednesday 25 November 2026's world news: 38 stories from 7 regions, led by Shenzhou-24 lifting off with the first Pakistani astronaut aboard.

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/ehzugzvn/news-image-20261125-tabloid/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/ehzugzvn/news-image-20261125-tabloid/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

Entry for the [news-image-20261125 bounty on make.fun](https://make.fun/bounty/news-image-20261125).

## How it works

`render.py` (Pillow) draws `entry.png` — a 1024×1024 near-black tabloid page: giant date, a rocket-at-dawn lead illustration, three more illustrated leads, a day-in-numbers strip, ten tier-2 stories with pictograms and verification tags, a numbered world map, 24 large-type briefs, a UTC timeline, a date-check strip and a "how sure" legend. Every story happened, or was first reported, on Wednesday 25 November 2026.

`main.py` (Python 3.13, standard library only) copies the pre-rendered `entry.png` to `MAKEFUN_OUTPUT_DIR` (or `/output`).

## Run

```sh
python3 render.py   # produces entry.png
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```
