# Lead Hunter Skill
## Description
Find local service-area businesses with missing, weak, broken, directory-only, or social-only web presence. Use when sourcing prospects by niche and city for FieldLaunch-style site generation and outbound sales workflows.

**Mandatory Pre-Processor (MANDATORY):** The first step in any lead hunt must be to call the `geo-resolver-local` skill to standardize the input location string, ensuring reliable coordinates before calling the Google Places API.

## Workflow
1. **Resolve Location:** Call `geo-resolver-local` using the input location string.
2. **Search:** Use the resolved coordinates and the specified niche/radius to query Google Places API.
3. **Filter & Output:** Deduplicate and structure the resulting leads, returning them as a JSON list.

## Parameters
- `niche`: The service category (e.g., roofing, plumbing).
- `city`: The raw location string (e.g., "Austin, TX area").
- `limit`: The maximum number of leads to retrieve.

---
*This skill is the entry point for all lead sourcing.*