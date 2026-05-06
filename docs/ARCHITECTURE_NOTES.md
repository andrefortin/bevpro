# ARCHITECTURE NOTES - System Evolution Log

## 📘 Architectural Principles (The Prime Directives)

1.  **Local-First Persistence:** All critical state, caching, and history must reside in local databases (SQLite) or local filesystems. Cloud/API storage is treated as a high-latency, non-essential source of truth.
2.  **Modularity First:** No single function should handle more than one responsibility. All services must be exposed via distinct, dedicated skills (e.g., `lead-hunter-local`, `site-factory-local`, etc.).
3.  **State Machine Driven:** The entire workflow must be modeled as a state machine, ensuring that no action can occur without a valid, auditable preceding state.
4.  **Self-Correction:** The system must not only identify flaws (Audit) but also propose and execute the fix (Self-Correction Loop).

## ♻️ Core Pipeline Flow (The Loop)

1.  **Input:** Niche/City $\rightarrow$ (Skill: `lead-hunter-local`) $\rightarrow$ List of Raw Leads
2.  **Data Validation:** (New Step) $\rightarrow$ `schemas/data_validator.py` $\rightarrow$ Validated Leads
3.  **Enrichment:** (Skill: `business-enricher-local`) $\rightarrow$ Profile JSON
4.  **Deep Scrape:** (Skill: `deep-scrape-local`) $\rightarrow$ Contextual Data Overlays
5.  **Template Selection:** (UI/Logic) $\rightarrow$ Template Name/Config
6.  **Generation:** (Skill: `site-factory-local`) $\rightarrow$ Optimized HTML/React Code
7.  **Review & Optimize:** (UI/Logic) $\rightarrow$ `SEO Optimizer` (Self-Correction Loop) $\rightarrow$ Final Code
8.  **Deployment:** (Skill: `vercel-cli`) $\rightarrow$ Live Site URL
9.  **Outreach:** (Skill: `outreach-launcher-local`) $\rightarrow$ Campaign State Update

## 💡 Key Improvements Implemented

*   **Schema Contract:** Mandatory data structure contract enforced between enrichment and generation.
*   **State Tracking:** `outreach-launcher-local` now manages a full state machine (Drafted $\rightarrow$ Sent $\rightarrow$ Replied $\rightarrow$ Failed).
*   **Actionable UI:** The dashboard now provides a dedicated `Action Checklist` to guide the human operator on necessary fixes.

## 🚀 Next Architectural Focus
The next major phase must be integrating the full *Response Handling Loop* to complete the cycle. This requires connecting the `outreach-launcher-local` skill to a real-time monitoring system for replies.
