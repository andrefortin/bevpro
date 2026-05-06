---
name: outreach-scheduler-local
description: Returns outreach_events that are due to fire based on their scheduled_at timestamp. Run on cron or on-demand.
---

# outreach-scheduler-local

Reads the DB and returns all approved pending events where `scheduled_at <= NOW`. The caller sends them via `outreach-launcher-local`.

## Usage

```bash
python3 outreach-scheduler.py <db_path> [--campaign <id>] [--output <path>]
```

Output:
```json
{
  "due": [
    {
      "id": 42, "lead_id": 7, "campaign_id": 3,
      "channel": "email", "sequence_step": 2,
      "contact_email": "info@example.com",
      "subject": "Quick follow-up...",
      "message_body": "..."
    }
  ]
}
```

## Scheduling

Run via a cron job or the agent scheduler once or twice a day:

```bash
python3 outreach-scheduler.py data/fieldlaunch.db --output /tmp/due.json
# then pass each event to outreach-launcher
```
