#!/usr/bin/env python3
"""
sequence-builder-local — Builds a personalized multi-touch outreach sequence for a lead.

Usage:
  python3 sequence-builder.py <input_json_path> [--output <path>]

Input JSON:
  {
    "lead":         { "business_name": ..., "city": ..., "niche": ..., "phone": ... },
    "contact":      { "email": ..., "name": ..., "confidence": ... },
    "site_url":     "https://...",
    "booking_url":  "https://cal.com/...",   (optional)
    "price_onetime": 697,
    "price_monthly": 97
  }

Output JSON:
  {
    "sequence": "roofing-4touch",
    "steps": [
      { "step": 1, "channel": "email", "delay_days": 0, "subject": "...", "body": "..." },
      ...
    ]
  }
"""

import sys
import json
import argparse

# ---------------------------------------------------------------------------
# Templates — one dict per niche, each with a list of touch definitions.
# Keys: step, channel, delay_days, subject_tpl, body_tpl
# Template vars: {name} {business_name} {city} {site_url} {booking_url}
#                {price_onetime} {price_monthly} {niche}
# ---------------------------------------------------------------------------

SEQUENCES: dict[str, list[dict]] = {

    "roofing": [
        {
            "step": 1,
            "channel": "email",
            "delay_days": 0,
            "subject_tpl": "We built {business_name} a free roofing website — it's live now",
            "body_tpl": """\
Hi {name},

My name is Andre — I build websites for local roofing companies.

I noticed {business_name} didn't have a strong web presence, so I went ahead and built you one. It's live right now:

  {site_url}

It's set up for {city}, showcases your services (repairs, replacements, storm damage, insurance work), and has a click-to-call button. No catch — this is yours to keep.

To claim it, just reply to this email or book a quick 10-min call:
  {booking_url}

We typically set these up for ${price_onetime} one-time, or ${price_monthly}/month if you'd prefer.

— Andre Fortin
  FieldLaunch
  andre@fortinmedia.net
""",
        },
        {
            "step": 2,
            "channel": "email",
            "delay_days": 3,
            "subject_tpl": "Did you see your site, {business_name}?",
            "body_tpl": """\
Hi {name},

Just following up — wanted to make sure you saw the free roofing site I built for {business_name}:

  {site_url}

It takes about 2 minutes to claim. Just reply with YES and I'll get it set up under your name.

— Andre
""",
        },
        {
            "step": 3,
            "channel": "email",
            "delay_days": 7,
            "subject_tpl": "Last chance — offering this to another roofer in {city}",
            "body_tpl": """\
Hi {name},

I've been holding this site for {business_name} but I haven't heard back.

If I don't get a reply by end of this week, I'll offer it to the next roofing company on my list in {city}.

  {site_url}

Reply YES to claim it, or let me know if the timing isn't right. Happy to hold it a bit longer.

— Andre
""",
        },
        {
            "step": 4,
            "channel": "sms",
            "delay_days": 10,
            "subject_tpl": "",
            "body_tpl": "Hey, Andre here. I built a free site for {business_name} and sent emails last week. Reply YES to claim it or STOP to opt out. {site_url}",
        },
    ],

    "hvac": [
        {
            "step": 1,
            "channel": "email",
            "delay_days": 0,
            "subject_tpl": "Free HVAC website for {business_name} — live now",
            "body_tpl": """\
Hi {name},

My name is Andre — I build websites for local HVAC contractors.

I built a free website for {business_name} — it's live now:

  {site_url}

It's optimized for {city}, highlights your services (AC repair, heating, seasonal tune-ups, emergency calls), and has a click-to-call button. No strings attached.

To claim it, reply to this email or book a quick call:
  {booking_url}

Setup is ${price_onetime} one-time, or ${price_monthly}/month.

— Andre Fortin, FieldLaunch
""",
        },
        {
            "step": 2,
            "channel": "email",
            "delay_days": 3,
            "subject_tpl": "Quick follow-up — {business_name}'s free site",
            "body_tpl": """\
Hi {name},

Just checking in. The free HVAC site for {business_name} is still available:

  {site_url}

Season's picking up — a strong web presence now means more calls when people need you most. Reply YES and I'll get it set up.

— Andre
""",
        },
        {
            "step": 3,
            "channel": "email",
            "delay_days": 7,
            "subject_tpl": "Last call — free HVAC site for {city}",
            "body_tpl": """\
Hi {name},

One last note — I'm moving on to the next HVAC company on my list in {city} if I don't hear back this week.

{business_name}'s site:
  {site_url}

Reply YES to claim it, or let me know if you'd prefer I reach out another time.

— Andre
""",
        },
        {
            "step": 4,
            "channel": "sms",
            "delay_days": 10,
            "subject_tpl": "",
            "body_tpl": "Hey, Andre here. Built a free HVAC site for {business_name} and emailed last week. Reply YES to claim it or STOP to opt out. {site_url}",
        },
    ],

    "plumbing": [
        {
            "step": 1,
            "channel": "email",
            "delay_days": 0,
            "subject_tpl": "Free plumbing website for {business_name} — live now",
            "body_tpl": """\
Hi {name},

My name is Andre — I build websites for local plumbing companies.

I put together a free website for {business_name}:

  {site_url}

It covers {city}, highlights your services, and has 24/7 emergency call CTAs. No obligation.

Reply to claim it or book a quick call:
  {booking_url}

${price_onetime} one-time or ${price_monthly}/month.

— Andre Fortin, FieldLaunch
""",
        },
        {
            "step": 2,
            "channel": "email",
            "delay_days": 3,
            "subject_tpl": "Your free plumbing site — still available",
            "body_tpl": """\
Hi {name},

Following up on the free site for {business_name}:

  {site_url}

Just reply YES and I'll get it set up for you.

— Andre
""",
        },
        {
            "step": 3,
            "channel": "email",
            "delay_days": 7,
            "subject_tpl": "Last chance — moving on to next plumber in {city}",
            "body_tpl": """\
Hi {name},

Haven't heard back — if there's no reply this week I'll offer this to another plumbing company in {city}.

  {site_url}

Reply YES to claim it.

— Andre
""",
        },
        {
            "step": 4,
            "channel": "sms",
            "delay_days": 10,
            "subject_tpl": "",
            "body_tpl": "Andre here. Free plumbing site for {business_name}, sent emails last week. Reply YES to claim or STOP to opt out. {site_url}",
        },
    ],

    "generic": [
        {
            "step": 1,
            "channel": "email",
            "delay_days": 0,
            "subject_tpl": "We built {business_name} a free website — take a look",
            "body_tpl": """\
Hi {name},

My name is Andre — I build websites for local service businesses.

I built a free website for {business_name}. It's live now:

  {site_url}

It's set up for {city}, showcases your services, and is optimized for local search. No obligation.

To claim it, reply to this email or book a quick call:
  {booking_url}

${price_onetime} one-time, or ${price_monthly}/month.

— Andre Fortin, FieldLaunch
  andre@fortinmedia.net
""",
        },
        {
            "step": 2,
            "channel": "email",
            "delay_days": 3,
            "subject_tpl": "Quick follow-up — your free site",
            "body_tpl": """\
Hi {name},

Just following up on the free website for {business_name}:

  {site_url}

Reply YES and I'll get it set up.

— Andre
""",
        },
        {
            "step": 3,
            "channel": "email",
            "delay_days": 7,
            "subject_tpl": "Last chance — free site for {business_name}",
            "body_tpl": """\
Hi {name},

One last note — I'll be moving on to the next business on my list if I don't hear back this week.

  {site_url}

Reply YES to claim it, or let me know if the timing isn't right.

— Andre
""",
        },
        {
            "step": 4,
            "channel": "sms",
            "delay_days": 10,
            "subject_tpl": "",
            "body_tpl": "Andre here. Built a free website for {business_name} and emailed last week. Reply YES to claim it or STOP to opt out. {site_url}",
        },
    ],
}


