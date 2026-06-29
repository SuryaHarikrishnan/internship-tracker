# Usage

`README.md` is auto-generated — don't hand-edit it, run `scripts/scrape.py` instead.

## Refresh job listings
```
python scripts/scrape.py
```
Pulls active listings from SimplifyJobs/Summer2026-Internships and
vanshb03/Summer2026-Internships, dedupes by company+role+location, and
rewrites `README.md` and `data/listings.json`.

## Track your own applications
```
python scripts/track.py add "Company" "Role" "2026-06-28" "Applied" "optional notes"
python scripts/track.py update <row_index> "Interviewing"
python scripts/track.py render
```
Writes to `data/applications.csv` and regenerates `APPLICATIONS.md`.
