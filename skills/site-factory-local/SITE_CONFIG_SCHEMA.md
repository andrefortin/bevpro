# site-config.json Schema

This is the canonical content schema consumed by all FieldLaunch site templates.
Templates are presentation-only — they render whatever is in `site-config.json`.
Content and design are fully decoupled.

## How it works

1. **Factory** generates `site-config.json` for a business using Claude Haiku
2. **Template** is a pre-built static site (React/Vite, plain HTML, etc.)
3. **Factory** copies the template, drops `site-config.json` in the root, and patches `index.html` with inline config + SEO meta
4. **Site** loads: React app reads `window.SITE_CONFIG` (inline, instant) or fetches `/site-config.json` (fallback)

To build a new template skin, implement support for these fields:

---

## Top-level fields

| Field | Type | Description |
|-------|------|-------------|
| `template` | string | Template identifier, e.g. `"roofing-v1"` |
| `niche` | string | Business niche, e.g. `"roofing"` |

---

## `company`

Core business identity — used in header, footer, contact, CTAs.

| Field | Description |
|-------|-------------|
| `name` | Full business name |
| `nameShort` | Abbreviated name for logo lockup (CAPS) |
| `nameSub` | Sub-label under logo (e.g. "Roofing") |
| `tagline` | One-sentence brand tagline |
| `phone` | E.164 format for `tel:` links |
| `phoneFormatted` | Display format: `(XXX) XXX-XXXX` |
| `email` | Contact email |
| `city` | Primary city |
| `state` | Two-letter state abbreviation |
| `serviceArea` | Human-readable service area string |
| `license` | License string (e.g. "NC Lic. #67492") or `""` |
| `licenseNumber` | Raw license number |
| `yearsInBusiness` | String like `"15+"` |
| `yearsLabel` | e.g. `"Years in Charlotte"` |
| `siteUrl` | Full site URL or `""` |
| `copyright` | Footer copyright line |
| `emergency` | e.g. `"24/7 Emergency Service"` |

---

## `seo`

| Field | Description |
|-------|-------------|
| `homeTitle` | `<title>` tag (≤60 chars) |
| `homeDescription` | Meta description (≤155 chars) |
| `ogImage` | Open Graph image URL or `""` |

---

## `announcement`

Dismissible top bar.

| Field | Description |
|-------|-------------|
| `enabled` | boolean |
| `text` | Text before the link |
| `linkText` | Anchor text |
| `linkHref` | Link URL (usually `"#contact"`) |
| `suffix` | Text after the link |

---

## `hero`

Full-screen hero section.

| Field | Description |
|-------|-------------|
| `h1` | Array of 3 strings — headline split across lines |
| `h1Highlight` | Index (0-based) of the highlighted/colored line |
| `subtitle` | 1-2 sentence supporting copy |
| `badges` | Array of trust badge strings (3 recommended) |
| `bgImage` | Hero background image URL |
| `rating` | Star rating string e.g. `"4.9"` |
| `reviewCount` | Review count string e.g. `"200+"` |
| `stats` | Array of `{ stat, label }` objects (4 recommended) |
| `primaryCta` | CTA button label |

---

## `trustBadges`

Array of `{ name, icon }` objects. `icon` is an emoji.

---

## `services`

Array of service objects. Each service has:

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Service display name |
| `description` | string | Short description for card |
| `href` | string | Link — must be `/services/{slug}` (not `#services`) |
| `slug` | string | URL-safe identifier, e.g. `reroofs-replacements`. **Always explicit in config — never derived from title.** |
| `intro` | string | Opening paragraph for detail page |
| `features` | string[] | 6-8 bullet points for features checklist |
| `process` | `{step, title, desc}[]` | 4 numbered process steps |
| `materials` | string[] | Material/product name pills |
| `faqs` | `{q, a}[]` | 3 FAQs specific to this service |

---

## `howItWorks`

Process/steps section.

| Field | Description |
|-------|-------------|
| `sectionLabel` | Small label above heading |
| `h2` | Section heading |
| `badgeStat` | Stat in floating badge (e.g. `"15+"`) |
| `badgeLabel` | Label under badge stat |
| `image` | Section photo URL |
| `ctaText` | CTA button text |
| `steps` | Array of `{ num, title, desc }` (4 recommended) |

---

## `gallery`

Portfolio/work showcase.

| Field | Description |
|-------|-------------|
| `h2` | Section heading |
| `projects` | Array of `{ neighborhood, title, material, image }` |

---

## `testimonials`

| Field | Description |
|-------|-------------|
| `h2` | Section heading |
| `reviews` | Array of `{ name, location, text, initials }` |

---

## `contact`

| Field | Description |
|-------|-------------|
| `h2` | Section heading |
| `sectionLabel` | Small label above heading |
| `ctaButtonText` | Form submit button text |
| `serviceOptions` | Array of service dropdown strings |

Contact details (phone, email, serviceArea, emergency) come from `company.*`.

---

## `faq`

| Field | Description |
|-------|-------------|
| `h2` | Section heading |
| `items` | Array of `{ q, a }` objects |

---

## `cta`

Bottom CTA section.

| Field | Description |
|-------|-------------|
| `h2` | Urgent headline |
| `subtext` | Supporting copy |
| `primaryCta` | Secondary button label |

Phone CTA uses `company.phone` / `company.phoneFormatted`.

---

## `locations`

Array of city/area objects for location landing pages. Populated from `profile.serviceAreas`.

| Field | Description |
|-------|-------------|
| `name` | Display name, e.g. `"Orlando"` |
| `slug` | URL-safe name, e.g. `"orlando"` |
| `href` | `/locations/{slug}` |

---

## `cta`

Bottom CTA section.

| Field | Description |
|-------|-------------|
| `h2` | Urgent headline |
| `subtext` | Supporting copy |
| `primaryCta` | Secondary button label |
| `bookingUrl` | Full URL for preview banner CTA and booking button. Set from `profile._bookingUrl`. |

Phone CTA uses `company.phone` / `company.phoneFormatted`.

---

## `footer`

| Field | Description |
|-------|-------------|
| `tagline` | Short brand tagline for footer |
| `services` | Array of `{ label, href }` — hrefs must be `/services/{slug}` |
| `serviceAreas` | Array of `{ label, href }` — hrefs must be `/locations/{slug}` |

---

## Adding a new template

1. Create `templates/<niche>-v2/` with your pre-built static files
2. Implement rendering for all schema fields above
3. Read from `window.SITE_CONFIG` (inline injection) with `fetch('/site-config.json')` as fallback
4. Add niche detection in `site-factory.py` or pass `--template` flag
5. Copy `site-config.json` + `vercel.json` from this directory as starting points
