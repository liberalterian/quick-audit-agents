# Quick Audit — End-to-End Automation Plan

**Prepared by:** Claude, for Daniel Goodrich
**Date:** May 21, 2026
**Purpose:** Hands-off automation from SPP intake through Quick Audit delivery, with a parallel MVS qualification check that routes high-fit prospects to the team for an in-person meeting.

**Note:** v1 was corrected several times mid-build. The current version reflects all corrections: minimal SPP intake (eight fields), self-reported revenue with a soft-fail band, US-only lock, hard-fail on LSA-eligible vertical, and the **Quick Audit narrative .md** as the single deliverable. The Digital Presence Scorecard exists in the S&C portfolio as a separate artifact, but it isn't part of this pipeline — cohort comparison, letter grades, and the 4-category scoring rubric are Scorecard concepts, not Quick Audit ones.

---

## The Shape of the System

The prospect submits a short SPP form. From that submission, the **Audit Agent** gathers everything it needs — website crawl, GBP, PageSpeed, Ahrefs data, social profiles, ads transparency, live brand and pack SERPs — and produces a Quick Audit (.md). The **Qualification Agent** reads the same enrichment record the Audit Agent built and applies the MVS rubric. The Audit Agent always delivers the Quick Audit. The Qualification Agent decides whether the team gets emailed, and on which routing path (qualified, soft-fail, not qualified).

```
SPP Intake (minimal)
        │
        ▼
Intake Record  ──►  Audit Agent  ─────────►  Quick Audit (.md)  ──►  Prospect Inbox
        │                                          │
        │                                          ▼ (enrichment record available here)
        │
        └─────────►  Qualification Agent (consumes enrichment)
                              │
                              ├─ Hard PASS  ──► Team Email: "Qualified Prospect"
                              ├─ Soft FAIL ──► Team Email: "Marginal — needs human review"
                              └─ Hard FAIL ──► No alert. Report ships. End.
```

The single most important architectural decision: the Audit Agent collects all the data first, the Qualification Agent reads from that same enrichment record. No double-pulling. The qualification decision uses the same `gbp_claimed`, `review_count`, `avg_rating`, and GBP primary category data that the Quick Audit references.

---

## Section 1: SPP Intake — Minimal

The prospect provides only what's needed to identify the business unambiguously and deliver the report. Everything else — review counts, GBP claim status, ad spend, social handles, schema, PageSpeed, organic traffic — the Audit Agent fetches itself. Asking the prospect to do that work undermines the whole value proposition of a Quick Audit: *we do the work for you*.

### The Fields

| # | Field | Type | Required | Why |
|---|---|---|---|---|
| 1 | Business name | text | Yes | Brand search anchor, GBP fuzzy-match target |
| 2 | Primary website URL | URL | Yes | Anchor for crawl, PageSpeed, schema, source-code, ads-transparency lookup |
| 3 | Primary city | text | Yes | Local-pack search target, peer-cohort scope, GBP disambiguation when multiple locations share a name |
| 4 | State | select | Yes | Disambiguation + US-only confirmation (see below) |
| 5 | Annual revenue (range) | select (<$500K, $500K–1M, $1M–1.5M, $1.5M–2M, $2M–5M, $5M–10M, $10M+) | Yes | Self-reported; feeds the MVS qualification rubric directly. Removes any need for the agent to estimate revenue from external signals. |
| 6 | Contact name | text | Yes | Email salutation |
| 7 | Contact email | email | Yes | Report delivery + qualified-prospect follow-up |
| 8 | Contact phone | tel | Optional | Backup channel; used in the team alert if the prospect qualifies |

That's the form. Eight fields. The agent fills the rest in.

The one field that "asks the prospect to do work" is annual revenue — and it's a range select, not an exact figure. The trade-off is worth it: self-reported revenue makes the qualification rubric deterministic on its hardest-to-infer criterion. Without it the agent has to estimate from LinkedIn FTE counts, GBP fleet photos, and review velocity, all of which are noisy enough to push the band wider than is useful.

### What the Agent Fills In (not asked of the prospect)

For reference — these are signals the Audit Agent will collect via its tooling chain, not via intake:

- GBP URL / Place ID (resolve from business name + city via Google Places)
- GBP review count, rating, photo count, categories, claim status, recent posts
- Number of locations (GBP query)
- Social profile URLs (discover via brand search + footer crawl)
- Schema markup status (view-source)
- PageSpeed score (PSI API or Chrome to pagespeed.web.dev)
- Active Google Ads (Ads Transparency Center)
- Active Meta Ads (Meta Ad Library)
- Organic keyword count / DA / referring domains (Ahrefs MCP, fallback DataForSEO)
- LSA category eligibility (mapped from GBP primary category)

### US-Only Lock

MVS is US-only. SPP's standard signup already collects address/region during account creation, which provides a US-country gate at the platform layer. Add a single confirmation in the audit intake's submit-screen language: "Quick Audit is currently available for US businesses only." If a non-US business submits anyway, the Audit Agent's first sanity check — resolving the business via Google Places against a US state code — fails, and the workflow terminates with a polite "we don't currently serve [country]" email instead of running the audit.

No country picker on the form. No "are you US-based?" checkbox. The state field plus the SPP signup gate handle it.

---

## Section 2: The Audit Agent

Produces a single deliverable: **the Quick Audit (.md)**. Six numbered Checks, each ending with a Revenue Translation paragraph; a Headline finding at the top; a What To Fix First priority table; a Glass Half Full closing section. Modeled on the S&C client Quick Audits in `Claude Outputs/S&C/<Client>/<Client>_Quick-Audit_v1.md`.

