#!/usr/bin/env python3
"""
outreach-scheduler-local — Returns outreach events that are due to fire based on scheduled_at.

Run this on a cron or on-demand to find follow-up touches ready to send.
The caller (API route or agent) handles the actual send via outreach-launcher.

Usage:
  python3 outreach-scheduler.py <db_path> [--campaign <id>] [--output <path>]

Output JSON:
  {
    "due": [
      { "id": 42, "lead_id": 7, "campaign_id": 3, "channel": "email",
        "sequence_step": 2, "contact_email": "...", "subject": "...", "body": "..." }
    ]
  }
"""

import json
import argparse
import sqlite3
from datetime import datetime, timezone


def get_due_events(db_path: str, campaign_id: int | None = None) -> list[dict]:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    query = """
        SELECT
            oe.id, oe.lead_id, oe.site_id, oe.campaign_id,
            oe.channel, oe.sequence_step, oe.subject, oe.message_body,
            oe.scheduled_at, oe.outcome,
            c.email AS contact_email, c.phone AS contact_phone
        FROM outreach_events oe
        LEFT JOIN contacts c ON c.id = oe.contact_id
        WHERE oe.status = 'pending'
          AND oe.approved = 1
          AND (oe.scheduled_at IS NULL OR oe.scheduled_at <= ?)
    """
    params: list = [now]

    if campaign_id is not None:
        query += " AND oe.campaign_id = ?"
        params.append(campaign_id)

    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("db_path", help="Path to SQLite database")
    parser.add_argument("--campaign", type=int, help="Filter by campaign ID")
    parser.add_argument("--output", help="Output path (default: stdout)")
    args = parser.parse_args()

    due = get_due_events(args.db_path, args.campaign)
    result = {"due": due}

    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
