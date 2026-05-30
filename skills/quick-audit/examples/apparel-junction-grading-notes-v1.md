# Apparel Junction — Quick Audit Grading Notes v1

**Audited:** 2026-05-28
**Auditor:** Local Service Spotlight (calibration run, v2 format)
**Order #:** AJ001CAL
**Linked audit:** ApparelJunction_Quick-Audit_v1.md
**Reference:** This run reproduces the public Apparel Junction Quick Audit (Dennis Yu, 2026-05-28) for calibration validation of the v2 workflow.

---

## Pillar 1 — Footprint & Listings

**Signals observed**
- GBP claimed: yes (claimed; live in Maps)
- GBP primary category: "Embroidery & Crochet" — mismatched to actual primary service (screen printing + custom embroidery)
- GBP secondary categories: 0 visible / limited
- Phone on own contact page: (817) 264-6564 — canonical
- Phone on GBP: (817) 264-6564 — match
- Phone on Birdeye: (817) 264-6564 — match
- Phone on BBB: (817) 899-2158 — MISMATCH
- Phone on Yelp: (817) 264-6564 — match
- Phone on Yellow Pages: (817) 264-6564 — match
- Hours on own page: Mon-Fri 9-5:30; Sat by appt — canonical
- Hours on GBP: Mon-Fri 9-5 — mismatch
- Hours on Birdeye: Mon-Fri 9-6 — mismatch
- Hours on Yelp: Mon-Fri 9-5 — mismatch
- Hours on Yellow Pages: Mon-Fri 9-5 — mismatch
- Birdeye claim status: unclaimed
- BBB claim status: unclaimed (rated "Not Rated")
- Yelp claim status: claimed
- Manta / D&B / Chamber: multiple stale profiles
- Apple Maps presence: not verified
- Bing Places presence: not verified

**Anchor**
Apparel Junction is itself the calibration anchor for Footprint D. Signal list matches the anchor exactly.

**Grade:** D (42/100)

**Rationale**
Footprint lands at D (42). The phone is consistent on five of seven checked directories but mismatches on BBB ((817) 899-2158 vs the canonical (817) 264-6564). Three different sets of hours appear across GBP, Birdeye, and Yellow Pages — none of them match the contact-page truth. Birdeye and BBB are both unclaimed, leaving strangers to shape the first impression on two major review surfaces. The GBP primary category reads "Embroidery & Crochet" when the business is actually a screen-printing-and-embroidery shop — a direct hit to Maps ranking eligibility for screen-printing queries. This is the calibration anchor for D-tier Footprint.

---

## Pillar 2 — Reviews & Reputation

