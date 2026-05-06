# Geo-Resolver Skill
## Description
A critical skill for normalizing location inputs. Use this when any process requires a structured `{City, State, County, Zip, GeoCoordinates}` from a free-text location string (e.g., "Downtown area near the Capitol" or "Gloucester, ON"). This skill acts as a mandatory pre-processor for all `lead-hunter-local` and `business-enricher-local` inputs.

**Mandate:** Never accept a location string without first calling this skill.

## Parameters
- `location_string`: The raw, user-provided location (e.g., "Near the Capitol" or "Austin, TX").
- `api_key`: The required API key for the geocoding service (e.g., Google Maps API key).

## Output
A standardized, structured JSON object containing the resolved components, coordinates, and confidence score.

## Implementation Details
This skill must wrap an external geocoding API call and handle failure by returning the original input and a low confidence score, flagging it for manual review.

---
*This skill is foundational to the entire FieldLaunch pipeline, ensuring all location inputs are standardized.*