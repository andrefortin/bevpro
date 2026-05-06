# Stripe Setup Skill

## Description

Creates (or retrieves) Stripe products and payment links for the FieldLaunch offer stack. Safe to run multiple times — idempotent by design.

## Products Created

| Product | Price | Type | Settings Key |
|---------|-------|------|-------------|
| Professional Website | $497 | One-time | `stripe_payment_link_onetime` |
| Website Maintenance | $97/mo | Recurring | `stripe_payment_link_monthly` |
| Chatbot Add-On | $197/mo | Recurring | `stripe_payment_link_chatbot` |

## Idempotency

1. Lists all Stripe Products, matches by name before creating
2. Lists all Prices for matched product, matches by unit amount before creating
3. Lists Payment Links, fetches line items per link to match by price ID before creating

Re-running after partial failure is safe — no duplicates.

## Input

| Param | Source |
|-------|--------|
| `stripe_secret_key` | Settings DB (`stripe_secret_key`) |

## Output (JSON)

```json
{
  "products": {
    "website_onetime": { "product_id": "...", "price_id": "...", "payment_link": "https://buy.stripe.com/..." },
    "website_monthly": { "product_id": "...", "price_id": "...", "payment_link": "https://buy.stripe.com/..." },
    "chatbot_monthly": { "product_id": "...", "price_id": "...", "payment_link": "https://buy.stripe.com/..." }
  }
}
```

## Usage

Called via `POST /api/stripe` in the web UI (Settings → Stripe → "Setup Products" button). Results are stored in settings DB and shown in the UI.

## Per-Client Prefill

The sequence builder appends per-client query params to payment link base URLs:
```
{payment_link}?prefilled_email={email}&client_reference_id=lead_{id}
```

This happens in `sequence-builder.py`, not in this skill. The base URLs here are shared; the prefill is client-specific.