def _pick_sequence(niche: str) -> tuple[str, list[dict]]:
    niche_lower = niche.lower()
    for key in SEQUENCES:
        if key in niche_lower:
            return key, SEQUENCES[key]
    return "generic", SEQUENCES["generic"]


def _render(tpl: str, ctx: dict) -> str:
    try:
        return tpl.format(**ctx)
    except KeyError:
        return tpl


def build_sequence(
    lead: dict,
    contact: dict,
    site_url: str,
    booking_url: str = "https://cal.com/andre-fortin",
    price_onetime: int = 697,
    price_monthly: int = 97,
    payment_link_onetime: str = "",
    payment_link_monthly: str = "",
) -> dict:
    niche = lead.get("niche") or ""
    seq_name, steps = _pick_sequence(niche)

    contact_name = (contact.get("name") or "").strip() or "there"
    contact_email = (contact.get("email") or "").strip()

    # Build per-contact prefilled payment URLs when base links are available
    def _prefill(base: str) -> str:
        if not base:
            return booking_url
        lead_id = lead.get("id") or ""
        params = []
        if contact_email:
            params.append(f"prefilled_email={contact_email}")
        if lead_id:
            params.append(f"client_reference_id=lead_{lead_id}")
        return base + ("?" + "&".join(params) if params else "")

    payment_link = _prefill(payment_link_onetime or payment_link_monthly)

    ctx = {
        "name": contact_name,
        "business_name": lead.get("business_name") or "your business",
        "city": lead.get("city") or "your area",
        "niche": niche,
        "site_url": site_url,
        "booking_url": booking_url,
        "price_onetime": price_onetime,
        "price_monthly": price_monthly,
        "payment_link": payment_link,
        "payment_link_onetime": _prefill(payment_link_onetime),
        "payment_link_monthly": _prefill(payment_link_monthly),
    }

    rendered = []
    for step in steps:
        rendered.append({
            "step": step["step"],
            "channel": step["channel"],
            "delay_days": step["delay_days"],
            "subject": _render(step["subject_tpl"], ctx),
            "body": _render(step["body_tpl"], ctx),
        })

    return {"sequence": seq_name, "steps": rendered}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json", help="Path to input JSON file")
    parser.add_argument("--output", help="Output path (default: stdout)")
    args = parser.parse_args()

    with open(args.input_json) as f:
        data = json.load(f)

    result = build_sequence(
        lead=data.get("lead", {}),
        contact=data.get("contact", {}),
        site_url=data.get("site_url", ""),
        booking_url=data.get("booking_url", "https://cal.com/andre-fortin"),
        price_onetime=data.get("price_onetime", 697),
        price_monthly=data.get("price_monthly", 97),
        payment_link_onetime=data.get("payment_link_onetime", ""),
        payment_link_monthly=data.get("payment_link_monthly", ""),
    )

    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
