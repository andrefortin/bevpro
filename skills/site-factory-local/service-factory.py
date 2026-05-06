#!/usr/bin/env python3
"""
service-factory — Generic site factory for all non-roofing niches.

Uses the roofing React template as the rendering shell (fully config-driven via
window.SITE_CONFIG), with the correct layered niche config (base → niche → profile).

Supported niches: plumbing, hvac, lawn-care (and any future niche with a config file)

Usage:
  python3 service-factory.py <profile.json> --output-dir <dir> [--niche plumbing]
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
# Reuse the roofing React SPA — it renders from window.SITE_CONFIG, niche-agnostic
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "roofing")
CONFIG_DIR   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "config")

NICHE_KEYWORDS = {
    "plumbing":   {"plumb", "plumber", "drain", "pipe", "sewer", "water heater", "faucet", "toilet"},
    "hvac":       {"hvac", "heating", "cooling", "air condition", "furnace", "heat pump", "ac repair", "ductwork"},
    "lawn-care":  {"lawn", "landscap", "mowing", "grass", "yard", "fertiliz", "weed control", "irrigation", "sprinkler"},
    "electrical": {"electric", "electrician", "wiring", "panel", "outlet", "breaker"},
    "painting":   {"paint", "painter", "interior paint", "exterior paint", "staining"},
}


# ---------------------------------------------------------------------------
# Helpers (shared with roofing-site-factory)
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
    result = copy.deepcopy(base)
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = _deep_merge(result[k], v)
        elif v is not None and v != "" and v != [] and v != {}:
            result[k] = v
    return result


def _load_layered_config(niche: str) -> dict:
    base_path  = os.path.join(CONFIG_DIR, "base-service-config.json")
    niche_path = os.path.join(CONFIG_DIR, "niches", f"{niche}.json")

    with open(base_path, encoding="utf-8") as f:
        cfg = json.load(f)

    if os.path.exists(niche_path):
        with open(niche_path, encoding="utf-8") as f:
            niche_cfg = json.load(f)
        cfg = _deep_merge(cfg, niche_cfg)
    else:
        print(f"  [WARN] No niche config for '{niche}', using base only.", file=sys.stderr)

    return cfg


def _extract_profile_fields(profile: dict, niche: str) -> dict:
    name        = profile.get("businessName") or profile.get("business_name") or "Local Business"
    city        = profile.get("city") or "Your City"
    state       = profile.get("state") or ""
    county      = profile.get("county") or ""
    phone_raw   = (profile.get("contact") or {}).get("phone") or profile.get("phone") or ""
    phone       = _phone_format(phone_raw) or "(555) 555-0000"
    phone_e164  = _phone_strip(phone_raw) or "+15555550000"
    email       = (profile.get("contact") or {}).get("email") or profile.get("email") or ""
    website     = (profile.get("contact") or {}).get("website") or profile.get("website") or ""
    rating      = profile.get("rating") or 5.0
    review_count = int(profile.get("reviewCount") or 0)
    years       = profile.get("yearsInBusiness") or "10+"
    license_str = profile.get("license") or ""
    license_num = profile.get("licenseNumber") or ""
    description = profile.get("description") or ""

    raw_areas   = profile.get("serviceAreas") or []
    service_areas = [a for a in raw_areas if a and a != state and len(a) > 2]
    if not service_areas:
        service_areas = [city]

    city_state = f"{city}, {state}".strip(", ") if state else city
    city_state_county = (
        f"{city}, {county}, {state}".strip(", ")
        if county and county.lower() != city.lower()
        else city_state
    )

    year       = datetime.datetime.now().year
    name_short = re.sub(r'[^A-Z0-9 ]', '', name.upper()).strip()[:12]
    niche_label = niche.replace("-", " ").title()

    return {
        "name": name, "name_short": name_short, "niche": niche, "niche_label": niche_label,
        "city": city, "state": state, "county": county,
        "city_state": city_state, "city_state_county": city_state_county,
        "phone": phone_e164, "phone_fmt": phone,
        "email": email, "website": website,
        "rating": rating, "review_count": review_count,
        "years": years, "license": license_str, "license_num": license_num,
        "service_areas": service_areas, "description": description, "year": year,
    }


def _apply_business_fields(cfg: dict, p: dict) -> dict:
    areas = p["service_areas"]
    niche_label = p["niche_label"]

    cfg["company"].update({
        "name":             p["name"],
        "nameShort":        p["name_short"],
        "tagline":          f"Your trusted {niche_label.lower()} contractor in {p['city_state']}.",
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
        "homeTitle":       f"{p['name']} — {niche_label} in {p['city_state']}",
        "homeDescription": (
            f"Trusted {niche_label.lower()} serving {p['city_state_county']}. "
            f"Free estimates, licensed & insured. Call {p['phone_fmt']} today."
        )[:155],
    })

    cfg["announcement"]["suffix"] = f"available this week in {p['city']}."

    cfg["hero"]["rating"]      = str(p["rating"])
    cfg["hero"]["reviewCount"] = f"{p['review_count']}+" if p["review_count"] else "50+"
    cfg["hero"]["subtitle"]    = (
        f"Your trusted {niche_label.lower()} in {p['city_state']} — "
        f"licensed, insured, and backed by a satisfaction guarantee."
    )
    for s in cfg["hero"]["stats"]:
        if "Years" in s.get("label", ""):
            s["label"] = f"Years in {p['city']}"
        if s.get("label") == "Google Rating":
            s["stat"] = f"{p['rating']}★"

    cfg["howItWorks"]["badgeStat"]  = p["years"]
    cfg["howItWorks"]["badgeLabel"] = f"Years in {p['city']}"

    for i, proj in enumerate(cfg["gallery"].get("projects", [])):
        proj["neighborhood"] = areas[i] if i < len(areas) else p["city"]
    cfg["gallery"]["h2"] = f"Recent jobs in {p['city']}."

    reviews = cfg.get("testimonials", {}).get("reviews", [])
    if not reviews:
        reviews = [
            {"name": "James T.", "initials": "JT",
             "text": f"Great service and very professional. Highly recommend to anyone in {p['city']}."},
            {"name": "Sandra M.", "initials": "SM",
             "text": "Fast, clean, and fairly priced. They showed up when they said they would."},
            {"name": "David R.", "initials": "DR",
             "text": "Called in the morning, problem was fixed by afternoon. No surprises on the bill."},
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
        f"Get your free estimate today. No obligation, no pressure — "
        f"just an honest assessment from {p['city']}'s most trusted {p['niche_label'].lower()} team."
    )

    cfg["footer"]["tagline"] = (
        f"Your trusted {p['niche_label'].lower()} in {p['city_state']}. "
        f"Licensed, insured, satisfaction guaranteed."
    )
    cfg["footer"]["serviceAreas"] = [{"label": a, "href": "#contact"} for a in areas[:8]]

    return cfg


def _fallback_config(profile: dict, niche: str) -> dict:
    p   = _extract_profile_fields(profile, niche)
    cfg = _load_layered_config(niche)
    return _apply_business_fields(cfg, p)


def _ai_config(profile: dict, niche: str) -> dict:
    p   = _extract_profile_fields(profile, niche)
    cfg = _load_layered_config(niche)
    cfg = _apply_business_fields(cfg, p)

    client    = anthropic.Anthropic()
    areas_str = ", ".join(p["service_areas"][:6])

    prompt = f"""Generate creative marketing copy for a {p['niche_label']} company website. Return ONLY valid JSON.

