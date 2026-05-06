---
name: contact-resolver-local
description: Resolves the best contact email and name for a business lead by scraping the website and trying domain patterns.
---

# contact-resolver-local

Finds the decision-maker's contact email for a lead. Runs after enrichment, before sequence building.

## Priority

1. GMB-listed email (confidence 0.90)
2. Website scrape — homepage + /contact + /about for mailto: links and raw email patterns (0.80 if on business domain, 0.60 otherwise)
3. Domain pattern guesses — info@, contact@, owner@, etc. (0.30)
4. Phone only — no email found (0.10)
5. No contact found (0.00)

## Usage

```bash
python3 contact-resolver.py <lead_json_path> [--output <path>]
```

Input: JSON file with lead fields (`website`, `phone`, `email`, `business_name`, `city`).

Output:
```json
{
  "email": "info@example.com",
  "name": null,
  "phone": "+15551234567",
  "source": "website_scrape",
  "confidence": 0.80
}
```

## Confidence Thresholds

- ≥ 0.70 → reliable, send outreach
- 0.30–0.69 → low confidence, mark for human review
- < 0.30 → skip email, try phone/SMS only
