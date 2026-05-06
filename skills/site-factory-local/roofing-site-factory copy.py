#!/usr/bin/env python3
"""
roofing-site-factory — Generate a roofing company website from an enriched business profile.

Uses the pre-built React/Vite roofing template (templates/roofing/) and injects
a window.SITE_CONFIG JSON object into index.html. No per-site build required.

Config is built via 3-layer merge:
  1. base-service-config.json   — skeleton with all fields
  2. niches/roofing.json        — roofing-specific static content
  3. business profile           — real business data from enricher

Haiku is used to generate creative copy (taglines, testimonials, CTA) on top
of the merged niche structure. Fallback path uses profile data directly.

Usage:
  python3 roofing-site-factory.py <profile.json> --output-dir <dir>
"""

import argparse
import copy
import datetime
import json
import os
import re
import shutil
import sys

ANTHROPIC_AVAILABLE = False
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    pass

MODEL = "claude-haiku-4-5-20251001"
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "roofing")
CONFIG_DIR   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "config")
NICHE        = "roofing"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _phone_strip(phone: str) -> str:
    return re.sub(r'[^\d+]', '', phone)


def _phone_format(phone: str) -> str:
    digits = re.sub(r'\D', '', phone)
    if len(digits) == 11 and digits[0] == '1':
        digits = digits[1:]
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return phone


def _deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge override into base. Non-empty lists replace; dicts recurse."""
    result = copy.deepcopy(base)
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = _deep_merge(result[k], v)
        elif v is not None and v != "" and v != [] and v != {}:
            result[k] = v
    return result


def _load_layered_config(niche: str) -> dict:
    """Load base-service-config.json deep-merged with niches/{niche}.json."""
    base_path  = os.path.join(CONFIG_DIR, "base-service-config.json")
    niche_path = os.path.join(CONFIG_DIR, "niches", f"{niche}.json")

    with open(base_path, encoding="utf-8") as f:
        cfg = json.load(f)

    if os.path.exists(niche_path):
        with open(niche_path, encoding="utf-8") as f:
            niche_cfg = json.load(f)
        cfg = _deep_merge(cfg, niche_cfg)

    return cfg


def _brand_split(name: str) -> tuple:
    """Strip legal suffixes and split company name into two visually balanced lines."""
    clean = re.sub(
        r'\s*,?\s*\b(LLC|Inc\.?|Co\.?|Corp\.?|Ltd\.?|LLP|LP|PLLC|PC|PA|PLC)\b\.?\s*$',
        '', name, flags=re.IGNORECASE
    ).strip().rstrip(',').strip()

    words = clean.split()
    if len(words) <= 1:
        return (clean, '')
    if len(words) == 2:
        return (words[0], words[1])

    best_i, best_diff = 1, float('inf')
    for i in range(1, len(words)):
        l1 = ' '.join(words[:i])
        l2 = ' '.join(words[i:])
        diff = abs(len(l1) - len(l2))
        if diff < best_diff:
            best_diff, best_i = diff, i

    return (' '.join(words[:best_i]), ' '.join(words[best_i:]))


def _extract_profile_fields(profile: dict) -> dict:
    """Normalize all location/contact fields from a raw enriched profile."""
    name       = profile.get("businessName") or profile.get("business_name") or "Local Roofing"
    city       = profile.get("city") or "Your City"
    state      = profile.get("state") or ""
    county     = profile.get("county") or ""
    phone_raw  = (profile.get("contact") or {}).get("phone") or profile.get("phone") or ""
    phone      = _phone_format(phone_raw) or "(555) 555-0000"
    phone_e164 = _phone_strip(phone_raw) or "+15555550000"
    email      = (profile.get("contact") or {}).get("email") or profile.get("email") or ""
    website    = (profile.get("contact") or {}).get("website") or profile.get("website") or ""
    rating     = profile.get("rating") or 5.0
    review_count = int(profile.get("reviewCount") or 0)
    years      = profile.get("yearsInBusiness") or "10+"
    license_str = profile.get("license") or ""
    license_num = profile.get("licenseNumber") or ""
    description = profile.get("description") or ""
    categories  = profile.get("categories") or ["Roofing Contractor"]

    # Service areas — real nearby cities/neighborhoods; never the bare state abbreviation
    raw_areas = profile.get("serviceAreas") or []
    service_areas = [a for a in raw_areas if a and a != state and len(a) > 2]
    if not service_areas:
        service_areas = [city]

    # Computed location strings
    city_state = f"{city}, {state}".strip(", ") if state else city
    city_state_county = (
        f"{city}, {county}, {state}".strip(", ")
        if county and county.lower() != city.lower()
        else city_state
    )

    year = datetime.datetime.now().year
    brand_line1, brand_line2 = _brand_split(name)

    return {
        "name": name, "name_short": brand_line1, "brand_line1": brand_line1, "brand_line2": brand_line2,
        "city": city, "state": state, "county": county,
        "city_state": city_state, "city_state_county": city_state_county,
        "phone": phone_e164, "phone_fmt": phone,
        "email": email, "website": website,
        "rating": rating, "review_count": review_count,
        "years": years, "license": license_str, "license_num": license_num,
        "service_areas": service_areas,
        "description": description, "categories": categories,
        "year": year,
    }


# ---------------------------------------------------------------------------
# Fallback config builder (no AI)
# ---------------------------------------------------------------------------

def _fallback_config(profile: dict) -> dict:
    """Build config from layered niche JSON + real profile data. No AI needed."""
    p = _extract_profile_fields(profile)
    cfg = _load_layered_config(NICHE)

    areas = p["service_areas"]

    # -- company --
    cfg["company"].update({
        "name":             p["name"],
        "nameShort":        p["brand_line1"],
        "nameSub":          p["brand_line2"],
        "tagline":          f"Your trusted roofing contractor in {p['city_state']}.",
        "phone":            p["phone"],
        "phoneFormatted":   p["phone_fmt"],
        "email":            p["email"],
        "city":             p["city"],
        "state":            p["state"],
        "county":           p["county"],
        "cityState":        p["city_state"],
        "cityStateCounty":  p["city_state_county"],
        "serviceArea":      f"{p['city_state']} & Surrounding Areas",
        "license":          p["license"],
        "licenseNumber":    p["license_num"],
        "yearsInBusiness":  p["years"],
        "yearsLabel":       f"Years in {p['city']}",
        "siteUrl":          p["website"],
        "copyright":        f"© {p['year']} {p['name']} LLC",
    })

    # -- seo --
    cfg["seo"].update({
        "homeTitle":       f"{p['name']} — Roofing Contractor in {p['city_state']}",
        "homeDescription": (
            f"Trusted roofing contractor serving {p['city_state_county']}. "
            f"Free inspections, storm damage claims, roof replacements. "
            f"Call {p['phone_fmt']} today."
        )[:155],
    })

    # -- announcement --
    cfg["announcement"]["suffix"] = f"available this week in {p['city']}."

    # -- hero --
    cfg["hero"]["rating"]      = str(p["rating"])
    cfg["hero"]["reviewCount"] = f"{p['review_count']}+" if p["review_count"] else "50+"
    cfg["hero"]["subtitle"]    = (
        f"Your trusted roofing contractor in {p['city_state']} — "
        f"quality craftsmanship, storm damage claims, and lifetime guarantees."
    )
    # Patch city-specific stat labels
    for s in cfg["hero"]["stats"]:
        if s.get("label") in ("Years Experience", f"Years in {p['city']}"):
            s["label"] = f"Years in {p['city']}"
        if s.get("label") == "Google Rating":
            s["stat"] = f"{p['rating']}★"

    # -- howItWorks badge --
    cfg["howItWorks"]["badgeStat"]  = p["years"]
    cfg["howItWorks"]["badgeLabel"] = f"Years in {p['city']}"

    # -- gallery: assign real neighborhoods --
    for i, proj in enumerate(cfg["gallery"].get("projects", [])):
        proj["neighborhood"] = areas[i] if i < len(areas) else p["city"]
    cfg["gallery"]["h2"] = f"Our work across {p['city']}."

    # -- testimonials: assign real locations --
    reviews = cfg.get("testimonials", {}).get("reviews", [])
    if not reviews:
        reviews = [
            {"name": "John D.", "initials": "JD",
             "text": f"After a storm hit our neighborhood they were out the next morning. Great crew, finished in one day. Highly recommend for anyone in {p['city']}."},
            {"name": "Maria S.", "initials": "MS",
             "text": "They handled our insurance claim from start to finish. Professional, fast, and we got a full replacement covered."},
            {"name": "Robert K.", "initials": "RK",
             "text": "Called Monday, crew was on the roof Wednesday. Exactly what they quoted, no surprises. Will use again."},
        ]
    for i, r in enumerate(reviews):
        r["location"] = areas[i] if i < len(areas) else p["city"]
    cfg.setdefault("testimonials", {})["reviews"] = reviews

    # -- faq: fill "What areas do you serve?" --
    area_list = ", ".join(areas[:6])
    for item in cfg["faq"].get("items", []):
        if "areas do you serve" in item.get("q", "").lower() and not item.get("a"):
            item["a"] = (
                f"We serve {area_list} and surrounding communities "
                f"throughout {p['city_state_county']}. Call us to confirm your area."
            )

    # -- cta --
    cfg["cta"]["subtext"] = (
        f"Get your free inspection today. No obligation, no pressure — "
        f"just an honest assessment from {p['city']}'s most trusted roofing team."
    )

    # -- footer --
    cfg["footer"]["tagline"] = (
        f"Your trusted roofing contractor in {p['city_state']}. "
        f"Premium materials, expert craftsmanship, lifetime guarantee."
    )
    cfg["footer"]["serviceAreas"] = _location_hrefs(areas[:8])
    cfg["locations"] = [
        {"name": a, "slug": _area_slug(a), "href": f"/locations/{_area_slug(a)}"}
        for a in areas[:8]
    ]

    return cfg


# ---------------------------------------------------------------------------
# AI config builder (Haiku fills creative copy on top of niche config)
# ---------------------------------------------------------------------------

def _ai_config(profile: dict) -> dict:
    """Load layered niche config, then use Haiku to fill creative/business copy."""
    p   = _extract_profile_fields(profile)
    cfg = _load_layered_config(NICHE)

    # Fill all structural/factual fields first (same as fallback)
    cfg = _apply_business_fields(cfg, p)

    # Ask Haiku only for the creative copy that benefits from generation
    client = anthropic.Anthropic()
    areas_str = ", ".join(p["service_areas"][:6])

    prompt = f"""Generate creative marketing copy for a roofing company website. Return ONLY valid JSON.

