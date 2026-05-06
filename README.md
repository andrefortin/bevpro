# BevPro

**Premium Beverage Catering & Mixology Classes website** — React SPA for BevPro LLC, an Atlanta-based mobile bar service. Alcohol catering, coffee bars, mocktail packages, wine tastings, hands-on mixology workshops, and professional bartender training.

Target audience for this README: **Vector (AI coding agent)**. See `~/.openclaw/workspace/` for user profile, memory, and protocols.

---

## Tech Stack

- **Runtime:** Node 22+, pnpm 10
- **Frontend:** React 19, TypeScript 5.6, Vite 7
- **Styling:** Tailwind CSS v4, `tailwindcss-animate`, `tw-animate-css`
- **Components:** shadcn/ui (new-york style), Radix UI primitives
- **Routing:** wouter (patched via `patches/wouter@3.7.1.patch`)
- **Forms:** react-hook-form + zod
- **Animations:** framer-motion
- **Charts:** recharts
- **Server:** Express (production static file serving)
- **Lint/Format:** Prettier

---

## Directory Map

```
bevpro/
├── client/                    # Vite React SPA (root of dev server)
│   ├── index.html             # Entry HTML — fonts via <link>, JSON-LD schema, SEO meta
│   └── src/
│       ├── main.tsx            # React root mount
│       ├── App.tsx             # Router + providers (8 routes)
│       ├── index.css           # Tailwind v4, green/gold palette, double-bezel cards, cubic-bezier
│       ├── const.ts            # OAuth login URL builder
│       ├── components/         # App components + shadcn/ui/
│       │   ├── ui/             # 40+ shadcn/ui components (new-york)
│       │   ├── ErrorBoundary.tsx
│       │   ├── Map.tsx
│       │   └── ManusDialog.tsx
│       ├── pages/              # Route pages (8 total)
│       │   ├── Home.tsx        # Landing — hero, services bento, service area, FAQ, testimonials
│       │   ├── Services.tsx    # 5 service detail sections with images
│       │   ├── Packages.tsx    # 3-tier pricing with double-bezel cards
│       │   ├── About.tsx       # Company story, values, stats
│       │   ├── Contact.tsx     # Quote request form + FAQ accordion
│       │   ├── Terms.tsx       # Terms & Conditions (11 sections)
│       │   ├── Privacy.tsx     # Privacy Policy (12 sections)
│       │   └── NotFound.tsx    # 404 page
│       ├── contexts/           # ThemeContext.tsx (dark/light)
│       ├── hooks/              # useMobile, useComposition, usePersistFn
│       └── lib/                # utils.ts (cn()), images.ts (Unsplash URLs)
├── server/
│   └── index.ts                # Express static server (production)
├── shared/
│   └── const.ts                # COOKIE_NAME, ONE_YEAR_MS
├── skills/                     # FieldLaunch pipeline skills (16 total)
├── docs/                       # Architecture, expertise, memory, plans
├── commands/                   # boot.md, prime.md (agent commands)
├── .claude/                    # Claude-specific config
├── .pi/                        # Pi agent config
├── package.json                # Dependencies + scripts
├── vite.config.ts              # Vite config (aliases, plugins, debug collector)
├── components.json             # shadcn/ui config (new-york, neutral base)
├── tsconfig.json               # TypeScript config
└── ideas.md                    # Design brief — green & gold Wolfgang Puck theme
```

---

## Routes

| Path | Component | Notes |
|------|-----------|-------|
| `/` | `Home.tsx` | Landing — hero, services, service area, FAQ, testimonials, Groupon CTA |
| `/services` | `Services.tsx` | 5 service detail sections: Alcohol, Coffee, Mocktail, Wine, Classes |
| `/packages` | `Packages.tsx` | 3 tiers (Essential/Premium/Grand) + add-ons + comparison table |
| `/about` | `About.tsx` | Company story, core values, stats |
| `/contact` | `Contact.tsx` | Quote request form, direct contact, trust badges, FAQ |
| `/terms` | `Terms.tsx` | 11-section Terms & Conditions |
| `/privacy` | `Privacy.tsx` | 12-section Privacy Policy |
| `/404` | `NotFound.tsx` | Explicit 404 |
| `*` | `NotFound.tsx` | Catch-all fallback |

---

## Design System

> Full brief in `ideas.md`. Skill-guided via `high-end-visual-design`, `design-taste-frontend`, and `stitch-design-taste`.

### Color Palette — Wolfgang Puck Green & Gold

| Token | Hex | Role |
|-------|-----|------|
| Forest | `#1A5632` | Primary — headers, CTAs, nav active, section BGs |
| Forest Light | `#2D8A4E` | Secondary green accent, checkmarks |
| Gold | `#C8962E` | Accent — buttons, badges, highlights |
| Gold Light | `#F5D77A` | Special emphasis, footer headings |
| Cream | `#FDFBF7` | Section backgrounds |
| Warm Dark | `#1E1810` | Footer, dark text — never pure `#000` |

### Typography
- **Headings:** Playfair Display (serif, elegant, editorial)
- **Body:** Plus Jakarta Sans (clean geometric sans — Inter is **banned** per design skills)

### Signature Patterns
- **Double-Bezel cards** — `.card-shell` (outer tray) + `.card-core` (inner glass plate) with concentric radii
- **Button-in-Button** — CTA buttons with nested icon circles that translate diagonally on hover
- **Floating pill nav** — detached glass navbar (`backdrop-blur-xl`, `rounded-full`, `shadow-diffuse`)
- **Curved pill tabs** — `.nav-tab` / `.nav-tab.active` in `rounded-full` container
- **Custom cubic-bezier** — `cubic-bezier(0.32, 0.72, 0, 1)` over 700ms — no `ease-in-out`
- **Scroll reveals** — `IntersectionObserver`-driven `.reveal-up` with blur-to-clear + translate-y
- **Diffusion shadows** — `shadow-diffuse` (20px/60px/-20px at 8% opacity)
- **No emojis** — replaced with Lucide icons (`strokeWidth={1.5}`) + SVG dot patterns
- **No 3-column equal grids** — asymmetric bento layout on services

