# FieldLaunch Architecture

## Overview

FieldLaunch is a lead generation and site deployment pipeline for local service businesses. The system has two interfaces:
- **Web UI** — Next.js app for human-in-the-loop operation (`app/`)
- **Agent CLI** — `fieldlaunch-skill.py` for autonomous pipeline execution

## Pipeline

```
Hunt → Enrich → Generate → SEO → Deploy → Outreach
```

| Phase | Code | Notes |
|-------|------|-------|
| Hunt | `skills/lead-hunter-local/lead-hunter.py` | goplaces search + pagination, dedup by place_id, SQLite token cache for resume |
| Enrich | `skills/business-enricher-local/business-enricher.py` | GMB details via goplaces, source attribution, city/state parsing, places_cache |
| Generate | `skills/site-factory-local/site-factory.py` | Claude Haiku, HTML templates, parallel in web UI |
| SEO | _(pending)_ | Post-generation: title, meta, h1, OG, JSON-LD via Haiku |
| Deploy | Vercel CLI (`vercel --prod`) | Called from `app/src/lib/skills.ts:deployToVercel()` |
| Outreach | `skills/outreach-launcher-local/outreach-launcher.py` | SMTP email, SMTP_USER/SMTP_PASS required |

## Database — `data/fieldlaunch.db`

| Table | Purpose |
|-------|---------|
| `campaigns` | id, niche, city, limit_count, approval_mode, status |
| `leads` | campaign_id, place_id, business_name, phone, website, score, selected, status, raw_data, enriched_data |
| `sites` | lead_id, campaign_id, local_path, vercel_url, status, approved |
| `outreach_events` | lead_id, site_id, campaign_id, channel, status, subject, message_body, approved, sent_at |
| `search_cache` | Caches goplaces search results by query_key |
| `places_cache` | Caches goplaces detail results by place_id |
| `page_token_cache` | Stores pagination tokens per (query_key, page_num) for hunt resume |

## Web API Routes (`app/src/app/api/`)

| Route | Method | Purpose |
|-------|--------|---------|
| `/api/campaigns` | GET/POST | List + create campaigns |
| `/api/campaigns/[id]` | GET/PATCH | Fetch campaign with leads/sites/outreach; edit niche/city/limit |
| `/api/campaigns/[id]/hunt` | POST | Run lead hunter. Body: `{ mode: 'fresh' \| 'continue' }`. Dedupes by place_id; re-hunt updates ALL fields. |
| `/api/campaigns/[id]/enrich` | POST | Run business enricher on selected leads |
| `/api/campaigns/[id]/generate` | POST | Generate sites (parallel via Promise.all); injects `_bookingUrl` from settings |
| `/api/campaigns/[id]/deploy` | POST | Deploy all draft sites to Vercel |
| `/api/campaigns/[id]/outreach` | GET/POST/DELETE | List/draft outreach; DELETE removes all events for a lead |
| `/api/campaigns/[id]/outreach/send` | POST | Manual send for approved outreach |
| `/api/campaigns/[id]/outreach/regenerate` | POST | Delete + re-draft outreach for one lead |
| `/api/campaigns/[id]/outreach/[eventId]/approve` | POST | Approve, reject, or reset a single event |
| `/api/campaigns/[id]/sites/[siteId]/regenerate` | POST | Re-run site factory for one site |
| `/api/campaigns/[id]/leads` | PATCH | Bulk select/deselect leads |
| `/api/approvals` | GET | Cross-campaign pending sites + outreach |
| `/api/stripe` | GET/POST | Fetch stored payment links; POST runs stripe-setup skill |
| `/api/settings` | GET/POST | Read/write settings (Vercel, SMTP, Twilio, Stripe, Cal.com) |

## Skills

