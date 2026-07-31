# BevPro — Swarm OS Prime

**Premium Beverage Catering & Mixology Classes website** — React SPA for BevPro LLC (Atlanta mobile bar service: alcohol catering, coffee bars, mocktails, wine tastings, mixology workshops, bartender training).

---

## Core Identity

```
BevPro is a marketing funnel, not a SaaS.
Goal: convert visitors → quote requests / intake forms.
5-agent swarm (orchestrator → lead → worker-1/worker-2 → qa-agent) handles site work.
```

## Quick Start

```bash
# Dev / build
cd ~/batcave/bevpro && pnpm dev          # Vite (root: client/)
pnpm build                                # prod build → dist/ (TS errors block)

# Agents (managed via worker_pi.py)
cd ~/batcave/swarm-os
python3 shared/worker_pi.py orchestrator --project bevpro
python3 shared/worker_pi.py lead --project bevpro
python3 shared/worker_pi.py worker-1 --project bevpro
python3 shared/worker_pi.py worker-2 --project bevpro
python3 shared/worker_pi.py qa-agent --project bevpro

# Dispatch a task (meta-orchestration)
python3 -c "from lavinmq.dispatch import TaskDispatch; d=TaskDispatch(); d.push('bevpro', 'orchestrator', {'task_id':'TASK-TEST-001','title':'Test task','action':'execute'})"

# Ask bevpro a question
python3 -c "from lavinmq.swarm import SwarmOrchestrator; s=SwarmOrchestrator(); print(s.ask('bevpro','orchestrator',{'action':'query_context','payload':{'question':'Status?'}}, timeout=10))"
```

## Stack
React 19 · TypeScript 5.6 · Vite 7 · Tailwind v4 · shadcn/ui (new-york) · wouter (patched) · RHF+zod · framer-motion · Express static server

## Key Files
| Path | Purpose |
|------|---------|
| `client/src/App.tsx` | Router + providers |
| `client/src/index.css` | Green/gold palette, double-bezel cards, cubic-bezier |
| `client/src/pages/Intake.tsx` | 14-question quote funnel (RHF + zod) |
| `client/index.html` | Fonts, JSON-LD schema, SEO meta |
| `server/index.ts` | Express static server (prod) |
| `.pi/agents/*.md` | 5 swarm agent configs |
| `.pi/memory/*.md` | SOUL / KNOWLEDGE / EXPERTISE / PROTOCOL / TODO |

## Rules
- Preserve brand (green/gold, double-bezel) — see KNOWLEDGE.md design system
- `pnpm build` must pass before claiming done
- Mobile-first; Groupon CTA + quote funnel untouched unless asked
- Escalate: deploys, paid services, DNS, external comms
