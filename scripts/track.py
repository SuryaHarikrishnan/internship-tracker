#!/usr/bin/env python3
"""Personal application tracker.

Usage:
  python scripts/track.py add "Company" "Role" "2026-06-28" "Applied" "optional notes"
  python scripts/track.py update <row_index> <new_status>
  python scripts/track.py render   # regenerate APPLICATIONS.md from applications.csv
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "applications.csv"
FIELDS = ["company", "role", "date_applied", "status", "notes"]


def load():
    if not CSV_PATH.exists():
        return []
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save(rows):
    CSV_PATH.parent.mkdir(exist_ok=True)
    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def render(rows):
    lines = ["# My Applications\n", "| # | Company | Role | Date Applied | Status | Notes |",
              "|---|---|---|---|---|---|"]
    for i, r in enumerate(rows):
        lines.append(
            f"| {i} | {r['company']} | {r['role']} | {r['date_applied']} | {r['status']} | {r.get('notes','')} |"
        )
    (ROOT / "APPLICATIONS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    cmd = args[0]
    rows = load()

    if cmd == "add":
        company, role, date_applied, status = args[1], args[2], args[3], args[4]
        notes = args[5] if len(args) > 5 else ""
        rows.append({"company": company, "role": role, "date_applied": date_applied,
                     "status": status, "notes": notes})
        save(rows)
        render(rows)
        print(f"Added {company} - {role}")
    elif cmd == "update":
        idx, new_status = int(args[1]), args[2]
        rows[idx]["status"] = new_status
        save(rows)
        render(rows)
        print(f"Updated row {idx} -> {new_status}")
    elif cmd == "render":
        render(rows)
        print("Rendered APPLICATIONS.md")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