Business:
- Name: {p['name']}
- Location: {p['city_state_county']}
- Phone: {p['phone_fmt']}
- Rating: {p['rating']} ({p['review_count']} reviews)
- Service areas: {areas_str}
- Years in business: {p['years']}
- Description: {p['description'] or 'Local roofing contractor'}

Fill ONLY these fields (all others are already set):

{{
  "company": {{
    "tagline": "<one punchy sentence — no city name>",
    "copyright": "© {p['year']} {p['name']} LLC"
  }},
  "seo": {{
    "homeTitle": "<≤60 chars, include city + roofing>",
    "homeDescription": "<≤155 chars, call to action, include city>"
  }},
  "announcement": {{
    "text": "<short urgent hook, e.g. 'Storm season is here —'>",
    "suffix": "available this week in {p['city']}."
  }},
  "hero": {{
    "h1": ["<4-5 word line>", "<highlighted phrase>", "<4-5 word line>"],
    "subtitle": "<2 sentences — mention {p['city_state']}, key services>"
  }},
  "testimonials": {{
    "reviews": [
      {{"name": "John D.", "location": "{p['service_areas'][0] if p['service_areas'] else p['city']}", "text": "<2-3 sentence review about roofing in {p['city']}>", "initials": "JD"}},
      {{"name": "Maria S.", "location": "{p['service_areas'][1] if len(p['service_areas']) > 1 else p['city']}", "text": "<2-3 sentence review about insurance claim>", "initials": "MS"}},
      {{"name": "Robert K.", "location": "{p['service_areas'][2] if len(p['service_areas']) > 2 else p['city']}", "text": "<2-3 sentence review about speed and quality>", "initials": "RK"}}
    ]
  }},
  "cta": {{
    "h2": "<urgent 8-12 word headline about not delaying roof repair>",
    "subtext": "<2 sentences — free inspection, no obligation, mention {p['city']}>"
  }},
  "footer": {{
    "tagline": "<one sentence footer tagline, mention {p['city_state']}>"
  }}
}}"""

    msg = client.messages.create(
        model=MODEL, max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )
    text = msg.content[0].text.strip()
    text = re.sub(r'^```(?:json)?\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'\s*```$', '', text, flags=re.MULTILINE)
    ai_patch = json.loads(text)

    # Deep merge AI creative copy over the already-structured config
    return _deep_merge(cfg, ai_patch)


def _apply_business_fields(cfg: dict, p: dict) -> dict:
    """Apply all factual/structural business fields to a layered config dict."""
    areas = p["service_areas"]

    cfg["company"].update({
        "name":             p["name"],
        "nameShort":        p["brand_line1"],
        "nameSub":          p["brand_line2"],
        "tagline":          f"Your trusted roofing contractor in {p['city_state']}.",
        "phone":            p["phone"],
        "phoneFormatted":   p["phone_fmt"],
        "email":            p["email"],
        "city":             p["city"],
        "state":            p["state"],
        "county":           p["county"],
        "cityState":        p["city_state"],
        "cityStateCounty":  p["city_state_county"],
        "serviceArea":      f"{p['city_state']} & Surrounding Areas",
        "license":          p["license"],
        "licenseNumber":    p["license_num"],
        "yearsInBusiness":  p["years"],
        "yearsLabel":       f"Years in {p['city']}",
        "siteUrl":          p["website"],
        "copyright":        f"© {p['year']} {p['name']} LLC",
    })

    cfg["seo"].update({
        "homeTitle":       f"{p['name']} — Roofing Contractor in {p['city_state']}",
        "homeDescription": (
            f"Trusted roofing contractor serving {p['city_state_county']}. "
            f"Free inspections, storm damage claims, roof replacements. "
            f"Call {p['phone_fmt']} today."
        )[:155],
    })

    cfg["announcement"]["suffix"] = f"available this week in {p['city']}."

    cfg["hero"]["rating"]      = str(p["rating"])
    cfg["hero"]["reviewCount"] = f"{p['review_count']}+" if p["review_count"] else "50+"
    cfg["hero"]["subtitle"]    = (
        f"Your trusted roofing contractor in {p['city_state']} — "
        f"quality craftsmanship, storm damage claims, and lifetime guarantees."
    )
    for s in cfg["hero"]["stats"]:
        if s.get("label") in ("Years Experience", f"Years in {p['city']}"):
            s["label"] = f"Years in {p['city']}"
        if s.get("label") == "Google Rating":
            s["stat"] = f"{p['rating']}★"

    cfg["howItWorks"]["badgeStat"]  = p["years"]
    cfg["howItWorks"]["badgeLabel"] = f"Years in {p['city']}"

    for i, proj in enumerate(cfg["gallery"].get("projects", [])):
        proj["neighborhood"] = areas[i] if i < len(areas) else p["city"]
    cfg["gallery"]["h2"] = f"Our work across {p['city']}."

    reviews = cfg.get("testimonials", {}).get("reviews", [])
    if not reviews:
        reviews = [
            {"name": "John D.", "initials": "JD",
             "text": f"Great crew, finished in one day. Highly recommend for anyone in {p['city']}."},
            {"name": "Maria S.", "initials": "MS",
             "text": "They handled our insurance claim from start to finish. Professional and fast."},
            {"name": "Robert K.", "initials": "RK",
             "text": "Called Monday, crew was on the roof Wednesday. No surprises."},
        ]
    for i, r in enumerate(reviews):
        r["location"] = areas[i] if i < len(areas) else p["city"]
    cfg.setdefault("testimonials", {})["reviews"] = reviews

    area_list = ", ".join(areas[:6])
    for item in cfg["faq"].get("items", []):
        if "areas do you serve" in item.get("q", "").lower() and not item.get("a"):
            item["a"] = (
                f"We serve {area_list} and surrounding communities "
                f"throughout {p['city_state_county']}. Call us to confirm your area."
            )

    cfg["cta"]["subtext"] = (
        f"Get your free inspection today. No obligation, no pressure — "
        f"just an honest assessment from {p['city']}'s most trusted roofing team."
    )

    cfg["footer"]["tagline"] = (
        f"Your trusted roofing contractor in {p['city_state']}. "
        f"Premium materials, expert craftsmanship, lifetime guarantee."
    )
    cfg["footer"]["serviceAreas"] = _location_hrefs(areas[:8])
    cfg["locations"] = [
        {"name": a, "slug": _area_slug(a), "href": f"/locations/{_area_slug(a)}"}
        for a in areas[:8]
    ]

    return cfg


def _area_slug(area: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', area.lower()).strip('-')


def _location_hrefs(areas: list) -> list:
    return [{"label": a, "href": f"/locations/{_area_slug(a)}"} for a in areas]


def _build_location_html(cfg: dict, location: dict) -> str:
    """Generate a city/service-area landing page from site-config data."""
    company  = cfg.get("company", {})
    name     = company.get("name", "This Company")
    city     = company.get("city", "")
    state    = company.get("state", "")
    phone    = company.get("phone", "")
    phone_fmt = company.get("phoneFormatted", phone)
    email    = company.get("email", "")
    booking  = cfg.get("cta", {}).get("bookingUrl", "") or ""
    cta_href = booking or "#contact"
    services = cfg.get("services", [])
    all_locs = cfg.get("locations", [])

    area       = location["name"]
    slug       = location["slug"]
    hq_city    = city
    location_s = f"{area}, {state}".strip(", ")

    # Nearby areas sidebar (exclude current)
    other_locs = [l for l in all_locs if l["slug"] != slug]

    # Service card links
    svc_cards = "".join(
        f'<a href="{s.get("href", "/services")}" style="display:flex;align-items:center;gap:10px;'
        f'padding:.75rem 1rem;border:1.5px solid #e5e7eb;border-radius:8px;'
        f'color:#0D1B2A;font-weight:600;font-size:.875rem;transition:border-color .2s;"'
        f' onmouseover="this.style.borderColor=\'#E8890C\'" onmouseout="this.style.borderColor=\'#e5e7eb\'">'
        f'<span style="color:#E8890C;">→</span>{s.get("title","")}</a>'
        for s in services
    )

    # Other areas links
    other_area_links = "".join(
        f'<a href="/locations/{l["slug"]}" style="display:block;padding:.4rem 0;'
        f'color:#E8890C;font-size:.875rem;border-bottom:1px solid #f3f4f6;">{l["name"]}</a>'
        for l in other_locs
    )
    other_area_block = (
        f'<div style="background:#f9fafb;border-radius:10px;padding:1.25rem;margin-top:2rem;">'
        f'<div style="font-size:.75rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;'
        f'color:#9ca3af;margin-bottom:.75rem;">Other Areas We Serve</div>'
        f'{other_area_links}</div>'
    ) if other_locs else ""

    phone_html = (
        f'<div style="margin-top:1rem;font-size:.85rem;color:#9ca3af;">'
        f'Or call: <a href="tel:{phone}" style="color:#E8890C;">{phone_fmt}</a></div>'
    ) if phone else ""

    body = f"""
