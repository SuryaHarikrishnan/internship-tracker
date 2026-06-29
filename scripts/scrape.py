#!/usr/bin/env python3
"""Aggregates internship/new-grad listings from several open-source tracker
repos into one deduplicated README table.

Sources (each maintains a machine-readable listings.json fed by their own
scrapers/bots):
  - SimplifyJobs/Summer2026-Internships
  - vanshb03/Summer2026-Internships
  - speedyapply/2026-SWE-College-Jobs
"""
import json
import re
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

SOURCES = {
    "simplify": "https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/dev/.github/scripts/listings.json",
    "vanshb03": "https://raw.githubusercontent.com/vanshb03/Summer2026-Internships/dev/.github/scripts/listings.json",
}

HEADERS = {"User-Agent": "internship-tracker/1.0 (personal aggregator)"}


def fetch_json(url: str):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "")).strip().lower()


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

    write_readme(listings, fetched_sources)
    print(f"Merged {len(listings)} unique listings from {fetched_sources}")


def write_readme(listings, fetched_sources):
    active = [l for l in listings if l.get("active", True) and l.get("is_visible", True)]
    by_category = defaultdict(list)
    for l in active:
        cat = l.get("category") or "Other"
        by_category[cat].append(l)
    for cat in by_category:
        by_category[cat].sort(key=lambda x: x.get("date_posted", 0), reverse=True)

    lines = []
    lines.append("# Internship & New Grad Job Tracker\n")
    lines.append(
        f"Aggregated daily from {', '.join(fetched_sources) or 'cached data'} "
        f"(deduplicated, active listings only). Last refreshed: "
        f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}.\n"
    )
    lines.append(f"**Active listings:** {len(active)} (of {len(listings)} total seen)\n")
    lines.append("See [APPLICATIONS.md](APPLICATIONS.md) for personal application tracking.\n")

    for cat in sorted(by_category):
        rows = by_category[cat]
        lines.append(f"\n## {cat} ({len(rows)})\n")
        lines.append("| Company | Role | Location | Terms | Sources |")
        lines.append("|---|---|---|---|---|")
        for l in rows:
            company = l.get("company_name", "")
            title = l.get("title", "")
            url = l.get("url", "")
            loc = ", ".join(l.get("locations", []) or [])
            terms = ", ".join(l.get("terms", []) or [])
            srcs = ", ".join(l.get("_sources", []))
            company_cell = f"[{company}]({url})" if url else company
            lines.append(f"| {company_cell} | {title} | {loc} | {terms} | {srcs} |")

    (ROOT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
