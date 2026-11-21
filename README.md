# Saturday 21 November 2026 — the world in one image

A newspaper front page that sums up Saturday 21 November 2026 in
five stories plus a ticker:

- **Poland / NATO (lead).** Two Russian missiles and a suspected
  drone came down inside Poland during a massive Russian attack on
  Ukraine. No injuries. Prime Minister Donald Tusk called it an
  intentional provocation; NATO called it a grave violation of
  allied airspace.
- **Markets / New York.** US stocks fell about 3.7% on Friday,
  pushing the S&P 500 and the Dow into correction territory as AI
  and chip shares sold off; Nvidia's crash deepened the rout.
- **Justice / The Hague.** The International Court of Justice ruled
  that Myanmar's security forces committed state-sponsored genocide
  against the Rohingya. Myanmar called the ruling unfair.
- **Europe / Brussels.** The UK and EU struck their biggest
  post-Brexit deal: food checks scrapped, carbon markets linked,
  100,000 youth visas each way for up to three years, and Britain
  rejoins the Erasmus+ exchange.
- **Peru / earthquake.** A magnitude 6.8 quake struck Junin in
  central Peru, 129 km deep, and was felt in Lima, where people ran
  into the streets. No casualties were reported.

The ticker adds Denmark foiling an alleged Russian plot and
expelling its defence attache, Trump threatening a ban on US firms
building AI data centres abroad, Mamdani setting 2032 to close
Rikers Island, KL Rahul completing Test centuries in all SENA
countries, and COP31 entering its final stage.

[![news-image-20261121 on make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/keikuroba/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/keikuroba/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

## Running it

    python3 main.py

This copies `assets/entry.png` to `/output/entry.png` (or to
`$MAKEFUN_OUTPUT_DIR` / `$ENTRY_OUTPUT_DIR` if set). First it
validates the artwork — PNG signature, chunk checksums, 1024x1024
size, under 1 MiB, nothing past the IEND chunk — and after writing
it reads the file back and compares SHA-256 digests. No network, no
clock, no randomness: two runs write identical bytes.

## Layout

- `main.py` — the entrypoint: validate, copy, verify.
- `assets/entry.png` — the finished page (1024x1024, 154,399 bytes).
- `tools/make_image.py` — the build-time Pillow script that drew the
  page from the day's stories; the grader never runs it.
