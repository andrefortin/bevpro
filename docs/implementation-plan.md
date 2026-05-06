# FieldLaunch Implementation Plan

## Project Name
- FieldLaunch

## Goal
- Build a repeatable system to find service-area businesses with weak or missing websites, generate tailored preview sites, publish them publicly, and sell them through outbound outreach.

## Phase 1 - Foundation
- define niche-specific qualification rules
- define lead schema
- define business profile schema
- define generated site schema
- define outreach event schema
- define preview labeling policy
- define compliance rules for email, SMS, and phone outreach

## Phase 2 - Skills + Reusable Components
- create `lead-hunter-local`
- create `business-enricher-local`
- create `site-factory-local`
- create `outreach-launcher-local`
- create niche website component blocks
- create service-business site template system

## Phase 3 - MVP Build
- source leads for one niche in one market
- enrich leads
- score leads
- generate preview sites
- deploy previews to public URLs
- prepare outreach sequences
- track replies and conversions

## Phase 4 - Operator Loop
- build a simple queue/dashboard
- approve or reject generated sites
- approve outreach before send
- track outcomes by niche and market

## Recommended MVP Constraints
- first niche: roofing
- first market: one metro
- first outbound channel: email
- preview sites must be clearly marked as previews until sold

## Immediate Build Order
1. schemas
2. first skill set
3. first reusable site template
4. first sample business profile JSON
5. first generated preview site pipeline

## Deliverables I am building now
- project folder scaffold
- planning docs
- schemas
- first skills
- first reusable website template starter
