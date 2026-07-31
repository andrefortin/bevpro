# EXPERTISE.md — BevPro Operations

## Dev Server
```bash
cd ~/batcave/bevpro
pnpm install          # first time (pnpm-lock.yaml exists)
pnpm dev              # Vite dev server (root: client/)
```

## Build / Deploy
```bash
pnpm build            # builds dist/ (vite build)
pnpm start            # if script exists: Express static server (server/index.ts)
```

## Common Fixes
- **wouter routes 404 in prod** — `patches/wouter@3.7.1.patch` must be applied; re-run `pnpm install` if lockfile changes
- **Tailwind v4 class issues** — palette + card treatments live in `client/src/index.css`; check `@theme` block before adding utility overrides
- **Images broken** — `client/src/lib/images.ts` holds Unsplash URLs; verify against live Unsplash (they rotate)

## Swarm OS Agent Commands
```bash
# Run bevpro agents via worker_pi.py (from swarm-os)
python3 shared/worker_pi.py orchestrator --project bevpro
python3 shared/worker_pi.py lead --project bevpro
python3 shared/worker_pi.py worker-1 --project bevpro
python3 shared/worker_pi.py worker-2 --project bevpro
python3 shared/worker_pi.py qa-agent --project bevpro

# Queue health
cd ~/batcave/swarm-os && python3 -c "from lavinmq.topology import ForgeTopology; print(ForgeTopology().queue_summary())"
```

## Health Checks
- `systemctl --user status swarm-mission-control.service` — Swarm OS alive
- `curl -s -H "Authorization: Bearer $KEY" http://localhost:8920/api/overview` — dashboard
- `pnpm build` exit 0 — site compiles
