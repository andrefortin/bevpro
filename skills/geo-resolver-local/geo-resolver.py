#!/usr/bin/env python3
"""
geo-resolver — Resolve a location string or lat/lng into canonical city/state/county/zip.

Uses Google Geocoding API for forward/reverse geocoding and goplaces nearby search
for discovering real nearby service areas.

Usage (module):
    from geo_resolver import resolve_location, resolve_latlng, get_nearby_cities

Usage (CLI):
    python3 geo-resolver.py "Charlotte, NC"
    python3 geo-resolver.py --lat 35.22 --lng -80.84
    python3 geo-resolver.py "Austin, TX" --nearby --radius 40000
"""

import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

GEOCODE_URL      = "https://maps.googleapis.com/maps/api/geocode/json"
API_KEY_ENV      = "GOOGLE_PLACES_API_KEY"
DEFAULT_RADIUS_M = 40_000   # 40 km ≈ 25 miles


# ---------------------------------------------------------------------------
# Core geocoding
# ---------------------------------------------------------------------------

def _geocode_request(params: dict) -> dict:
    key = os.environ.get(API_KEY_ENV)
    if not key:
        raise EnvironmentError(f"{API_KEY_ENV} not set")
    params["key"] = key
    url = f"{GEOCODE_URL}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=10) as r:
        data = json.load(r)
    if data.get("status") not in ("OK", "ZERO_RESULTS"):
        raise RuntimeError(f"Geocoding API error: {data.get('status')} — {data.get('error_message', '')}")
    results = data.get("results", [])
    return results[0] if results else {}


def _parse_components(components: list) -> dict:
    out = {"city": "", "state": "", "county": "", "zip": "", "country": ""}
    for c in components:
        types = c.get("types", [])
        name  = c.get("long_name", "")
        short = c.get("short_name", "")
        if "locality" in types or "sublocality_level_1" in types:
            out["city"] = name
        elif "administrative_area_level_2" in types:
            out["county"] = re.sub(r'\s+County$', '', name, flags=re.IGNORECASE)
        elif "administrative_area_level_1" in types:
            out["state"] = short    # "NC" not "North Carolina"
        elif "postal_code" in types:
            out["zip"] = name
        elif "country" in types:
            out["country"] = short
    return out


def resolve_location(query: str) -> dict:
    """Forward geocode: query string → {city, state, county, zip, lat, lng}."""
    if not query or not query.strip():
        return {"error": "Empty query"}
    try:
        result = _geocode_request({"address": query})
        if not result:
            return {"error": f"No results for: {query}"}
        loc  = result.get("geometry", {}).get("location", {})
        info = _parse_components(result.get("address_components", []))
        info["lat"] = loc.get("lat")
        info["lng"] = loc.get("lng")
        info["formatted_address"] = result.get("formatted_address", "")
        return info
    except Exception as e:
        return {"error": str(e)}


def resolve_latlng(lat: float, lng: float) -> dict:
    """Reverse geocode: lat/lng → {city, state, county, zip, ...}."""
    try:
        result = _geocode_request({"latlng": f"{lat},{lng}", "result_type": "locality"})
        if not result:
            result = _geocode_request({"latlng": f"{lat},{lng}"})
        if not result:
            return {"error": f"No results for: {lat},{lng}"}
        loc  = result.get("geometry", {}).get("location", {})
        info = _parse_components(result.get("address_components", []))
        info["lat"] = loc.get("lat", lat)
        info["lng"] = loc.get("lng", lng)
        info["formatted_address"] = result.get("formatted_address", "")
        return info
    except Exception as e:
        return {"error": str(e)}


# ---------------------------------------------------------------------------
# Nearby cities via goplaces
# ---------------------------------------------------------------------------

def get_nearby_cities(lat: float, lng: float, radius_m: int = DEFAULT_RADIUS_M,
                      primary_city: str = "") -> list:
    """
    Return list of city names near lat/lng using goplaces nearby search.
    Primary city is always first; duplicates and numeric entries removed.
    """
    try:
        cmd = [
            "goplaces", "nearby",
            f"--lat={lat}", f"--lng={lng}",
            f"--radius-m={radius_m}",
            "--type=locality",
            "--limit=12",
            "--json",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if result.returncode != 0:
            return [primary_city] if primary_city else []

        places = json.loads(result.stdout)
        seen   = set()
        cities = []

        if primary_city:
            cities.append(primary_city)
            seen.add(primary_city.lower())

        for p in places:
            name = p.get("name", "").strip()
            if not name or name.lower() in seen:
                continue
            if re.search(r'\d', name):   # skip entries with digits
                continue
            cities.append(name)
            seen.add(name.lower())

        return cities[:8]
    except Exception as e:
        print(f"  [WARN] get_nearby_cities failed: {e}", file=sys.stderr)
        return [primary_city] if primary_city else []


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _cli():
    import argparse
    parser = argparse.ArgumentParser(description="Resolve a location to canonical geo data.")
    parser.add_argument("query", nargs="?", help="Location string, e.g. 'Charlotte, NC'")
    parser.add_argument("--lat",    type=float, help="Latitude for reverse geocode")
    parser.add_argument("--lng",    type=float, help="Longitude for reverse geocode")
    parser.add_argument("--nearby", action="store_true", help="Also fetch nearby cities")
    parser.add_argument("--radius", type=int, default=DEFAULT_RADIUS_M, help="Nearby radius in meters")
    args = parser.parse_args()

    if args.lat is not None and args.lng is not None:
        info = resolve_latlng(args.lat, args.lng)
    elif args.query:
        info = resolve_location(args.query)
    else:
        parser.print_help()
        sys.exit(1)

    if args.nearby and not info.get("error"):
        lat = info.get("lat") or args.lat
        lng = info.get("lng") or args.lng
        if lat and lng:
            info["nearby_cities"] = get_nearby_cities(lat, lng, args.radius, info.get("city", ""))

    print(json.dumps(info, indent=2))


if __name__ == "__main__":
    _cli()
