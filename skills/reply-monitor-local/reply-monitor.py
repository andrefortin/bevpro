#!/usr/bin/env python3
"""
reply-monitor-local — Polls IMAP inbox for replies to sent outreach emails.

Matches replies by subject (Re: prefix) and updates outreach_event outcome.

Usage:
  python3 reply-monitor.py <db_path> <config_json_path> [--output <path>]

Config JSON:
  {
    "imap_host": "imap.gmail.com",
    "imap_port": 993,
    "imap_user": "andre@fortinmedia.net",
    "imap_pass": "..."
  }

Output JSON:
  {
    "replies": [
      { "event_id": 42, "from": "owner@roofer.com", "subject": "Re: ...", "snippet": "..." }
    ]
  }
"""

import json
import argparse
import sqlite3
import imaplib
import email as email_lib
import re
from datetime import datetime, timezone


def _strip_re(subject: str) -> str:
    return re.sub(r"^(re:\s*)+", "", subject.strip(), flags=re.IGNORECASE).strip()


def monitor(db_path: str, cfg: dict) -> list[dict]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    # Load all sent events with their subjects
    sent = conn.execute(
        "SELECT id, subject FROM outreach_events WHERE status = 'sent' AND outcome = 'no_response'"
    ).fetchall()

    if not sent:
        conn.close()
        return []

    subject_map: dict[str, int] = {}
    for row in sent:
        clean = _strip_re(row["subject"] or "")
        if clean:
            subject_map[clean.lower()] = row["id"]

    replies = []
    try:
        with imaplib.IMAP4_SSL(cfg["imap_host"], int(cfg.get("imap_port", 993))) as m:
            m.login(cfg["imap_user"], cfg["imap_pass"])
            m.select("INBOX")

            # Search for recent emails with Re: prefix
            status, data = m.search(None, 'SUBJECT', '"Re:"')
            if status != "OK":
                conn.close()
                return []

            ids = data[0].split()
            for uid in ids[-50:]:  # check last 50 to avoid scanning whole inbox
                _, msg_data = m.fetch(uid, "(RFC822)")
                raw = msg_data[0][1] if msg_data and msg_data[0] else None
                if not raw:
                    continue

                msg = email_lib.message_from_bytes(raw)
                subj = email_lib.header.decode_header(msg.get("Subject") or "")
                subj_str = "".join(
                    part.decode(enc or "utf-8") if isinstance(part, bytes) else part
                    for part, enc in subj
                )
                from_addr = msg.get("From") or ""

                clean_subj = _strip_re(subj_str).lower()
                event_id = subject_map.get(clean_subj)
                if not event_id:
                    continue

                # Extract plain text snippet
                snippet = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            snippet = part.get_payload(decode=True).decode("utf-8", errors="ignore")[:300]
                            break
                else:
                    snippet = msg.get_payload(decode=True).decode("utf-8", errors="ignore")[:300]

                # Update DB
                conn.execute(
                    "UPDATE outreach_events SET outcome = 'replied' WHERE id = ?",
                    (event_id,)
                )
                replies.append({
                    "event_id": event_id,
                    "from": from_addr,
                    "subject": subj_str,
                    "snippet": snippet.strip(),
                })

    except Exception as e:
        conn.close()
        return [{"error": str(e)}]

    conn.commit()
    conn.close()
    return replies


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("db_path", help="Path to SQLite database")
    parser.add_argument("config_json", help="IMAP config JSON path")
    parser.add_argument("--output", help="Output path (default: stdout)")
    args = parser.parse_args()

    with open(args.config_json) as f:
        cfg = json.load(f)

    replies = monitor(args.db_path, cfg)
    result = {"replies": replies}

    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