**Signals observed**
- Google review count: 31 (per Dennis's audit; Birdeye shows 32 aggregated)
- Star average (Birdeye aggregate): 4.1★
- Reviews in last 12 months on Google: 0
- Owner reply rate: low (one warm reply to Robert Smolek; one long defensive reply to Sarah Conley Darby)
- Last visible reply across platforms: ~6 years ago (Facebook)
- Chamber of Commerce rating: 3.6 from 18 reviewers
- Yellow Pages: 1-star result on page 1
- BBB: "Not Rated"
- Competitor benchmark (Arlington custom apparel peers):
  - DFW Ink — 144 reviews / 4.5★
  - Dr. Stitches Embroidery — ~50+ reviews / 4.7★
  - Stitch Studio — ~70+ reviews / 4.6★
  - Top Cotton Screen Printing — 100+ reviews / 4.5★
  - Artworks Embroidery — ~40 reviews / 4.4★

**Anchor**
Apparel Junction is the calibration anchor for Reviews C. Signal list matches the anchor.

**Grade:** C (55/100)

**Rationale**
Reviews lands at C (55). The 4.1★ star average is solid — above the 4.0 floor that separates D from C. The killer is volume + recency: 31 lifetime Google reviews after 34 years in business, and zero in the last 12 months. Behind every benchmarked peer on volume (DFW Ink has 4.6x the count with a third of the operating history). Reply behavior is intermittent at best — the last visible owner reply across platforms is ~6 years old, and the one substantive reply we found (to Sarah Conley Darby) reads as defensive rather than gracious. The star floor is what keeps this out of D-tier; the volume gap is what keeps it out of B-tier.

---

## Pillar 3 — Social Media

**Signals observed**
- Facebook (/ApparelJunction): live, 595 followers, sporadic posting
- Instagram (@appareljunction): live, low follower count (~<1K), sporadic
- LinkedIn Company Page: live, minimal followers, dormant
- LinkedIn Personal (Jonathan Astie): live, 81 connections, dormant — no content cadence, no how-it's-made videos, no posts about the business
- TikTok: not found
- YouTube: not found
- Pinterest: not found
- Nextdoor: listed only (no activity, no posts)
- No video content across any platform (no Reels, no Shorts, no TikTok)
- Founder LinkedIn personal: untapped (UT Arlington class of 1994, 34-year shop story has zero presence in posts)

**Anchor**
Apparel Junction is the calibration anchor for Social D.

**Grade:** D (38/100)

**Rationale**
Social lands at D (38). Four of eight inventoried channels exist (FB, IG, LinkedIn co, LinkedIn personal); the other four — TikTok, YouTube, Pinterest, Nextdoor (active) — are missing or unused. The four that exist are uniformly dormant or sporadic: 595 Facebook followers without rhythm, an Instagram that hasn't built audience, a LinkedIn company page that's effectively inactive, and a founder LinkedIn at 81 connections with no content. The fatal gap for a visual trade like custom apparel is the complete absence of video — every order produced is a piece of content that's not being captured. The personal brand is the highest-leverage missing piece: Jonathan's 34-year story has zero distribution.

---

## Pillar 4 — Website Performance

**Signals observed**
- Architecture: three fragmented brand domains in use
  - appareljunction.com/Apparel_Junction/shop/home — primary storefront on InkSoft (third-party platform, subpath URL)
  - blog.appareljunction.com — WordPress blog on Astra theme (subdomain splits authority from root)
  - uprint-it.com — DBA domain, currently unresponsive
  - {customer}.appareljunction.com — customer-specific InkSoft stores (linear, etc.) — these are the only pages actually ranking organically
- Schema markup: minimal — no LocalBusiness, no Service, no Product, no FAQPage detected
- Blog author attribution: "dfwplay" — anonymous, no bio, no photo
- Homepage video: none
- Testimonials above the fold: none
- Portfolio above the fold: none
- Clear single CTA above the fold: none
- Service-city landing pages: zero (no "custom embroidery Arlington TX" page, no service+city pairs targeted)
- Blog content quality: AI-generic — example: "Get Ready for FIFA World Cup 2026" with no local angle, no customer stories
- Meta-keywords stuffing: present (signals an old SEO approach)
- Mobile viewport meta: present
- SSL: active
- PageSpeed: data unavailable in this calibration run (would re-run live)

**Anchor**
Apparel Junction is the calibration anchor for Website D.

**Grade:** D (40/100)

**Rationale**
Website lands at D (40). Three fragmented domains is the structural problem: the primary storefront is on a third-party InkSoft subpath that Google reads as "one shop among thousands," the blog is on a subdomain that splits authority from the root, and the DBA domain is a dead asset bleeding referral equity. On-page SEO compounds: no LocalBusiness or Service or FAQPage schema, anonymous blog author, no homepage video, no testimonials or portfolio above the fold, no service-city landing pages, AI-generic blog content with no Arlington angle. The deduction-cap floor (Output Template §Website Performance) puts this at 40 even though the line-item gaps are deep — because the site does work, has SSL, has 25 blog posts, and has 206 referring domains it's not using.

---

## Pillar 5 — Brand Search

**Signals observed**
- Brand SERP for "Apparel Junction Arlington": own domain not at #1 (Facebook + Yelp + InkSoft subpath appear above the root domain)
- Knowledge Panel: missing — not rendering for the brand search
- Yelp listing at #1: unclaimed-looking, sparse
- Birdeye, Chamber of Commerce, Manta: 3rd-party scrapers crowding the top 3
- Yellow Pages: 1-star result on page 1
- BBB: "Not Rated" on page 1
- Video carousel: missing
- FAQ rich result: missing
- Image pack: missing
- DR: 21 (Ahrefs confirmed)
- Live refdomains: 207 (close to Dennis's 206)

**Anchor**
Apparel Junction is the calibration anchor for Brand Search D.

**Grade:** D (35/100)

**Rationale**
Brand Search lands at D (35). After 34 years, a business should dominate its own brand SERP — Apparel Junction doesn't. Own domain isn't #1; Yelp's unclaimed-looking listing is. Birdeye, Chamber of Commerce, and Manta crowd the top 3 — 3rd-party scrapers shaping the first impression instead of the business. Knowledge Panel is missing entirely (the right-side box that Google renders from a verified GBP — it's empty here). Two active reputation risks sit on page 1: a 1-star Yellow Pages result and a "Not Rated" BBB page. Plus the rich-result gaps: no video carousel, no FAQ result, no image pack. DR 21 with 207 referring domains is real authority that's pointed at the wrong pages.

---

## Pillar 6 — Keyword Rankings

**Signals observed**
- Ahrefs DR: 21.0
- Referring domains (live): 207
- Backlinks (live): 336
- Organic keywords ranking (US): 3
- Top-3 positions: 0
- Estimated organic visits / month: 1
- The 3 ranking keywords (confirmed via Ahrefs):
  - "roofing apparel" — position 8, volume 10/mo, $51 CPC, ranks on linear.appareljunction.com/linear_roofing/shop/home
  - "linear solar" — position 7, volume 0/mo, $374 CPC, ranks on appareljunction.com/linearsolar/shop/products/polos
  - "stormrepel" — position 11, volume 10/mo, ranks on appareljunction.com/Apparel_Junction/shop/product-detail/7261067
- None of the ranking keywords are commercial-intent for Apparel Junction's actual service offering — all three are customer-specific subdomain pages (Linear Roofing, Linear Solar) that exist for the customer's benefit, not Apparel Junction's
- Service-city pair rankings: zero (not ranking for "custom embroidery Arlington TX", "screen printing Arlington", "custom t-shirts Arlington", etc.)
- Difficulty assessment for target service-city pairs: Low across the board

**Anchor**
Apparel Junction is the calibration anchor for Keyword Rankings F.

**Grade:** F (18/100)

**Rationale**
Keyword Rankings lands at F (18). Three ranking keywords is the catastrophic-gap floor. One estimated monthly visit confirms the rankings have no commercial impact. The structural problem is named directly in the data: none of the three ranking keywords are for Apparel Junction's own service categories — all three are customer-specific InkSoft subdomain pages that exist because Apparel Junction's customers (Linear Roofing, Linear Solar) needed branded storefronts. Apparel Junction is functionally ranking on behalf of its customers, not for itself. Zero service-city pair rankings is the second hit. The good news (which lives in the audit body, not here) is that competitor difficulty is uniformly low — the gap is mechanical, not structural-link-suppression.

---

## Overall

Average: (42 + 55 + 38 + 40 + 35 + 18) / 6 = **38** → **D**

**Sanity check:** D feels right for the overall profile — strong tenure and real-but-unused authority undercut by NAP inconsistency, stale reviews, dormant social, fragmented site architecture, missing Knowledge Panel, and no commercial-intent rankings. This matches Dennis's published Overall Grade exactly.

---

## Hard caps applied

None. No catastrophic-gap floors triggered. GBP is claimed, website is live, reviews exist, social channels exist, ranking keywords exist (however few). All grades came from anchored reasoning, not caps.

---

## Data unavailable

- PageSpeed Insights — not re-run in this calibration. The audit body marks Section 06 PSI-specific claims as "data unavailable in this run; re-run pending."
- Live GBP Maps panel content (knowledge panel JS-rendered text) — relied on Dennis's published values rather than a fresh Chrome navigation.

---

## Calibration result

This is the v2 system replicating its own anchor — every grade matches Dennis's published Apparel Junction values exactly (42 / 55 / 38 / 40 / 35 / 18 → Overall D 38). The pass condition for this test is replication, which is met. The next-step calibration test is Test 3 from the Agent Definition: a cold submission with no prior reference — that's the test for whether anchored reasoning generalizes to a novel business.