### Output Format: Quick Audit (canonical)

Filename: `<BusinessName>_Quick-Audit_v1.md`

**Structure (strict — every Quick Audit in the S&C portfolio matches this):**

**Title and sub-header**

```
# <BusinessName> — Quick Audit

**<City, State> · <Services/Industry list> · Audited YYYY-MM-DD**

A fast, honest read on what your digital presence is actually showing potential customers — and the dollar value tied to fixing it.

---
```

The one-sentence promise under the sub-header is literal text, identical across every Quick Audit. It's part of the format, not a per-prospect rewrite.

**Headline finding** — One paragraph (2–6 sentences) naming the dominant insight. This is the most important paragraph in the document — it frames everything that follows. Two patterns surface across the S&C portfolio:

- *"You've built X strength. The bottleneck is Y. Closing that gap is mechanical."* (TennCrete, Cheetah Screens) — when there's real foundation to amplify.
- *"Your GBP points at a broken website."* / *"Your knowledge panel says you're not open."* (SAPS Exteriors, Apollo Beach) — when there's a structural break worth leading with.

The agent picks the pattern that matches what the enrichment surfaces. Don't force a "you've built something strong" headline onto a prospect whose GBP is unclaimed.

**Check 1: Brand Search**

What surfaces when someone Googles the business by name. Captures:
- Knowledge panel state (claimed, review count + rating, categories, hours, phone)
- Top organic result (is it the business's own site?)
- Social profile presence on page 1 (Facebook, Instagram, YouTube)
- Any NAP inconsistencies (phone differences, name-spelling drift across surfaces)
- Any competing-brand domains that surface (e.g., the targetpaintingca.com problem)

Ends with: `**Revenue translation:**` paragraph tying findings to lost-call/lost-form-fill risk.

**Check 2: Page Performance — homepage on mobile**

The literal H2 line in the doc is *"Check 2: Page Performance — homepage on mobile"*. Captures:
- Mobile PageSpeed score (absolute, with bounce-risk framing for low scores)
- Core Web Vitals status (Passed / Mixed / Failed)
- SSL status (yes/no)
- Mobile-friendly (verified via viewport meta + responsive layout check)
- Tech stack (WordPress, Squarespace, etc.)
- Visible quality issues (template placeholders, broken images, duplicate content)

Ends with: `**Revenue translation:**` quantifying mobile-bounce loss at the observed score level.

**Check 3: Source Code — what Google's bots see**

The literal H2 line is *"Check 3: Source Code — what Google's bots see"*. Captures:
- Schema markup types present (LocalBusiness, HomeAndConstructionBusiness, AggregateRating, Service, BreadcrumbList) and what's missing
- Meta description (managed by what, customized or default)
- Analytics installed (GA4 measurement ID + GTM container ID when discoverable)

Ends with: `**Revenue translation:**` framing schema work as one-time investment, CTR uplift on existing rankings.

**Check 4: Social Alignment — name + brand consistency across platforms**

The literal H2 line is *"Check 4: Social Alignment — name + brand consistency across platforms"*. Renders a 4-column table:

`| Platform | Listed Name | Activity | Notes |`

Rows cover: Website / GBP / Facebook / Instagram / YouTube / HomeAdvisor / Yelp / phone-everywhere. Followed by 2–4 bullet points of cleanup items (name reconciliation, dormant page handling, missing-platform gaps).

Ends with: `**Revenue translation:**` paragraph on entity-consolidation signal value.

**Check 5: Top Non-Brand Keyword — "[keyword]"**

The H2 includes the actual keyword the agent searched. Captures:
- Local pack composition (numbered list, top 3-8 results with review count and rating for each)
- Where the target ranks (or doesn't — "not in visible top 8")
- The play to win: 2–3 numbered moves (review velocity, GBP categories, service-area content, citations)

Ends with: `**Revenue translation:**` paragraph quantifying ticket size in the local market + expected lead lift from pack-rank improvement.

**Check 6: Ads Transparency — paid presence**

The literal H2 line is *"Check 6: Ads Transparency — paid presence"*. Captures:
- Active Google ads (yes/no, from Ads Transparency Center)
- Active Meta ads (yes/no, from Meta Ad Library)
- Sequencing recommendation (e.g., "wait until GA4 conversion tracking is in" — calibrated to other check findings)

Ends with: `**Revenue translation:**` paragraph estimating local CPC + CPL ranges if paid were turned on.

**What To Fix First** — Priority table with 7–10 rows.

```
| Priority | Action | Owner | Timing | Why It Matters |
|---|---|---|---|---|
| 1 | **<verb-first action>** | Owner / Web developer / Office manager | <timing> | <leverage rationale> |
```

Rows are ranked by leverage, not sequence (items can run in parallel). Owner column is concrete (not "the team" — Owner via GBP dashboard / Web developer / Office or job manager). Timing is concrete (15 minutes / 1-2 hours / 90 days).

**Glass Half Full — what you're already doing right** — 8–12 bullets. Each ties an existing strength to a competitive advantage or future-leverage opportunity. *Genuine — write fewer rows rather than pad with consolation.* This is explicit in the S&C training prompt and visible across the portfolio: empty fields don't get filled with platitudes.

**Footer**

```
---

*Quick audit prepared by Local Service Spotlight.*
```

Some Quick Audits also include a Sources section above the footer with reference links (KTM Exteriors, Haaheo Masonry) — that's a stylistic variant, not part of the strict format. The "Companion document: Scorecard.docx" footer that appears in the S&C portfolio Quick Audits is dropped here because the Scorecard isn't part of this pipeline.

### Voice and Tone

The S&C training prompt is direct about this: *"confident, specific, conversational. Quote real numbers and competitor names when relevant. No hedging language. If you don't have enough information to make a claim, say so clearly rather than producing soft language."* No "highlighting" / "underscoring" / "showcasing" — concrete claims with the actual numbers. Revenue Translation paragraphs are where the prose earns its place: every check ends with one, and they each name a dollar consequence.

### Enrichment Record (internal)

The Audit Agent maintains an enrichment record per prospect — a structured JSON object the Qualification Agent reads from. It isn't a deliverable to the prospect; it's the working data the Quick Audit narrative cites. Minimum shape:

```json
{
  "company": {
    "name": "Business Name",
    "city": "City",
    "state": "TN",
    "website": "domain.com",
    "place_id": "ChIJ...",
    "gbp_url": "https://maps.google.com/...",
    "gbp_primary_category": "Concrete contractor",
    "gbp_secondary_categories": [],
    "phone": "+1XXXXXXXXXX",
    "address": "Full street address",
    "gbp_claimed": true,
    "review_count": 7,
    "avg_rating": 5.0,
    "photo_count": 2,
    "gbp_post_count_90d": 0
  },
  "enrichment": {
    "pagespeed_mobile": 92,
    "core_web_vitals_status": "passed | mixed | failed",
    "has_ssl": true,
    "is_mobile_friendly": false,
    "cms_detected": "WordPress",
    "ga4_measurement_id": "G-XXXXX",
    "gtm_container_id": "GTM-XXXXX",
    "has_chat_widget": false,
    "has_blog": false,
    "blog_post_count": 0,
    "schema_types_present": ["WebPage", "WebSite", "Organization", "BreadcrumbList"],
    "schema_types_missing_high_value": ["LocalBusiness", "AggregateRating", "Service"],
    "domain_authority": 22.2,
    "organic_traffic_est": 29,
    "keyword_count": 43,
    "referring_domains": 201,
    "backlink_count": 1095,
    "facebook_page_url": "...",
    "facebook_followers": null,
    "facebook_last_post_date": "...",
    "instagram_handle": "...",
    "youtube_url": null,
    "youtube_video_count": 0,
    "active_google_ads": false,
    "active_meta_ads": false,
    "brand_serp_snapshot": { "knowledge_panel_present": true, "top_organic_url": "...", "social_on_page_1": ["facebook", "instagram"] },
    "pack_serp_snapshot": { "head_keyword": "concrete contractor columbia tn", "pack_size": 3, "target_rank": 3, "top_results": [{"name": "AMC Concrete", "rating": 5.0, "reviews": 32}, ...] },
    "enriched_at": "..."
  }
}
```

The Quick Audit cites these fields by name in prose. The Qualification Agent reads `gbp_claimed`, `review_count`, `avg_rating`, `gbp_primary_category` directly.

### Peer Cohort Logic

For each industry slug (concrete, painting, screens, roofing, masonry, HVAC, plumbing, electrical, landscaping, etc.), the agent maintains a peer cohort scored on the same rubric. Cohort target: top 20 businesses in the same industry serving the same city/metro.

**Cohort construction:**
1. Map the prospect's GBP primary category to an industry slug. Build a category-to-slug crosswalk file — TennCrete → "concrete," Cheetah Screens → "screens," etc.
2. For the prospect's primary city, query Google Places (or Ahrefs SERP) for the top 20 results on the primary commercial keyword for that industry (e.g., "concrete contractor Franklin TN").
3. If fewer than 20 results exist locally, expand to the metro area (e.g., Nashville MSA for Franklin).
4. Score each peer using the same enrichment pipeline (cached if already scored within 90 days).
5. Compute averages, medians, and p75 across the cohort. Persist to the peer_stats block.

Two practical wrinkles:
- **First-of-industry prospects.** If the agent has never scored an industry slug before, the first prospect triggers a cohort build (20 peer scoring runs upfront, ~20 minutes per cohort). Subsequent prospects in the same industry+market reuse the cohort, refreshed every 90 days.
- **Low-density markets.** If even the metro expansion can't produce 20 peers, fall back to a national industry cohort with a noted methodology footnote in the Scorecard.

### JSON Sidecar Schema

Modeled directly on the S&C JSON output (e.g., `tenncrete_concrete_contractor_2026-05-04.json`). Persisted alongside the .docx in Google Drive and written to the Quick Audit Tracker sheet.

```json
{
  "company": {
    "company_id": "uuid",
    "name": "Business Name",
    "address": "Full street address",
    "city": "City",
    "state": "TN",
    "zip": "37067",
    "phone": "+1XXXXXXXXXX",
    "website": "domain.com",
    "gbp_url": "https://maps.google.com/...",
    "place_id": "ChIJ...",
    "review_count": 7,
    "avg_rating": 5.0,
    "photo_count": 2,
    "categories": ["Concrete contractor"],
    "gbp_claimed": true,
    "gbp_post_count_90d": 0,
    "created_at": "...",
    "updated_at": "..."
  },
  "enrichment": {
    "organic_traffic_est": 29,
    "keyword_count": 43,
    "domain_authority": 22.2,
    "referring_domains": 201,
    "backlink_count": 1095,
    "cms_detected": "WordPress",
    "has_analytics": true,
    "has_chat_widget": false,
    "pagespeed_mobile": 92,
    "core_web_vitals_status": "passed | mixed | failed",
    "has_ssl": true,
    "is_mobile_friendly": false,
    "has_blog": false,
    "blog_post_count": 0,
    "has_facebook": true,
    "facebook_page_url": "...",
    "facebook_followers": null,
    "facebook_posts_30d": null,
    "youtube_video_count": 0,
    "youtube_uploads_90d": 0,
    "has_instagram": false,
    "maps_rank_primary_keyword": 10,
    "enriched_at": "...",
    "pagespeed_attempted_at": "...",
    "pagespeed_error": null
  },
  "score": {
    "industry_slug": "concrete",
    "rubric_version": "targeted-v1",
    "maps_score": 11,
    "website_score": 11,
    "seo_score": 11,
    "social_score": 2,
    "total_score": 35,
    "letter_grade": "D",
    "next_grade": "C",
    "signals": [
      { "key": "...", "label": "...", "category": "maps|website|seo|social",
        "value": "...", "points": 0, "max_points": 8 },
      ...
    ]
  },
  "peer_stats": {
    "cohort_size": 17,
    "peer_review_avg": 143.5,
    "peer_review_avg_median": 11.0,
    "peer_review_avg_p75": 39.0,
    "peer_rating_avg": 4.6,
    ... [all the peer_* fields from the S&C exemplar]
  },
  "recommendations": [
    {
      "key": "review_count",
      "title": "Build your review base",
      "body": "You have 7 Google reviews; the typical Concrete peer in your market has 143.5...",
      "points": 8,
      "effort": "Substantial"
    },
    ...
  ],
  "industry_slug": "concrete"
}
```

### Sequence (Audit Agent)

```
Intake Record
   │
   ├─ Step 1: Identity Resolution             ── Google Places + Chrome (GBP knowledge panel)
   ├─ Step 2: Web Enrichment                  ── Chrome (homepage view-source, PSI) + Ahrefs MCP (site-explorer-*, organic-keywords) + tag-audit skill (analytics/tags)
   ├─ Step 3: Social Enrichment               ── Chrome (FB/IG/YouTube discovery + follower counts)
   ├─ Step 4: Brand Search Snapshot           ── Chrome (Google SERP for business name + city; knowledge panel state, top organic, social on page 1, NAP drift)
   ├─ Step 5: Live Pack Snapshot              ── Chrome (Google SERP for "[industry head term] [city]"; top 3-8 local pack with review counts and ratings; target's pack rank)
   ├─ Step 6: Ads Transparency Snapshot       ── Chrome (Google Ads Transparency Center, Meta Ad Library)
   ├─ Step 7: Signal Emit                     ── Write enrichment JSON to Tracker; signal Qualification Agent to run
   ├─ Step 8: Synthesis                       ── Pick Headline-finding pattern; generate What-To-Fix-First (7-10 rows ranked by leverage); generate Glass Half Full bullets
   ├─ Step 9: Render Quick Audit (.md)        ── Apply the strict 6-check format with Revenue Translation per check, table, Glass Half Full, footer
   └─ Step 10: Deliver                        ── Gmail MCP → prospect (.md attached or .pdf rendering); Drive → BlitzMetrics shared drive
```

### Step Detail

**Step 1 — Identity Resolution.** Query Google Places by business name + city + state. Resolve to a single Place ID. If multiple matches, pick the closest by website domain. If no match, the Quick Audit ships with the "your GBP isn't findable" Headline pattern.

**Step 2 — Web Enrichment.** Chrome navigates to the website. Captures CMS, SSL status, mobile-friendliness (viewport meta + responsive check), schema markup types via view-source, GA4 measurement ID + GTM container ID via tag-audit, chat widget, blog presence and post count. PSI returns mobile score + Core Web Vitals. Ahrefs MCP returns DA, organic traffic, keyword count, referring domains, backlink count. Captures visible quality issues for the Quick Audit (template placeholders, broken images, duplicate testimonials, "0+ years of experience" defaults).

**Step 3 — Social Enrichment.** Chrome searches "[Business Name] [City] Facebook," "[Business Name] [City] Instagram," "[Business Name] [City] YouTube." Captures profile URLs. Visits each: Facebook (followers, last post date), Instagram (followers, latest post date), YouTube (video count, uploads last 90 days). Falls back to "Unknown" — Quick Audit Check 4 names the gap explicitly.

**Step 4 — Brand Search Snapshot.** Chrome runs the literal Google search "[Business Name] [City]". Captures: knowledge panel state (claimed, reviews + rating, categories, hours, phone, address); top organic result URL; social profiles on page 1; any competing-brand domains. Used in Quick Audit Check 1.

**Step 5 — Live Pack Snapshot.** Chrome runs the literal Google search for the industry head term + city. Industry head term derived directly from the GBP primary category (e.g., "Concrete contractor" → "concrete contractor [city]"; "Roofing contractor" → "roofing contractor [city]"). No slug crosswalk — the GBP primary category is the source of truth. Captures: top 3-8 local pack composition with each result's name, review count, and rating; whether the target appears and at what rank. Used in Quick Audit Check 5.

**Step 6 — Ads Transparency Snapshot.** Chrome opens `adstransparency.google.com` and Meta Ad Library, captures presence/absence of active campaigns. Used in Quick Audit Check 6.

**Step 7 — Signal Emit.** Write the enrichment JSON to the Quick Audit Tracker row. Signal the Qualification Agent that the enrichment is ready — the Qualification Agent runs against this record in parallel with Steps 8–10.

**Step 8 — Synthesis.** Pick the Headline-finding pattern: "structural break" if `gbp_claimed = false`, the website is unreachable, or the GBP-listed website doesn't match the working website (SAPS Exteriors case); "foundation strength to amplify" if the prospect has real assets — strong DA, high review count, claimed GBP — but a specific bottleneck (TennCrete, Cheetah Screens cases); otherwise a balanced "here's what your digital presence looks like, here's what to fix first" headline. Generate What-To-Fix-First (7-10 rows). Each row: action (verb-first, bold), Owner (Owner via GBP dashboard / Web developer / Office or job manager), Timing (15 minutes / 1-2 hours / 90 days), Why It Matters (leverage rationale). Generate 8-12 Glass Half Full bullets from genuine strengths in the enrichment record — write fewer rather than pad.

**Step 9 — Render Quick Audit (.md).** Apply the strict 6-check format. Each Revenue Translation paragraph quantifies in the local market — ticket size in industry × pack-rank lift = expected leads, or schema CTR uplift = expected pipeline value, or specific CPC/CPL ranges for the ads-transparency check.

**Step 10 — Deliver.** Gmail MCP creates a draft (with the .pdf attached) addressed to the prospect; the draft sits in Drafts for human review and send (today's Gmail MCP exposes create_draft but not auto-send). Subject: `Your Quick Audit — <Business Name>`. Body language varies per qualification (Section 4). Drive saves the .md + .pdf in `Maps Visibility / Quick Audits / <Business Name>` folder.

### Failure Modes

- **GBP not found.** Quick Audit leads with the structural-break Headline pattern: "Your business doesn't have a findable Google Business Profile — that's the highest-priority finding on its own." Check 1 reads accordingly; other checks proceed where data is available.
- **Website unreachable.** Quick Audit Headline pattern goes structural: "Your website is currently not reachable — restore it before any other marketing work matters." Checks 2, 3, 5, 6 mark "data unavailable" rather than fabricating findings.
- **PSI throttling.** Retry once after 60s. If still failing, Check 2 says so explicitly.
- **Ahrefs MCP unavailable.** Fall back to whatever SEO data source is wired in. Quick Audit Check 3 notes "DA" as directional rather than absolute.

---

## Section 3: The Qualification Agent

Reads the enrichment record produced by the Audit Agent. Applies the MVS rubric. Emits a three-state decision: **Hard Pass**, **Soft Fail**, or **Hard Fail**.

### Decision Bands

| Criterion | Hard Pass | Soft Fail | Hard Fail | Source |
|---|---|---|---|---|
| **LSA-eligible vertical** | GBP primary category maps to an LSA-eligible category | — (no soft path) | Not LSA-eligible | [Google Local Services Help — US category list](https://support.google.com/localservices/answer/6224841?hl=en&co=GENIE.CountryCode%3DUS) |
| **Annual revenue (self-reported via intake)** | $2M+ band selected | $1.5M–$2M band selected | < $1.5M | LSS LP copy: "$2M+ in revenue" |
| **Google reviews + rating** | ≥ 200 reviews AND avg ≥ 4.5★ | 150–199 reviews at ≥ 4.5★ OR ≥ 200 reviews at 4.3–4.5★ | < 150 reviews OR avg < 4.3★ | LSS LP copy: "200+ five-star reviews" |
| **Home service vertical** (overlaps with LSA but stricter — home/contractor trades, not healthcare/legal) | HVAC, plumbing, roofing, electrical, painting, landscaping, concrete, masonry, pest, locksmith, garage door, drain, fencing, flooring, foundations, junk removal, kitchen/bath remodeling, lawn care, moving, pool, sewage, siding, snow removal, solar, tree, water damage, window — i.e., LSA "home service" subset | — | All other LSA-eligible (healthcare, legal, professional, wellness) | LSS "This Is Not For" exclusion list |
| **Established / operating** | Years in business ≥ 2 (estimated from domain age + GBP age + WHOIS) | — | < 2 years | LSS LP copy: "Startups or one-person operations" |
| **GBP claimed & verified** | `gbp_claimed = true` | — | `gbp_claimed = false` or GBP not findable | LSS LP copy: "Owners unwilling to provide access" — implied |
| **GBP API access (Manager invite accepted within 48h of report delivery)** | Confirmed access | — | Not granted | Required for MVS service delivery |

### Why Hard vs. Soft for Each

- **LSA-eligible vertical = HARD-FAIL.** MVS is built around Maps visibility for businesses where Maps is a primary lead source. If Google doesn't even let them run Local Services Ads in their category, the LSA-driven Maps strategy doesn't apply. Binary signal, no ambiguity, no soft path. Sourced directly from Google's published category list.
- **Revenue = SOFT-FAIL.** Self-reported, but kept in a band because (a) the published $2M bar isn't a cliff — a strong $1.7M business with high review velocity and tight ops can be a better fit than a sloppy $2.5M one, and (b) prospects round and bucket. A real $2.1M business filling in the form quickly may pick "$1.5M–2M" if it feels closer to the truth than "$2M–5M." Soft-failing the $1.5M–$2M band routes those cases to human judgment rather than auto-disqualifying. Sub-$1.5M is far enough below the bar that further investigation isn't worth team time.
- **Reviews + rating = SOFT-FAIL when close.** A 195-review prospect at 4.7★ is one good month of review-gen work from the bar. A 215-review prospect at 4.4★ has the volume but the rating's a yellow flag — the team should look. Hard-fail kicks in only when both the volume is well off (≤149 reviews) or the rating is clearly weak (<4.3★).
- **Home service vertical = HARD-FAIL.** Tighter than LSA-eligible — LSA includes dentists, lawyers, real estate. MVS is built for home services. Hard-fail because the marketing motion (review gen, GBP optimization, local pack ranking, Maps Posts) is calibrated for contractors and trades. We can revisit later if MVS expands.
- **Established / operating = HARD-FAIL.** A 6-month-old business doesn't yet have the review/citation foundation MVS amplifies.
- **GBP claimed/verified = HARD-FAIL.** Hard prerequisite for the service we'd actually sell them. If unclaimed, the Scorecard's first recommendation handles the gap and we can revisit at re-score in 90 days.
- **GBP access (post-delivery) = HARD-FAIL** after the report ships, only triggers the "we can't actually start MVS" branch — not the qualification decision itself. The Qualification Agent assumes "will probably grant access" because there's no way to check before the report goes out.

### Pass/Fail Logic

```
if any hard-fail criterion fails:
    decision = HARD_FAIL
elif any soft-fail criterion is in its soft band:
    decision = SOFT_FAIL
else:
    decision = HARD_PASS
```

Soft-fail accumulates: a prospect in the soft band on revenue AND in the soft band on reviews is still SOFT_FAIL — just with two flags instead of one. The team alert lists every soft signal so they can judge.

### Sequence (Qualification Agent)

```
Enrichment Record (from Audit Agent) + Intake Record (revenue from prospect)
   │
   ├─ Step 1: Apply hard-fail checks (LSA category, vertical, established, GBP claimed)
   │       If any fail → emit HARD_FAIL decision, exit.
   │
   ├─ Step 2: Evaluate self-reported revenue band (hard pass / soft fail / hard fail)
   ├─ Step 3: Evaluate reviews+rating band (hard pass / soft fail / hard fail)
   │       If either → HARD_FAIL → exit.
   │
   ├─ Step 4: Aggregate decision (hard pass / soft fail / hard fail)
   └─ Step 5: Emit decision record to Quick Audit Tracker
```

### Output Record

```json
{
  "decision": "HARD_PASS | SOFT_FAIL | HARD_FAIL",
  "hard_fail_reasons": [],
  "soft_fail_signals": [
    {"criterion": "revenue", "value": "$1.5M–$2M (self-reported)", "band": "soft"}
  ],
  "criteria": {
    "lsa_eligible_vertical": true,
    "home_service_vertical": true,
    "revenue_band": "hard_pass | soft_fail | hard_fail",
    "revenue_reported": "$1.5M–$2M",
    "reviews_band": "hard_pass | soft_fail | hard_fail",
    "review_count": 247,
    "avg_rating": 4.8,
    "established_operating": true,
    "gbp_claimed_verified": true
  },
  "decision_timestamp": "..."
}
```

---

## Section 4: Routing

Three routing paths, one always-on prospect delivery. All team notifications are email (no Slack).

### Always: Quick Audit to the Prospect

Regardless of decision, the Quick Audit ships to the prospect's email. The Audit Agent owns this. The cover-note language varies by decision:

- **HARD_PASS:** *"Based on what we see here, you fit the profile of businesses we typically meet with in person. We'll be in touch within 3 business days to schedule a call."*
- **SOFT_FAIL:** *"Based on what we see, your business may be a strong fit for ongoing Maps Visibility work. Someone from our team will be in touch within 3 business days to learn more and figure out the right next step together."*
- **HARD_FAIL:** *"If you'd like to dig deeper on any of these recommendations, here are three free resources: [link 1] [link 2] [link 3]. If your business grows past the point where the Maps Visibility System makes sense, we'd love to hear from you."*

### HARD_PASS → "Qualified Prospect" Team Email

To: `dylan@localservicespotlight.com`, `668sierra@gmail.com`
Subject: `[MVS Qualified] <Business Name> — meeting candidate`

```
New MVS-Qualified Prospect: <Business Name>

GBP Primary Category: <category>
Location: <city, state>
Website: <website URL>

Reviews: <count> at <rating>★
Revenue (self-reported): <revenue_band>

Top 3 from Quick Audit (What To Fix First, items 1-3):
1. <action 1>
2. <action 2>
3. <action 3>

Quick Audit: <Drive link>
Intake record: <Sheet link>

Contact: <Name>  <email>  <phone>

Cover note to prospect committed a 3-business-day response. Schedule accordingly.
```

### SOFT_FAIL → "Marginal — Human Review" Team Email

Same recipients (`dylan@localservicespotlight.com`, `668sierra@gmail.com`).
Subject: `[MVS Marginal] <Business Name> — human review needed`

```
Marginal MVS Prospect — human review needed: <Business Name>

Why marginal:
- <soft_fail_signal 1: criterion + value + reasoning>
- <soft_fail_signal 2: criterion + value + reasoning>

GBP Primary Category: <category>
Location: <city, state>
Website: <website URL>

Reviews: <count> at <rating>★
Revenue (self-reported): <revenue_band>

Top 3 from Quick Audit (What To Fix First, items 1-3):
1. <action 1>
2. <action 2>
3. <action 3>

Quick Audit: <Drive link>
Contact: <Name>  <email>  <phone>

Suggested action: review the soft-fail signals. If the prospect clears the bar on closer inspection, advance to qualified-prospect outreach (3-business-day SLA committed in their cover note). Otherwise no action — the Quick Audit already shipped.
```

### HARD_FAIL → No Alert

The Quick Audit ships with the hard-fail cover-note language. No team email. The Tracker row records the decision and the hard-fail reasons. A failed prospect isn't re-evaluated — if they later qualify, they re-submit through SPP.

---

## Section 5: Orchestration

Reuses the same intake-to-Sheet pattern: SPP → Sheets → workflow watches sheet → workflow does work → writes back. Same shape the team already debugs.

```
SPP webhook
   │
   ▼
Google Sheet: "Quick Audit Tracker" (new tab on the Maps Visibility Master Sheet)
   │
   ├──────────────►  Audit Agent (runtime TBD; today a Cowork scheduled task)
   │
   └──────────────►  Qualification Agent (waits for Audit Agent's enrichment to populate, then runs)

Both write back to the same row.
Routing Agent (third workflow) polls the row.
When BOTH agents complete AND scorecard .docx is rendered:
   - Always: ship Scorecard to prospect
   - Conditional: emit appropriate team alert
```

### Why the Qualification Agent Waits for the Audit Agent

In v1 these were strictly parallel. They can't be — the Qualification Agent consumes the same enrichment record (GBP claim, review count, rating, GBP primary category) that the Audit Agent produces. Re-architecting: Audit Agent runs Steps 1–6 (data collection); Step 7 writes the enrichment block to the Tracker and signals "enrichment_ready." Qualification Agent triggers off that signal and runs in parallel with the Audit Agent's Steps 8–10 (synthesis, rendering, delivery). Saves API calls, removes double-pull risk.

### Sheet Schema (new tab: "Quick Audit Tracker")

| Column | Type | Set By |
|---|---|---|
| Submission ID | string | SPP webhook |
| Submitted At | datetime | SPP webhook |
| Business Name | string | SPP intake |
| Website | URL | SPP intake |
| City, State | string | SPP intake |
| Contact Name | string | SPP intake |
| Contact Email | string | SPP intake |
| Contact Phone | string | SPP intake |
| Place ID | string | Audit Agent (Step 1) |
| GBP Primary Category | string | Audit Agent (Step 1) |
| Enrichment Status | enum | Audit Agent (`pending`, `enriching`, `ready`, `failed`) |
| Enrichment JSON URL | URL | Audit Agent (Step 7) |
| Audit Status | enum | Audit Agent (`pending`, `rendering`, `complete`, `failed`) |
| Quick Audit .md URL | URL | Audit Agent (Step 9) |
| Top 3 What-To-Fix-First (titles) | text | Audit Agent (Quick Audit table, items 1-3) |
| Qualification Status | enum | Qualification Agent (`pending`, `complete`, `error`) |
| Decision | enum | Qualification Agent (`HARD_PASS`, `SOFT_FAIL`, `HARD_FAIL`) |
| Hard Fail Reasons | text | Qualification Agent |
| Soft Fail Signals | text | Qualification Agent |
| Revenue (self-reported band) | string | SPP intake (mirrored from intake field) |
| Routed | y/n | Routing Agent |
| Routed At | datetime | Routing Agent |
| Notes | text | Manual |

### Failure Handling

- **Audit Agent fails before enrichment ready:** Qualification Agent doesn't run. Quick Audit not produced. Logged to Failures tab. Manual recovery: human reads the failure, decides whether to retry or refund the audit fee (if any).
- **Audit Agent renders but qualification errors:** Quick Audit still ships with hard-fail cover-note language (no team email). Logged for review.
- **Both succeed but Routing Agent timeout:** Routing Agent reruns hourly until both statuses are complete. After 24 hours of no progress, escalates to a human.
- **Soft-fail accumulation review:** If the rate of SOFT_FAIL is much higher than HARD_PASS (suggested ratio threshold: 3:1), the bands are probably too generous and need tightening. Reviewed monthly.

### Logging

Every agent writes its status into the Tracker row before/after each major step. Failures get a row in a Failures tab with: submission ID, business name, step that failed, error message, retry count. Daily review of the Failures tab is in the operating cadence.

---

## Section 6: What This Replaces vs. What's New

**Replaces:**
- The current SPP intake form (six fields, basically right already — minor tweaks to add city + state if not currently collected, ensure phone is optional)
- Any manual one-off Quick Audits done in Cowork sessions

**Extends:**
- The existing intake-to-Sheet zap stack (Zapier). Same pattern, same sheet-as-control-hub design.
- The S&C Quick Audit format. The strict 6-check structure, Revenue Translation framing, What To Fix First table shape, and Glass Half Full closing are reused directly from the S&C portfolio Quick Audits.

**Net new:**
- The Audit Agent's identity-resolution-through-rendering pipeline (10 steps)
- The Qualification Agent's three-state decision logic
- The Routing Agent
- The Quick Audit Tracker sheet tab
- The team email templates (qualified vs. marginal)
- A monthly review of soft-fail band rates

---

## Section 7: Decisions Locked

All ten open questions from the build-prep round resolved with Daniel on 2026-05-21. Captured here as the working decision record.

1. **GBP Primary Category, no slug.** The agent uses the GBP primary category string directly (e.g., "Concrete contractor", "Roofing contractor") wherever it would otherwise have used an industry slug. No crosswalk file. The category drives the Check 5 head-keyword search and feeds the team-email payload as-is.

2. **No cohort comparison.** Cohort comparison is a Scorecard concept. The Quick Audit pipeline doesn't compute peer averages, doesn't build cohorts, doesn't cite "above peer cohort of X" callouts. Findings are absolute. Where the S&C Quick Audits had cohort callouts inline, this pipeline drops them.

3. **Revenue field placed last on SPP.** Order: business name → website → city/state → contact info → revenue, framed as "to make sure the Maps Visibility System is right for your business."

4. **Hard-fail is terminal.** A prospect who hard-fails isn't re-evaluated. If they later qualify (claim a GBP, hit the revenue threshold, accumulate reviews), they re-submit through SPP and the agent runs a fresh audit.

5. **Email-only routing, no Slack.** Team notifications go to `dylan@localservicespotlight.com` and `668sierra@gmail.com`. Subject-line prefixes distinguish `[MVS Qualified]` from `[MVS Marginal]`.

6. **3 business days, both tiers.** Both qualified-prospect and soft-fail cover-note CTAs commit to 3 business days. The team has the buffer to triage soft-fail cases without missing the SLA.

7. **No scoring rubric.** The Quick Audit doesn't score the prospect. There's no letter grade, no point totals, no category scores. The What To Fix First table is ranked by leverage judgment, not by a quantitative rubric.

8. **SEO data source: whatever's available.** Default to Ahrefs MCP because it's already wired in. If Ahrefs is unavailable, fall back to whatever SEO data source the agent has access to. The Quick Audit cites DA, organic traffic, keyword count, referring domains as data points — no preference battle to settle since this isn't a Scorecard.

9. **No cohort pre-warm.** Same as #2 — there are no cohorts to build, pre-warm, or refresh in this pipeline.

10. **Soft-fail daily review.** Soft-fail emails get reviewed within 24h by Dylan or the secondary recipient. Volume is expected low enough that this is manageable as part of normal inbox triage rather than a dedicated workflow.

---

## Sources

### S&C Quick Audit exemplars (canonical format source)

- [Claude Outputs / S&C / QuickAudit_Training-Prompt_v1.md](/Users/danielgoodrich/My%20Drive/Claude%20Co-Work/Claude%20Outputs/S%26C/QuickAudit_Training-Prompt_v1.md) — methodology origin doc; defines the strict structure
- [Claude Outputs / S&C / TennCrete / TennCrete_Quick-Audit_v1.md](/Users/danielgoodrich/My%20Drive/Claude%20Co-Work/Claude%20Outputs/S%26C/TennCrete/TennCrete_Quick-Audit_v1.md) — primary format reference (concrete vertical)
- [Claude Outputs / S&C / Cheetah Screens / CheetahScreens_Quick-Audit_v1.md](/Users/danielgoodrich/My%20Drive/Claude%20Co-Work/Claude%20Outputs/S%26C/Cheetah%20Screens/CheetahScreens_Quick-Audit_v1.md) — cross-industry validation (motorized screens / awnings vertical)
- [Claude Outputs / S&C / SAPS Exteriors / SAPSExteriors_Quick-Audit_v3.md](/Users/danielgoodrich/My%20Drive/Claude%20Co-Work/Claude%20Outputs/S%26C/SAPS%20Exteriors/SAPSExteriors_Quick-Audit_v3.md) — structural-break Headline pattern reference (broken-GBP-link case, roofing/exteriors vertical)
- Plus filename verification across the portfolio (15+ Quick Audits in `Claude Outputs/S&C/<Client>/<Client>_Quick-Audit_v1.md`) — all consistent with the structure documented in Section 2

### Other project files referenced

- [About Me / about-me.md](/Users/danielgoodrich/My%20Drive/Claude%20Co-Work/About%20Me/about-me.md)
- [About Me / anti-ai-writing-style.md](/Users/danielgoodrich/My%20Drive/Claude%20Co-Work/About%20Me/anti-ai-writing-style.md)
- [GLOBAL-INSTRUCTIONS.md](/Users/danielgoodrich/My%20Drive/Claude%20Co-Work/GLOBAL-INSTRUCTIONS.md)
- [Claude Outputs / Pure Green / SPP_Service_Config_MVS.md](/Users/danielgoodrich/My%20Drive/Claude%20Co-Work/Claude%20Outputs/Pure%20Green/SPP_Service_Config_MVS.md) — current SPP intake baseline
- [Claude Outputs / Pure Green / MVS_Build_Blueprint.md](/Users/danielgoodrich/My%20Drive/Claude%20Co-Work/Claude%20Outputs/Pure%20Green/MVS_Build_Blueprint.md) — intake-to-Sheet architecture reference
- [Claude Outputs / System Building / MVS_Pipedream_Workflows.md](/Users/danielgoodrich/My%20Drive/Claude%20Co-Work/Claude%20Outputs/System%20Building/MVS_Pipedream_Workflows.md) — current MVS workflow doc
- [Claude Outputs / Local Service Spotlight / LocalServiceSpotlight_LP-Copy_v3.md](/Users/danielgoodrich/My%20Drive/Claude%20Co-Work/Claude%20Outputs/Local%20Service%20Spotlight/LocalServiceSpotlight_LP-Copy_v3.md) — qualification criteria source ($2M+, 200+ reviews)

### Dennis Yu / BlitzMetrics articles

- [The Quick Audit — BlitzMetrics (definitive)](https://blitzmetrics.com/quick-audit/)
- [Human vs AI: The Quick-Audit Challenge That Changed How We Manage Audits](https://blitzmetrics.com/human-vs-ai-quick-audit-challenge/)
- [Local Service Business Website Checklist](https://blitzmetrics.com/local-service-business-website-checklist/)
- [Google Business Profile (GBP) Checklist For Local Service Businesses](https://blitzmetrics.com/google-business-profile-gbp-checklist-for-local-service-businesses/)

### Google Local Services Ads

- [Getting started with Local Services Ads — United States (full eligible category list)](https://support.google.com/localservices/answer/6224841?hl=en&co=GENIE.CountryCode%3DUS)
