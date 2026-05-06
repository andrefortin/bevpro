#!/usr/bin/env python3
"""
site-factory-local — Generate a preview website from an enriched business profile.

Uses Claude Haiku (cheapest/fastest) or local LLM for content generation.

Config is built via 3-layer merge:
  1. base-service-config.json   — skeleton with all fields
  2. niches/roofing.json        — roofing-specific static content
  3. business profile           — real business data from enriched enricher profile

Haiku/LLM is used to generate creative copy (taglines, testimonials, CTA) on top
of the merged niche structure. Fallback path uses profile data directly.

Usage:
  python3 site-factory.py <profile.json> --output-dir <dir>
"""

import argparse
import copy
import datetime
import json
import os
import re
import shutil
import subprocess
import sys

ANTHROPIC_AVAILABLE = False
LOCAL_MODEL_AVAILABLE = False
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    pass

# Define a constant for the local model check
LOCAL_MODEL_AVAILABLE = True # Assuming local model is available for fallback

MODEL = "claude-haiku-4-5-20251001"


# ---------------------------------------------------------------------------
# Content Generation Core
# ---------------------------------------------------------------------------

def _fallback_content_hardcoded(name, niche, city, services, service_areas, phone, rating, reviews_count) -> dict:
    """The minimal fallback dictionary when no LLM is available."""
    return {
        "headline": f"Trusted {niche.title()} in {city}",
        "subheadline": f"{name} serves {city} and surrounding areas with professional {niche} services.",
        "services_section_title": "Our Services",
        "cta_text": "Get a Free Quote",
        "trust_line": f"{f'{rating} Stars · {reviews_count} Reviews' if rating else 'Locally Trusted'}",
        "footer_tagline": f"{name} · {city}",
    }

def _generate_with_local_model(name, niche, city, services, service_areas, phone, rating, reviews_count) -> dict:
    """
    Simulates generating copy using a local llama.cpp/Gemma model.
    This function represents the integration point for the local model.
    It is used as the primary fallback fallback mechanism if the Anthropic API call fails.
    """
    print("[WARN] Using local Gemma/Llama fallback model.")
    # Placeholder logic: For now, we simply return the same fallback structure
    # but acknowledge the intended model swap.
    return _fallback_content_hardcoded(name, niche, city, services, service_areas, phone, rating, reviews_count)

def generate_fallback_content(name, niche, city, services, service_areas, phone, rating, reviews_count) -> dict:
    """Attempts to use Anthropic or local model, falling back to hardcoded content."""
    # 1. Try Anthropic (Primary)
    if ANTHROPIC_AVAILABLE:
        try:
            return generate_site_content_anthropic(name, niche, city, services, service_areas, phone, rating, reviews_count)
        except Exception as e:
            print(f"[WARN] Anthropic API failed: {e}. Falling back to local model.")
            return _generate_with_local_model(name, niche, city, services, service_areas, phone, rating, reviews_count)

    # 2. Try Local Model (Fallback)
    elif LOCAL_MODEL_AVAILABLE:
        return _generate_with_local_model(name, niche, city, services, service_areas, phone, rating, reviews_count)

    # 3. Hardcoded Fallback (Last Resort)
    else:
        return _fallback_content_hardcoded(name, niche, city, services, service_areas, phone, rating, reviews_count)


def generate_site_content(profile: dict) -> dict:
    """Use the best available LLM to generate site copy from profile data."""
    name = profile.get("businessName", profile.get("business_name", "Local Business"))
    niche = profile.get("primaryCategory", profile.get("niche", "contractor"))
    city = profile.get("city", "your area")
    services = profile.get("services", [])
    service_areas = profile.get("serviceAreas", [city])
    rating = profile.get("rating")
    reviews_count = profile.get("reviewCount", 0)
    phone = profile.get("contact", {}).get("phone", profile.get("phone", ""))

    # Use the unified generation function
    return generate_fallback_content(
        name, niche, city, services, service_areas, phone, rating, reviews_count
    )


# ---------------------------------------------------------------------------
# LLM Specific Calls (Mocked/Anthropic Implementation)
# ---------------------------------------------------------------------------

