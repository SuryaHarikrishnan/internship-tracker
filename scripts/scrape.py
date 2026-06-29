#!/usr/bin/env python3
"""Aggregates internship/new-grad listings from several open-source tracker
repos into one deduplicated README table.

Sources (each maintains a machine-readable listings.json fed by their own
scrapers/bots):
  - SimplifyJobs/Summer2026-Internships (MIT)
  - vanshb03/Summer2026-Internships (MIT)
  - vanshb03/Summer2027-Internships (MIT)
"""
import json
import re
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
LISTINGS_DIR = ROOT / "listings"
DATA_DIR.mkdir(exist_ok=True)
LISTINGS_DIR.mkdir(exist_ok=True)

SOURCES = {
    "simplify-2026": "https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/dev/.github/scripts/listings.json",
    "vanshb03-2026": "https://raw.githubusercontent.com/vanshb03/Summer2026-Internships/dev/.github/scripts/listings.json",
    "vanshb03-2027": "https://raw.githubusercontent.com/vanshb03/Summer2027-Internships/dev/.github/scripts/listings.json",
}

HEADERS = {"User-Agent": "internship-tracker/1.0 (personal aggregator)"}


def fetch_json(url: str):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "")).strip().lower()


def slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s or "other"


CATEGORY_ALIASES = {
    "software": "Software Engineering",
    "software engineering": "Software Engineering",
    "ai/ml/data": "Data Science, AI & Machine Learning",
    "data science, ai & machine learning": "Data Science, AI & Machine Learning",
    "hardware": "Hardware Engineering",
    "hardware engineering": "Hardware Engineering",
    "quant": "Quantitative Finance",
    "quantitative finance": "Quantitative Finance",
    "product": "Product Management",
    "product management": "Product Management",
}


def normalize_category(cat: str) -> str:
    return CATEGORY_ALIASES.get(norm(cat), cat or "Other")


def dedup_key(item: dict) -> str:
    return f"{norm(item.get('company_name'))}|{norm(item.get('title'))}|{norm(item.get('locations', [''])[0] if item.get('locations') else '')}"


def main():
    merged = {}
    fetched_sources = []
    for name, url in SOURCES.items():
        try:
            items = fetch_json(url)
        except Exception as exc:
            print(f"[warn] failed to fetch {name}: {exc}")
            continue
        fetched_sources.append(name)
        for item in items:
            key = dedup_key(item)
            if key not in merged:
                item["_sources"] = [name]
                merged[key] = item
            else:
                if name not in merged[key]["_sources"]:
                    merged[key]["_sources"].append(name)

    listings = list(merged.values())
    listings.sort(key=lambda x: x.get("date_updated", 0), reverse=True)

    (DATA_DIR / "listings.json").write_text(
        json.dumps(listings, indent=2), encoding="utf-8"
    )

    write_listings(listings, fetched_sources)
    print(f"Merged {len(listings)} unique listings from {fetched_sources}")


def category_table(rows, today):
    lines = ["| Company | Role | Location | Terms | Date Posted | Days Old | Sources |",
             "|---|---|---|---|---|---|---|"]
    for l in rows:
        company = l.get("company_name", "")
        title = l.get("title", "")
        url = l.get("url", "")
        loc = ", ".join(l.get("locations", []) or [])
        terms = ", ".join(l.get("terms", []) or [])
        srcs = ", ".join(l.get("_sources", []))
        company_cell = f"[{company}]({url})" if url else company

        date_posted_ts = l.get("date_posted")
        if date_posted_ts:
            posted_date = datetime.fromtimestamp(date_posted_ts, tz=timezone.utc).date()
            date_str = posted_date.strftime("%Y-%m-%d")
            days_old = (today - posted_date).days
        else:
            date_str = "Unknown"
            days_old = "Unknown"

        lines.append(f"| {company_cell} | {title} | {loc} | {terms} | {date_str} | {days_old} | {srcs} |")
    return lines


def write_listings(listings, fetched_sources):
    active = [l for l in listings if l.get("active", True) and l.get("is_visible", True)]
    by_category = defaultdict(list)
    for l in active:
        cat = normalize_category(l.get("category"))
        by_category[cat].append(l)
    for cat in by_category:
        by_category[cat].sort(key=lambda x: x.get("date_posted", 0), reverse=True)

    today = datetime.now(timezone.utc).date()
    refreshed_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # one file per category under listings/
    existing_files = set(LISTINGS_DIR.glob("*.md"))
    written_files = set()
    category_links = []
    for cat in sorted(by_category):
        rows = by_category[cat]
        slug = slugify(cat)
        path = LISTINGS_DIR / f"{slug}.md"
        written_files.add(path)
        category_links.append((cat, slug, len(rows)))

        lines = [f"# {cat} ({len(rows)})\n", "[← back to index](../README.md)\n"]
        lines += category_table(rows, today)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    for stale in existing_files - written_files:
        stale.unlink()

    # slim index — header is static/SEO-oriented, body is regenerated daily
    index = [
        "# Internship Tracker — Summer 2026 & Summer 2027 Internships + New Grad Jobs\n",
        "A daily-updated, deduplicated list of **software engineering, AI/ML, data science, "
        "hardware, quant, and product internships and new grad roles**, aggregated from "
        "multiple community-maintained sources into one place, browsable by category.\n",
        "If you're searching for a **Summer 2027 internships GitHub repo**, a "
        "**Summer 2026 internships tracker**, or a **new grad software engineering jobs list**, "
        "this aggregates several of those trackers so you don't have to check each one.\n",
        "⭐ Star this repo to get notified of new listings, or watch it for daily updates.\n",
        "## How this works\n",
        "A script pulls the latest active listings from the source repos below every day, "
        "merges and deduplicates them by company + role + location, and rewrites this index "
        "and the per-category files in [`listings/`](listings/). See "
        "[ATTRIBUTION.md](ATTRIBUTION.md) for source licensing and credit, and "
        "[USAGE.md](USAGE.md) for how to run the scripts yourself.\n",
    ]
    index.append(
        f"Last refreshed: {refreshed_at}. "
        f"Sources currently live: {', '.join(fetched_sources) or 'none (using cached data)'}.\n"
    )
    index.append(f"**Active listings:** {len(active)} (of {len(listings)} total seen across all sources)\n")
    index.append("See [APPLICATIONS.md](APPLICATIONS.md) for personal application tracking.\n")
    index.append("\n## Categories\n")
    index.append("| Category | Listings |")
    index.append("|---|---|")
    for cat, slug, count in category_links:
        index.append(f"| [{cat}](listings/{slug}.md) | {count} |")

    (ROOT / "README.md").write_text("\n".join(index) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
