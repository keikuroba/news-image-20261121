# The world on Saturday 21 November 2026 — in one image

One newspaper front page for Saturday 21 November 2026. Five stories
lead the day, and a ticker carries the rest:

1. Two Russian missiles and a suspected drone came down inside Poland
   during a massive Russian attack on Ukraine. No injuries; Prime
   Minister Donald Tusk called it an intentional provocation and NATO
   called it a grave violation of allied airspace.
2. Wall Street slides into correction: US stocks fell about 3.7% on
   Friday, pushing the S&P 500 and the Dow into correction territory
   as AI and chip shares sold off; Nvidia's crash deepened the rout.
3. The International Court of Justice ruled that Myanmar's security
   forces committed state-sponsored genocide against the Rohingya.
   Myanmar called the ruling unfair.
4. The UK and EU struck their biggest post-Brexit deal: food checks
   scrapped, carbon markets linked, 100,000 youth visas each way for
   up to three years, and Britain rejoins the Erasmus+ exchange.
5. A magnitude 6.8 earthquake struck Junin in central Peru, 129 km
   deep, and was felt in Lima, where people ran into the streets. No
   casualties were reported.

Ticker: Denmark foiling an alleged Russian plot and expelling its
defence attache, Trump threatening a ban on US firms building AI data
centres abroad, Mamdani setting 2032 to close Rikers Island, KL Rahul
completing Test centuries in all SENA countries, and COP31 entering
its final stage.

[![news-image-20261121 on make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/keikuroba/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/keikuroba/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

## How to run

    python3 main.py

That copies `assets/entry.png` to `/output/entry.png` (or
`$MAKEFUN_OUTPUT_DIR` / `$ENTRY_OUTPUT_DIR` when set). Before copying,
the program validates the artwork: PNG magic, IHDR first, every chunk
CRC, 1024×1024 dimensions, under 1 MiB, pixel data inflating to
exactly the right size, nothing after the IEND chunk — and after
writing it reads the file back and checks the SHA-256 matches. No
network, no clock, no randomness, so two runs produce identical bytes.

## Files

- `main.py` — the entrypoint. Validate, copy, verify the write.
- `assets/entry.png` — the finished page: 1024×1024, 154,399 bytes.
- `tools/make_image.py` — the build-time Pillow script that drew the
  page from the day's stories. The grader never runs it.
