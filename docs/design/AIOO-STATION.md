# AiOO Station — design language

Reference bundle: `aioo-station-demo.html` (self-contained snapshot, built
2026-09-04). The live version runs from a folder + `serve_station.py`; the
bundle inlines every data file, so it opens with no network and no server.

## What it is

A fleet health console for ~558 sites/devices. One `diagnose.py` sweep writes
`station_data.js`; `build_bundle.py` inlines it into a single page; `nightly.py`
re-runs the whole chain. The screen is a **projection of one sweep**, never a
live poll — which is why it can be honest about staleness.

Per entity the sweep records: `verdict`, `state`, `tier`, `temp` + `temp_series`
+ `temp_cause`, `mem` + `mem_series` + `mem_cause`, `cause`, `fix`,
`confidence`, `hinges`, `watch`, `since`, `samples`, `hours_driven`, `lost_h`.
Note the shape: every metric ships with **its cause and a proposed fix**, and
every verdict ships with **a confidence**. Nothing is a bare number.

## The law

> The interface must never assert state the run cannot prove.

Carried over from StarNet (androoAGI/starnet, MIT), and credited as such in the
stylesheet. It is the reason there is a `nodata` colour at all: "we did not
measure this" is a distinct, visible state, not a zero and not a gap.

**This is the rule to demo to the jury.** Any panel that shows a number it
cannot trace to a sweep is a bug, not a placeholder.

## Visual system

- **Phosphor CRT.** One swappable chrome colour (`--ph`) with five themes:
  white (default), amber, green, blue, violet. `VT323` embedded as base64, so
  no font CDN.
- **Verdict colours never move.** `--ok #5fd07a` · `--warn #ff9f1c` ·
  `--bad #ff5c4d` · `--nodata #838383` — identical on every phosphor. Only the
  furniture re-themes. If verdict colours shifted with the theme the screen
  would stop meaning anything.
- White is the default because amber-on-black plus flicker hurt legibility.
  The CRT is a texture, not an effect; `--scan` (0.09) is the legibility dial.
- Top-down tile station on `<canvas>`; chrome drawn as instrument housings.

## Panels worth stealing

| Panel | Idea |
| --- | --- |
| **Crew / sprite crew** | Agents as characters with live state, not rows in a table. |
| **X — the Overseer** | One agent whose job is watching the others. |
| **Second Brain** | Force-directed graph over notes/folders — real edges, not decoration. |
| **Run log** | Append-only record of what actually executed. |
| **Incidents / alerts** | `level`, `ask`, `note` — an alert carries the question it wants answered. |
| **Delta strip** | What changed since the previous sweep. |
| **Live mode + fleet capsule relay** | Progress and latency shown while a sweep runs. |

## If the brief is a dashboard

Reuse the law, the verdict palette, the "metric + cause + fix + confidence"
record shape, and the sweep→snapshot→render pipeline. Those are the parts that
make it read as engineered rather than decorated. The CRT skin is optional and
should be dropped if the client's brief implies a corporate audience.
