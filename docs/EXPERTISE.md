# EXPERTISE.md - Durable Lessons Learned and Operational Best Practices

This file serves as the collective mental model for the agents, capturing durable lessons, architectural patterns, and process improvements learned during complex, multi-stage projects.

## 📚 Core Principles of Resilient Pipelines

1.  **Configuration-First Design:** Always assume a central, canonical configuration schema (`base-service-config.json`) exists. Niche and operational logic must be built by merging/overwriting this base, never by hardcoding values.
2.  **Schema Validation:** Every data point (lead, profile, site content) must pass through a defined schema (`*.schema.json`) before being considered "complete."
3.  **Progressive Context Loading:** For large, multi-stage pipelines, always load context in phases: **Base Template $\rightarrow$ Niche Overrides $\rightarrow$ Dynamic/Lead Data**.
4.  **Geographic Resolution is Mandatory:** Never trust a raw string input for a location. The first action for any location-based task must be to pass the input through a structured Geocoder (e.g., Google Geocoding API) to ensure `{City, State, County, Zip}` structure.

## 🔧 Technical Pattern: The 3-Way Merge (New)

When combining data, the priority must be: **Dynamic Data > Niche Config > Base Config**.

*   **Base Config:** Defines the *possible* structure (the schema).
*   **Niche Config:** Defines the *default* values for a vertical (e.g., plumbing requires specific trust badges and service descriptions).
*   **Dynamic Data (Lead/Profile):** Overwrites everything else (the actual run-time values for a specific business).

## 💡 Skill Provisioning Protocol (AUTONOMOUS)

**EMERGENCY PROTOCOL:** When a necessary skill or capability is identified through project flow analysis, I am authorized to automatically:
1. **Identify:** Determine the missing piece.
2. **Design:** Draft the full specification (`SKILL.md`) and implementation (`.py` file) for the skill.
3. **Provision:** Write all necessary files to the correct directory (`skills/` or `config/`) and update the documentation (`README.md`, `TODO.md`) to reflect the new asset.
I will notify the user of every skill I provision.

## 💡 Process Memory (From 2026-04-19)

*   **Lesson:** Skills can be silently overwritten with stub/simulation versions during development. Always git-diff skill files when debugging "no results" errors — the script may be structurally broken, not just misconfigured.
*   **Action:** After any session where new skills were generated or discussed, run `git diff --stat skills/` to confirm no regressions.
*   **Lesson:** `goplaces --json` outputs clean JSON to **stdout** and `next_page_token: <token>` to **stderr**. Parse stdout with `json.loads()` directly; extract token from `result.stderr`. Do NOT mix them — confirmed by running `goplaces ... > /tmp/out.txt 2> /tmp/err.txt` and inspecting both.
*   **Lesson:** Vercel CLI v51 requires `--scope <team-slug>` in non-interactive mode for team accounts. Without it, deploy fails with `action_required: missing_scope` — which can be silently swallowed if the route returns 200 regardless. Always return 4xx/5xx when all operations fail, even if some succeeded partially.
*   **Lesson:** Vercel CLI v51 outputs structured JSON to stdout (not bare URLs). URL extraction must parse `deployment.url` from the JSON block. The `Production:` line in stderr is a fallback. The old pattern of `lines.find(l => l.startsWith('https://'))` no longer works.
*   **Lesson:** Stamp positional metadata (rank, page) on results **as they are collected**, before deduplication. After dedup the original order is preserved but absolute positions would need re-derivation. Assigning `_map_rank = len(all_results) + j + 1` and `_map_page = current_page` inline during the page loop is the clean pattern.
*   **Lesson:** Google Places API requires **≥2 seconds** between page requests when using `nextPageToken`. Using 0.5s causes silent failures on page 3+ — goplaces exits non-zero, the loop breaks, and you get partial results with no visible error unless you log every failure explicitly.
*   **Lesson:** For long-running `spawnSync` calls (lead hunt, enrichment), calculate the realistic worst-case duration before setting the timeout. Formula: `pages × page_sleep + leads × detail_call_time`. For 100 leads: 5 × 2s + 100 × 2s = 210s minimum — well over the default 180s.
*   **Lesson:** `turbopack.root` in `next.config.ts` overrides the module resolution root. Setting it to the workspace root instead of the `app/` dir causes `tailwindcss` and all `node_modules` to fail to resolve. Never set `turbopack.root` unless intentionally hosting a monorepo.
*   **Lesson:** `GOOGLE_PLACES_API_KEY` must be in `app/.env.local` (not just shell env) so the Next.js server process inherits it when spawning Python skill subprocesses via `spawnSync`.
*   **Lesson:** When `execSync` throws (non-zero exit), `e.message` only contains `"Command failed: <full command>"` — the actual CLI output is in `e.stdout` (when `2>&1` is used) or `e.stderr` separately. Always read `e.stdout ?? e.stderr` from the error object, not `e.message`, to surface real error details to the user.
*   **Lesson:** `vercel` CLI must be invoked as `npx vercel` (not bare `vercel`) when called from a Next.js server process via `execSync`. The Next.js process PATH does not include global npm binaries; `npx` resolves from local `node_modules/.bin/vercel` automatically.

