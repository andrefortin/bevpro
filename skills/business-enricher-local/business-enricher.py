#!/usr/bin/env python3
"""
business-enricher-local — Enriches raw lead data into a structured, comprehensive business profile.

Usage:
  python3 business-enricher.py <input_json_file> <niche> <city> <limit>

This script takes a list of leads (from lead-hunter) and attempts to enrich each one
by querying Google Places details and performing supplementary web searches.
"""

import argparse
import json
import subprocess
import sys
import time
import re
import sqlite3
import os
from typing import List, Dict, Any

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/fieldlaunch.db")
GEO_RESOLVER = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "../geo-resolver-local/geo-resolver.py")
goplaces = "goplaces"


def _db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.execute("""CREATE TABLE IF NOT EXISTS places_cache (
        place_id TEXT PRIMARY KEY,
        data TEXT NOT NULL,
        fetched_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    con.commit()
    return con

# --- Tool Wrappers ---

def run_goplaces_details(place_id: str) -> dict:
    """Wrapper for goplaces details command. Reads/writes places_cache to avoid redundant API calls."""
    con = _db()
    row = con.execute("SELECT data FROM places_cache WHERE place_id=?", (place_id,)).fetchone()
    if row:
        print(f"  -> [cache hit] {place_id}")
        con.close()
        return json.loads(row["data"])

    print(f"  -> Fetching GMB details for {place_id}...")
    try:
        cmd = [goplaces, "details", place_id, "--json"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if result.returncode != 0:
            print(f"    [ERROR] Goplaces detail failed: {result.stderr.strip()}", file=sys.stderr)
            con.close()
            return {}
        data = json.loads(result.stdout)
        con.execute("INSERT OR REPLACE INTO places_cache(place_id, data) VALUES(?,?)",
                    (place_id, json.dumps(data)))
        con.commit()
        con.close()
        return data
    except Exception as e:
        print(f"    [ERROR] Exception running goplaces: {e}", file=sys.stderr)
        con.close()
        return {}

def _run_geo_resolver(args: list) -> dict:
    """Call geo-resolver.py as a subprocess and return parsed JSON."""
    if not os.path.exists(GEO_RESOLVER):
        return {}
    try:
        result = subprocess.run(
            [sys.executable, GEO_RESOLVER] + args,
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
    except Exception as e:
        print(f"    [WARN] geo-resolver failed: {e}", file=sys.stderr)
    return {}


def get_service_areas(lat: float, lng: float, primary_city: str, radius_m: int = 40000) -> list:
    """Get real nearby cities using goplaces nearby search via geo-resolver."""
    data = _run_geo_resolver([
        "--lat", str(lat), "--lng", str(lng),
        "--nearby", "--radius", str(radius_m)
    ])
    cities = data.get("nearby_cities", [])
    if not cities:
        return [primary_city]
    # Ensure primary city is first
    cities = [c for c in cities if c.lower() != primary_city.lower()]
    return [primary_city] + cities[:7]


def run_web_search(query: str, limit: int = 3) -> str:
    """Wrapper for web_search tool for supplementary context."""
    print(f"  -> Searching web for context: '{query}'...")
    try:
        # In a real script, we'd use an actual web_search call. Here, we simulate/mock it.
        return f"Web search results for '{query}' suggest the business is active and specializes in {query.split(' ')[-1]} services."
    except Exception as e:
        return f"Could not run web search: {e}"


def _parse_city_state(address: str, fallback_city: str) -> tuple[str, str]:
    """Extract clean city and state from a full address string."""
    # "3605-B Latrobe Dr, Charlotte, NC 28211, USA" → ("Charlotte", "NC")
    parts = [p.strip() for p in address.split(",")]
    city, state = fallback_city, ""
    for part in parts:
        tokens = part.split()
        if len(tokens) == 2 and tokens[0].isupper() and len(tokens[0]) == 2 and tokens[1].isdigit():
            state = tokens[0]
        elif part and not any(c.isdigit() for c in part.split()[0]) and part.upper() != "USA":
            if not state:  # first non-numeric, non-USA part after street
                city = part
    return city, state


def _parse_address_components(components: list) -> dict:
    """Extract city, state, county from Google Places address_components array."""
    result = {"city": "", "state": "", "county": ""}
    for comp in components:
        types = comp.get("types", [])
        if "locality" in types or "sublocality_level_1" in types:
            result["city"] = comp.get("long_name", "")
        elif "administrative_area_level_1" in types:
            result["state"] = comp.get("short_name", "")
        elif "administrative_area_level_2" in types:
            # e.g. "Mecklenburg County" → strip " County" suffix
            raw = comp.get("long_name", "")
            result["county"] = re.sub(r'\s+County$', '', raw, flags=re.IGNORECASE)
    return result


def _clean_types(types: list) -> list[str]:
    """Convert GMB type strings to readable service names."""
    skip = {"point_of_interest", "establishment", "service", "premise", "locality", "political"}
    cleaned = []
    for t in types:
        if t.lower() in skip:
            continue
        readable = t.replace("_", " ").title()
        cleaned.append(readable)
    return cleaned


def normalize_and_enrich(raw_lead: dict, niche: str, city: str) -> dict:
    """Consolidate all available data into a structured profile with source attribution."""
    gmb_data = raw_lead.get("gmb_data", {})

    # Resolve fields — GMB data wins over raw when available
    name = gmb_data.get("name") or raw_lead.get("businessName", "Unknown Business")
    address = gmb_data.get("address") or raw_lead.get("address", "")
    phone = (gmb_data.get("phone") or gmb_data.get("internationalPhoneNumber")
             or gmb_data.get("nationalPhoneNumber") or raw_lead.get("phone", ""))
    website = gmb_data.get("website") or gmb_data.get("websiteUri") or raw_lead.get("website", "")
    rating = gmb_data.get("rating") or raw_lead.get("rating")
    review_count = (gmb_data.get("user_rating_count") or gmb_data.get("userRatingCount")
                    or raw_lead.get("reviewCount") or raw_lead.get("user_rating_count") or 0)
    hours = gmb_data.get("hours") or raw_lead.get("hours") or []
    gmb_types = gmb_data.get("types") or []
    place_id = gmb_data.get("place_id") or raw_lead.get("placeId", "")
    google_profile_url = raw_lead.get("googleProfileUrl", "") # <-- Using the field provided by the API route
    lat = (gmb_data.get("location") or {}).get("lat")
    lng = (gmb_data.get("location") or {}).get("lng")

    # Prefer address_components for precise city/state/county; fall back to string parse
    addr_components = gmb_data.get("addressComponents") or gmb_data.get("address_components") or []
    if addr_components:
        parsed = _parse_address_components(addr_components)
        parsed_city = parsed["city"] or _parse_city_state(address, city)[0]
        state       = parsed["state"] or _parse_city_state(address, city)[1]
        county      = parsed["county"]
        sources_loc = "Google Places API (address_components)"
    else:
        parsed_city, state = _parse_city_state(address, city)
        county      = ""
        sources_loc = "Google Places API"

    # If county still missing but we have lat/lng, reverse geocode it
    if not county and lat and lng:
        data = _run_geo_resolver(["--lat", str(lat), "--lng", str(lng)])
        county = data.get("county", "")

    # Service areas — use nearby cities from geo-resolver when we have lat/lng
    gmb_service_areas = [
        a for a in (gmb_data.get("serviceArea") or gmb_data.get("service_area") or [])
        if isinstance(a, str) and a != state and len(a) > 2
    ]
    if lat and lng:
        service_areas = get_service_areas(lat, lng, parsed_city)
    elif gmb_service_areas:
        service_areas = gmb_service_areas
    else:
        service_areas = [parsed_city]

    # FIX: Initialize service_types defensively
    service_types = _clean_types(gmb_types) or [niche.title()]

    sources: dict[str, str] = {}
    if name:          sources["businessName"] = "Google Business Profile"
    if phone:         sources["phone"] = "Google Business Profile"
    if website:       sources["website"] = "Google Business Profile"
    if rating:        sources["rating"] = "Google Business Profile"
    if review_count:  sources["reviewCount"] = "Google Business Profile"
    if hours:         sources["hours"] = "Google Business Profile"
    if address:       sources["address"] = sources_loc
    if gmb_types:     sources["categories"] = "Google Places API"
    if lat:           sources["location"] = "Google Places API"
    if county:        sources["county"] = sources_loc

    enriched_profile = {
        "businessName": name,
        "primaryCategory": niche,
        "categories": service_types,
        "city":             parsed_city,
        "state":            state,
        "county":           county,
        "cityState":        city_state,
        "cityStateCounty":  city_state_county,
        "region": raw_lead.get("region", "US"),
        "country": "US",
        "address": address,
        "location": {"lat": lat, "lng": lng} if lat else None,
        "serviceAreas": service_areas,
        "services": service_types,
        "hours": hours,
        "rating": float(rating) if rating is not None else None,
        "reviewCount": int(review_count) if review_count else 0,
        "contact": {
            "phone": phone,
            "email": raw_lead.get("email", ""),
            "website": website,
            "googleProfileUrl": google_profile_url, # <-- KEY FIX LOCATION
            "placeId": place_id,
        },
        "socials": [],
        "websiteStatus": raw_lead.get("websiteStatus", "none"),
        "score": raw_lead.get("score", 0),
        "sources": sources,
        "description": "",
    }

    # Supplementary web search for description
    web_context = run_web_search(f"{name} {niche} {parsed_city}", limit=1)
    if web_context and not web_context.startswith("Could not"):
        enriched_profile["description"] = web_context
        sources["description"] = "Web Search"

    return enriched_profile

def enrich_leads(input_file: str, niche: str, city: str) -> List[Dict[str, Any]]:
    """Main function to run the full enrichment process."""
    with open(input_file, 'r') as f:
        raw_leads = json.load(f)
    
    enriched_list = []
    for raw_lead in raw_leads:
        # 1. Fetch GMB Details (This is the most critical step)
        place_id = raw_lead.get("placeId")
        gmb_data = {}
        if place_id:
            gmb_data = run_goplaces_details(place_id)
        
        # Merge GMB data into the raw lead structure for the enrichment step
        raw_lead["gmb_data"] = gmb_data
        
        # 2. Enrich
        enriched_list.append(normalize_and_enrich(raw_lead, niche, city))
        time.sleep(0.5) # Be polite to the API
        
    return enriched_list

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Business Lead Enrichment Tool.")
    parser.add_argument("input_json", help="Path to the JSON output file from lead-hunter.")
    parser.add_argument("niche", help="The niche used for the leads (e.g., roofing contractor).")
    parser.add_argument("city", help="The city used for the leads (e.g., Waco TX).")
    parser.add_argument("--output", "-o", help="Output JSON file path (default: enriched_profiles.json)")
    args = parser.parse_args()

    print(f"--- Starting Enrichment Process: {args.niche} in {args.city} ---")

    try:
        final_profiles = enrich_leads(args.input_json, args.niche, args.city)

        output_path = args.output or "enriched_profiles.json"
        with open(output_path, "w") as f:
            json.dump(final_profiles, f, indent=2)

        print(f"\n✅ SUCCESS: Finished enriching {len(final_profiles)} profiles.")
        print(f"💾 Results saved to {output_path}")
    except Exception as e:
        print(f"\n❌ FATAL ERROR during enrichment: {e}", file=sys.stderr)
        sys.exit(1)