| Skill | Purpose |
|-------|---------|
| `lead-hunter-local` | Google Places hunt, pagination, dedup, mapRank |
| `business-enricher-local` | Full GMB enrichment |
| `site-factory-local` | Roofing SPA + standalone service/location/privacy/terms pages + preview banner |
| `seo-optimizer-local` | Haiku: title, meta, h1, OG, JSON-LD |
| `outreach-launcher-local` | SMTP email, test mode |
| `sequence-builder-local` | Multi-step email sequence; prefills Stripe payment links per client |
| `stripe-setup-local` | Creates/retrieves Stripe products and payment links (idempotent) |
| `puppeteer-screenshot-local` | Site screenshot via Puppeteer |
| `lighthouse-local` | Lighthouse audit |
| `config-merger-local` | 3-way config merge (base → niche → lead) |
| `geo-resolver-local` | Normalizes city/state inputs |

## Skills Interface (`app/src/lib/skills.ts`)

All Python skills are called via `spawnSync` (or async `spawn` for site factory). Key functions:
- `runLeadHunter(niche, city, limit, startPage)` — passes `--start-page`
- `runBusinessEnricher(inputFile, niche, city, outputFile)` — calls `business-enricher.py`
- `runSiteFactory(profileFile, outputDir)` — sync, single site
- `runSiteFactoryAsync(profile, outputDir)` — async, used for parallel generate; accepts profile object directly
- `deployToVercel(siteDir, projectName)` — extracts URL with hard-stop regex `https://[a-z0-9-]+\.vercel\.app`
- `buildSequence(lead, settings)` — calls sequence-builder; passes payment link URLs from settings DB
- `setupStripe(secretKey)` — calls stripe-setup skill, returns product/price/link data

## Pagination Resume Logic

Hunt route calculates `startPage = Math.floor(existingLeadCount / 20) + 1` when `mode === 'continue'`. Python `hunt()` fast-forwards through earlier pages to collect their tokens (needed as chained cursors), then collects from `startPage` onward.

## Approval Modes

- `per-lead` — review each site/email before send
- `batch` — review all together
- `full-auto` — pipeline runs end-to-end

## Model Strategy

- **Haiku** (`claude-haiku-4-5-20251001`) — site content generation, SEO optimization (fast + cheap)
- **Sonnet** (`claude-sonnet-4-6`) — mid-complexity reasoning, code gen, refactoring
- **Opus** (`claude-opus-4-7`) — architecture decisions, novel problem solving

## Key Env Vars

```
ANTHROPIC_API_KEY        # site generation + SEO
SMTP_HOST                # outreach email
SMTP_PORT
SMTP_USER
SMTP_PASS
SMTP_FROM
GOOGLE_PLACES_API_KEY    # used by goplaces CLI
CAL_API_KEY              # Cal.com booking integration
```

Settings stored in SQLite (set via Settings UI):
- `vercel_token`, `vercel_scope` — Vercel deployment
- `booking_url` — injected as `profile._bookingUrl` into factory; populates preview banner CTA
- `twilio_sid`, `twilio_auth_token`, `twilio_from` — SMS (future)
- `stripe_secret_key`, `stripe_publishable_key` — Stripe products/links
- `stripe_payment_link_onetime`, `stripe_payment_link_monthly`, `stripe_payment_link_chatbot` — stored after setup

## Site Factory: Standalone Page Generation

`roofing-site-factory.py` generates these files alongside the React SPA:

| File | Route |
|------|-------|
| `privacy.html` | `/privacy` |
| `terms.html` | `/terms` |
| `services.html` | `/services` |
| `services/{slug}.html` | `/services/{slug}` |
| `locations.html` | `/locations` |
| `locations/{city-slug}.html` | `/locations/{city-slug}` |

All standalone pages share a `_page_shell` HTML template with:
- Preview banner (52px fixed) with booking URL CTA
- Matching brand styles (colors from site_config)
- Navigation links

`vercel.json` is generated with explicit rewrite rules for each page.

A capture-phase click listener in `index.html` intercepts hrefs matching `/services|locations|privacy|terms` and forces `window.location.href`, bypassing React Router so Vercel serves the standalone HTML files.
