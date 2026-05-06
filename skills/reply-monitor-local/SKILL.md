---
name: reply-monitor-local
description: Polls IMAP inbox for replies to sent outreach emails and updates outcome in the DB.
---

# reply-monitor-local

Scans the INBOX for `Re:` emails matching sent outreach subjects. Updates `outcome = 'replied'` on matching events.

## Usage

```bash
python3 reply-monitor.py <db_path> <config_json_path> [--output <path>]
```

Config JSON:
```json
{
  "imap_host": "imap.gmail.com",
  "imap_port": 993,
  "imap_user": "andre@fortinmedia.net",
  "imap_pass": "znda pwor owil elfv"
}
```

Output:
```json
{
  "replies": [
    {
      "event_id": 42,
      "from": "owner@roofer.com",
      "subject": "Re: We built Summit Roofing a free website...",
      "snippet": "Hey, I'm interested! Can we talk tomorrow?"
    }
  ]
}
```

## Schedule

Run 2–4× per day via cron or agent scheduler. Each run scans the last 50 INBOX messages.

## Outcome Values

`no_response` → `replied` → (manual) `interested` → `claimed` / `not_interested`