Business:
- Name: {p['name']}
- Niche: {p['niche_label']}
- Location: {p['city_state_county']}
- Phone: {p['phone_fmt']}
- Rating: {p['rating']} ({p['review_count']} reviews)
- Service areas: {areas_str}
- Years in business: {p['years']}
- Description: {p['description'] or p['niche_label'] + ' contractor'}

Fill ONLY these fields:

{{
  "company": {{
    "tagline": "<one punchy sentence — no city name>"
  }},
  "seo": {{
    "homeTitle": "<≤60 chars, include city + {p['niche_label'].lower()}>",
    "homeDescription": "<≤155 chars, call to action, include city>"
  }},
  "announcement": {{
    "text": "<short urgent hook for {p['niche_label'].lower()}>",
    "suffix": "available this week in {p['city']}."
  }},
  "hero": {{
    "h1": ["<4-5 word line>", "<highlighted phrase>", "<4-5 word line>"],
    "subtitle": "<2 sentences — mention {p['city_state']}, key services>"
  }},
  "testimonials": {{
    "reviews": [
      {{"name": "James T.", "location": "{p['service_areas'][0] if p['service_areas'] else p['city']}", "text": "<2-3 sentence review about {p['niche_label'].lower()} work in {p['city']}>", "initials": "JT"}},
      {{"name": "Sandra M.", "location": "{p['service_areas'][1] if len(p['service_areas']) > 1 else p['city']}", "text": "<2-3 sentence review about service quality>", "initials": "SM"}},
      {{"name": "David R.", "location": "{p['service_areas'][2] if len(p['service_areas']) > 2 else p['city']}", "text": "<2-3 sentence review about speed and price>", "initials": "DR"}}
    ]
  }},
  "cta": {{
    "h2": "<urgent 8-12 word headline about {p['niche_label'].lower()} problem>",
    "subtext": "<2 sentences — free estimate, no obligation, mention {p['city']}>"
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
    return _deep_merge(cfg, json.loads(text))


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def generate_site(profile: dict, output_dir: str, niche: str) -> dict:
    print(f"  -> Generating {niche} site for: {profile.get('businessName', '?')}")

    if not os.path.isdir(TEMPLATE_DIR):
        return {"error": f"Template not found at {TEMPLATE_DIR}"}

    if ANTHROPIC_AVAILABLE:
        try:
            print(f"  -> Generating creative copy with Haiku...")
            site_config = _ai_config(profile, niche)
            print(f"  -> Content generated.")
        except Exception as e:
            print(f"  [WARN] AI config failed: {e}. Using fallback.", file=sys.stderr)
            site_config = _fallback_config(profile, niche)
    else:
        print(f"  [WARN] anthropic not installed, using fallback config.", file=sys.stderr)
        site_config = _fallback_config(profile, niche)

    site_config["template"] = f"{niche}-v1"
    site_config["niche"]    = niche

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    shutil.copytree(TEMPLATE_DIR, output_dir)

    config_path = os.path.join(output_dir, "site-config.json")
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(site_config, f, indent=2, ensure_ascii=False)
    print(f"  -> site-config.json written")

    index_path = os.path.join(output_dir, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    seo         = site_config.get("seo", {})
    company     = site_config.get("company", {})
    title       = seo.get("homeTitle") or company.get("name", f"{niche.title()} Contractor")
    description = seo.get("homeDescription", "")

    html = re.sub(r'<title>[^<]*</title>', f'<title>{title}</title>', html)
    injection = (
        f'    <meta name="description" content="{description}">\n'
        f'    <meta property="og:title" content="{title}">\n'
        f'    <meta property="og:description" content="{description}">\n'
        f'    <meta property="og:type" content="website">\n'
        f'    <script>window.SITE_CONFIG={json.dumps(site_config, separators=(",", ":"), ensure_ascii=False)};</script>'
    )
    html = html.replace("</head>", f"{injection}\n  </head>")

    # Normalize absolute asset paths to relative so the site works locally and on Vercel
    html = re.sub(r'(src|href)="/assets/', r'\1="./assets/', html)
    html = re.sub(r'(href)="/favicon', r'\1="./favicon', html)

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  -> Site written to {output_dir}")
    return {
        "status":      "ok",
        "output_dir":  output_dir,
        "title":       title,
        "config_file": config_path,
        "template":    f"{niche}-v1",
    }


def detect_niche(profile: dict) -> str:
    text = " ".join([
        (profile.get("primaryCategory") or ""),
        (profile.get("niche") or ""),
        " ".join(profile.get("categories") or []),
    ]).lower()
    for niche, keywords in NICHE_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return niche
    return "general"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generic service site factory.")
    parser.add_argument("profile_json", help="Path to enriched business profile JSON")
    parser.add_argument("--output-dir", required=True, help="Directory to write the generated site into")
    parser.add_argument("--niche", default=None, help="Niche override (e.g. plumbing, hvac, lawn-care)")
    args = parser.parse_args()

    if not os.path.exists(args.profile_json):
        print(json.dumps({"error": f"Profile not found: {args.profile_json}"}))
        sys.exit(1)

    with open(args.profile_json) as f:
        profile = json.load(f)

    niche = args.niche or detect_niche(profile)
    result = generate_site(profile, args.output_dir, niche)
    print(json.dumps(result, indent=2))
    if result.get("error"):
        sys.exit(1)
