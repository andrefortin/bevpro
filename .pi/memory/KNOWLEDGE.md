# KNOWLEDGE.md — BevPro Project Knowledge Base

> Canonical technical knowledge for the BevPro SPA. Replaces stale FieldLaunch content (2026-07-31).

## Tech Stack
- **Runtime:** Node 22+, pnpm 10
- **Frontend:** React 19, TypeScript 5.6, Vite 7
- **Styling:** Tailwind CSS v4, `tailwindcss-animate`, `tw-animate-css`
- **Components:** shadcn/ui (new-york style, 40+ components in `client/src/components/ui/`), Radix UI primitives
- **Routing:** wouter (patched via `patches/wouter@3.7.1.patch`)
- **Forms:** react-hook-form + zod (Intake page)
- **Animations:** framer-motion | **Charts:** recharts
- **Server:** Express (`server/index.ts`) — production static file serving

## Key Files
| Path | Purpose |
|------|---------|
| `client/index.html` | Entry — fonts, JSON-LD schema, SEO meta |
| `client/src/main.tsx` | React root mount |
| `client/src/App.tsx` | Router + providers (9+ routes) |
| `client/src/index.css` | Tailwind v4, green/gold palette, double-bezel cards, cubic-bezier |
| `client/src/const.ts` | OAuth login URL builder |
| `client/src/lib/images.ts` | Unsplash image URLs |
| `client/src/contexts/ThemeContext.tsx` | dark/light |
| `server/index.ts` | Express static server (prod) |
| `shared/const.ts` | COOKIE_NAME, ONE_YEAR_MS |

## Routes
| Path | Page | Notes |
|------|------|-------|
| `/` | Home | hero, services bento, service area, FAQ, testimonials, Groupon CTA |
| `/services` | Services | 5 service sections: Alcohol, Coffee, Mocktail, Wine, Mixology Classes |
| `/packages` | Packages | 3 tiers (Essential/Premium/Grand) + 7 add-ons |
| `/about` | About | company story, values, stats |
| `/contact` | Contact | quote request form, FAQ accordion |
| `/intake` | Intake | 14-question event planning form, 3 sections (RHF + zod) |
| `/bartender-training` | BartenderTraining | 1-day course, curriculum, placement |
| `/terms` `/privacy` | Legal | 11/12 sections |
| `*` | NotFound | 404 |

## Design System
- **Palette:** green & gold (Wolfgang Puck-inspired) in `index.css`
- **Cards:** double-bezel border treatment
- **Motion:** cubic-bezier transitions, framer-motion
- **Dark/light:** ThemeContext toggle

## Infrastructure
- **Local dev:** `pnpm dev` (Vite, root = `client/`)
- **Prod:** `pnpm build` → Express static server serves `dist/`
- **Domain/hosting:** managed outside this repo (see EXPERTISE.md / docs/)

## Swarm OS Integration (2026-07-31)
- Registered: MQ queues `swarm.bevpro.{orchestrator,lead,worker-1,worker-2,qa-agent,...}`
- Agents: orchestrator → lead → worker-1/worker-2 → qa-agent (5 canonical)
- Routing: default_agent worker-1, 5 model routes, 7 agent routes
- DB: `~/.swarm/tasks.db`; ledger `~/.forge-writer/cost_ledger.jsonl`

## Form → Email Pipeline (2026-07-31)
- Both forms POST JSON to `/api/intake` + `/api/contact` → nodemailer SMTP → **info@mybevpro.com**
- **Sender = info@mybevpro.com** (Workspace app password in Vercel env: SMTP_USER/PASS/FROM). Local dev still uses ~/.bashrc fortinmedia creds (shared with outreach — don't touch).
- Reply-To = lead's email (reply in Gmail → goes to prospect directly)
- Honeypot: hidden `website` input — bots get silent 200, no email
- Code layout: `api/_form-handlers.ts` (shared logic), `api/intake.ts` + `api/contact.ts` (Vercel functions), mounted also in `server/index.ts` + Vite dev middleware
- **Vercel rule:** with `"framework": "vite"`, function builder transpiles api/*.ts file-by-file — no sibling-dir bundling, ESM needs explicit `.js` import extensions (`./_form-handlers.js`). Cross-dir imports from api/ → runtime 500 ERR_MODULE_NOT_FOUND.
- Debug: `vercel logs <url> --json | grep error`
- Env vars on Vercel: SMTP_HOST/PORT/USER/PASS/FROM, LEAD_EMAIL. See `.env.example`.
