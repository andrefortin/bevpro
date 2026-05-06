# Site Factory Skill

## Description

Generates complete, deployable preview websites for local service businesses. For the roofing niche, produces a React SPA with injected `window.SITE_CONFIG` plus a full set of standalone HTML pages (services, locations, privacy, terms) — all with a preview banner linking to the booking URL.

## What It Generates

**Core files (all niches):**
- `dist/index.html` — React SPA with inline `window.SITE_CONFIG` and click-intercept script
- `dist/site-config.json` — canonical config object
- `dist/vercel.json` — Vercel routing rules for all pages

**Standalone HTML pages (roofing niche):**
- `dist/privacy.html` → `/privacy`
- `dist/terms.html` → `/terms`
- `dist/services.html` → `/services`
- `dist/services/{slug}.html` → `/services/{slug}` (one per service)
- `dist/locations.html` → `/locations`
- `dist/locations/{city-slug}.html` → `/locations/{city-slug}` (one per service area)

**Preview banner** (injected into every page):
- 52px fixed bar at top with `body { padding-top: 52px }`
- "Preview" pill badge, business name, "Make It Mine →" CTA
- CTA links to `site_config.cta.bookingUrl` (sourced from `profile._bookingUrl`)

## Parameters

| Key | Source | Notes |
|-----|--------|-------|
| `profile` | Lead enriched data | Full business profile JSON |
| `profile._bookingUrl` | Injected by generate route | Read from `booking_url` setting in DB |
| `output_dir` | Generate route | Absolute path to write site into |

## Workflow

1. Receives profile JSON (with `_bookingUrl` pre-injected by the API route)
2. Calls Claude Haiku to generate `site_config` from profile
3. Copies React template from `templates/roofing-v1/`
4. Patches `index.html`: injects `window.SITE_CONFIG`, click-intercept script, preview banner
5. Generates standalone HTML pages using `_page_shell` template
6. Writes `vercel.json` with rewrite rules for all routes

## Key Design Decisions

- **`_bookingUrl` injection**: Settings DB values cross the Node→Python boundary via profile JSON. The factory reads `profile._bookingUrl` early and sets `site_config.cta.bookingUrl` before any HTML is written.
- **Click-intercept script**: Capture-phase listener on `document` forces `window.location.href` for `/services/`, `/locations/`, `/privacy`, `/terms` hrefs, bypassing React Router so Vercel serves standalone HTML.
- **Explicit slugs**: Services in `roofing.json` carry an explicit `slug` field. Never derive slugs at runtime from display names — the href↔filename↔vercel.json triad must stay in sync.
- **`_page_shell` template**: All standalone pages share one HTML template string with preview banner, nav, brand styles, and footer. Changes to the shell apply everywhere.

## Config Schema

See `SITE_CONFIG_SCHEMA.md` for the full `site_config` object structure consumed by templates.

---
*Turns enriched lead data into a sellable, deployed preview website.*
