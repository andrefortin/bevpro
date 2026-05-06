# Business Enricher Skill
## Description
Enrich local service business leads using Google Business Profile and public web data. Use when preparing structured business profiles for generated preview websites, niche site templates, and outbound personalization.

**Mandatory Pre-Processor (MANDATORY):** The first step in any enrichment process must be to call the `geo-resolver-local` skill to standardize the location input. This ensures the enrichment data is tied to reliable coordinates.

## Workflow
1. **Resolve Location:** Call `geo-resolver-local` using the input location string.
2. **Fetch Data:** Use the resolved location and lead ID to query Google Business Profile and public web data sources.
3. **Structure & Enhance:** Populate the structured business profile JSON, ensuring source attribution is maintained for every data point.

## Parameters
- `lead_id`: The unique ID of the lead being enriched.
- `location_string`: The raw, user-provided location string.
- `api_key`: The required API key for the enrichment service.

---
*This skill turns a raw lead into a fully structured, usable business profile.*