## 💡 Process Memory (From 2026-04-19 session 12)

*   **Lesson:** Vercel preview deployments on team plans are auth-gated — they return 401 to unauthenticated visitors. For prospect-facing sites, always deploy with `--prod`. Production URLs (`https://<project>.vercel.app`) have no auth gate.
*   **Lesson:** Without `--name <project>` in the Vercel CLI call, Vercel derives the project name from the directory name, not from any variable you calculate. The `vercel_project_id` column was storing our calculated name while Vercel used a different one. Always pass `--name`.
*   **Lesson:** Vercel CLI uses `\r` (carriage return) for progress updates. When stdout+stderr are merged via `2>&1`, progress text can appear directly adjacent to URLs in the captured string (e.g., `...vercel.appBuilding...` — no whitespace between them). The `\S+` regex does NOT stop at `\r`. Fix: split output on `/[\n\r]+/` and match URLs with `/https:\/\/[a-zA-Z0-9-]+\.vercel\.app/` (hard stop at domain boundary).
*   **Lesson:** Apply the `.vercel.app` hard-stop regex to ALL URL extraction paths (JSON parse path AND fallback line-scan path) to prevent any future concatenation bugs.

## 💡 Process Memory (From 2026-04-19 session 13)

*   **Lesson:** `booking_url` (and any settings value needed by the Python factory) must cross the Node→Python boundary via the profile JSON payload. Inject it as a reserved key (`profile._bookingUrl`) in the generate route; read it in `generate_site()` before building site_config, then set `site_config.cta.bookingUrl`. Do not rely on environment variables inside the factory — the subprocess doesn't inherit the DB state.
*   **Lesson:** React Router intercepts all `<a>` clicks for hrefs that match its route table, even when those hrefs point to standalone HTML files. Fix with a capture-phase click listener on `document` that matches `/services|locations|privacy|terms` and sets `window.location.href` directly, before React Router sees the event. This is the only reliable escape hatch from a pre-built React bundle.
*   **Lesson:** Title-based slugification is fragile. "ReRoofs & Replacements" → `reroofs-replacements` works today but any change to the slugifier breaks the href↔filename↔vercel.json triad. Add an explicit `slug` field to every item in the niche config JSON and use it everywhere. Never derive slugs at runtime from display names.
*   **Lesson:** Stripe's list APIs return all objects — use them to find existing products/prices before creating new ones. Match products by name, prices by product ID + unit amount. Payment links are matched by fetching line items per link. This makes the setup script idempotent and safe to re-run after partial failures.
*   **Lesson:** When generating per-client Stripe payment link URLs, append query params (`?prefilled_email=X&client_reference_id=lead_N`) to the base payment link URL in the sequence builder, not at the Stripe API level. Payment Link objects are shared; client-specific data goes in the URL.

## 💡 Process Memory (From 2026-04-18)

*   **Lesson:** Hardcoded strings or assumed location formats break the system. Explicit schema enforcement and resolver skills are necessary for robust scaling.
*   **Action:** All agents must check if a `geo-resolver` skill is available and use it when location is an input.

## 💡 BevPro Site Development (2026-05-05)

### Footer Editing

*   **Footers use single-line format.** Most page footers use `<p className="text-[#B8A88A] text-sm">Premium beverage catering.<br />Atlanta, Georgia.</p>` on one line. When batch-editing across pages, match the exact single-line format — multiline `oldText` won't match.

### Component Constraints

*   **`RevealSection` only accepts `className`.** It does NOT pass through `id` or `style`. When a scroll anchor or custom background is needed, wrap with `<section id="foo">` or `<div>` and nest `RevealSection` inside.

### Service Updates

*   **Adding a service requires a checklist.** Update: page headings (count changes), service lists in all footers, JSON-LD `OfferCatalog`, SEO meta keywords, README.md, ideas.md, Contact form dropdown, Terms sections, Privacy references. Miss any one and the site reads inconsistently.

### SEO Structure

*   **Heading hierarchy must be verified after structural changes.** Run `grep "<h[1-6]" <file>` to confirm H1→H2→H3→H4 flow with no skipped levels. The "Who We Serve" cards were found using `<h5>` — promoted to `<h3>` to fix the skip.
*   **NAP signals belong in body text, not just the footer.** Linked phone and email in the service area section improve local SEO. Use `<a href="tel:...">` and `<a href="mailto:...">` with the site's accent color.