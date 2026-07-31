# BevPro — TODO

> Last updated: 2026-07-31

## ✅ Bootstrapped (2026-07-31)
- [x] Swarm OS registration (MQ queues, registry, routing table, DB tasks)
- [x] 5 canonical agents (orchestrator, lead, worker-1, worker-2, qa-agent)
- [x] .pi structure complete (agents, extensions, memory, prompts, skills, tasks, reviews, sessions, specs)
- [x] Extensions: cost-tracker.ts, model-fallback.ts
- [x] settings.json (canonical forge-writer format)
- [x] Memory files rewritten with real bevpro content (was stale FieldLaunch)
- [x] prime.md → Swarm OS style with worker_pi commands

## 🔄 In Progress
- [x] ~~Verify agents actually execute via worker_pi.py end-to-end (dispatch a test task)~~ ✅ DONE 2026-07-31 — TASK-BOOT-E2E-03 completed in 14s ($0.0004), result in performance ledger, worker stable

## 🚀 Next
- [ ] Review site pages against current live production (visual regression)
- [ ] Confirm deploy pipeline / hosting for bevpro (see EXPERTISE.md — needs real deploy docs)
- [ ] Consider graphify code graph for bevpro (.graphify/ exists — verify it's current)

## ✅ Form → Email Pipeline (2026-07-31)
- [x] Wire Intake + Contact forms to POST /api/intake + /api/contact
- [x] Deploy Vercel functions (fixed ERR_MODULE_NOT_FOUND — shared code in api/ with .js imports)
- [x] Sender = info@mybevpro.com (Workspace app password in Vercel env)
- [x] Tested: honeypot 200/no-send, validation 400, real send 200 ✅

## 🚀 Next (unchanged)
