#!/usr/bin/env python3
"""
site-factory-local — Generate a preview website from an enriched business profile.

Uses Claude Haiku (cheapest/fastest) for content generation.

Usage:
  python3 site-factory.py <profile.json> --output-dir <dir>

Output:
  A static HTML site in the specified directory, ready for Vercel deployment.
"""

import argparse
import json
import os
import sys
import re
import shutil

ANTHROPIC_AVAILABLE = False
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    pass

# Haiku is used for all content generation — fastest and cheapest model
MODEL = "claude-haiku-4-5-20251001"


def slugify(text: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def generate_site_content(profile: dict) -> dict:
    """Use Claude Haiku to generate site copy from profile data."""
    name = profile.get("businessName", profile.get("business_name", "Local Business"))
    niche = profile.get("primaryCategory", profile.get("niche", "contractor"))
    city = profile.get("city", "your area")
    services = profile.get("services", [])
    service_areas = profile.get("serviceAreas", [city])
    rating = profile.get("rating")
    reviews_count = profile.get("reviewsCount", 0)
    description = profile.get("description", "")
    phone = profile.get("contact", {}).get("phone", profile.get("phone", ""))

    if not ANTHROPIC_AVAILABLE:
        return _fallback_content(name, niche, city, services, service_areas, phone, rating, reviews_count)

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    prompt = f"""Generate website copy for a local {niche} business. Return ONLY valid JSON, no markdown.

Business: {name}
Location: {city}
Services: {', '.join(services[:8]) if services else niche + ' services'}
Service areas: {', '.join(service_areas[:5]) if service_areas else city}
Rating: {f"{rating} stars ({reviews_count} reviews)" if rating else "not available"}
Description: {description[:300] if description else ""}

Return this exact JSON structure:
{{
  "headline": "compelling h1 headline under 10 words",
  "subheadline": "supporting line under 20 words, mentions city",
  "services_section_title": "short section title",
  "cta_text": "call to action button text (4-6 words)",
  "trust_line": "short trust statement mentioning experience or reviews",
  "footer_tagline": "short footer tagline"
}}"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        text = response.content[0].text.strip()
        # strip markdown code fences if present
        text = re.sub(r'^```json?\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
        return json.loads(text)
    except (json.JSONDecodeError, IndexError):
        return _fallback_content(name, niche, city, services, service_areas, phone, rating, reviews_count)


def _fallback_content(name, niche, city, services, service_areas, phone, rating, reviews_count) -> dict:
    return {
        "headline": f"Trusted {niche.title()} in {city}",
        "subheadline": f"{name} serves {city} and surrounding areas with professional {niche} services.",
        "services_section_title": "Our Services",
        "cta_text": "Get a Free Quote",
        "trust_line": f"{f'{rating} Stars · {reviews_count} Reviews' if rating else 'Locally Trusted'}",
        "footer_tagline": f"{name} · {city}",
    }


def build_html(profile: dict, copy: dict) -> str:
    name = profile.get("businessName", profile.get("business_name", "Local Business"))
    phone = profile.get("contact", {}).get("phone", profile.get("phone", ""))
    services = profile.get("services", [])
    service_areas = profile.get("serviceAreas", [])
    rating = profile.get("rating")
    reviews_count = profile.get("reviewsCount", 0)
    niche = profile.get("primaryCategory", profile.get("niche", "contractor"))
    color = "#4f46e5"  # indigo — swap per niche later

    services_html = "\n".join(
        f'<li class="service-item">{s}</li>'
        for s in (services[:8] if services else [niche.title() + " Services"])
    )
    areas_html = ", ".join(service_areas[:6]) if service_areas else profile.get("city", "")

    rating_html = ""
    if rating:
        stars = "★" * int(rating) + ("½" if rating % 1 >= 0.5 else "")
        rating_html = f'<div class="rating">{stars} <span>{rating} ({reviews_count} reviews)</span></div>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{name}</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: system-ui, -apple-system, sans-serif; color: #111; }}
    .preview-banner {{
      background: {color}; color: #fff; text-align: center; padding: 10px;
      font-size: 13px; font-weight: 600; letter-spacing: 0.05em;
    }}
    .hero {{
      background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
      color: white; padding: 80px 24px; text-align: center;
    }}
    .hero h1 {{ font-size: clamp(2rem, 5vw, 3.5rem); font-weight: 800; margin-bottom: 16px; }}
    .hero p {{ font-size: 1.2rem; opacity: 0.85; max-width: 600px; margin: 0 auto 32px; }}
    .cta {{ background: {color}; color: white; padding: 16px 40px; border-radius: 8px;
             font-size: 1.1rem; font-weight: 700; text-decoration: none; display: inline-block; }}
    .cta:hover {{ background: #4338ca; }}
    .section {{ padding: 64px 24px; max-width: 900px; margin: 0 auto; }}
    .section h2 {{ font-size: 2rem; font-weight: 700; margin-bottom: 32px; text-align: center; }}
    .services {{ list-style: none; display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px; }}
    .service-item {{
      background: #f5f3ff; border-left: 4px solid {color};
      padding: 16px; border-radius: 8px; font-weight: 500;
    }}
    .trust {{ background: #f9fafb; }}
    .trust-inner {{ padding: 48px 24px; max-width: 700px; margin: 0 auto; text-align: center; }}
    .rating {{ font-size: 1.5rem; color: #f59e0b; margin-bottom: 8px; }}
    .rating span {{ color: #374151; font-size: 1rem; }}
    .areas {{ color: #6b7280; margin-top: 16px; }}
    .contact {{ background: {color}; color: white; padding: 64px 24px; text-align: center; }}
    .contact h2 {{ font-size: 2rem; margin-bottom: 16px; }}
    .phone {{ font-size: 2rem; font-weight: 800; display: block; margin: 24px 0 8px; color: #c7d2fe; }}
    footer {{ background: #111; color: #6b7280; text-align: center; padding: 24px; font-size: 14px; }}
  </style>
</head>
<body>
  <div class="preview-banner">PREVIEW — This is a demo website built for {name}</div>

  <section class="hero">
    <h1>{copy['headline']}</h1>
    <p>{copy['subheadline']}</p>
    <a class="cta" href="#contact">{copy['cta_text']}</a>
  </section>

  <section class="section">
    <h2>{copy['services_section_title']}</h2>
    <ul class="services">{services_html}</ul>
  </section>

  <section class="trust">
    <div class="trust-inner">
      <h2>Why Choose {name}?</h2>
      {rating_html}
      <p style="color:#374151;margin-top:12px;">{copy['trust_line']}</p>
      {f'<p class="areas">Serving: {areas_html}</p>' if areas_html else ''}
    </div>
  </section>

  <section class="contact" id="contact">
    <h2>Ready to Get Started?</h2>
    <p>Contact us today for a free, no-obligation quote.</p>
    {f'<a class="phone" href="tel:{phone}">{phone}</a>' if phone else ''}
    <a class="cta" style="background:white;color:{color};" href="tel:{phone}">{copy['cta_text']}</a>
  </section>

  <footer>
    <p>{copy['footer_tagline']}</p>
    <p style="margin-top:6px;font-size:12px;">This is a preview website created by FieldLaunch.</p>
  </footer>
</body>
</html>"""


def build_vercel_json() -> str:
    return json.dumps({"version": 2, "routes": [{"src": "/(.*)", "dest": "/index.html"}]}, indent=2)


ROOFING_KEYWORDS = {
    "roofing", "roofer", "roof repair", "roof replacement", "re-roof", "reroof",
    "roofing contractor", "roofing company", "shingle", "gutters", "siding",
}

SERVICE_KEYWORDS = {
    "plumbing", "plumber", "drain", "pipe", "sewer", "water heater",
    "hvac", "heating", "cooling", "air condition", "furnace", "heat pump",
    "lawn", "landscap", "mowing", "grass", "yard", "fertiliz", "irrigation",
    "electrical", "electrician", "wiring", "panel",
    "painting", "painter",
}


def _detect_niche(profile: dict) -> str | None:
    """Return detected niche slug or None if unknown."""
    text = " ".join([
        (profile.get("primaryCategory") or ""),
        (profile.get("niche") or ""),
        " ".join(profile.get("categories") or []),
    ]).lower()

    if any(kw in text for kw in ROOFING_KEYWORDS):
        return "roofing"
    if any(kw in text for kw in {"plumb", "drain", "pipe", "sewer", "water heater", "faucet"}):
        return "plumbing"
    if any(kw in text for kw in {"hvac", "heating", "cooling", "air condition", "furnace", "heat pump"}):
        return "hvac"
    if any(kw in text for kw in {"lawn", "landscap", "mowing", "grass", "fertiliz", "irrigation", "sprinkler"}):
        return "lawn-care"
    if any(kw in text for kw in SERVICE_KEYWORDS):
        return "general"
    return None


def main():
    parser = argparse.ArgumentParser(description="Generate a preview website from a business profile.")
    parser.add_argument("profile", help="Path to enriched business profile JSON")
    parser.add_argument("--output-dir", required=True, help="Directory to write the site into")
    args = parser.parse_args()

    with open(args.profile) as f:
        profile = json.load(f)

    import subprocess
    niche = _detect_niche(profile)
    factory_dir = os.path.dirname(os.path.abspath(__file__))

    if niche == "roofing":
        print(f"[site-factory] Detected roofing — using roofing-site-factory")
        script = os.path.join(factory_dir, "roofing-site-factory.py")
        result = subprocess.run(
            [sys.executable, script, args.profile, "--output-dir", args.output_dir],
            capture_output=False,
        )
        sys.exit(result.returncode)

    if niche in ("plumbing", "hvac", "lawn-care", "general"):
        print(f"[site-factory] Detected {niche} — using service-factory")
        script = os.path.join(factory_dir, "service-factory.py")
        result = subprocess.run(
            [sys.executable, script, args.profile, "--output-dir", args.output_dir, "--niche", niche],
            capture_output=False,
        )
        sys.exit(result.returncode)

    os.makedirs(args.output_dir, exist_ok=True)

    print(f"[site-factory] Generating content for: {profile.get('businessName', 'business')}")
    copy = generate_site_content(profile)

    html = build_html(profile, copy)
    with open(os.path.join(args.output_dir, "index.html"), "w") as f:
        f.write(html)

    with open(os.path.join(args.output_dir, "vercel.json"), "w") as f:
        f.write(build_vercel_json())

    print(f"[site-factory] Site written to: {args.output_dir}")
    print(json.dumps({"status": "ok", "output_dir": args.output_dir, "headline": copy["headline"]}))


if __name__ == "__main__":
    main()
