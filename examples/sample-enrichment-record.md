# Sample Enrichment Record

```json
{
  "company": {
    "name": "Example Services",
    "city": "Denver",
    "state": "CO",
    "website": "https://example-services.test",
    "place-id": "places/example",
    "gbp-primary-category": "Plumber",
    "gbp-claimed": true,
    "review-count": 240,
    "average-rating": 4.7
  },
  "enrichment": {
    "cms-detected": "WordPress",
    "has-ssl": true,
    "pagespeed-mobile": 72,
    "domain-rating": 18,
    "referring-domains": 112,
    "organic-keywords": 86,
    "organic-traffic-estimate": 420,
    "data-unavailable": []
  },
  "sources": [
    {"field": "review-count", "source": "Google Places Details"},
    {"field": "domain-rating", "source": "Ahrefs MCP"}
  ]
}
```
