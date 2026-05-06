---
name: sequence-builder-local
description: Builds a personalized multi-touch outreach sequence (email + SMS) for a lead based on niche templates.
---

# sequence-builder-local

Selects the right niche sequence and renders all touches with lead-specific data.

## Supported Niches

| Niche | Sequence | Touches |
|-------|----------|---------|
| roofing | `roofing-4touch` | Email day 0, 3, 7 · SMS day 10 |
| hvac | `hvac-4touch` | Email day 0, 3, 7 · SMS day 10 |
| plumbing | `plumbing-4touch` | Email day 0, 3, 7 · SMS day 10 |
| anything else | `generic-4touch` | Email day 0, 3, 7 · SMS day 10 |

## Usage

```bash
python3 sequence-builder.py <input_json_path> [--output <path>]
```

Input:
```json
{
  "lead":          { "business_name": "...", "city": "...", "niche": "roofing contractor", "phone": "..." },
  "contact":       { "email": "info@...", "name": null, "confidence": 0.8 },
  "site_url":      "https://fl-acme-roofing.vercel.app",
  "booking_url":   "https://cal.com/andre-fortin",
  "price_onetime": 697,
  "price_monthly": 97
}
```

Output:
```json
{
  "sequence": "roofing",
  "steps": [
    { "step": 1, "channel": "email", "delay_days": 0, "subject": "...", "body": "..." },
    { "step": 2, "channel": "email", "delay_days": 3, "subject": "...", "body": "..." },
    { "step": 3, "channel": "email", "delay_days": 7, "subject": "...", "body": "..." },
    { "step": 4, "channel": "sms",   "delay_days": 10, "subject": "", "body": "..." }
  ]
}
```

## Template Variables

`{name}` `{business_name}` `{city}` `{niche}` `{site_url}` `{booking_url}` `{price_onetime}` `{price_monthly}`
