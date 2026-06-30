# Contributing

This repo's listings are auto-generated — don't hand-edit `README.md` or files
under `listings/`, they get overwritten by the next refresh.

Useful ways to contribute:

- **Report a stale/wrong listing** — open an issue using the "Stale or incorrect listing" template. Note it likely needs fixing upstream (in the source repo), but flag it here too so we know.
- **Suggest a new source** — open an issue using the "Suggest a new source" template. Must be a repo/feed with a clear license or explicit reuse permission (see [ATTRIBUTION.md](ATTRIBUTION.md) for why this matters).
- **Improve the scripts** — `scripts/scrape.py` (listings aggregation) and `scripts/track.py` (personal application tracker) are plain Python with no dependencies beyond the standard library. PRs welcome.

To add a source yourself: add an entry to the `SOURCES` dict in `scripts/scrape.py`
pointing at a `listings.json`-style feed, run `python scripts/scrape.py` to confirm
it merges cleanly, and open a PR.
