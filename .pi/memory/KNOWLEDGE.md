# KNOWLEDGE.md - FieldLaunch Project Knowledge Base

This file stores canonical, technical, and project-specific knowledge relevant to the FieldLaunch project and its surrounding systems.

## Core Systems
- **Primary Domain:** Local service business lead generation.
- **Key Components:**
    - `hunt` (Lead identification/scraping)
    - `enrich` (Business profile enrichment)
    - `generate` (Website/Site generation)
    - `deploy` (Hosting/Deployment)
    - `outreach` (Outbound communication)
- **Data Stack:** Python, SQLite, Next.js, Vercel.

## Technical Standards
- All generated sites must adhere to modern accessibility (WCAG 2.1 AA).
- Use of schema markup is mandatory for local SEO targeting.
- **Optimization Note:** Always check for rate limits when running `hunt` and `enrich`.

## Project Scope Changes
(Log changes here for historical context)