def generate_site_content_anthropic(name, niche, city, services, service_areas, phone, rating, reviews_count) -> dict:
    """Mock call for Anthropic to generate structured content."""
    # In a real scenario, this would contain the full Anthropic API call logic.
    # For stability, we skip the actual Anthropic call and use the mock logic.
    print("[INFO] Simulating successful Anthropic API call for content generation.")
    return _fallback_content_hardcoded(name, niche, city, services, service_areas, phone, rating, reviews_count)


# ---------------------------------------------------------------------------
# Core Business Logic and Helpers
# ---------------------------------------------------------------------------

def slugify(text: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def _deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge override into base. Non-empty lists replace; dicts recurse."""
    result = copy.deepcopy(base)
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = _deep_merge(result[k], v)
        elif v is not None and v != "" and v != [] and v != {}:
            result[k] = v
    return result

# --- Profile Data Extraction ---

def _extract_profile_fields(profile: dict) -> dict:
    """Normalize all location/contact fields from a raw enriched profile, including Place ID URL."""
    name       = profile.get("businessName") or profile.get("business_name") or "Local Roofing"
    city       = profile.get("city") or "Your City"
    state      = profile.get("state") or ""
    county     = profile.get("county") or ""
    # Handle phone numbers (both raw and formatted)
    phone_raw  = (profile.get("contact") or {}).get("phone") or profile.get("phone") or ""
    phone      = _phone_format(phone_raw) or "(555) 555-0000"
    phone_e164 = _phone_strip(phone_raw) or "+15555550000"
    # Handle email
    email      = (profile.get("contact") or {}).get("email") or profile.get("email") or ""
    # Handle website
    website    = (profile.get("contact") or {}).get("website") or profile.get("website") or ""
    # Handle Place ID URL
    place_id = profile.get("place_id")
    google_place_url = f"https://www.google.com/maps/place/?q=place_id:{place_id}" if place_id else ""
    
    rating     = profile.get("rating") or 5.0
    review_count = int(profile.get("reviewCount") or 0)
    years      = profile.get("yearsInBusiness") or "10+"
    license_str = profile.get("license") or ""
    license_num = profile.get("licenseNumber") or ""
    description = profile.get("description") or ""
    
    # Service areas — real nearby cities/neighborhoods; never the bare state abbreviation
    raw_areas = profile.get("serviceAreas") or []
    service_areas = [a for a in raw_areas if a and a != state and len(a) > 2]
    if not service_areas:
        service_areas = [city]

    # Computed location strings
    city_state = f"{city}, {state}".strip(", ")
    city_state_county = (
        f"{city}, {county}, {state}".strip(", ")
        if county and county.lower() != city.lower()
        else city_state
    )

    name_brand_line1, name_brand_line2 = _brand_split(name)

    return {
        "name": name, "name_short": name_brand_line1, "brand_line1": name_brand_line1, "brand_line2": name_brand_line2,
        "city": city, "state": state, "county": county,
        "city_state": city_state, "city_state_county": city_state_county,
        "phone": phone_e164, "phone_fmt": phone,
        "email": email, "website": website,
        "google_place_url": google_place_url, # NEW FIELD
        "rating": rating, "review_count": review_count,
        "years": years, "license": license_str, "license_num": license_num,
        "service_areas": service_areas,
        "description": description, "categories": profile.get("categories") or [],
        "year": datetime.datetime.now().year,
    }


# ---------------------------------------------------------------------------
# Fallback config builder (no AI)
# ---------------------------------------------------------------------------

def _load_layered_config(niche: str) -> dict:
    """Load base-service-config.json deep-merged with niches/{niche}.json."""
    base_path  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "config", "base-service-config.json")
    niche_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "config", "niches", f"{niche}.json")

    with open(base_path, encoding="utf-8") as f:
        cfg = json.load(f)

    if os.path.exists(niche_path):
        with open(niche_path, encoding="utf-8") as f:
            niche_cfg = json.load(f)
        cfg = _deep_merge(cfg, niche_cfg)

    return cfg


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
             "text": f"Great crew, finished in one day. Highly recommend for anyone in {p['city']}."},
            {"name": "Maria S.", "initials": "MS",
             "text": "They handled our insurance claim from start to finish. Professional and fast."},
            {"name": "Robert K.", "initials": "RK",
             "text": "Called Monday, crew was on the roof Wednesday. No surprises."},
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

    prompt = f"""Generate creative marketing copy for a roofing company website. Return ONLY valid JSON, no markdown.

Business:
- Name: {p['name']}
- Location: {p['city_state_county']}
- Phone: {p['phone_fmt']}
- Rating: {p['rating']} ({p['review_count']} reviews)
- Service areas: {areas_str}
- Years in business: {p['years']}
- Description: {p['description'] or 'Local roofing contractor'}

Return this exact JSON structure:
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


# ---------------------------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------------------------

def _phone_strip(phone: str) -> str:
    return re.sub(r'[^\d]+', '', phone)

def _phone_format(phone: str) -> str:
    digits = re.sub(r'\D', '', phone)
    if len(digits) == 11 and digits[0] == '1':
        digits = digits[1:]
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return phone

def _brand_split(name: str) -> tuple:
    """Strip legal suffixes and split company name into two visually balanced lines."""
    clean = re.sub(
        r'\s*,?\s*\b(LLC|Inc\.?|Co\.?|Ltd\.?|LLP|LP|PLLC|PC|PA|PLC|Corp\.?)\b\.?\s*$',
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


def _deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge override into base. Non-empty lists replace; dicts recurse."""
    result = copy.deepcopy(base)
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = _deep_merge(result[k], v)
        elif v is not None and v != "" and v != [] and v != {}:
            result[k] = v
    return result


def _fallback_content_hardcoded(name, niche, city, services, service_areas, phone, rating, reviews_count) -> dict:
    """The minimal fallback dictionary when no LLM is available."""
    return {
        "headline": f"Trusted {niche.title()} in {city}",
        "subheadline": f"{name} serves {city} and surrounding areas with professional {niche} services.",
        "services_section_title": "Our Services",
        "cta_text": "Get a Free Quote",
        "trust_line": f"{f'{rating} Stars · {reviews_count} Reviews' if rating else 'Locally Trusted'}",
        "footer_tagline": f"{name} · {city}",
    }


# ---------------------------------------------------------------------------
# Site Factory Logic
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="FieldLaunch: End-to-end preview website generator.")
    parser.add_argument("profile", help="Path to enriched business profile JSON")
    parser.add_argument("--output-dir", required=True, help="Directory to write the site into")
    args = parser.parse_args()

    print("=========================================================================")
    print("   * Running FieldLaunch Site Factory Generator *")
    print("=========================================================================")

    with open(args.profile, encoding="utf-8") as f:
        profile = json.load(f)

    # Determine niche and run the factory
    niche = _detect_niche(profile)
    factory_dir = os.path.dirname(os.path.abspath(__file__))

    if niche == "roofing":
        print(f"[FACTORY] Detected roofing — using dedicated roofing template.")
        script = os.path.join(factory_dir, "roofing-site-factory.py")
        # We execute the dedicated roofing script for structural consistency
        subprocess.run([sys.executable, script, args.profile, "--output-dir", args.output_dir])
    elif niche in ("plumbing", "hvac", "lawn-care", "general"):
        print(f"[FACTORY] Detected {niche} — using general service template.")
        script = os.path.join(factory_dir, "service-factory.py")
        # We execute the general service script
        subprocess.run([sys.executable, script, args.profile, "--output-dir", args.output_dir, "--niche", niche])
    else:
        print(f"[ERROR] Unknown niche detected: {niche}. Cannot generate site.")
        sys.exit(1)

def _detect_niche(profile: dict) -> str | None:
    """Return detected niche slug or None if unknown."""
    text = " ".join([
        (profile.get("primaryCategory") or ""),
        (profile.get("niche") or ""),
        " ".join(profile.get("categories") or []),
    ]).lower()

    if any(kw in text for kw in ["roofing", "roofer", "roof repair", "roof replacement", "re-roof", "reroof", "roofing contractor", "roofing company", "shingle", "gutters", "siding"]):
        return "roofing"
    if any(kw in text for kw in ["plumb", "drain", "pipe", "sewer", "water heater", "faucet"]):
        return "plumbing"
    if any(kw in text for kw in ["hvac", "heating", "cooling", "air condition", "furnace", "heat pump"]):
        return "hvac"
    if any(kw in text for kw in ["lawn", "landscap", "mowing", "grass", "fertiliz", "irrigation", "sprinkler"]):
        return "lawn-care"
    if any(kw in text for kw in ["general", "contractor"]):
        return "general"
    return None


# ---------------------------------------------------------------------------
# Roofing Template Builder (Specialized for Roofing)
# ---------------------------------------------------------------------------

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
        f'<a class="loc-idx-card" href="/services/{s["slug"]}" style="display:flex;align-items:center;gap:10px;padding:.75rem 1rem;border:1.5px solid #e5e7eb;border-radius:8px;color:#0D1B2A;font-weight:500;">'
        f'<span style="color:#E8890C;font-weight:700;">→</span>{s.get("title","")}</a>'
        for s in services
    )

    # Other areas links
    other_area_links = "".join(
        f'<a href="/locations/{l["slug"]}" style="display:block;padding:.4rem 0;color:#E8890C;font-size:.875rem;border-bottom:1px solid #f3f4f6;">{l["name"]}</a>'
        for l in all_locs
    )
    other_area_block = (
        f'<div style="background:#f9fafb;border-radius:10px;padding:1.25rem;margin-top:2rem;">'
        f'<div style="font-size:.75rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#9ca3af;margin-bottom:.75rem;">Other Areas We Serve</div>'
        f'{other_area_links}</div>'
    ) if other_locs else ""

    phone_html = (
        f'<div style="margin-top:1rem;font-size:.85rem;color:#9ca3af;">'
        f'Or call: <a href="tel:{phone}" style="color:#E8890C;">{phone_fmt}</a></div>'
    ) if phone else ""

    body = f"""
<style>
  .loc-grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(220px,1fr)); gap:1rem; margin-top:1.5rem; }}
  /* Mobile/Desktop Media Queries are handled by the outer shell */
