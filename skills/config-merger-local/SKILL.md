# Config-Merger Skill
## Description
A universal service for performing a structured, three-way merge on configuration objects. This skill ensures data integrity by enforcing a strict merge hierarchy: Dynamic Lead Data > Niche Specific Configuration > Base System Configuration. It is mandatory for all site generation pipelines to guarantee consistency and prevent hardcoded values.

**Merge Priority (High to Low):**
1.  **Dynamic Data:** Runtime data from the specific lead/profile (highest priority, always overwrites).
2.  **Niche Configuration:** Service-specific defaults (e.g., roofing requires specific hero copy/badges).
3.  **Base Configuration:** The core, system-wide template default (lowest priority, fallback).

## Usage
Use when generating site content, configuring services, or merging any three distinct data layers.

## Parameters
- `base_config`: The general, non-niche-specific template defaults (JSON object).
- `niche_config`: The specific industry-specific overrides (JSON object).
- `dynamic_data`: The current lead or profile data (JSON object).

## Output
A single, validated, merged configuration object ready for template consumption.

## Implementation Notes
This skill relies on the calling skill to validate the schemas provided in the input arguments before merging.

---
*This skill centralizes the core logic of the entire FieldLaunch platform.*