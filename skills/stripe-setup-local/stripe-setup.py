#!/usr/bin/env python3
"""
stripe-setup — Create/retrieve Stripe products and payment links for FieldLaunch.

Creates (idempotently):
  - Product: "Professional Website" with a one-time price
  - Product: "Website Maintenance" with a monthly recurring price
  - Product: "Chatbot Add-On" with a monthly recurring price
  - Payment Links for each

Usage:
  python3 stripe-setup.py '{"stripe_secret_key":"sk_...", "price_onetime":697, "price_monthly":97, "price_chatbot":47}'
  python3 stripe-setup.py --input input.json --output output.json
"""

import json
import os
import sys

try:
    import stripe
except ImportError:
    print(json.dumps({"error": "stripe package not installed — run: pip3 install stripe"}))
    sys.exit(1)


def _find_or_create_product(name: str, description: str) -> str:
    """Return existing active product ID matching name, or create a new one."""
    page = stripe.Product.list(active=True, limit=100)
    for p in page.data:
        if p.name == name:
            return p.id
    product = stripe.Product.create(name=name, description=description)
    return product.id


def _find_or_create_price(product_id: str, amount_cents: int, currency: str,
                           recurring: dict | None) -> str:
    """Return existing price ID matching product/amount/interval, or create one."""
    existing = stripe.Price.list(product=product_id, active=True, limit=100)
    for p in existing.data:
        if p.unit_amount != amount_cents:
            continue
        if recurring is None and p.recurring is None:
            return p.id
        if (recurring is not None and p.recurring is not None and
                p.recurring.interval == recurring.get("interval")):
            return p.id
    kwargs: dict = dict(product=product_id, unit_amount=amount_cents, currency=currency)
    if recurring:
        kwargs["recurring"] = recurring
    price = stripe.Price.create(**kwargs)
    return price.id


def _find_or_create_payment_link(price_id: str, label: str) -> str:
    """Return existing active payment link for this price, or create one."""
    page = stripe.PaymentLink.list(active=True, limit=100)
    for pl in page.data:
        try:
            li = stripe.PaymentLink.list_line_items(pl.id, limit=1)
            if li.data and li.data[0].price.id == price_id:
                return pl.url
        except Exception:
            continue
    pl = stripe.PaymentLink.create(
        line_items=[{"price": price_id, "quantity": 1}],
        metadata={"fieldlaunch_label": label},
    )
    return pl.url


def setup(cfg: dict) -> dict:
    api_key = cfg.get("stripe_secret_key") or os.getenv("STRIPE_SECRET_KEY")
    if not api_key:
        return {"error": "stripe_secret_key required"}

    stripe.api_key = api_key

    price_onetime = int(cfg.get("price_onetime", 697))
    price_monthly  = int(cfg.get("price_monthly", 97))
    price_chatbot  = int(cfg.get("price_chatbot", 47))

    try:
        # One-time website product
        ot_product_id = _find_or_create_product(
            "Professional Website",
            "Custom roofing/contractor website — one-time setup"
        )
        ot_price_id = _find_or_create_price(
            ot_product_id, price_onetime * 100, "usd", None
        )
        ot_payment_link = _find_or_create_payment_link(ot_price_id, "website_onetime")

        # Monthly maintenance product
        mo_product_id = _find_or_create_product(
            "Website Maintenance",
            "Monthly hosting, updates, and support for your contractor website"
        )
        mo_price_id = _find_or_create_price(
            mo_product_id, price_monthly * 100, "usd", {"interval": "month"}
        )
        mo_payment_link = _find_or_create_payment_link(mo_price_id, "website_monthly")

        # Chatbot add-on product
        cb_product_id = _find_or_create_product(
            "Chatbot Add-On",
            "Live chat widget added to your website — monthly"
        )
        cb_price_id = _find_or_create_price(
            cb_product_id, price_chatbot * 100, "usd", {"interval": "month"}
        )
        cb_payment_link = _find_or_create_payment_link(cb_price_id, "chatbot_monthly")

        return {
            "stripe_onetime_price_id":    ot_price_id,
            "stripe_monthly_price_id":    mo_price_id,
            "stripe_chatbot_price_id":    cb_price_id,
            "stripe_onetime_payment_link": ot_payment_link,
            "stripe_monthly_payment_link": mo_payment_link,
            "stripe_chatbot_payment_link": cb_payment_link,
        }

    except stripe.AuthenticationError:
        return {"error": "Invalid Stripe API key"}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    if len(sys.argv) >= 2 and not sys.argv[1].startswith("--"):
        cfg = json.loads(sys.argv[1])
        print(json.dumps(setup(cfg), indent=2))
        sys.exit(0)

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",  required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    with open(args.input) as f:
        cfg = json.load(f)

    result = setup(cfg)
    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)

    if result.get("error"):
        print(json.dumps(result))
        sys.exit(1)
