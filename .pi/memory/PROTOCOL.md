# PROTOCOL.md — BevPro Working Process

## Feature Development Checklist
- [ ] Read `client/src/App.tsx` first — know the route graph before touching pages
- [ ] Check `client/src/components/ui/` for an existing shadcn component before writing new UI
- [ ] Preserve green/gold palette + double-bezel cards (index.css) — no new color systems
- [ ] Keep forms react-hook-form + zod (Intake is the pattern reference)
- [ ] Run `pnpm build` before claiming done — TypeScript errors are blockers
- [ ] Verify mobile breakpoint (marketing funnel is mobile-heavy)

## Content / SEO Checklist (marketing site)
- [ ] JSON-LD schema in `client/index.html` stays in sync with NAP (name/address/phone)
- [ ] Page titles/meta per route — no duplicate titles across pages
- [ ] Groupon CTA and quote-request funnel untouched unless asked

## Anti-Patterns — What NOT to Do
- Do NOT inline new Tailwind palettes — extend the existing `@theme` in index.css
- Do NOT add heavy deps for what wouter + React already do
- Do NOT hardcode Unsplash URLs outside `lib/images.ts`
- Do NOT bypass the wouter patch (breaks prod routing)
- Do NOT restructure App.tsx routing without checking all links/CTAs

## Swarm OS Routing
- Orchestrator classifies → lead delegates → worker-1 generates / worker-2 gates → qa-agent approves
- Escalate to Andre for: deploys, paid services, DNS/domain, external comms
