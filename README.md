# Internship Tracker — Summer 2026 & Summer 2027 Internships + New Grad Jobs

A daily-updated, deduplicated list of **software engineering, AI/ML, data science, hardware, quant, and product internships and new grad roles**, aggregated from multiple community-maintained sources into one place, browsable by category.

If you're searching for a **Summer 2027 internships GitHub repo**, a **Summer 2026 internships tracker**, or a **new grad software engineering jobs list**, this aggregates several of those trackers so you don't have to check each one.

⭐ Star this repo to get notified of new listings, or watch it for daily updates.

## Track your own applications, not just browse listings

Most listing repos stop at the list. This one also gives you a personal application tracker that lives next to the data:

```
git clone https://github.com/SuryaHarikrishnan/internship-tracker
cd internship-tracker
python scripts/track.py add "Company" "Role" "2026-06-29" "Applied"
python scripts/track.py render
```

This writes to `data/applications.csv` and regenerates [APPLICATIONS.md](APPLICATIONS.md) with a *days-since-applied* column so you can see at a glance what's gone quiet. **Fork the repo** to keep your own tracker — the daily listings refresh runs automatically via GitHub Actions on any fork (`.github/workflows/refresh.yml`), no local machine needed. See [USAGE.md](USAGE.md) for the full script reference.

## How this works

A script pulls the latest active listings from the source repos below every day, merges and deduplicates them by company + role + location, and rewrites this index and the per-category files in [`listings/`](listings/). See [ATTRIBUTION.md](ATTRIBUTION.md) for source licensing and credit, and [USAGE.md](USAGE.md) for how to run the scripts yourself.

Last refreshed: 2026-06-30 15:23 UTC. Sources currently live: simplify-2026, vanshb03-2026, vanshb03-2027.

**Active listings:** 1235 (of 13705 total seen across all sources)

See [APPLICATIONS.md](APPLICATIONS.md) for personal application tracking.


## Categories

| Category | Listings |
|---|---|
| [Data Science, AI & Machine Learning](listings/data-science-ai-machine-learning.md) | 467 |
| [Hardware Engineering](listings/hardware-engineering.md) | 196 |
| [Other](listings/other.md) | 111 |
| [Product Management](listings/product-management.md) | 22 |
| [Quantitative Finance](listings/quantitative-finance.md) | 46 |
| [Software Engineering](listings/software-engineering.md) | 393 |
