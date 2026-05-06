#!/usr/bin/env python3
"""
seo-optimizer-local — Optimize a generated HTML site's SEO metadata.

Uses Claude Haiku to improve title, meta description, h1, Open Graph tags, and JSON-LD
structured data in a generated site's index.html.

Usage:
  python3 seo-optimizer.py <site_dir> <profile_json>

Output:
  Modifies <site_dir>/index.html in-place. Prints a JSON summary to stdout.
"""

import argparse
import json
import os
import re
import sys

ANTHROPIC_AVAILABLE = False
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    pass

MODEL = "claude-haiku-4-5-20251001"


def _ai_seo(name: str, niche: str, city: str, description: str) -> dict:
    """Ask Haiku to produce optimized SEO strings."""
    if not ANTHROPIC_AVAILABLE:
        return _fallback_seo(name, niche, city)

    client = anthropic.Anthropic()
    prompt = f"""You are an SEO copywriter. For a local {niche} business named "{name}" in {city}.

Business description: {description or f"{name} is a {niche} serving {city}."}

Return ONLY valid JSON with these keys:
- title (max 60 chars, include city + niche keyword)
- meta_description (max 155 chars, include a call-to-action)
- h1 (max 70 chars, should differ from title)
- og_title (same as title or slight variant)
- og_description (same as meta_description or slight variant)
- json_ld_description (2-3 sentence rich description for structured data)

JSON only, no explanation."""

    msg = client.messages.create(
        model=MODEL,
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    )
    text = msg.content[0].text.strip()
    # Strip any markdown code fences
    text = re.sub(r'^```(?:json)?\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'\s*```$', '', text, flags=re.MULTILINE)
    return json.loads(text)


def _fallback_seo(name: str, niche: str, city: str) -> dict:
    title = f"{name} | {niche.title()} in {city}"[:60]
    meta = f"Looking for {niche} in {city}? {name} delivers quality work. Call today for a free estimate."[:155]
    return {
        "title": title,
        "meta_description": meta,
        "h1": f"Professional {niche.title()} Services in {city}",
        "og_title": title,
        "og_description": meta,
        "json_ld_description": f"{name} is a trusted {niche} serving {city} and surrounding areas.",
    }


def _patch_html(html: str, seo: dict, profile: dict) -> str:
    name = profile.get("businessName", "")
    city = profile.get("city", "")
    state = profile.get("state", "")
    phone = (profile.get("contact") or {}).get("phone", "")
    website = (profile.get("contact") or {}).get("website", "")
    niche = profile.get("primaryCategory", "")

    # Title
    html = re.sub(r'<title>[^<]*</title>', f'<title>{seo["title"]}</title>', html)

    # Meta description
    if re.search(r'<meta\s+name=["\']description["\']', html):
        html = re.sub(
            r'<meta\s+name=["\']description["\']\s+content=["\'][^"\']*["\']',
            f'<meta name="description" content="{seo["meta_description"]}"',
            html
        )
    else:
        html = html.replace('</head>', f'  <meta name="description" content="{seo["meta_description"]}">\n</head>')

    # OG tags — replace or inject
    def _replace_og(prop: str, value: str, src: str) -> str:
        pattern = rf'<meta\s+property=["\']og:{prop}["\']\s+content=["\'][^"\']*["\']'
        replacement = f'<meta property="og:{prop}" content="{value}"'
        if re.search(pattern, src):
            return re.sub(pattern, replacement, src)
        return src.replace('</head>', f'  {replacement}>\n</head>')

    html = _replace_og('title', seo['og_title'], html)
    html = _replace_og('description', seo['og_description'], html)

    # H1 — update SITE_CONFIG.hero.headline (React SPA has no static h1)
    def _inject_h1_into_config(src: str, h1: str) -> str:
        pattern = r'(window\.SITE_CONFIG\s*=\s*)(\{[\s\S]*?\})(\s*;?\s*</script>)'
        match = re.search(pattern, src)
        if not match:
            return src
        try:
            cfg = json.loads(match.group(2))
            if 'hero' in cfg and isinstance(cfg['hero'], dict):
                cfg['hero']['headline'] = h1
            elif 'hero' not in cfg:
                cfg['hero'] = {'headline': h1}
            new_cfg = json.dumps(cfg)
            return src[:match.start(2)] + new_cfg + src[match.end(2):]
        except Exception:
            return src
    html = _inject_h1_into_config(html, seo['h1'])

    # JSON-LD structured data — replace or inject LocalBusiness schema
    json_ld = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": name,
        "description": seo["json_ld_description"],
        "address": {
            "@type": "PostalAddress",
            "addressLocality": city,
            "addressRegion": state,
            "addressCountry": "US"
        }
    }
    if phone:
        json_ld["telephone"] = phone
    if website:
        json_ld["url"] = website
    if niche:
        json_ld["@type"] = "LocalBusiness"  # keep generic; specific types need more data

    json_ld_tag = f'<script type="application/ld+json">\n{json.dumps(json_ld, indent=2)}\n</script>'

    if re.search(r'<script\s+type=["\']application/ld\+json["\']', html):
        html = re.sub(
            r'<script\s+type=["\']application/ld\+json["\']>[\s\S]*?</script>',
            json_ld_tag,
            html,
            count=1
        )
    else:
        html = html.replace('</head>', f'  {json_ld_tag}\n</head>')

    return html


def optimize(site_dir: str, profile: dict) -> dict:
    index_path = os.path.join(site_dir, 'index.html')
    if not os.path.exists(index_path):
        return {"error": f"index.html not found in {site_dir}"}

    name = profile.get("businessName", "Local Business")
    niche = profile.get("primaryCategory", "contractor")
    city = profile.get("city", "your area")
    description = profile.get("description", "")

    try:
        seo = _ai_seo(name, niche, city, description)
    except Exception as e:
        print(f"  [WARN] AI SEO failed, using fallback: {e}", file=sys.stderr)
        seo = _fallback_seo(name, niche, city)

    with open(index_path, 'r', encoding='utf-8') as f:
        html = f.read()

    patched = _patch_html(html, seo, profile)

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(patched)

    return {
        "status": "optimized",
        "site_dir": site_dir,
        "title": seo["title"],
        "meta_description": seo["meta_description"],
        "h1": seo["h1"],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SEO optimizer for generated sites.")
    parser.add_argument("site_dir", help="Path to the generated site directory (contains index.html)")
    parser.add_argument("profile_json", help="Path to the enriched business profile JSON file")
    args = parser.parse_args()

    if not os.path.isdir(args.site_dir):
        print(json.dumps({"error": f"site_dir not found: {args.site_dir}"}))
        sys.exit(1)

    with open(args.profile_json, 'r') as f:
        profile = json.load(f)

    result = optimize(args.site_dir, profile)
    print(json.dumps(result, indent=2))

    if result.get("error"):
        sys.exit(1)
    print(f"\n✅ SEO optimized: {result['title']}", file=sys.stderr)