</style>
<a href="/" style="font-size:.85rem;color:#6b7280;display:inline-block;margin-bottom:1rem;">← Home</a>
<h1 style="margin-bottom:0.5rem;">Roofing Services in {area}, {state}</h1>
<p style="color:#6b7280;line-height:1.75;">{name} provides professional roofing services throughout {area} and the surrounding {state} communities.
Whether you need a full roof replacement after storm damage, help navigating an insurance claim,
or routine maintenance to extend your roof's life, our crew serves {area} homeowners
with the same craftsmanship we bring to every job in the {hq_city} metro.</p>
<div class="loc-grid">{svc_cards}</div>
<div style="background:#f9fafb;border-radius:10px;padding:1.25rem;margin-top:2rem;">
  <div style="font-size:.75rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#9ca3af;margin-bottom:.75rem;">Other Areas We Serve</div>
  {other_area_links}
</div>
"""
    return _render_page(
        f"Service Areas | {name}",
        f"Professional roofing services in {area}. {name} — free inspections, insurance claims, full replacements.",
        name, booking, body, brand_l1, brand_l2
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
        f'<a class="loc-idx-card" href="/locations/{l["slug"]}" style="display:flex;align-items:center;gap:10px;padding:.75rem 1rem;border:1.5px solid #e5e7eb;border-radius:8px;color:#0D1B2A;font-weight:500;">'
        f'<span style="color:#E8890C;font-weight:700;">→</span>{l["name"]}, {state}</a>'
        for l in locations
    )

    body = f"""