<style>
  .loc-grid {{ display:grid; grid-template-columns:1fr; gap:1rem; margin:1.25rem 0; }}
  @media(min-width:480px){{ .loc-grid{{ grid-template-columns:1fr 1fr; }} }}
  .loc-why {{ display:grid; grid-template-columns:1fr; gap:1rem; margin:1.25rem 0; }}
  @media(min-width:600px){{ .loc-why{{ grid-template-columns:1fr 1fr; }} }}
</style>

<a href="/" style="font-size:.85rem;color:#6b7280;display:inline-block;margin-bottom:1rem;">← Home</a>
<span style="display:inline-block;background:#fff3e0;color:#E8890C;font-size:.75rem;font-weight:700;
  letter-spacing:.05em;text-transform:uppercase;padding:3px 10px;border-radius:4px;margin-bottom:.75rem;">
  Service Area
</span>

<h1 style="margin-bottom:.75rem;">Roofing Services in {area}, {state}</h1>
<p style="font-size:1.05rem;color:#374151;line-height:1.75;margin-bottom:2rem;">
  {name} provides professional roofing services throughout {area} and the surrounding {state} communities.
  Whether you need a full roof replacement after storm damage, help navigating an insurance claim,
  or routine maintenance to extend your roof&apos;s life, our crew serves {area} homeowners
  with the same craftsmanship we bring to every job in the {hq_city} metro.
</p>

<h2>Services Available in {area}</h2>
<div class="loc-grid">{svc_cards}</div>

<div style="background:#0D1B2A;color:#fff;border-radius:12px;padding:2rem;margin:2.5rem 0;">
  <div style="font-size:1.2rem;font-weight:800;margin-bottom:.5rem;">
    Free Roof Inspection in {area}
  </div>
  <p style="color:#d1d5db;font-size:.9rem;margin-bottom:1.25rem;">
    We come to you — no trip charges, no pressure, just an honest assessment of your roof&apos;s condition.
  </p>
  <a href="{cta_href}" style="display:inline-block;background:#E8890C;color:#fff;
    padding:.75rem 1.75rem;border-radius:6px;font-weight:700;font-size:.95rem;text-decoration:none;">
    Schedule My Free Inspection
  </a>
  {phone_html}
</div>

