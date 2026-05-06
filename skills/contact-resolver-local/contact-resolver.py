#!/usr/bin/env python3
"""
contact-resolver-local — Resolves the best contact email and name for a business lead.

Priority order:
  1. Scrape business website for mailto: links and contact pages
  2. Try common email patterns against the business domain
  3. Fall back to GMB phone only

Usage:
  python3 contact-resolver.py <lead_json_path> [--output <path>]

Output JSON:
  { "email": "...", "name": "...", "phone": "...", "source": "...", "confidence": 0.0-1.0 }
"""

import sys
import json
import re
import argparse
import urllib.request
import urllib.parse
import urllib.error
from html.parser import HTMLParser


class EmailExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.emails = []
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self._in_title = True
        if tag == "a":
            for k, v in attrs:
                if k == "href" and v and v.lower().startswith("mailto:"):
                    email = v[7:].split("?")[0].strip().lower()
                    if _valid_email(email):
                        self.emails.append(email)

    def handle_data(self, data):
        if self._in_title:
            self.title += data

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False


def _valid_email(email: str) -> bool:
    return bool(re.match(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$", email))


def _extract_domain(url: str) -> str | None:
    if not url:
        return None
    try:
        parsed = urllib.parse.urlparse(url if "://" in url else f"http://{url}")
        host = parsed.hostname or ""
        host = host.lstrip("www.")
        return host if "." in host else None
    except Exception:
        return None


def _fetch_html(url: str, timeout: int = 8) -> str | None:
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; FieldLaunch/1.0)"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read(200_000).decode("utf-8", errors="ignore")
    except Exception:
        return None


def _scrape_website(website: str):
    """Try homepage then /contact."""
    base = website.rstrip("/")
    pages = [base, f"{base}/contact", f"{base}/contact-us", f"{base}/about"]
    all_emails = []

    for url in pages:
        html = _fetch_html(url)
        if not html:
            continue
        parser = EmailExtractor()
        parser.feed(html)
        all_emails.extend(parser.emails)

        # Also scan raw text for email patterns
        found = re.findall(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", html)
        for e in found:
            e = e.lower()
            if _valid_email(e):
                all_emails.append(e)

    # Deduplicate, filter junk (image/asset emails)
    seen = set()
    clean = []
    junk_domains = {"sentry.io", "example.com", "wixpress.com", "squarespace.com"}
    for e in all_emails:
        domain = e.split("@")[1] if "@" in e else ""
        if e not in seen and domain not in junk_domains:
            seen.add(e)
            clean.append(e)

    return clean


COMMON_PATTERNS = ["info", "contact", "hello", "owner", "admin", "office", "support"]


def _guess_domain_emails(domain: str) -> list[str]:
    return [f"{p}@{domain}" for p in COMMON_PATTERNS]


def resolve(lead: dict) -> dict:
    website = (lead.get("website") or "").strip()
    phone = (lead.get("phone") or "").strip()
    gmb_email = (lead.get("email") or "").strip()  # rarely populated
    name = (lead.get("business_name") or "").strip()

    # 1. GMB email (high confidence if present)
    if gmb_email and _valid_email(gmb_email):
        return {
            "email": gmb_email,
            "name": None,
            "phone": phone or None,
            "source": "gmb",
            "confidence": 0.90,
        }

    # 2. Scrape website
    if website:
        scraped = _scrape_website(website)
        domain = _extract_domain(website)
        if scraped:
            # Prefer emails on the business domain, deprioritise generic mail hosts
            own = [e for e in scraped if domain and domain in e]
            chosen = own[0] if own else scraped[0]
            return {
                "email": chosen,
                "name": None,
                "phone": phone or None,
                "source": "website_scrape",
                "confidence": 0.80 if own else 0.60,
            }

        # 3. Pattern guesses on business domain
        if domain:
            guesses = _guess_domain_emails(domain)
            return {
                "email": guesses[0],  # info@ is most likely
                "name": None,
                "phone": phone or None,
                "source": "domain_guess",
                "confidence": 0.30,
                "alternatives": guesses[1:],
            }

    # 4. Phone only
    if phone:
        return {
            "email": None,
            "name": None,
            "phone": phone,
            "source": "phone_only",
            "confidence": 0.10,
        }

    return {"email": None, "name": None, "phone": None, "source": "none", "confidence": 0.0}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("lead_json", help="Path to lead JSON file")
    parser.add_argument("--output", help="Output path (default: stdout)")
    args = parser.parse_args()

    with open(args.lead_json) as f:
        lead = json.load(f)

    result = resolve(lead)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