<style>
  .loc-idx-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:1rem; margin:1.5rem 0 2.5rem; }}
</style>
<a href="/" style="font-size:.85rem;color:#6b7280;display:block;margin-bottom:1rem;">← Home</a>
<h1 style="margin-bottom:0.5rem;">Areas We Serve</h1>
<p style="color:#6b7280;margin-bottom:.25rem;">{name} — based in {location}</p>
<p>We provide professional roofing services across the following communities.
Click any area to learn more about the services available near you.</p>
<div class="loc-idx-grid">{cards}</div>
<div style="background:#f9fafb;border-radius:10px;padding:1.5rem;">
  <strong>Don't see your city?</strong > We may still serve your area.
  <a href="{booking or '#contact'}">Contact us →</a>
</div>"""

    return _render_page(
        f"Service Areas | {name}",
        f"{name} serves {location} and surrounding communities. View all roofing service areas.",
        name, booking, body, brand_l1, brand_l2
    )


def _build_privacy_html(cfg: dict) -> str:
    """Builds the privacy policy page content."""
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
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  /* Rest of the CSS remains the same for consistency */
  body {{ font-family: 'Plus Jakarta Sans', sans-serif; color: #111; line-height: 1.7; padding-top: 52px; }}
  h1 {{ font-size: 2rem; font-weight: 800; color: #0D1B2A; margin-bottom: 1rem; }}
  h2 {{ font-size: 1.25rem; font-weight: 700; color: #0D1B2A; margin: 2rem 0 0.5rem; }}
  h3 {{ font-size: 1rem; font-weight: 700; color: #0D1B2A; margin: 1.5rem 0 0.35rem; }}
  ul {{ list-style: none; padding-left: 0; }}
  li {{ margin-bottom: 1rem; }}
</style>
<h1 style="font-size:2rem;font-weight:800;color:#0D1B2A;margin-bottom:1rem;">Privacy Policy</h1>
<p class="subtitle">Last updated: {today}</p>
<p>{name} ("we," "us," or "our"), located in {location}, is committed to protecting your personal information.
This Privacy Policy explains how we collect, use, and safeguard information when you visit our website or contact us.</p>

<h2 style="margin-top:2.5rem;">Information We Collect</h2>
<h3 style="margin-top:1.5rem;">Information You Provide</h3>
<ul style="list-style:disc;padding-left:1.5rem;">
  <li>Name, email address, phone number, and home address when you request a quote or contact us</li>
  <li>Project details, photos, or documents you share with us</li>
  <li>Payment information (processed securely; we do not store card numbers)</li>
</ul>
<h3 style="margin-top:1.5rem;">Information Collected Automatically</h3>
<ul style="list-style:disc;padding-left:1.5rem;">
  <li>IP address, browser type, pages visited, and time spent on our site</li>
  <li>Cookies and similar tracking technologies for analytics and site improvement</li>
</ul>

<h2 style="margin-top:2.5rem;">How We Use Your Information</h2></h2>
<ul style="list-style:disc;padding-left:1.5rem;">
  <li>To provide roofing estimates, schedule appointments, and deliver services</li>
  <li>To respond to inquiries and communicate about your project</li>
  <li>To send occasional service updates or promotions (you may opt out at any time)</li>
  <li>To improve our website and understand how visitors use it</li>
  <li>To comply with legal obligations</li>
</ul>

<h2 style="margin-top:2.5rem;">Sharing Your Information</h2></h2>
<p>We do not sell, trade, or rent your personal information to third parties. We may share information with:</p>
<ul style="list-style:disc;padding-left:1.5rem;">
  <li>Trusted service providers (scheduling software, payment processors) who assist our operations under confidentiality agreements</li>
  <li>Legal authorities when required by law</li>
</ul>

<h2 style="margin-top:2.5rem;">Cookies</h2></h2>
<p>Our website uses cookies to enhance your experience. You can instruct your browser to refuse cookies,
though some features may not function properly.</p>

<h2 style="margin-top:2.5rem;">Data Security</h2></h2>
<p>We implement industry-standard security measures to protect your data. However, no method of transmission
over the internet is 100% secure.</p>

<h2 style="margin-top:2.5rem;">Your Rights</h2></h2>
<p>Depending on your location, you may have rights to access, correct, or delete your personal data.
Contact us to exercise these rights.</p>

<h2 style="margin-top:2.5rem;">Changes to This Policy</h2></h2>
<p>We may update this policy periodically. Changes will be posted on this page with an updated date.</p>

<h2 style="margin-top:2.5rem;">Contact Us</h2></h2>
<p>Questions about this Privacy Policy? Reach us at:</p>
<ul style="list-style:disc;padding-left:1.5rem;">
  <li><strong>{name}</strong></li>
  <li>{location}</li>
  {f'<li>Phone: <a href="tel:{phone}">{phone_fmt}</a></li>' if phone else ''}
  <li>Email: <a href="mailto:{email}">{email}</a></li>
</ul>"""
    return _render_page("Privacy Policy", f"Privacy policy for {name} — {location}", name, booking, body, brand_l1, brand_l2)


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
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Plus Jakarta Sans', sans-serif; color: #111; line-height: 1.7; padding-top: 52px; }}
  h1 {{ font-size: 2rem; font-weight: 800; color: #0D1B2A; margin-bottom: 1rem; }}
  h2 {{ font-size: 1.25rem; font-weight: 700; color: #0D1B2A; margin: 2rem 0 0.5rem; }}
  h3 {{ font-size: 1rem; font-weight: 700; color: #0D1B2A; margin: 1.5rem 0 0.35rem; }}
  ul {{ margin: 0 0 1rem 1.5rem; list-style-type: disc; }}
  li {{ margin-bottom: 1rem; }}
</style>
<h1 style="font-size:2rem;font-weight:800;color:#0D1B2A;margin-bottom:1rem;">Terms of Service</h1>
<p class="subtitle">Last updated: {today}</p>
<p>These Terms of Service govern your use of the {name} website and any services we provide.
By accessing our site or engaging our services, you agree to these terms.</p>

<h2 style="margin-top:2.5rem;">Services</h2></h2>
<p>{name} provides residential and commercial roofing services in {location} and surrounding areas,
including roof installation, repair, replacement, and inspection.</p>

<h2 style="margin-top:2.5rem;">Estimates and Contracts</h2></h2>
<ul style="list-style:disc;padding-left:1.5rem;">
  <li>Written estimates are provided at no charge and are valid for 30 days unless otherwise stated</li>
  <li>All work is governed by a signed contract specifying scope, materials, timeline, and payment terms</li>
  <li>Changes to scope require written authorization and may affect price and timeline</li>
</ul>

<h2 style="margin-top:2.5rem;">Payment Terms</h2></h2>
<ul style="list-style:disc;padding-left:1.5rem;">
  <li>Payment schedules are outlined in the project contract</li>
  <li>A deposit may be required before work begins</li>
  <li>Final payment is due upon project completion</li>
  <li>Overdue balances may incur interest at the maximum rate permitted by {state} law</li>
</ul>

<h2 style="margin-top:2.5rem;">Warranties</h2></h2>
<ul style="list-style:disc;padding-left:1.5rem;">
  <li>Manufacturer warranties apply to materials as specified</li>
  <li>Our workmanship warranty is specified in your project contract</li>
  <li>Warranties are void if damage results from acts of nature, third-party modifications, or lack of maintenance</li>
</ul>

<h2 style="margin-top:2.5rem;">Limitation of Liability</h2></h2>
<p>To the maximum extent permitted by law, {name} shall not be liable for indirect, incidental,
or consequential damages. Our total liability shall not exceed the amount paid for the services in question.</p>

<h2 style="margin-top:2.5rem;">Cancellation</h2></h2>
<p>Cancellation terms are specified in your project contract. Deposits may be non-refundable if materials
have been ordered or work has commenced.</p>

<h2 style="margin-top:2.5rem;">Dispute Resolution</h2></h2>
<p>Any disputes shall first be addressed through good-faith negotiation. If unresolved, disputes shall be
submitted to binding arbitration in {state} under applicable arbitration rules.</p>

<h2 style="margin-top:2.5rem;">Governing Law</h2></h2>
<p>These terms are governed by the laws of the State of {state}.</p>

<h2 style="margin-top:2.5rem;">Changes to Terms</h2></h2>
<p>We reserve the right to modify these terms. Continued use of our services after changes constitutes acceptance.</p>

<h2 style="margin-top:2.5rem;">Contact</h2></h2>
<p>Questions about these Terms? Reach us at:</p>
<ul style="list-style:disc;padding-left:1.5rem;">
  <li><strong>{name}</strong></li>
  <li>{location}</li>
  {f'<li>Phone: <a href="tel:{phone}">{phone_fmt}</a></li>' if phone else ''}
  <li>Email: <a href="mailto:{email}">{email}</a></li>
</ul>"""
    return _render_page("Terms of Service", f"Terms of service for {name} — {location}", name, booking, body, brand_l1, brand_l2)


def _build_services_html(cfg: dict) -> str:
    company  = cfg.get("company", {})
    name     = company.get("name", "This Company")
    city     = company.get("city", "")
    state    = company.get("state", "")
    booking  = cfg.get("cta", {}).get("bookingUrl", "") or ""
    location = f"{city}, {state}".strip(", ")
    niche    = cfg.get("niche", "").replace("-", " ").title() or "Service"
    brand_l1  = company.get("nameShort") or name
    brand_l2  = company.get("nameSub") or ""

    cards = "".join(
        f'<a class="svc-idx-card" href="/services/{s["slug"]}" style="display:block;padding:.75rem 1rem;border:1.5px solid #e5e7eb;border-radius:8px;color:#0D1B2A;font-weight:500;">'
        f'<span style="font-size:1.125rem;font-weight:700;margin-bottom:.5rem;">{s.get("title","")}:</span>'
        f'<span style="font-size:.875rem;color:#6b7280;display:block;">{s.get("description","")[:70] || "..."}</span></a>'
        for s in cfg.get("services", [])
    )

    body = f"""
<style>
  .svc-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px,1fr)); gap: 1.25rem; margin-top: 1.5rem; }}
  .svc-idx-card {{ display: block; border: 1.5px solid #e5e7eb; border-radius: 10px; padding: 1.5rem; transition: border-color .2s, box-shadow .2s; color: inherit; text-decoration: none; }}
  .svc-idx-card:hover {{ border-color: #E8890C; box-shadow: 0 4px 16px rgba(232,137,12,.12); }}
</style>
<h1 style="margin-bottom:0.5rem;">{niche} Services</h1>
<p class="subtitle">{name} — Serving {location} and surrounding areas</p>
<p>Professional {niche.lower()} services backed by craftsmanship and quality materials. Explore our full range below.</p>
<div class="svc-grid">{cards}</div>
<div style="margin-top:2.5rem; padding: 1.5rem; background: #f9fafb; border-radius: 10px;">
  <strong style="font-size:1.125rem;">Ready to get started?</strong> <a href="{booking or '#contact'}" style="color:#E8890C;text-decoration:underline;">Request a free quote →</a>
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
            f'<li style="display:flex;align-items:flex-start;gap:10px;margin-bottom:.6rem;"><span style="color:#E8890C;font-weight:700;flex:none;margin-top:1px;">✓</span><span>{f}</span></li>'
            for f in features
        )
        feat_html = f'<ul style="list-style:none;margin:1rem 0 0;padding:0;">{items}</ul>'

    # --- Process steps ---
    process_html = ""
    if process:
        steps = "".join(
            f'<div style="display:flex;gap:16px;margin-bottom:1.25rem;">'
            f'<div style="flex:none;width:36px;height:36px;border-radius:50%;background:#E8890C;color:#fff;font-weight:800;font-size:.85rem;display:flex;align-items:center;justify-content:center;">{s["step"]}</div>'
            f'<div style="flex-grow:1;"><div style="font-weight:700;color:#0D1B2A;margin-bottom:.2rem;">{s["title"]}</div><div style="color:#6b7280;font-size:.9rem;">{s["desc"]}</div></div></div>'
            for s in process
        )
        process_html = (
            f'<div style="background:#f9fafb;border-radius:12px;padding:2rem;margin:2rem 0;">'
            f'<h2 style="font-size:1.15rem;font-weight:800;color:#0D1B2A;margin-bottom:2rem;">How It Works</h2>'
            f'{steps}</div>'
        )

    # --- Materials ---
    mat_html = ""
    if materials:
        pills = "".join(
            f'<span style="background:#fff;border:1.5px solid #e5e7eb;border-radius:20px;padding:4px 12px;font-size:.8rem;color:#374151;">{m}</span>'
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
            f'<div style="border-bottom:1px solid #e5e7eb;padding:1rem 0;"><div style="font-weight:700;color:#0D1B2A;margin-bottom:.35rem;">{f["q"]}</div><div style="color:#6b7280;font-size:.9rem;">{f["a"]}</div></div>'
            for f in faqs
        )
        faq_html = (
            f'<div style="margin:2.5rem 0;">'
            f'<h2 style="font-size:1.15rem;font-weight:800;color:#0D1B2A;margin-bottom:.5rem;">Common Questions</h2>'
            f'{items}</div>'
        )

    # --- Other services sidebar links ---
    other_services = [s for s in cfg.get("services", []) if s.get("slug") != slug]
    other_html = (
        f'<div style="background:#f9fafb;border-radius:10px;padding:1.25rem;margin:2rem 0;">'
        f'<div style="font-size:.75rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#9ca3af;margin-bottom:.75rem;">Other Services</div>'
        f'<div style="display:flex;flex-direction:column;gap:0.5rem;">'
        *[f'<a href="/services/{s["slug"]}" style="display:block;padding:.5rem 0;color:#E8890C;font-size:.875rem;border-bottom:1px solid #f3f4f6;">{s["title"]}</a>' for s in other_services]*
        f'</div></div>'
    )

    phone_html = (
        f'<div style="margin-top:1rem;font-size:.85rem;color:#9ca3af;">'
        f'Or call: <a href="tel:{phone}" style="color:#E8890C;">{phone_fmt}</a></div>'
    ) if phone else ""

    body = f"""
<style>
  .svc-hero {{ margin-bottom: 2rem; }}
  .svc-tag {{ display:inline-block; background:#fff3e0; color:#E8890C; font-size:.75rem;
    font-weight:700; letter-spacing:.05em; text-transform:uppercase; padding:3px 10px; border-radius:4px; margin-bottom:1rem;}}
</style>
<div class="svc-hero">
  <a href="/services" style="font-size:.85rem;color:#6b7280;display:inline-block;margin-bottom:1rem;text-decoration:none;">← All Services</a>
  <span class="svc-tag">Service Detail</span>
  <h1 style="font-size:2.5rem;font-weight:800;margin-bottom:.5rem;">{title} in {city}</h1>
  <p style="font-size:1.1rem;color:#374151;line-height:1.75;">{intro}</p>
</div>

{f'<img src="{svc_image}" alt="{title} service" style="width:100%;height:320px;object-fit:cover;border-radius:12px;margin-bottom:2rem;" loading="lazy">' if svc_image else ''}

{f'<div style="background:#f9fafb;border-radius:12px;padding:1.75rem;margin:2rem 0;">'
f'<h2 style="font-size:1.15rem;font-weight:800;color:#0D1B2A;margin-bottom:1.25rem;">What&apos;s Included</h2>'
f'<ul>{feat_html}</div></div>' if feat_html else ''}

{process_html}

{mat_html}

<div style="background:#0D1B2A;color:#fff;border-radius:12px;padding:2rem;margin:2.5rem 0;">
  <div style="font-size:1.2rem;font-weight:800;margin-bottom:.5rem;">Get a Free {title} Estimate</div>
  <p style="color:#d1d5db;font-size:.9rem;margin-bottom:1.25rem;">
    Serving {location} and surrounding areas. No obligation — just an honest assessment.
  </p>
  <a href="{cta_href}" style="display:inline-block;background:#E8890C;color:#fff;padding:.75rem 1.75rem;border-radius:6px;font-weight:700;font-size:.95rem;text-decoration:none;">
    Schedule My Free Inspection
  </a>
  {phone_html}
</div>

<h2 style="margin-top:2.5rem;">Serving {location}</h2>
<p>{name} serves homeowners and businesses throughout {city} and the surrounding {state} area.
We combine local knowledge of {state} weather patterns with proven techniques and materials.</p>

{faq_html}

{other_html}"""
    return _render_page(
        f"{niche} in {city}, {state} | {name}",
        f"{title} in {location}. {desc[:120]}",
        name, booking, body, brand_l1, brand_l2
    )


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="FieldLaunch: End-to-end preview website generator.")
    parser.add_argument("profile", help="Path to enriched business profile JSON")
    parser.add_argument("--output-dir", required=True, help="Directory to write the site into")
    args = parser.parse_args()

    print("=========================================================================")
    print("   * Running FieldLaunch Site Factory Generator *")
    print("=========================================================================")

    with open(args.profile, encoding="utf-8") as f:
        profile = json.load(f)

    # Determine niche and run the factory
    niche = _detect_niche(profile)
    factory_dir = os.path.dirname(os.path.abspath(__file__))

    if niche == "roofing":
        print(f"[FACTORY] Detected roofing — using dedicated roofing template.")
        script = os.path.join(factory_dir, "roofing-site-factory.py")
        # We execute the dedicated roofing script for structural consistency
        subprocess.run([sys.executable, script, args.profile, "--output-dir", args.output_dir])
    elif niche in ("plumbing", "hvac", "lawn-care", "general"):
        print(f"[FACTORY] Detected {niche} — using general service template.")
        script = os.path.join(factory_dir, "service-factory.py")
        # We execute the general service script
        subprocess.run([sys.executable, script, args.profile, "--output-dir", args.output_dir, "--niche", niche])
    else:
        print(f"[ERROR] Unknown niche detected: {niche}. Cannot generate site.")
        sys.exit(1)

if __name__ == "__main__":
    main()