<h2>Why {area} Homeowners Choose {name}</h2>
<div class="loc-why">
  <div style="background:#f9fafb;border-radius:10px;padding:1.25rem;">
    <div style="font-weight:700;color:#0D1B2A;margin-bottom:.4rem;">🏅 Certified &amp; Insured</div>
    <div style="color:#6b7280;font-size:.875rem;">
      GAF Master Elite certified. Full general liability and workers&apos; comp.
      Certificates available on request.
    </div>
  </div>
  <div style="background:#f9fafb;border-radius:10px;padding:1.25rem;">
    <div style="font-weight:700;color:#0D1B2A;margin-bottom:.4rem;">⚡ Fast Response</div>
    <div style="color:#6b7280;font-size:.875rem;">
      Storm damage inspections often within 24 hours.
      Emergency tarping available when you need it most.
    </div>
  </div>
  <div style="background:#f9fafb;border-radius:10px;padding:1.25rem;">
    <div style="font-weight:700;color:#0D1B2A;margin-bottom:.4rem;">📋 Insurance Experts</div>
    <div style="color:#6b7280;font-size:.875rem;">
      We handle the entire claims process — documentation, adjuster meetings,
      and supplement negotiations — so you only pay your deductible.
    </div>
  </div>
  <div style="background:#f9fafb;border-radius:10px;padding:1.25rem;">
    <div style="font-weight:700;color:#0D1B2A;margin-bottom:.4rem;">🛡️ Lifetime Warranty</div>
    <div style="color:#6b7280;font-size:.875rem;">
      Every replacement comes with our lifetime workmanship warranty plus
      the manufacturer&apos;s product warranty.
    </div>
  </div>
  <div style="background:#f9fafb;border-radius:10px;padding:1.25rem;">
    <div style="font-weight:700;color:#0D1B2A;margin-bottom:.4rem;">💰 $0 Down Financing</div>
    <div style="color:#6b7280;font-size:.875rem;">
      Don&apos;t delay a needed repair. Flexible financing with approvals in minutes
      and terms up to 12 years.
    </div>
  </div>
  <div style="background:#f9fafb;border-radius:10px;padding:1.25rem;">
    <div style="font-weight:700;color:#0D1B2A;margin-bottom:.4rem;">🏠 Local Knowledge</div>
    <div style="color:#6b7280;font-size:.875rem;">
      We know {state} weather — the heat cycles, the summer storms, the humidity.
      We spec materials that hold up in this climate.
    </div>
  </div>
</div>

<h2>Frequently Asked Questions — {area}</h2>
<div style="margin-bottom:1rem;border-bottom:1px solid #e5e7eb;padding-bottom:1rem;">
  <div style="font-weight:700;color:#0D1B2A;margin-bottom:.35rem;">Do you serve {area} directly or subcontract?</div>
  <div style="color:#6b7280;font-size:.9rem;">We serve {area} directly with our own crew — no subcontractors.
  Your project is managed start to finish by our team.</div>
</div>
<div style="margin-bottom:1rem;border-bottom:1px solid #e5e7eb;padding-bottom:1rem;">
  <div style="font-weight:700;color:#0D1B2A;margin-bottom:.35rem;">Is there a trip charge for {area}?</div>
  <div style="color:#6b7280;font-size:.9rem;">No. Inspections and estimates in {area} are always free,
  with no trip charge.</div>
</div>
<div style="margin-bottom:1rem;border-bottom:1px solid #e5e7eb;padding-bottom:1rem;">
  <div style="font-weight:700;color:#0D1B2A;margin-bottom:.35rem;">How quickly can you start a project in {area}?</div>
  <div style="color:#6b7280;font-size:.9rem;">Typically within 1–2 weeks of contract signing,
  depending on material availability and current project load.</div>
</div>
<div style="margin-bottom:2rem;border-bottom:1px solid #e5e7eb;padding-bottom:1rem;">
  <div style="font-weight:700;color:#0D1B2A;margin-bottom:.35rem;">What if I have storm damage in {area} right now?</div>
  <div style="color:#6b7280;font-size:.9rem;">Call or book online and we&apos;ll schedule an emergency
  inspection within 24 hours. We can tarp active leaks immediately.</div>
</div>

{other_area_block}"""

    return _render_page(
        f"Roofing Services in {area}, {state} | {name}",
        f"Professional roofing services in {area}, {state}. {name} — free inspections, insurance claims, full replacements.",
        name, booking, body
    )


# ---------------------------------------------------------------------------
# Standalone page builders (bypass hardcoded bundle content)
# ---------------------------------------------------------------------------

def _build_locations_index_html(cfg: dict) -> str:
    """Locations/service-areas index page."""
    company   = cfg.get("company", {})
    name      = company.get("name", "This Company")
    city      = company.get("city", "")
    state     = company.get("state", "")
    booking   = cfg.get("cta", {}).get("bookingUrl", "") or ""
    locations = cfg.get("locations", [])
    location  = f"{city}, {state}".strip(", ")

    cards = "".join(
        f'<a class="loc-idx-card" href="/locations/{l["slug"]}">'
        f'<span class="loc-idx-name">{l["name"]}, {state}</span>'
        f'<span class="loc-idx-link">View services →</span>'
        f'</a>'
        for l in locations
    )

    body = f"""
