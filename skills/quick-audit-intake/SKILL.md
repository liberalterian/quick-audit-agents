---
name: quick-audit-intake
description: Validate and normalize a Quick Audit intake payload before enrichment.
---

# Quick Audit Intake Skill

## Inputs

A JSON intake payload containing submission ID, timestamp, business name, website, city, state, revenue band, contact details, and Tracker row ID.

## Required fields

- `submission-id` or `submission_id`
- `business-name` or `business_name`
- `website`
- `primary-city` or `primary_city`
- `state`
- `annual-revenue-band` or `annual_revenue_band`
- `contact-name` or `contact_name`
- `contact-email` or `contact_email`
- `tracker-row-id` or `tracker_row_id`

## Actions

1. Parse JSON from the Routine `text` field.
2. Normalize keys to dash-case internally.
3. Validate state is a US state abbreviation.
4. Normalize website to absolute HTTPS URL when possible.
5. Generate `business-slug` in dash-case.
6. Return a run context object.

## Failure

If required fields are missing, write a structured validation error and stop the run before enrichment.