### Images
- **Source:** Unsplash via `images.unsplash.com` with required `ixlib=rb-4.0.3` parameter
- **Helper:** `client/src/lib/images.ts` — 14 pre-built `IMG.*` constants
- **Format:** `https://images.unsplash.com/photo-{id}?ixlib=rb-4.0.3&auto=format&fit=crop&w={width}&q=80`
- **IDs:** 10 unique photos across 14 slots (some reused at different crops)
- **Alt text:** All images have keyword-rich descriptive alt attributes

---

## SEO

### On-Page
- **Title:** `BevPro — Beverage Catering & Mixology Classes | Atlanta` (50 chars)
- **Meta description:** Keyword-rich, includes CTA
- **OG/Twitter:** Full card metadata
- **Canonical:** `https://mybevpro.com`
- **Keywords:** `mixology classes Atlanta, bartender training Atlanta, beverage catering, mobile bar service, alcohol catering, coffee catering, mocktail bar, wine tasting Atlanta, corporate event bar, wedding bar service`

### Structured Data
- **JSON-LD:** `LocalBusiness` with `OfferCatalog` (all 5 services), `GeoCircle` for Atlanta metro, `OpeningHoursSpecification`, `PostalAddress`

### Content
- **H1:** Includes primary keywords ("Atlanta beverage catering & mixology classes")
- **13 FAQ items** on Home page covering: service area, event types, dry-hire, classes, pricing, differentiation, mocktails, venues, booking, insurance, custom menus
- **Service Area section:** 16 Atlanta neighborhoods listed with local keyword density
- **Home page content:** ~3,500 words, 13 H2s

### Current Limitations
- No `sitemap.xml`
- No blog/content hub for topical authority
- No Google Business Profile integration
- Images are stock (Unsplash) — real event photos would improve EEAT

---

## Commands

```bash
pnpm dev          # Vite dev server (port 3000, --host)
pnpm build        # vite build + esbuild server
pnpm start        # Production (NODE_ENV=production node dist/index.js)
pnpm preview      # Vite preview (--host)
pnpm check        # tsc --noEmit
pnpm format       # prettier --write .
```

---

## Aliases

```
@/          → client/src/
@shared/    → shared/
@assets/    → attached_assets/
```

---

## Vite Plugins

1. `@vitejs/plugin-react`
2. `@tailwindcss/vite`
3. `@builder.io/vite-plugin-jsx-loc` — JSX source locations
4. `vite-plugin-manus-runtime` — Manus platform runtime
5. `manus-debug-collector` — Custom plugin, writes browser logs to `.manus-logs/` (auto-trims at 1MB)

---

## Services

1. Alcohol Catering
2. Coffee Catering
3. Mocktail Packages
4. Wine Tasting Experience
5. Mixology Classes (Atlanta local — Groupon deals available)
6. Bartender Training (4-week career program — guaranteed festival placement)

---

## Environment

- **Umami analytics:** Removed from `index.html` (env vars not configured)
- **Fonts:** Loaded via `<link>` in `index.html` (NOT `@import` in CSS — breaks Tailwind v4 PostCSS ordering)
- **Google Places API:** In `app/.env.local` for FieldLaunch, not needed for BevPro site

---

## Known Gotchas

- **wouter** is patched via `patches/wouter@3.7.1.patch` — don't upgrade without checking
- **CSS `@import` ordering:** Tailwind v4 expands inline — Google Fonts MUST be loaded via `<link>` in `index.html`, NOT `@import` in CSS
- **Unsplash images** require `ixlib=rb-4.0.3` parameter — without it, all return 404
- **shadcn/ui components** were scaffolded for corporate navy theme — site uses green/gold palette, some component internals may still reference old colors
- **turbopack.root** in config overrides module resolution — don't set unless monorepo
- **FieldLaunch skills** in `skills/` are a separate concern — don't modify for BevPro site work
- **Footer text is single-line** in most pages (`<p>...</p></div>`) — match exact single-line format when batch-editing footers
- **ringColor is not a valid React CSS property** — use `--tw-ring-color` CSS custom property with `as React.CSSProperties` cast
- **RevealSection component** doesn't accept `id` or `style` props — wrap with `<section>` or `<div>` when needed
- **lucide-react lacks branded social icons** — use `react-icons` (Fa6) for Instagram, TikTok, LinkedIn, X
- **Service count in copy** must stay updated when services are added/removed (heading text, JSON-LD, SEO meta)
- **Google Maps image** in `client/public/` — referenced as `/google-maps-atlanta-ga.png`, no hash in filename

---

## Current State (2026-05-05)

- **All 8 pages:** Fully built with green/gold design system applied
- **Navigation:** Floating glass pill with curved tab navigation on all pages
- **Images:** 14 Unsplash photos, all verified working (HTTP 200), served via `@/lib/images`
- **SEO:** JSON-LD schema, meta tags, OG/twitter cards, 13 FAQ items, service area content
- **Legal:** `/terms` and `/privacy` pages built with full branding
- **Footer:** Terms and Privacy links on all pages
- **Design skills applied:** `high-end-visual-design`, `design-taste-frontend`, `stitch-design-taste`
- **Build:** Requires `pnpm install && pnpm dev` (dependencies not installed in this sandbox)