<style>
  .loc-idx-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:1rem; margin:1.5rem 0 2.5rem; }}
  .loc-idx-card {{ display:flex; flex-direction:column; justify-content:space-between; border:1.5px solid #e5e7eb;
    border-radius:10px; padding:1.25rem 1.5rem; transition:border-color .2s,box-shadow .2s; color:inherit; }}
  .loc-idx-card:hover {{ border-color:#E8890C; box-shadow:0 4px 16px rgba(232,137,12,.12); text-decoration:none; }}
  .loc-idx-name {{ font-weight:700; font-size:.95rem; color:#0D1B2A; margin-bottom:.5rem; }}
  .loc-idx-link {{ font-size:.8125rem; font-weight:600; color:#E8890C; }}
</style>
<a href="/" style="font-size:.85rem;color:#6b7280;display:inline-block;margin-bottom:1rem;">← Home</a>
<h1>Areas We Serve</h1>
<p style="color:#6b7280;margin-bottom:.25rem;">{name} — based in {location}</p>
<p>We provide professional roofing services across the following communities.
Click any area to learn more about the services available near you.</p>
<div class="loc-idx-grid">{cards}</div>
<div style="background:#f9fafb;border-radius:10px;padding:1.5rem;">
  <strong>Don&apos;t see your city?</strong> We may still serve your area.
  <a href="{booking or '#contact'}">Contact us →</a>
</div>"""

    return _render_page(
        f"Service Areas | {name}",
        f"{name} serves {location} and surrounding communities. View all roofing service areas.",
        name, booking, body
    )

_PAGE_SHELL = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | {company}</title>
  <meta name="description" content="{meta_desc}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'Plus Jakarta Sans', sans-serif; background: #fff; color: #1a1a2e; line-height: 1.7; padding-top: 52px; }}
    a {{ color: #E8890C; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .nav {{ background: #0D1B2A; padding: 1rem 2rem; display: flex; align-items: center; justify-content: space-between; }}
    .nav-logo {{ display:flex; align-items:center; gap:10px; text-decoration:none; }}
    .nav-logo-icon {{ flex:none; }}
    .nav-brand {{ display:flex; flex-direction:column; line-height:1.15; }}
    .nav-brand-l1 {{ color:#fff; font-size:1rem; font-weight:800; letter-spacing:-0.01em; }}
    .nav-brand-l2 {{ color:#E8890C; font-size:0.7rem; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; }}
    .nav-cta {{ background: #E8890C; color: #fff; padding: 0.5rem 1.25rem; border-radius: 6px; font-weight: 600; font-size: 0.875rem; }}
    .nav-cta:hover {{ background: #d17a0b; text-decoration: none; }}
    .page {{ max-width: 820px; margin: 0 auto; padding: 3rem 1.5rem 5rem; }}
    h1 {{ font-size: 2rem; font-weight: 800; color: #0D1B2A; margin-bottom: 0.5rem; }}
    h2 {{ font-size: 1.25rem; font-weight: 700; color: #0D1B2A; margin: 2rem 0 0.5rem; }}
    h3 {{ font-size: 1rem; font-weight: 700; color: #0D1B2A; margin: 1.5rem 0 0.35rem; }}
    p {{ margin-bottom: 1rem; color: #374151; }}
    ul {{ margin: 0 0 1rem 1.5rem; color: #374151; }}
    li {{ margin-bottom: 0.4rem; }}
    .subtitle {{ color: #6b7280; font-size: 0.875rem; margin-bottom: 2.5rem; }}
    .footer {{ background: #0D1B2A; color: #9ca3af; padding: 2rem; font-size: 0.8125rem; }}
    .footer-inner {{ max-width:820px; margin:0 auto; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:1rem; }}
    .footer-brand {{ display:flex; align-items:center; gap:10px; text-decoration:none; }}
    .footer-brand-text {{ display:flex; flex-direction:column; line-height:1.15; }}
    .footer-brand-l1 {{ color:#fff; font-size:0.875rem; font-weight:800; letter-spacing:-0.01em; }}
    .footer-brand-l2 {{ color:#E8890C; font-size:0.65rem; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; }}
    .footer-copy {{ color:#6b7280; font-size:0.75rem; }}
    .back {{ display: inline-block; margin-bottom: 2rem; font-size: 0.875rem; color: #6b7280; }}
  </style>
</head>
<body>
  <div id="fl-preview-bar" style="position:fixed;top:0;left:0;right:0;z-index:99999;background:#0D1B2A;border-bottom:2px solid #E8890C;display:flex;align-items:center;justify-content:space-between;padding:0 16px;height:52px;gap:12px;font-family:'Plus Jakarta Sans',sans-serif;box-shadow:0 2px 12px rgba(0,0,0,.5);">
    <div style="min-width:0;overflow:hidden;">
      <span style="background:#E8890C;color:#fff;font-size:10px;font-weight:700;letter-spacing:.06em;padding:2px 7px;border-radius:4px;text-transform:uppercase;margin-right:10px;">Preview</span>
      <span style="color:#d1d5db;font-size:13px;font-weight:500;">This site was built for <strong style="color:#fff;">{company}</strong></span>
    </div>
    <a href="{booking_url}" style="flex:none;background:#E8890C;color:#fff;padding:9px 20px;border-radius:6px;font-weight:700;font-size:13px;text-decoration:none;white-space:nowrap;">Make It Mine →</a>
  </div>
  <nav class="nav">
    <a class="nav-logo" href="/">
      <svg class="nav-logo-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 46" width="24" height="23" fill="none" aria-hidden="true">
        <path fill="#E8890C" d="M25.946 44.938c-.664.845-2.021.375-2.021-.698V33.937a2.26 2.26 0 0 0-2.262-2.262H10.287c-.92 0-1.456-1.04-.92-1.788l7.48-10.471c1.07-1.497 0-3.578-1.842-3.578H1.237c-.92 0-1.456-1.04-.92-1.788L10.013.474c.214-.297.556-.474.92-.474h28.894c.92 0 1.456 1.04.92 1.788l-7.48 10.471c-1.07 1.498 0 3.579 1.842 3.579h11.377c.943 0 1.473 1.088.89 1.83L25.947 44.94z"/>
      </svg>
      <span class="nav-brand">
        <span class="nav-brand-l1">{brand_line1}</span>
        <span class="nav-brand-l2">{brand_line2}</span>
      </span>
    </a>
    <a class="nav-cta" href="{booking_url}">Get a Free Quote</a>
  </nav>
  <div class="page">
    <a class="back" href="/">← Back to home</a>
    {body}
  </div>
  <footer class="footer">
    <div class="footer-inner">
      <a class="footer-brand" href="/">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 46" width="20" height="19" fill="none" aria-hidden="true">
          <path fill="#E8890C" d="M25.946 44.938c-.664.845-2.021.375-2.021-.698V33.937a2.26 2.26 0 0 0-2.262-2.262H10.287c-.92 0-1.456-1.04-.92-1.788l7.48-10.471c1.07-1.497 0-3.578-1.842-3.578H1.237c-.92 0-1.456-1.04-.92-1.788L10.013.474c.214-.297.556-.474.92-.474h28.894c.92 0 1.456 1.04.92 1.788l-7.48 10.471c-1.07 1.498 0 3.579 1.842 3.579h11.377c.943 0 1.473 1.088.89 1.83L25.947 44.94z"/>
        </svg>
        <span class="footer-brand-text">
          <span class="footer-brand-l1">{brand_line1}</span>
          <span class="footer-brand-l2">{brand_line2}</span>
        </span>
      </a>
      <span class="footer-copy">&copy; {year} {company}. All rights reserved.</span>
    </div>
  </footer>
</body>
</html>"""


def _render_page(title: str, meta_desc: str, company: str, booking_url: str, body_html: str,
                 brand_line1: str = None, brand_line2: str = None) -> str:
    year = datetime.date.today().year
    l1, l2 = _brand_split(company) if brand_line1 is None else (brand_line1, brand_line2 or '')
    return _PAGE_SHELL.format(
        title=title, meta_desc=meta_desc, company=company,
        booking_url=booking_url or "#contact", year=year,
        body=body_html, brand_line1=l1, brand_line2=l2,
    )


def _build_privacy_html(cfg: dict) -> str:
    company = cfg.get("company", {})
    name    = company.get("name", "This Company")
    city    = company.get("city", "")
    state   = company.get("state", "")
    email   = company.get("email", "info@example.com")
    phone   = company.get("phone", "")
    phone_fmt = company.get("phoneFormatted", phone)
    booking = cfg.get("cta", {}).get("bookingUrl", "") or ""
    location = f"{city}, {state}".strip(", ")
    today   = datetime.date.today().strftime("%B %d, %Y")

    body = f"""
<h1>Privacy Policy</h1>
<p class="subtitle">Last updated: {today}</p>
<p>{name} ("we," "us," or "our"), located in {location}, is committed to protecting your personal information.
This Privacy Policy explains how we collect, use, and safeguard information when you visit our website or contact us.</p>

<h2>Information We Collect</h2>
<h3>Information You Provide</h3>
<ul>
  <li>Name, email address, phone number, and home address when you request a quote or contact us</li>
  <li>Project details, photos, or documents you share with us</li>
  <li>Payment information (processed securely; we do not store card numbers)</li>
</ul>
<h3>Information Collected Automatically</h3>
<ul>
  <li>IP address, browser type, pages visited, and time spent on our site</li>
  <li>Cookies and similar tracking technologies for analytics and site improvement</li>
</ul>

<h2>How We Use Your Information</h2>
<ul>
  <li>To provide roofing estimates, schedule appointments, and deliver services</li>
  <li>To respond to inquiries and communicate about your project</li>
  <li>To send occasional service updates or promotions (you may opt out at any time)</li>
  <li>To improve our website and understand how visitors use it</li>
  <li>To comply with legal obligations</li>
</ul>

<h2>Sharing Your Information</h2>
<p>We do not sell, trade, or rent your personal information to third parties. We may share information with:</p>
<ul>
  <li>Trusted service providers (scheduling software, payment processors) who assist our operations under confidentiality agreements</li>
  <li>Legal authorities when required by law</li>
</ul>

<h2>Cookies</h2>
<p>Our website uses cookies to enhance your experience. You can instruct your browser to refuse cookies,
though some features may not function properly.</p>

<h2>Data Security</h2>
<p>We implement industry-standard security measures to protect your data. However, no method of transmission
over the internet is 100% secure.</p>

<h2>Your Rights</h2>
<p>Depending on your location, you may have rights to access, correct, or delete your personal data.
Contact us to exercise these rights.</p>

<h2>Third-Party Links</h2>
<p>Our site may contain links to third-party websites. We are not responsible for their privacy practices.</p>

<h2>Children's Privacy</h2>
<p>Our services are not directed to children under 13. We do not knowingly collect data from children.</p>

<h2>Changes to This Policy</h2>
<p>We may update this policy periodically. Changes will be posted on this page with an updated date.</p>

<h2>Contact Us</h2>
<p>Questions about this Privacy Policy? Reach us at:</p>
<ul>
  <li><strong>{name}</strong></li>
  <li>{location}</li>
  {f'<li>Phone: <a href="tel:{phone}">{phone_fmt}</a></li>' if phone else ''}
  <li>Email: <a href="mailto:{email}">{email}</a></li>
</ul>"""
    return _render_page("Privacy Policy", f"Privacy policy for {name} — {location}", name, booking, body)


def _build_terms_html(cfg: dict) -> str:
    company = cfg.get("company", {})
    name    = company.get("name", "This Company")
    city    = company.get("city", "")
    state   = company.get("state", "")
    email   = company.get("email", "info@example.com")
    phone   = company.get("phone", "")
    phone_fmt = company.get("phoneFormatted", phone)
    booking = cfg.get("cta", {}).get("bookingUrl", "") or ""
    location = f"{city}, {state}".strip(", ")
    today   = datetime.date.today().strftime("%B %d, %Y")

    body = f"""
<h1>Terms of Service</h1>
<p class="subtitle">Last updated: {today}</p>
<p>These Terms of Service govern your use of the {name} website and any services we provide.
By accessing our site or engaging our services, you agree to these terms.</p>

<h2>Services</h2>
<p>{name} provides residential and commercial roofing services in {location} and surrounding areas,
including roof installation, repair, replacement, and inspection.</p>

<h2>Estimates and Contracts</h2>
<ul>
  <li>Written estimates are provided at no charge and are valid for 30 days unless otherwise stated</li>
  <li>All work is governed by a signed contract specifying scope, materials, timeline, and payment terms</li>
  <li>Changes to scope require written authorization and may affect price and timeline</li>
</ul>

<h2>Payment Terms</h2>
<ul>
  <li>Payment schedules are outlined in the project contract</li>
  <li>A deposit may be required before work begins</li>
  <li>Final payment is due upon project completion</li>
  <li>Overdue balances may incur interest at the maximum rate permitted by {state} law</li>
</ul>

<h2>Warranties</h2>
<ul>
  <li>Manufacturer warranties apply to materials as specified</li>
  <li>Our workmanship warranty is specified in your project contract</li>
  <li>Warranties are void if damage results from acts of nature, third-party modifications, or lack of maintenance</li>
</ul>

<h2>Limitation of Liability</h2>
<p>To the maximum extent permitted by law, {name} shall not be liable for indirect, incidental,
or consequential damages. Our total liability shall not exceed the amount paid for the services in question.</p>

<h2>Cancellation</h2>
<p>Cancellation terms are specified in your project contract. Deposits may be non-refundable if materials
have been ordered or work has commenced.</p>

<h2>Dispute Resolution</h2>
<p>Any disputes shall first be addressed through good-faith negotiation. If unresolved, disputes shall be
submitted to binding arbitration in {state} under applicable arbitration rules.</p>

<h2>Governing Law</h2>
<p>These terms are governed by the laws of the State of {state}.</p>

<h2>Changes to Terms</h2>
<p>We reserve the right to modify these terms. Continued use of our services after changes constitutes acceptance.</p>

<h2>Contact</h2>
<ul>
  <li><strong>{name}</strong></li>
  <li>{location}</li>
  {f'<li>Phone: <a href="tel:{phone}">{phone_fmt}</a></li>' if phone else ''}
  <li>Email: <a href="mailto:{email}">{email}</a></li>
</ul>"""
    return _render_page("Terms of Service", f"Terms of service for {name} — {location}", name, booking, body)


def _build_services_html(cfg: dict) -> str:
    company  = cfg.get("company", {})
    name     = company.get("name", "This Company")
    city     = company.get("city", "")
    state    = company.get("state", "")
    booking  = cfg.get("cta", {}).get("bookingUrl", "") or ""
    services = cfg.get("services", [])
    location = f"{city}, {state}".strip(", ")
    niche    = cfg.get("niche", "").replace("-", " ").title() or "Service"
    brand_l1 = company.get("nameShort") or name
    brand_l2 = company.get("nameSub") or ""

    cards = ""
    for svc in services:
        slug  = re.sub(r'[^a-z0-9]+', '-', svc.get("title", "service").lower()).strip('-')
        title = svc.get("title", "")
        desc  = svc.get("description", "")
        cards += f"""
  <a class="svc-card" href="/services/{slug}">
    <div class="svc-title">{title}</div>
    <div class="svc-desc">{desc}</div>
    <div class="svc-link">Learn more →</div>
  </a>"""

    body = f"""
<style>
  .svc-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 1.25rem; margin-top: 1.5rem; }}
  .svc-card {{ display: block; border: 1.5px solid #e5e7eb; border-radius: 10px; padding: 1.5rem; transition: border-color .2s, box-shadow .2s; color: inherit; }}
  .svc-card:hover {{ border-color: #E8890C; box-shadow: 0 4px 16px rgba(232,137,12,.12); text-decoration: none; }}
  .svc-title {{ font-weight: 700; font-size: 1rem; color: #0D1B2A; margin-bottom: 0.5rem; }}
  .svc-desc {{ font-size: 0.875rem; color: #6b7280; margin-bottom: 1rem; }}
  .svc-link {{ font-size: 0.8125rem; font-weight: 600; color: #E8890C; }}
  .hero-sub {{ color: #6b7280; margin-bottom: 0.5rem; }}
</style>
<h1>Our {niche} Services</h1>
<p class="hero-sub">{name} — Serving {location} and surrounding areas</p>
<p>Professional {niche.lower()} services backed by craftsmanship and quality materials. Explore our full range below.</p>
<div class="svc-grid">{cards}
</div>
<div style="margin-top:2.5rem; padding: 1.5rem; background: #f9fafb; border-radius: 10px;">
  <strong>Ready to get started?</strong> <a href="{booking or '#contact'}">Request a free quote →</a>
</div>"""
    return _render_page(f"{niche} Services", f"Professional {niche.lower()} services from {name} in {location}",
                        name, booking, body, brand_l1, brand_l2)


def _build_service_detail_html(cfg: dict, service: dict, slug: str) -> str:
    company  = cfg.get("company", {})
    name      = company.get("name", "This Company")
    city      = company.get("city", "")
    state     = company.get("state", "")
    phone     = company.get("phone", "")
    phone_fmt = company.get("phoneFormatted", phone)
    email     = company.get("email", "")
    booking   = cfg.get("cta", {}).get("bookingUrl", "") or ""
    location  = f"{city}, {state}".strip(", ")
    cta_href  = booking or "#contact"
    niche     = cfg.get("niche", "").replace("-", " ").title() or "Service"
    brand_l1  = company.get("nameShort") or name
    brand_l2  = company.get("nameSub") or ""

    title     = service.get("title", "Service")
    desc      = service.get("description", "")
    intro     = service.get("intro", desc)
    features  = service.get("features", [])
    process   = service.get("process", [])
    materials = service.get("materials", [])
    faqs      = service.get("faqs", [])
    svc_image = service.get("image", "")

    # --- What's Included ---
    feat_html = ""
    if features:
        items = "".join(
            f'<li style="display:flex;align-items:flex-start;gap:10px;margin-bottom:.6rem;">'
            f'<span style="color:#E8890C;font-weight:700;flex:none;margin-top:1px;">✓</span>'
            f'<span>{f}</span></li>'
            for f in features
        )
        feat_html = f'<ul style="list-style:none;margin:1rem 0 0;padding:0;">{items}</ul>'

    # --- Process steps ---
    process_html = ""
    if process:
        steps = "".join(
            f'<div style="display:flex;gap:16px;margin-bottom:1.25rem;">'
            f'<div style="flex:none;width:36px;height:36px;border-radius:50%;background:#E8890C;color:#fff;'
            f'font-weight:800;font-size:.85rem;display:flex;align-items:center;justify-content:center;">{s["step"]}</div>'
            f'<div><div style="font-weight:700;color:#0D1B2A;margin-bottom:.2rem;">{s["title"]}</div>'
            f'<div style="color:#6b7280;font-size:.9rem;">{s["desc"]}</div></div></div>'
            for s in process
        )
        process_html = (
            f'<div style="background:#f9fafb;border-radius:12px;padding:1.75rem;margin:2rem 0;">'
            f'<h2 style="font-size:1.15rem;font-weight:800;color:#0D1B2A;margin-bottom:1.25rem;">How It Works</h2>'
            f'{steps}</div>'
        )

    # --- Materials ---
    mat_html = ""
    if materials:
        pills = "".join(
            f'<span style="background:#fff;border:1.5px solid #e5e7eb;border-radius:20px;'
            f'padding:4px 12px;font-size:.8rem;color:#374151;">{m}</span>'
            for m in materials
        )
        mat_html = (
            f'<div style="margin:2rem 0;">'
            f'<h2 style="font-size:1.1rem;font-weight:800;color:#0D1B2A;margin-bottom:.75rem;">Materials &amp; Products</h2>'
            f'<div style="display:flex;flex-wrap:wrap;gap:8px;">{pills}</div></div>'
        )

    # --- FAQs ---
    faq_html = ""
    if faqs:
        items = "".join(
            f'<div style="border-bottom:1px solid #e5e7eb;padding:1rem 0;">'
            f'<div style="font-weight:700;color:#0D1B2A;margin-bottom:.4rem;">{f["q"]}</div>'
            f'<div style="color:#6b7280;font-size:.9rem;">{f["a"]}</div></div>'
            for f in faqs
        )
        faq_html = (
            f'<div style="margin:2.5rem 0;">'
            f'<h2 style="font-size:1.15rem;font-weight:800;color:#0D1B2A;margin-bottom:.25rem;">Common Questions</h2>'
            f'{items}</div>'
        )

    # --- Other services sidebar links ---
    other_services = [s for s in cfg.get("services", []) if s.get("slug") != slug]
    other_html = ""
    if other_services:
        links = "".join(
            f'<a href="/services/{s.get("slug","")}" style="display:block;padding:.5rem 0;'
            f'color:#E8890C;font-size:.875rem;border-bottom:1px solid #f3f4f6;">{s.get("title","")}</a>'
            for s in other_services
        )
        other_html = (
            f'<div style="background:#f9fafb;border-radius:10px;padding:1.25rem;margin:2rem 0;">'
            f'<div style="font-size:.75rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;'
            f'color:#9ca3af;margin-bottom:.75rem;">Other Services</div>'
            f'{links}</div>'
        )

    phone_html = (
        f'<div style="margin-top:1rem;font-size:.85rem;color:#9ca3af;">'
        f'Or call: <a href="tel:{phone}" style="color:#E8890C;">{phone_fmt}</a></div>'
    ) if phone else ""

    body = f"""
<style>
  .svc-hero {{ margin-bottom: 2rem; }}
  .svc-tag {{ display:inline-block; background:#fff3e0; color:#E8890C; font-size:.75rem;
    font-weight:700; letter-spacing:.05em; text-transform:uppercase;
    padding:3px 10px; border-radius:4px; margin-bottom:.75rem; }}
</style>
<div class="svc-hero">
  <a href="/services" style="font-size:.85rem;color:#6b7280;display:inline-block;margin-bottom:1rem;">← All Services</a>
  <span class="svc-tag">{niche} Service</span>
  <h1 style="margin-bottom:.75rem;">{title} in {city}</h1>
  <p style="font-size:1.05rem;color:#374151;line-height:1.75;">{intro}</p>
</div>

{f'<img src="{svc_image}" alt="{title} service" style="width:100%;height:320px;object-fit:cover;border-radius:12px;margin-bottom:2rem;" loading="lazy">' if svc_image else ''}

{f'<div><h2>What&apos;s Included</h2>{feat_html}</div>' if feat_html else ''}

{process_html}

{mat_html}

<div style="background:#0D1B2A;color:#fff;border-radius:12px;padding:2rem;margin:2.5rem 0;">
  <div style="font-size:1.2rem;font-weight:800;margin-bottom:.5rem;">Get a Free {title} Estimate</div>
  <p style="color:#d1d5db;font-size:.9rem;margin-bottom:1.25rem;">
    Serving {location} and surrounding areas. No obligation — just an honest assessment.
  </p>
  <a href="{cta_href}" style="display:inline-block;background:#E8890C;color:#fff;
    padding:.75rem 1.75rem;border-radius:6px;font-weight:700;font-size:.95rem;text-decoration:none;">
    Schedule My Free Inspection
  </a>
  {phone_html}
</div>

<h2>Serving {location}</h2>
<p>{name} serves homeowners and businesses throughout {city} and the surrounding {state} area.
We combine local knowledge of {state} weather patterns with proven techniques and manufacturer-certified materials.</p>

{faq_html}

{other_html}"""

    return _render_page(
        f"{title} in {city}, {state} | {name}",
        f"{title} in {location}. {desc[:120]}",
        name, booking, body, brand_l1, brand_l2
    )


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def generate_site(profile: dict, output_dir: str) -> dict:
    print(f"  -> Generating roofing site for: {profile.get('businessName', '?')}")

    if not os.path.isdir(TEMPLATE_DIR):
        return {"error": f"Template not found at {TEMPLATE_DIR}"}

    # Step 1: Build site-config via layered merge + AI or fallback
    if ANTHROPIC_AVAILABLE:
        try:
            print("  -> Generating creative copy with Haiku...")
            site_config = _ai_config(profile)
            print("  -> Content generated.")
        except Exception as e:
            print(f"  [WARN] AI config failed: {e}. Using fallback.", file=sys.stderr)
            site_config = _fallback_config(profile)
    else:
        print("  [WARN] anthropic not installed, using fallback config.", file=sys.stderr)
        site_config = _fallback_config(profile)

    site_config["template"] = "roofing-v1"
    site_config["niche"]    = NICHE

    # Inject operator booking URL from profile (passed by the generate route)
    if profile.get("_bookingUrl"):
        site_config.setdefault("cta", {})["bookingUrl"] = profile["_bookingUrl"]

    # Step 2: Copy template shell to output dir
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    shutil.copytree(TEMPLATE_DIR, output_dir)

    # Step 3: Write site-config.json (primary content artifact)
    config_path = os.path.join(output_dir, "site-config.json")
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(site_config, f, indent=2, ensure_ascii=False)
    print("  -> site-config.json written")

    # Step 4: Patch index.html — inject SEO meta + inline window.SITE_CONFIG
    index_path = os.path.join(output_dir, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    seo         = site_config.get("seo", {})
    company     = site_config.get("company", {})
    title       = seo.get("homeTitle") or company.get("name", "Roofing Contractor")
    description = seo.get("homeDescription", "")

    html = re.sub(r'<title>[^<]*</title>', f'<title>{title}</title>', html)

    business_name = company.get("name", "Your Business")
    booking_url   = (site_config.get("cta") or {}).get("bookingUrl") or ""

    injection = (
        f'    <meta name="description" content="{description}">\n'
        f'    <meta property="og:title" content="{title}">\n'
        f'    <meta property="og:description" content="{description}">\n'
        f'    <meta property="og:type" content="website">\n'
        f'    <script>window.SITE_CONFIG={json.dumps(site_config, separators=(",", ":"), ensure_ascii=False)};</script>\n'
        # Push body content below the fixed preview banner
        f'    <style>body{{padding-top:52px}}@media(max-width:600px){{.fl-pb-detail{{display:none}}}}</style>\n'
        # Click-intercept: force full page load for standalone pages
        # so vercel.json routes them instead of React Router swallowing the navigation
        f'    <script>(function(){{document.addEventListener("click",function(e){{var a=e.target.closest("a[href]");if(!a)return;var h=a.getAttribute("href");if(/^\\/(services|locations|privacy|terms)/.test(h)){{e.preventDefault();e.stopPropagation();window.location.href=h;}}}},true);}})();</script>'
    )
    html = html.replace("</head>", f"{injection}\n  </head>")

    # Normalize absolute asset paths to relative so the site works locally and on Vercel
    html = re.sub(r'(src|href)="/assets/', r'\1="./assets/', html)
    html = re.sub(r'(href)="/favicon', r'\1="./favicon', html)

    # Preview banner — injected right after <body> so it sits above the React app
    cta_href  = booking_url or "#contact"
    preview_bar = (
        f'<div id="fl-preview-bar" style="position:fixed;top:0;left:0;right:0;z-index:99999;'
        f'background:#0D1B2A;border-bottom:2px solid #E8890C;display:flex;align-items:center;'
        f'justify-content:space-between;padding:0 16px;height:52px;gap:12px;'
        f'font-family:\'Plus Jakarta Sans\',sans-serif;box-shadow:0 2px 12px rgba(0,0,0,.5);">'
        f'<div style="min-width:0;overflow:hidden;">'
        f'<span style="background:#E8890C;color:#fff;font-size:10px;font-weight:700;'
        f'letter-spacing:.06em;padding:2px 7px;border-radius:4px;text-transform:uppercase;'
        f'margin-right:10px;">Preview</span>'
        f'<span style="color:#d1d5db;font-size:13px;font-weight:500;">'
        f'This site was built for <strong style="color:#fff;">{business_name}</strong>'
        f'</span>'
        f'<span class="fl-pb-detail" style="color:#6b7280;font-size:13px;"> — not yet live</span>'
        f'</div>'
        f'<a href="{cta_href}" style="flex:none;background:#E8890C;color:#fff;'
        f'padding:9px 20px;border-radius:6px;font-weight:700;font-size:13px;'
        f'text-decoration:none;white-space:nowrap;letter-spacing:.01em;'
        f'transition:background .15s;" onmouseover="this.style.background=\'#d17a0b\'" '
        f'onmouseout="this.style.background=\'#E8890C\'">Make It Mine →</a>'
        f'</div>\n'
    )
    html = html.replace("<body>", f"<body>\n{preview_bar}", 1)

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)

    # Step 5: Generate standalone HTML pages (bypass hardcoded bundle content)
    services = site_config.get("services", [])

    with open(os.path.join(output_dir, "privacy.html"), "w", encoding="utf-8") as f:
        f.write(_build_privacy_html(site_config))
    with open(os.path.join(output_dir, "terms.html"), "w", encoding="utf-8") as f:
        f.write(_build_terms_html(site_config))
    with open(os.path.join(output_dir, "services.html"), "w", encoding="utf-8") as f:
        f.write(_build_services_html(site_config))

    services_dir = os.path.join(output_dir, "services")
    os.makedirs(services_dir, exist_ok=True)
    for svc in services:
        slug = svc.get("slug") or re.sub(r'[^a-z0-9]+', '-', svc.get("title", "service").lower()).strip('-')
        with open(os.path.join(services_dir, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(_build_service_detail_html(site_config, svc, slug))

    locations = site_config.get("locations", [])
    locations_dir = os.path.join(output_dir, "locations")
    os.makedirs(locations_dir, exist_ok=True)
    with open(os.path.join(output_dir, "locations.html"), "w", encoding="utf-8") as f:
        f.write(_build_locations_index_html(site_config))
    for loc in locations:
        with open(os.path.join(locations_dir, f"{loc['slug']}.html"), "w", encoding="utf-8") as f:
            f.write(_build_location_html(site_config, loc))

    print(
        f"  -> Standalone pages written: privacy, terms, services ({len(services)} pages), "
        f"locations ({len(locations)} pages)"
    )

    # Step 6: Rewrite vercel.json to route standalone pages before the catch-all
    def _svc_slug(svc: dict) -> str:
        return svc.get("slug") or re.sub(r'[^a-z0-9]+', '-', svc.get('title', '').lower()).strip('-')

    service_routes = [
        {"src": f"/services/{_svc_slug(svc)}", "dest": f"/services/{_svc_slug(svc)}.html"}
        for svc in services
    ]
    location_routes = [
        {"src": f"/locations/{loc['slug']}", "dest": f"/locations/{loc['slug']}.html"}
        for loc in locations
    ]
    vercel_cfg = {
        "version": 2,
        "routes": [
            {"src": "/assets/(.*)", "dest": "/assets/$1"},
            {"src": "/privacy", "dest": "/privacy.html"},
            {"src": "/terms", "dest": "/terms.html"},
            {"src": "/services", "dest": "/services.html"},
            *service_routes,
            {"src": "/locations", "dest": "/locations.html"},
            *location_routes,
            {"src": "/(.*)", "dest": "/index.html"},
        ]
    }
    vercel_path = os.path.join(output_dir, "vercel.json")
    with open(vercel_path, "w", encoding="utf-8") as f:
        json.dump(vercel_cfg, f, indent=2)
    print("  -> vercel.json updated with standalone page routes")

    print(f"  -> Site written to {output_dir}")
    return {
        "status":      "ok",
        "output_dir":  output_dir,
        "title":       title,
        "config_file": config_path,
        "template":    "roofing-v1",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Roofing site factory.")
    parser.add_argument("profile_json", help="Path to enriched business profile JSON")
    parser.add_argument("--output-dir", required=True, help="Directory to write the generated site into")
    args = parser.parse_args()

    if not os.path.exists(args.profile_json):
        print(json.dumps({"error": f"Profile not found: {args.profile_json}"}))
        sys.exit(1)

    with open(args.profile_json) as f:
        profile = json.load(f)

    result = generate_site(profile, args.output_dir)
    print(json.dumps(result, indent=2))
    if result.get("error"):
        sys.exit(1)
