#!/usr/bin/env python3
"""
lead-hunter-local — Find local service-area businesses with missing/weak web presence.

Usage:
  python3 lead-hunter.py "<niche>" "<city>" [--limit 20] [--output leads.json]

Examples:
  python3 lead-hunter.py "roofing contractor" "Austin TX" --limit 20
  python3 lead-hunter.py "plumber" "Denver CO"
  python3 lead-hunter.py "hvac" "Dallas Texas" --output /tmp/denver-hvac.json
"""

import argparse
import json
import subprocess
import sys
import time
import re
import sqlite3
import os
import urllib.parse
import urllib.request

GOPLACES = "goplaces"
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/fieldlaunch.db")
SERP_SEARCH_URL = "https://serpapi.com/search.json"
YELP_SEARCH_URL = "https://api.yelp.com/v3/businesses/search"


def _db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.execute("""CREATE TABLE IF NOT EXISTS places_cache (
        place_id TEXT PRIMARY KEY,
        data TEXT NOT NULL,
        fetched_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    con.execute("""CREATE TABLE IF NOT EXISTS search_cache (
        query_key TEXT PRIMARY KEY,
        data TEXT NOT NULL,
        fetched_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    con.execute("""CREATE TABLE IF NOT EXISTS page_token_cache (
        query_key TEXT NOT NULL,
        page_num  INTEGER NOT NULL,
        token     TEXT NOT NULL,
        fetched_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (query_key, page_num)
    )""")
    con.commit()
    return con


def _extract_page_token(stderr: str) -> str | None:
    """Extract next_page_token from goplaces stderr."""
    for line in stderr.splitlines():
        if line.startswith("next_page_token:"):
            return line.split(":", 1)[1].strip()
    return None


def _parse_goplaces_output(stdout: str, stderr: str) -> tuple[list, str | None]:
    """Parse goplaces JSON from stdout and next_page_token from stderr."""
    try:
        data = json.loads(stdout)
        if not isinstance(data, list):
            data = []
    except json.JSONDecodeError:
        data = []
    return data, _extract_page_token(stderr)


def _get_stored_token(con, base_key: str, page_num: int) -> str | None:
    row = con.execute(
        "SELECT token FROM page_token_cache WHERE query_key=? AND page_num=?",
        (base_key, page_num)
    ).fetchone()
    return row["token"] if row else None


def _store_token(con, base_key: str, page_num: int, token: str):
    con.execute(
        "INSERT OR REPLACE INTO page_token_cache(query_key, page_num, token) VALUES(?,?,?)",
        (base_key, page_num, token)
    )


def search_places(query: str, limit: int = 20, region: str = None, start_page: int = 1) -> list[dict]:
    """Search Google Places with pagination and deduplication by place_id.

    start_page: 1-based page to start collecting results from.
    Pages before start_page are fetched only to advance the token cursor.
    """
    base_key = f"{query}|{region or ''}"
    con = _db()

    # Resolve token for start_page from cache or fast-forward
    page_token: str | None = None
    if start_page > 1:
        page_token = _get_stored_token(con, base_key, start_page - 1)
        if page_token:
            print(f"  [token cache] resuming at page {start_page}")
        else:
            print(f"  [fast-forward] fetching pages 1–{start_page - 1} to resume at page {start_page}...")
            tok: str | None = None
            for skip_page in range(1, start_page):
                cmd = [GOPLACES, "search", query, "--limit", "20", "--json"]
                if region:
                    cmd += ["--region", region]
                if tok:
                    cmd += ["--page-token", tok]
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                if r.returncode != 0:
                    print(f"  [fast-forward] error on page {skip_page}: {r.stderr.strip()}", file=sys.stderr)
                    break
                _, next_tok = _parse_goplaces_output(r.stdout, r.stderr)
                if next_tok:
                    _store_token(con, base_key, skip_page, next_tok)
                    tok = next_tok
                else:
                    print(f"  [fast-forward] no more pages after page {skip_page}")
                    con.commit()
                    con.close()
                    return []
                time.sleep(2.0)
            con.commit()
            page_token = tok

    all_results: list[dict] = []
    remaining = limit
    current_page = start_page

    while remaining > 0:
        batch = min(remaining, 20)
        cmd = [GOPLACES, "search", query, "--limit", str(batch), "--json"]
        if region:
            cmd += ["--region", region]
        if page_token:
            cmd += ["--page-token", page_token]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            print(f"  [page {current_page}] goplaces error: {result.stderr.strip()}", file=sys.stderr)
            break

        page_results, next_token = _parse_goplaces_output(result.stdout, result.stderr)

        if not page_results:
            print(f"  [page {current_page}] empty response — stopping", file=sys.stderr)
            break

        # Stamp absolute rank and page before accumulating
        base_rank = len(all_results) + 1
        for j, r in enumerate(page_results):
            r['_map_rank'] = base_rank + j
            r['_map_page'] = current_page

        all_results.extend(page_results)
        remaining -= len(page_results)

        print(f"  [page {current_page}] +{len(page_results)} results (total: {len(all_results)}, next: {'yes' if next_token else 'no'})", file=sys.stderr)

        if next_token:
            _store_token(con, base_key, current_page, next_token)
            con.commit()

        if not next_token or len(page_results) < batch:
            break

        page_token = next_token
        current_page += 1
        # Google requires ≥2s before a nextPageToken becomes valid
        time.sleep(2.0)

    con.close()

    # Deduplicate by place_id, preserve order
    seen: set[str] = set()
    deduped: list[dict] = []
    for r in all_results:
        pid = r.get("place_id", "")
        if pid and pid not in seen:
            seen.add(pid)
            deduped.append(r)
        elif not pid:
            deduped.append(r)

    return deduped[:limit]


def get_details(place_id: str) -> dict:
    """Fetch full details for a single place. Caches by place_id."""
    con = _db()
    row = con.execute("SELECT data FROM places_cache WHERE place_id=?", (place_id,)).fetchone()
    if row:
        con.close()
        return json.loads(row["data"])

    cmd = [GOPLACES, "details", place_id, "--json"]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    if result.returncode != 0:
        con.close()
        return {}
    try:
        data = json.loads(result.stdout)
        con.execute("INSERT OR REPLACE INTO places_cache(place_id, data) VALUES(?,?)",
                    (place_id, json.dumps(data)))
        con.commit()
        con.close()
        return data
    except json.JSONDecodeError:
        con.close()
        return {}


def check_website_status(url: str | None, name: str) -> str:
    if not url:
        return "none"
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        domain = (parsed.hostname or "").lower()
        if domain.startswith("www."):
            domain = domain[4:]
    except Exception:
        return "none"

    directory_hosts = [
        "yelp.com", "yellowpages.com", "bbb.org", "angieslist.com",
        "houzz.com", "nextdoor.com", "thumbtack.com", "homeadvisor.com",
        "porch.com", "manta.com", "hotfrog.com", "foursquare.com",
    ]
    social_hosts = ["facebook.com", "instagram.com", "twitter.com", "x.com", "tiktok.com", "linkedin.com"]
    free_builder_hosts = [
        "wixsite.com", "sites.google.com", "wordpress.com", "blogspot.com",
        "weebly.com", "squarespace.com", "godaddysites.com",
    ]

    def match(d, pattern):
        return d == pattern or d.endswith("." + pattern)

    for d in directory_hosts:
        if match(domain, d):
            return "directory-only"
    for s in social_hosts:
        if match(domain, s):
            return "social-only"
    for f in free_builder_hosts:
        if match(domain, f):
            return "weak"
    return "has_website"


def score_lead(website_status: str, rating: float | None, review_count: int | None, has_phone: bool, has_email: bool) -> int:
    score = 50
    if website_status == "none":
        score += 30
    elif website_status == "broken":
        score += 25
    elif website_status in ("social-only", "directory-only"):
        score += 20
    elif website_status == "weak":
        score += 10
    elif website_status == "has_website":
        score -= 20

    if rating and rating >= 4.0:
        score += 10
    elif rating and rating >= 3.5:
        score += 5

    if review_count and review_count >= 20:
        score += 5
    elif review_count and review_count >= 10:
        score += 3

    if has_phone:
        score += 5
    if has_email:
        score += 5

    return min(score, 100)


def search_serp(query: str, city: str, api_key: str, limit: int = 20) -> list[dict]:
    if not api_key:
        return []
    print(f"  [SerpAPI] Searching: {query} in {city}...")
    params = {
        "engine": "google_local",
        "q": f"{query} {city}",
        "api_key": api_key,
        "num": min(limit, 20),
    }
    url = f"{SERP_SEARCH_URL}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            data = json.load(r)
    except Exception as e:
        print(f"  [SerpAPI] Error: {e}", file=sys.stderr)
        return []

    results = []
    for place in data.get("local_results", [])[:limit]:
        website = place.get("website", "")
        phone = place.get("phone", "")
        rating = place.get("rating")
        reviews = place.get("reviews")
        title = place.get("title", "")
        address = place.get("address", "")
        website_status = check_website_status(website, title)
        score = score_lead(website_status, float(rating) if rating else None,
                           int(reviews) if reviews else None, bool(phone), False)
        results.append({
            "businessName": title,
            "niche": query,
            "city": city,
            "address": address,
            "phone": phone,
            "email": "",
            "website": website,
            "websiteStatus": website_status,
            "rating": float(rating) if rating else None,
            "reviewCount": int(reviews) if reviews else None,
            "googleProfileUrl": "",
            "placeId": "",
            "score": score,
            "_source": "serp",
        })
    print(f"  [SerpAPI] +{len(results)} results")
    return results


def search_yelp(query: str, city: str, api_key: str, limit: int = 20) -> list[dict]:
    if not api_key:
        return []
    print(f"  [Yelp] Searching: {query} in {city}...")
    params = urllib.parse.urlencode({
        "term": query,
        "location": city,
        "limit": min(limit, 50),
        "sort_by": "review_count",
    })
    url = f"{YELP_SEARCH_URL}?{params}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {api_key}"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.load(r)
    except Exception as e:
        print(f"  [Yelp] Error: {e}", file=sys.stderr)
        return []

    results = []
    for biz in data.get("businesses", [])[:limit]:
        phone = biz.get("phone", "")
        rating = biz.get("rating")
        reviews = biz.get("review_count")
        name = biz.get("name", "")
        loc = biz.get("location", {})
        address = ", ".join(filter(None, [loc.get("address1", ""), loc.get("city", ""), loc.get("state", "")]))
        score = score_lead("directory-only", float(rating) if rating else None,
                           int(reviews) if reviews else None, bool(phone), False)
        results.append({
            "businessName": name,
            "niche": query,
            "city": city,
            "address": address,
            "phone": phone,
            "email": "",
            "website": "",
            "websiteStatus": "directory-only",
            "rating": float(rating) if rating else None,
            "reviewCount": int(reviews) if reviews else None,
            "googleProfileUrl": "",
            "placeId": "",
            "score": score,
            "_source": "yelp",
        })
    print(f"  [Yelp] +{len(results)} results")
    return results


def _dedup_leads(leads: list[dict]) -> list[dict]:
    """Deduplicate by place_id first, then by normalized name+city."""
    seen_ids: set[str] = set()
    seen_names: set[str] = set()
    out: list[dict] = []
    for lead in leads:
        pid = lead.get("placeId") or lead.get("place_id") or ""
        if pid:
            if pid in seen_ids:
                continue
            seen_ids.add(pid)
        else:
            key = re.sub(r'[^a-z0-9]', '', (lead.get("businessName") or "").lower())
            key += "|" + re.sub(r'[^a-z0-9]', '', (lead.get("city") or "").lower())
            if key in seen_names:
                continue
            seen_names.add(key)
        out.append(lead)
    return out


def hunt(niche: str, city: str, limit: int = 20, output: str | None = None,
         start_page: int = 1, sources: list[str] | None = None,
         serp_api_key: str = "", yelp_api_key: str = ""):
    city_clean = city.strip()
    query = f"{niche} in {city_clean}"
    active_sources = sources or ["google"]

    print(f"🔍 Searching: {query} (limit: {limit}, page: {start_page}, sources: {', '.join(active_sources)})")

    all_raw: list[dict] = []

    if "google" in active_sources:
        places = search_places(query, limit=limit, region="US", start_page=start_page)
        all_raw.extend(places)

    if "serp" in active_sources and serp_api_key:
        all_raw.extend(search_serp(niche, city_clean, serp_api_key, limit=limit))

    if "yelp" in active_sources and yelp_api_key:
        all_raw.extend(search_yelp(niche, city_clean, yelp_api_key, limit=limit))

    places = _dedup_leads(all_raw)

    if not places:
        print("❌ No results found.", file=sys.stderr)
        return

    print(f"📊 Found {len(places)} unique businesses. Fetching details...")

    leads = []
    for i, place in enumerate(places, 1):
        source = place.get("_source", "google")
        place_id = place.get("place_id") or place.get("placeId") or ""

        if source in ("serp", "yelp"):
            name = place.get("businessName", "Unknown")
            print(f"  [{i}/{len(places)}] {name} [{source}] → {place.get('websiteStatus')} (score: {place.get('score')})")
            leads.append(place)
            continue

        if not place_id:
            continue

        print(f"  [{i}/{len(places)}] {place.get('name', 'Unknown')}...", end=" ", flush=True)

        details = get_details(place_id)
        time.sleep(0.2)

        website_url = details.get("website") or details.get("websiteUri") or ""
        website_status = check_website_status(website_url, details.get("name", ""))
        phone = details.get("phone") or details.get("internationalPhoneNumber") or details.get("nationalPhoneNumber") or ""
        rating = details.get("rating")
        review_count = details.get("user_rating_count") or details.get("userRatingCount")
        score = score_lead(website_status, rating, review_count, bool(phone), False)

        leads.append({
            "businessName": details.get("name") or place.get("name", ""),
            "niche": niche,
            "city": city_clean,
            "address": details.get("address") or place.get("address", ""),
            "phone": phone,
            "email": "",
            "website": website_url,
            "websiteStatus": website_status,
            "rating": float(rating) if rating is not None else None,
            "reviewCount": int(review_count) if review_count is not None else None,
            "googleProfileUrl": f"https://maps.google.com/?cid={place_id}",
            "placeId": place_id,
            "mapRank": place.get("_map_rank"),
            "mapPage": place.get("_map_page"),
            "score": score,
            "_source": "google",
        })
        print(f"→ {website_status} (score: {score})")

    leads.sort(key=lambda x: x["score"], reverse=True)

    status_counts: dict[str, int] = {}
    for l in leads:
        s = l["websiteStatus"]
        status_counts[s] = status_counts.get(s, 0) + 1

    print(f"\n{'='*60}")
    print(f"🎯 {niche} in {city_clean} — {len(leads)} leads")
    for status, count in sorted(status_counts.items(), key=lambda x: -x[1]):
        print(f"  {status}: {count}")

    if output:
        with open(output, "w") as f:
            json.dump(leads, f, indent=2)
        print(f"\n💾 Saved {len(leads)} leads to {output}", file=sys.stderr)
    else:
        print(json.dumps(leads, indent=2))

    return leads


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find local businesses with missing/weak websites")
    parser.add_argument("niche", help="Business niche (e.g., 'roofing contractor')")
    parser.add_argument("city", help="City (e.g., 'Austin TX')")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--start-page", type=int, default=1, dest="start_page")
    parser.add_argument("--output", "-o")
    parser.add_argument("--sources", default="google")
    parser.add_argument("--serp-api-key", default="", dest="serp_api_key")
    parser.add_argument("--yelp-api-key", default="", dest="yelp_api_key")
    args = parser.parse_args()

    hunt(
        args.niche, args.city,
        limit=args.limit, output=args.output, start_page=args.start_page,
        sources=args.sources.split(","),
        serp_api_key=args.serp_api_key,
        yelp_api_key=args.yelp_api_key,
    )
