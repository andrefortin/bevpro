---
name: outreach-launcher-local
description: Send outreach emails (and later SMS/voice) to business prospects for FieldLaunch campaigns. Use when initiating or sending approved outreach messages tied to a deployed preview site.
---

# Outreach Launcher Local

Send email outreach to local business prospects who have been identified as leads and have a deployed preview site.

## Output Goal
- Draft personalized outreach messages for each lead
- Respect approval mode (per-lead, batch, full-auto)
- Track send status and replies
- Support email now; SMS and voice as future channels

## Standard Workflow
1. Receive lead contact info + deployed site URL
2. Generate a personalized outreach message (subject + body)
3. Queue event as `pending` in the database
4. If approval mode allows, send immediately; otherwise wait for approval
5. Update status to `sent` or `failed`

## Message Rules
- Mention the specific preview site URL
- Do not claim the site is already live for the business
- Be brief, direct, and professional
- Avoid spam trigger words
- Always provide opt-out instructions

## Channels
- `email`: SMTP via nodemailer (configured via SMTP_HOST, SMTP_USER, SMTP_PASS env vars)
- `sms`: Twilio (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) — Phase 2
- `voice`: Twilio Programmable Voice — Phase 3

## Approval Modes
- `per-lead`: Each outreach event must be individually approved before sending
- `batch`: All events created first, then approved as a group
- `full-auto`: Events created and sent immediately without human review

## Environment Variables Required
- `SMTP_HOST` — SMTP server (e.g. smtp.gmail.com)
- `SMTP_PORT` — SMTP port (default 587)
- `SMTP_USER` — SMTP username / email
- `SMTP_PASS` — SMTP password / app password
- `SMTP_FROM` — From address (defaults to SMTP_USER)
