"""Build the Expert Services audit spec JSON to verify the generalized renderer
produces the same PDF as the hardcoded v1 script. Run once, compare PDFs."""

import json

spec = {
    "meta": {
        "business_name": "Expert Services",
        "business_descriptor": "Plumbing, Heating, Air &amp; Electrical",
        "business_location_label": "Utah (Salt Lake + Utah Counties)",
        "contact_name": "Owner / Operations Lead",
        "contact_role": "Expert Services Plumbing, Heating, Air &amp; Electrical",
        "address_lines": [
            "1190 N 1200 W, Orem, UT 84057  (primary)",
            "2330 Main St, Ste 7, Salt Lake City, UT 84115  (secondary)",
        ],
        "phone": "(385) 446-5727",
        "website": "expertservicesutah.com",
        "issue_date": "May 28, 2026",
        "order_number": "F2F79621",
        "auditor_org": "BlitzMetrics  &bull;  Local Service Spotlight",
        "auditor_contact_line": "Local Service Spotlight  &bull;  dennis@blitzmetrics.com  &bull;  blitzmetrics.com",
        "footer_brand_line": "Expert Services Quick Audit  |  Prepared by BlitzMetrics — Local Service Spotlight",
    },
    "exec_summary": {
        "lede": ("Expert Services has the bones of a serious multi-location home-services brand &mdash; "
                 "nine service-area pages, a working WordPress site with Google Tag Manager, a Meta Pixel, "
                 "an active &lsquo;Expert Advice&rsquo; blog driving organic traffic, "
                 "<b>1,295 Google reviews at 4.9&#9733;</b> with recent and warm owner replies, "
                 "218 additional reviews across two Yelp locations, an Instagram account with 1,363 "
                 "followers, and an established Better Business Bureau profile. Yet a stranger Googling "
                 "the brand today hits a thicket: <b>thirteen different phone numbers</b> across your "
                 "own site and social channels, two competing brand descriptions of how long you&rsquo;ve "
                 "been in business (the website says &lsquo;over 10 years,&rsquo; the social videos say "
                 "&lsquo;30+ years&rsquo;), a Domain Rating of 8 after a decade-plus of operation, and "
                 "service-city pages that consistently rank at positions 7-11 &mdash; just outside the "
                 "top three, where the local clicks actually live. The review machine is genuinely strong. "
                 "The discovery machine that should be funneling people to those reviews isn&rsquo;t "
                 "keeping up."),
        "overall_grade": {
            "letter": "C",
            "name": "Strong review base, scattered discovery layer.",
            "oneliner": ("Expert Services has built a 1,295-review / 4.9&#9733; Google profile that most "
                         "Utah home-services peers would trade for. The discovery layer that funnels new "
                         "prospects toward those reviews &mdash; NAP consistency, schema, service-city "
                         "ranking depth, brand SERP cleanup &mdash; is still a band behind."),
        },
        "pillars": [
            {"letter": "D", "title": "1. Footprint",
             "text": ("~13 distinct phone numbers across the website, social profiles, and directory listings. "
                      "Brand-history mismatch between site (10 yrs) and social (&lsquo;30+ yrs&rsquo;). "
                      "BBB profile not accredited.")},
            {"letter": "B", "title": "2. Reviews &amp; Reputation",
             "text": ("1,295 Google reviews at 4.9&#9733; with recent, warm owner replies. 218 additional Yelp reviews. "
                      "Same band as Parley&rsquo;s (805) and Black Diamond (977); behind Any Hour (27,683) and Western (2,660).")},
            {"letter": "D", "title": "3. Social Media",
             "text": ("Six channels live. Instagram (1,363 followers) and Facebook produce video. No TikTok, no Nextdoor, "
                      "no founder voice surfaced.")},
            {"letter": "C", "title": "4. Website Performance",
             "text": ("WordPress + WP Rocket, GTM + Meta Pixel + Site Kit, nine service-area pages, real blog traffic. "
                      "No JSON-LD schema detectable. Authority fragmented across three sibling subdomains plus a parallel brand domain.")},
            {"letter": "D", "title": "5. Brand Search",
             "text": ("Own homepage holds #2 for &lsquo;expert services utah.&rsquo; DR 8 with 345 referring domains &mdash; "
                      "unusually low. Wheree duplicates, Yelp per-location pages, and BBB &lsquo;Not Accredited&rsquo; tile on page one.")},
            {"letter": "D", "title": "6. Keyword Rankings",
             "text": ("51 organic keywords, 184 visits/mo, 6 top-3 positions. Service-city pages rank at #4-#11 on their best queries. "
                      "One Orem AC page ranks for a Spanish-intent query &mdash; content-target mismatch.")},
        ],
        "scores": [
            {"pillar": "Footprint &amp; Listings",   "score": "40 / 100"},
            {"pillar": "Reviews &amp; Reputation",  "score": "75 / 100"},
            {"pillar": "Social Media",               "score": "45 / 100"},
            {"pillar": "Website Performance",        "score": "55 / 100"},
            {"pillar": "Brand Search",               "score": "45 / 100"},
            {"pillar": "Keyword Rankings",           "score": "45 / 100"},
        ],
        "bottom_line": ("If we consolidate the phone-number sprawl, reconcile the 10-vs-30-year brand history, "
                        "ship LocalBusiness schema across the nine service-area pages, and push three of the "
                        "existing #7-#11 service-city pages into the top 3 over the next 90 days, Expert Services "
                        "moves from low C to mid-C / low-B and starts qualifying for the local pack on the queries "
                        "that compound. The 1,295 Google reviews are an asset most peers can&rsquo;t match in a "
                        "quarter &mdash; the work ahead is making sure more prospects ever get far enough into "
                        "the funnel to see them."),
    },
    "sections": [
        {
            "id": "02", "title": "BUSINESS SNAPSHOT",
            "blocks": [
                {"type": "h3", "text": "Expert Services at a glance"},
                {"type": "data_table", "header": ["Field", "Value"],
                 "col_widths": [1.6, 5.0],
                 "rows": [
                    ["Operating since", "&lsquo;Over 10 years&rsquo; per About Us page (social channels reference 30+ years &mdash; needs reconciliation)"],
                    ["Owner", "Family-owned per public profiles; owner identity not surfaced on the website"],
                    ["Primary office", "1190 N 1200 W, Orem, UT 84057"],
                    ["Secondary office", "2330 Main St, Ste 7, Salt Lake City, UT 84115"],
                    ["Primary phone", "(385) 446-5727  (text: (385) 446-6013)"],
                    ["Website", "expertservicesutah.com (WordPress + WP Rocket)"],
                    ["Microsites", "financing.expertservicesutah.com &bull; go.expertservicesutah.com &bull; callexpertservicesutah.com (parallel Orem-targeted brand domain)"],
                    ["Services", "Plumbing (residential + commercial), HVAC (furnace, AC, residential + commercial), Electrical, Sewer, Water Treatment, Water Heaters"],
                    ["Target verticals", "Residential + Commercial &mdash; 24/7 emergency framing"],
                    ["Service area", "Lehi, Orem, Provo, Salt Lake City, Sandy, Millcreek, South Jordan, West Jordan, West Valley City"],
                 ]},
                {"type": "spacer", "height": 10},
                {"type": "paragraph",
                 "text": ("Expert Services has built more digital infrastructure than most local home-services brands "
                          "at this tenure &mdash; a real service-city page set, a real blog with real traffic, a real "
                          "tracking stack. The audit below treats those assets as real and worth amplifying. The gaps "
                          "are at the execution layer: consistency, schema, depth &mdash; not infrastructure.")},
            ],
        },
        {
            "id": "03", "title": "FOOTPRINT &amp; LISTINGS",
            "question": "Is the basic information consistent?",
            "blocks": [
                {"type": "grade_banner", "letter": "D", "pillar": "Footprint",
                 "oneliner": "~13 distinct phone numbers across own site and social/directory presence. "
                             "Brand-history mismatch between site and social. BBB profile not accredited."},
                {"type": "spacer", "height": 10},
                {"type": "h3", "text": "What we found &mdash; NAP consistency"},
                {"type": "data_table",
                 "header": ["Source", "Phone", "Status"],
                 "col_widths": [2.6, 2.0, 2.0],
                 "rows": [
                    ["Own site header (call CTA)", "(385) 446-5727", "Authoritative call number"],
                    ["Own site header (text CTA)", "(385) 446-6013", "Authoritative text number"],
                    ["Lehi location page", "(801) 960-1766", "Tracker number"],
                    ["Orem location page", "(801) 960-1565", "Tracker number"],
                    ["Provo location page", "(801) 734-9075", "Tracker number"],
                    ["Salt Lake City location page", "(385) 446-5727", "Matches header"],
                    ["Sandy location page", "(801) 871-0322", "Tracker number"],
                    ["Millcreek / S Jordan / W Jordan / WVC", "(801) 224-8118", "Shared tracker"],
                    ["Yelp &mdash; Salt Lake City listing", "(801) 549-0123", "Yelp-specific number"],
                    ["Yelp &mdash; Orem listing", "(801) 549-0133", "Yelp-specific number"],
                    ["Facebook /ExpertServicesUtah/ About", "(801) 823-1477", "Facebook-specific"],
                    ["Instagram @expertservicesutah bio", "(801) 896-1878", "Instagram-specific"],
                    ["<b>Google Business Profile (Orem)</b>", "<b>(801) 224-8118</b>", "Matches Millcreek tracker, NOT website header"],
                    ["BBB profile", "Profile present, Not Accredited", "Unclaimed accreditation"],
                 ]},
                {"type": "spacer", "height": 12},
                {"type": "callout", "head": "BRAND-HISTORY MISMATCH",
                 "body": ["The website&rsquo;s About Us page reads &lsquo;Delivering Expert Service and Repairs "
                          "for Over Ten Years.&rsquo; The recent Facebook and Instagram videos read &lsquo;At "
                          "Expert Services, we&rsquo;ve dedicated 30+ years to serving Utah homes.&rsquo; Same "
                          "brand, two tenures, three years apart in publication."]},
                {"type": "spacer", "height": 12},
                {"type": "h3", "text": "Why this matters"},
                {"type": "paragraph",
                 "text": ("Google&rsquo;s local algorithm uses NAP consistency as a primary trust signal &mdash; "
                          "every directory carrying a different number reads as a separate confidence vote that "
                          "the business identity may not be what it claims. Per-location call tracking is fine "
                          "when each location&rsquo;s Google Business Profile and each location&rsquo;s Yelp "
                          "listing carry the right per-location number &mdash; but here the social-profile numbers "
                          "don&rsquo;t match any location page, and the Yelp listings carry numbers that don&rsquo;t "
                          "appear anywhere on the website. Compounding the issue: a procurement-grade reader landing "
                          "on the Facebook page sees &lsquo;30+ years&rsquo; and then visits the website seeing "
                          "&lsquo;over 10 years&rsquo; &mdash; that&rsquo;s an unforced trust hit that costs deals "
                          "before any conversation starts.")},
                {"type": "spacer", "height": 6},
                {"type": "h3", "text": "Fixes &mdash; most doable this month"},
                {"type": "bullets", "items": [
                    "<b>Pick one master phone per location and reconcile every directory.</b> Decide which "
                    "call-tracker number is the canonical per-location number, then update Yelp, Facebook, "
                    "Instagram, BBB, Google Business Profile, Apple Maps, and Bing Places to match the "
                    "website&rsquo;s per-location page. The current 13-number sprawl can compress to 4-5.",
                    "<b>Reconcile the brand-history language.</b> Pick the true number (10, 20, or 30 years) "
                    "and use it consistently across the website, Facebook, Instagram, and LinkedIn. If the "
                    "30-year framing is the legacy of an earlier brand, name it in the About story.",
                    "<b>Claim BBB accreditation.</b> A 10-year (or 30-year) home-services brand with no BBB "
                    "accreditation reads as either inattentive or non-credible to first-time-buyer audiences.",
                    "<b>Audit GBP secondary categories.</b> The Orem GBP primary category is already &lsquo;Plumber.&rsquo; "
                    "Fill secondary categories (HVAC contractor, Electrician, Drain cleaning service, Water heater service) "
                    "so the listing competes on the full service breadth.",
                    "<b>Decide on callexpertservicesutah.com.</b> A second brand domain running its own Orem-targeted site "
                    "fragments brand authority. Either 301-redirect to expertservicesutah.com/locations/orem/ or fold the content in.",
                ]},
            ],
        },
        {
            "id": "04", "title": "REVIEWS &amp; REPUTATION",
            "question": "Are people actually saying good things &mdash; lately?",
            "blocks": [
                {"type": "grade_banner", "letter": "B", "pillar": "Reviews",
                 "oneliner": "1,295 Google reviews at 4.9&#9733; with recent warm owner replies. 218 additional Yelp "
                             "reviews. Competitive with Parley&rsquo;s / Black Diamond peer tier; behind Any Hour and Western."},
                {"type": "spacer", "height": 12},
                {"type": "h3", "text": "The numbers"},
                {"type": "stat_callout",
                 "stats": [["4.9&#9733;", "Google average"],
                           ["1,295", "Google reviews"],
                           ["218", "Yelp combined"],
                           ["Recent", "Owner replies"]]},
                {"type": "spacer", "height": 12},
                {"type": "paragraph",
                 "text": ("Expert Services has a real review machine. 1,295 Google reviews at 4.9&#9733; (confirmed "
                          "live via Knowledge Panel for the Orem location) puts you in the same conversation as the "
                          "next tier of Utah peers and reflects years of consistent customer experience. Owner replies "
                          "on visible reviews are recent (2-3 months) and warm, naming individual technicians and the "
                          "specific work performed. The asking infrastructure is wired (GBP write-review link surfaces "
                          "from the website&rsquo;s About Us footer), and the result shows.")},
                {"type": "h3", "text": "How you stack up in the Salt Lake / Utah County market"},
                {"type": "data_table",
                 "header": ["Competitor", "Google reviews", "Stars", "Snapshot"],
                 "col_widths": [2.4, 1.2, 0.7, 2.3],
                 "rows": [
                    ["Expert Services", "<b>1,295</b>", "<b>4.9&#9733;</b>", "Multi-location, multi-service"],
                    ["Any Hour Services", "27,683", "4.8&#9733;", "Direct multi-service peer at scale"],
                    ["Western Heating, Air &amp; Plumbing", "2,660", "4.9&#9733;", "HVAC-led Utah Valley incumbent"],
                    ["Black Diamond Experts", "977", "4.8&#9733;", "Comparable multi-service tier"],
                    ["Parley&rsquo;s Plumbing, Heating &amp; AC", "805", "4.8&#9733;", "Direct Orem competitor"],
                    ["Expert Plumber Provo", "28", "4.9&#9733;", "Single-location Provo specialist"],
                 ]},
                {"type": "spacer", "height": 10},
                {"type": "paragraph",
                 "text": ("Expert Services is ahead of Parley&rsquo;s and Black Diamond on review count and matches "
                          "Western on star rating. The gap to Any Hour Services (21x the review count) is the remaining "
                          "long-haul work &mdash; that incumbent anchors the local pack on multi-service &lsquo;near "
                          "me&rsquo; queries and represents a multi-year ServiceTitan-scale operations build to catch. "
                          "Catching Western&rsquo;s 2,660 inside 24 months is the realistic next-band target.")},
                {"type": "callout",
                 "head": "KEEP THE ENGINE RUNNING &mdash; AND ACCELERATE IT",
                 "body": ["After every completed job, fire a two-step automation: (1) same-day SMS with a thank-you "
                          "and the direct Google review URL; (2) 48-hour follow-up email with the same link plus a "
                          "photo of the completed work. Most field-service CRMs ship this natively at $0 incremental "
                          "cost. At one job/day per technician across nine service cities, this routinely produces "
                          "50-80 new Google reviews per month &mdash; enough to close the gap to Western Heating&rsquo;s "
                          "2,660 inside 24 months while widening the lead over Parley&rsquo;s and Black Diamond."]},
                {"type": "h3", "text": "Review response observation"},
                {"type": "paragraph",
                 "text": ("Owner replies on Google are consistent, warm, and named &mdash; naming the technician "
                          "(Chandler, Hunter, etc.) and the work performed. This is the right pattern; keep it as "
                          "the standard, and apply the same rhythm to Yelp (both locations) and any Facebook "
                          "recommendations that come in.")},
            ],
        },
        {
            "id": "05", "title": "SOCIAL MEDIA",
            "question": "Are you showing up where customers actually look?",
            "blocks": [
                {"type": "grade_banner", "letter": "D", "pillar": "Social",
                 "oneliner": "Six channels live with active Instagram + Facebook video. No TikTok, no Nextdoor, "
                             "no founder voice surfaced. Meta Pixel suggests paid social is real."},
                {"type": "spacer", "height": 12},
                {"type": "data_table",
                 "header": ["Channel", "Status", "Followers", "Notes"],
                 "col_widths": [2.2, 1.3, 0.7, 2.4],
                 "rows": [
                    ["Facebook &mdash; /ExpertServicesUtah/", "Live, active video", "n/a", "Recent President&rsquo;s Day video, &lsquo;30+ years&rsquo; video"],
                    ["Instagram &mdash; @expertservicesutah", "Live, active reels", "<b>1,363</b>", "Drip reel, fast-friendly reel"],
                    ["LinkedIn Company", "Live", "n/a", "Activity not verified"],
                    ["Twitter / X &mdash; @expertutah", "Live", "n/a", "Activity not verified"],
                    ["YouTube channel", "Live", "n/a", "Cadence not verified"],
                    ["Pinterest /expertplumbing1190/", "Live", "n/a", "Activity not verified"],
                    ["TikTok", "Not found", "&mdash;", "Missing channel"],
                    ["Nextdoor", "Not found", "&mdash;", "Missing channel &mdash; high-leverage for local trades"],
                 ]},
                {"type": "spacer", "height": 10},
                {"type": "paragraph",
                 "text": ("Social isn&rsquo;t a vanity exercise for a multi-city plumbing+HVAC brand. The two "
                          "highest-leverage social proofs in this trade are (1) a recurring &lsquo;behind-the-job&rsquo; "
                          "video cadence that converts to local search relevance and (2) a Nextdoor presence that "
                          "converts neighborhood referrals. The first is already started on Instagram and Facebook "
                          "&mdash; the second is completely missing.")},
                {"type": "callout",
                 "head": "QUICK WIN: PHONE-SHOOT ONE JOB PER DAY PER TECHNICIAN",
                 "body": ["Every completed job is a piece of content. A 30-second vertical video of a furnace "
                          "install, an AC swap, or a complex sewer-line repair &mdash; posted as a Reel to "
                          "Instagram + Facebook simultaneously &mdash; creates a compounding library of "
                          "trust-and-skill proof. At 9 service cities with multiple technicians per day, this "
                          "generates 30-60 pieces of original content per month, all from work that&rsquo;s "
                          "already happening."]},
                {"type": "spacer", "height": 10},
                {"type": "h3", "text": "The Nextdoor opening"},
                {"type": "paragraph",
                 "text": ("Nextdoor in Utah County and Salt Lake County is where neighborhood plumbing/HVAC "
                          "recommendations actually happen. A claimed business profile per service area, weekly "
                          "&lsquo;we just helped a homeowner in [Lehi] with X&rsquo; posts, and an opt-in for "
                          "emergency same-day calls produces a referral channel that doesn&rsquo;t cost ad spend. "
                          "Most direct competitors aren&rsquo;t running this &mdash; it&rsquo;s a green-field local channel.")},
                {"type": "h3", "text": "Founder voice"},
                {"type": "paragraph",
                 "text": ("A 10-year (or 30-year) home-services brand with no surfaced founder identity is leaving "
                          "trust signal on the table. In trades, the &lsquo;who runs this&rsquo; question converts "
                          "more than the &lsquo;what do you do&rsquo; question. Surface the founder/owner on the "
                          "About Us page (name + photo + the actual operating history), then build a LinkedIn cadence "
                          "around them.")},
            ],
        },
        {
            "id": "06", "title": "WEBSITE PERFORMANCE",
            "question": "Does the site sell, or just sit there?",
            "blocks": [
                {"type": "grade_banner", "letter": "C", "pillar": "Website",
                 "oneliner": "Modern architecture with real tracking. No detectable JSON-LD schema. "
                             "Authority fragmented across three sibling subdomains plus a separate brand domain."},
                {"type": "spacer", "height": 12},
                {"type": "h3", "text": "Architecture &mdash; strong bones, fragmented surface"},
                {"type": "data_table",
                 "header": ["Property", "What it is", "Problem"],
                 "col_widths": [2.2, 2.4, 2.0],
                 "rows": [
                    ["expertservicesutah.com", "Primary WordPress + WP Rocket site; nine service-area pages; active &lsquo;Expert Advice&rsquo; blog", "None at the architecture layer &mdash; this is the right hub"],
                    ["financing.expertservicesutah.com", "Financing subdomain", "Splits authority for any financing-related search"],
                    ["go.expertservicesutah.com", "Conversion-helper microsite ($250 guarantee, water treatment)", "Splits authority again; URL structure obscures brand"],
                    ["callexpertservicesutah.com", "<b>Parallel brand domain &mdash; &lsquo;Proudly Serving Orem&rsquo;</b>", "Competes with own root on Orem-area brand queries"],
                 ]},
                {"type": "spacer", "height": 10},
                {"type": "h3", "text": "The tracking stack is real"},
                {"type": "paragraph",
                 "text": ("Google Tag Manager (GTM-P4FN8L4) is live. Google Site Verification is set. Meta Pixel runs "
                          "with two distinct pixel IDs. Google AdSense / Site Kit is connected. reCAPTCHA is on contact "
                          "forms. This is much better than the baseline for local home-services brands. The tracking is "
                          "in place &mdash; the missing piece is schema.")},
                {"type": "spacer", "height": 4},
                {"type": "h3", "text": "On-page SEO &mdash; what&rsquo;s missing"},
                {"type": "bullets", "items": [
                    "<b>No detectable JSON-LD schema.</b> A multi-location plumbing+HVAC+electrical brand should "
                    "ship LocalBusiness schema with multi-location markup, Service schema for each service line, "
                    "FAQPage schema on the FAQ page, and AggregateRating schema. None surface in the homepage HTML.",
                    "<b>No founder / owner bio on the About Us page.</b> Add a 2-paragraph founder section with name, "
                    "photo, and operating history &mdash; and reconcile the 10-vs-30-year mismatch in the same paragraph.",
                    "<b>Brand-history inconsistency between site and social.</b> Pick one number, reflect it everywhere.",
                    "<b>Service-area pages are thin on local proof.</b> The per-city pages have the URL structure right but "
                    "don&rsquo;t carry per-city case studies, per-city testimonials, or per-city photo proof. A two-paragraph "
                    "&lsquo;we just completed X at Y in [city]&rsquo; block per page, refreshed monthly, is the cheapest "
                    "schema-adjacent ranking lift.",
                    "<b>AC Service Orem page ranks for a Spanish-intent query.</b> Best-ranking keyword is &lsquo;ac repair "
                    "spanish orem ut&rsquo; (#7, vol 80). The page itself is in English. Either build a Spanish-language "
                    "variant for the Hispanic market in Orem (real opportunity) or update on-page copy to disambiguate intent.",
                    "<b>No clear consolidation strategy for the four brand surfaces.</b> Either fold financing., go., and "
                    "callexpertservicesutah.com into the main root, or document a clear reason each subdomain/domain exists.",
                ]},
            ],
        },
        {
            "id": "07", "title": "BRAND SEARCH",
            "question": "What does a stranger see when they Google you?",
            "blocks": [
                {"type": "grade_banner", "letter": "D", "pillar": "Brand Search",
                 "oneliner": "Own homepage holds #2 for &lsquo;expert services utah.&rsquo; DR 8 after a decade is "
                             "anomalously low. Wheree duplicates and BBB &lsquo;Not Accredited&rsquo; tile on page one."},
                {"type": "spacer", "height": 12},
                {"type": "h3", "text": "What &lsquo;Expert Services Utah&rsquo; shows"},
                {"type": "data_table",
                 "header": ["Result", "Verdict"],
                 "col_widths": [3.3, 3.3],
                 "rows": [
                    ["Own homepage", "Holds #2 for the brand term (vol 50/mo) &mdash; should be #1"],
                    ["Yelp &mdash; Orem location (61 reviews)", "Sits high on brand SERP"],
                    ["Yelp &mdash; SLC location (157 reviews)", "Sits high on brand SERP"],
                    ["BBB profile (Not Accredited)", "Trust risk on page 1 &mdash; fix via accreditation"],
                    ["Wheree duplicates (4+ pages)", "3rd-party scrapers crowding the brand SERP"],
                    ["HomeAdvisor, Thumbtack, GuildQuality, Indeed", "All hold brand-name pages"],
                    ["callexpertservicesutah.com", "Likely surfaces on Orem brand queries; competes with own root"],
                    ["Knowledge Panel", "Renders well &mdash; 1,295 reviews at 4.9&#9733;, recent posts, current photos"],
                    ["Video carousel", "Not verified live"],
                    ["FAQ rich result", "Not present &mdash; no FAQPage schema detected"],
                 ]},
                {"type": "spacer", "height": 12},
                {"type": "callout",
                 "head": "THE DR-8 ANOMALY",
                 "body": ["A 10-year (or 30-year) home-services brand with 345 referring domains should typically "
                          "rate DR 20-30 on Ahrefs, not DR 8. DR 8 with this many refdomains usually means one of "
                          "two things: (1) the link profile is dominated by low-quality directory/scraper sites that "
                          "don&rsquo;t transfer authority, or (2) the link profile was built through paid PR placements "
                          "that Google has discounted. Worth an Ahrefs backlink audit to confirm &mdash; the answer "
                          "changes which fixes matter most."]},
                {"type": "spacer", "height": 12},
                {"type": "h3", "text": "The Knowledge Panel is mostly there &mdash; finish it"},
                {"type": "paragraph",
                 "text": ("Live Knowledge Panel inspection on 2026-05-28 shows the Orem panel rendering with 1,295 "
                          "reviews at 4.9&#9733;, &lsquo;Open 24 hours,&rsquo; primary category &lsquo;Plumber,&rsquo; "
                          "recent photos (24 days ago), and an active owner post from April 2026. This is well-maintained "
                          "&mdash; not the empty-panel problem some local brands have. The remaining work is per-location "
                          "parity: confirm the Salt Lake City location&rsquo;s GBP renders the same level of completeness "
                          "(photos current, owner posts published monthly, secondary categories filled).")},
            ],
        },
        {
            "id": "08", "title": "KEYWORD RANKINGS",
            "question": "Is anyone finding you on Google for what you sell?",
            "blocks": [
                {"type": "grade_banner", "letter": "D", "pillar": "Keyword Rankings",
                 "oneliner": "51 organic keywords, 184 visits/mo, 6 top-3 positions. Service-city pages rank at "
                             "positions 4-11 &mdash; close to the top, not in it."},
                {"type": "spacer", "height": 12},
                {"type": "h3", "text": "Ahrefs snapshot (as of May 28, 2026)"},
                {"type": "stat_callout",
                 "stats": [["8", "Domain rating"],
                           ["51", "Ranking keywords"],
                           ["184", "Org visits / mo"],
                           ["345", "Referring domains"]]},
                {"type": "spacer", "height": 10},
                {"type": "paragraph",
                 "text": ("Source: Ahrefs Site Explorer (US, subdomains mode). DR 8 with 345 referring domains is "
                          "anomalously low &mdash; see Brand Search section for the link-quality hypothesis. The 51 "
                          "keywords and 184 visits are a real footprint; the per-page ranking quality is the gap.")},
                {"type": "h3", "text": "What you actually rank for &mdash; top organic pages"},
                {"type": "data_table",
                 "header": ["Page", "Top keyword", "Pos.", "Vol.", "Visits"],
                 "col_widths": [2.5, 2.2, 0.5, 0.5, 0.6],
                 "rows": [
                    ["Homepage", "expert services utah (brand)", "#2", "50", "108"],
                    ["/blog/.../black-specks-in-water/", "black specks in water dangerous", "#6", "200", "21"],
                    ["/locations/west-jordan/west-jordan-plumber/", "sewer line repair west jordan", "#4", "100", "12"],
                    ["/blog/.../how-to-find-an-electrical-short/", "how to find short circuit in house", "#8", "100", "7"],
                    ["/blog/.../what-makes-an-expert-technician/", "expert technicians", "#6", "90", "7"],
                    ["/air-conditioning-service-orem-ut/", "ac repair spanish orem ut", "#7", "80", "5"],
                    ["/locations/provo/", "provo ut plumbers", "#11", "150", "4"],
                    ["/locations/orem/", "expert plumbers", "#9", "90", "4"],
                    ["/blog/.../how-to-find-a-leak-salt-lake-city/", "leak detection salt lake city", "#11", "150", "4"],
                 ]},
                {"type": "spacer", "height": 10},
                {"type": "paragraph",
                 "text": ("Two patterns. First, the blog drives 4 of the top 5 non-brand traffic pages &mdash; "
                          "service-city pages aren&rsquo;t doing the commercial heavy lifting they were built for. "
                          "Second, the location and service-city pages are clustered at positions #7-#11 across their "
                          "best queries &mdash; close enough to top-3 that focused on-page work could meaningfully "
                          "reposition them this quarter. The Spanish-intent AC Orem page is the one outlier worth "
                          "specific attention.")},
                {"type": "h3", "text": "Competitor reality check"},
                {"type": "data_table",
                 "header": ["Competitor", "DR", "Ranking keywords", "Organic visits / mo"],
                 "col_widths": [2.6, 0.7, 1.7, 1.6],
                 "rows": [
                    ["Expert Services Utah", "8", "51", "184"],
                    ["Any Hour Services", "29", "620", "8,157"],
                    ["333help.com", "39", "558", "2,839"],
                    ["American Leak Detection", "55", "1,175", "30,897"],
                    ["Cool Today", "49", "4,390", "13,903"],
                 ]},
                {"type": "spacer", "height": 10},
                {"type": "callout",
                 "head": "WHY THIS IS ACTUALLY GOOD NEWS",
                 "body": ["Nine service cities, an existing service-city page architecture, an active blog already "
                          "pulling commercial-adjacent traffic, and DR-floor-level competitor difficulty across most "
                          "target queries &mdash; the gap to top-3 on five-to-ten high-value service+city pairs is "
                          "mechanical work, not structural rebuild. The infrastructure to win is in place; the "
                          "on-page execution is the remaining work."]},
            ],
        },
        {
            "id": "09", "title": "THE 90-DAY PLAN",
            "question": "Exactly what we&rsquo;d do, in what order",
            "blocks": [
                {"type": "paragraph",
                 "text": ("Tier 1 is shop-runnable in the first 30 days with no outside help. Tier 2 needs ~20 hours "
                          "of focused work plus a developer for schema. Tier 3 is where BlitzMetrics&rsquo; Content "
                          "Factory typically takes over.")},
                {"type": "spacer", "height": 8},
                {"type": "h3", "text": "Tier 1 &mdash; Quick Wins (Days 0-30)"},
                {"type": "data_table",
                 "header": ["#", "Action", "Owner", "Effort", "Expected impact"],
                 "col_widths": [0.35, 2.6, 1.3, 0.9, 1.45],
                 "rows": [
                    ["1.1", "Pick one master phone per location; update all directories", "Office mgr", "4 hrs", "NAP consistency restored"],
                    ["1.2", "Reconcile 10-vs-30-year brand history across web + social", "Office mgr + owner", "2 hrs", "Credibility lift on brand SERP"],
                    ["1.3", "Audit GBP primary + secondary categories across both locations", "BlitzMetrics", "1 hr", "Maps ranking eligibility"],
                    ["1.4", "Claim BBB accreditation", "Office mgr", "1 hr + fee", "A+ tile on brand SERP"],
                    ["1.5", "Launch SMS + email review-request automation post-job", "BlitzMetrics", "Setup 4 hrs", "+20-40 Google reviews/mo"],
                    ["1.6", "Add founder name + photo + reconciled history to About Us", "Owner + web admin", "2 hrs", "E-E-A-T lift"],
                    ["1.7", "Reply to every existing Google + Yelp review with warm message", "Owner", "2 hrs", "Trust + ranking signal"],
                    ["1.8", "Decide on callexpertservicesutah.com: 301-redirect or document", "Web admin", "30 min + 1 hr", "Recover Orem brand authority"],
                    ["1.9", "Fix AC Service Orem page intent mismatch (Spanish-query)", "Web admin", "2 hrs", "Reposition page for English intent"],
                 ]},
                {"type": "spacer", "height": 12},
                {"type": "h3", "text": "Tier 2 &mdash; Mid-term (Days 30-60)"},
                {"type": "data_table",
                 "header": ["#", "Action", "Owner", "Effort", "Expected impact"],
                 "col_widths": [0.35, 2.6, 1.3, 0.9, 1.45],
                 "rows": [
                    ["2.1", "Ship LocalBusiness multi-location + Service + FAQPage schema", "Web dev", "1 day", "Rich results in SERP"],
                    ["2.2", "Deepen 9 service-city pages &mdash; per-city case study + photos + testimonial", "BlitzMetrics + owner", "9 pages / 2 wks", "Push #7-#11 toward top 3"],
                    ["2.3", "Consolidate financing. and go. subdomains into root", "Web dev", "1 day", "Authority back to root"],
                    ["2.4", "Launch Nextdoor business presence in 5 priority cities", "Office mgr", "Setup 1 day", "New referral channel"],
                    ["2.5", "Launch &lsquo;one job per day per tech&rsquo; Reels cadence (IG + FB)", "Shop team", "30-60 sec / job", "30-60 pieces / mo"],
                    ["2.6", "Backlink audit on 345 referring domains; disavow if needed", "BlitzMetrics", "1 day", "DR recovery toward 15-20"],
                    ["2.7", "Launch Google Local Services Ads in Orem + Lehi + SLC", "BlitzMetrics", "Setup 1 day", "$30-60 CPL target"],
                    ["2.8", "Set up CallRail on all 13 numbers for true per-source attribution", "BlitzMetrics", "1 day", "True attribution"],
                 ]},
                {"type": "spacer", "height": 12},
                {"type": "h3", "text": "Tier 3 &mdash; Strategic (Days 60-90)"},
                {"type": "data_table",
                 "header": ["#", "Action", "Owner", "Effort", "Expected impact"],
                 "col_widths": [0.35, 2.6, 1.3, 0.9, 1.45],
                 "rows": [
                    ["3.1", "Founder personal-brand build (LSS Personal Brand package)", "BlitzMetrics", "2-3 wks", "Industry authority + B2B pipeline"],
                    ["3.2", "LinkedIn content cadence &mdash; 3 posts/wk by founder", "Founder + BlitzMetrics", "30 min/day", "B2B pipeline"],
                    ["3.3", "Bilingual landing page set for Orem Hispanic-market AC + plumbing", "BlitzMetrics", "5 pages", "Captures Spanish-intent traffic"],
                    ["3.4", "Sustained content cadence on Expert Advice blog &mdash; 2 posts/wk", "BlitzMetrics", "2 posts/wk", "Compounding organic lift"],
                    ["3.5", "Outreach to 50 Utah HOAs, school districts, commercial property mgrs / qtr", "Sales", "Ongoing", "Anchor commercial accounts"],
                    ["3.6", "&lsquo;Made Right in Utah&rsquo; YouTube + podcast with local builders", "Founder + BlitzMetrics", "1 ep / wk", "Local PR + backlinks"],
                    ["3.7", "Quarterly Quick Audit re-run &mdash; grade improvement scorecard", "BlitzMetrics", "Recurring", "Continuous improvement"],
                 ]},
            ],
        },
        {
            "id": "10", "title": "WHAT TO EXPECT BY DAY 90",
            "question": "Targets, not promises",
            "blocks": [
                {"type": "paragraph",
                 "text": ("These projections assume Tier 1 is completed in the first 30 days and Tier 2 begins on day 31. "
                          "Numbers reflect ranges typical of local home-services brands at Expert Services&rsquo; tenure "
                          "and infrastructure level that complete similar implementation paths. Treat as directional, "
                          "not contractual.")},
                {"type": "spacer", "height": 8},
                {"type": "data_table",
                 "header": ["Metric", "Today", "Day 30", "Day 60", "Day 90"],
                 "col_widths": [2.3, 1.1, 1.1, 1.1, 1.0],
                 "rows": [
                    ["Google review count", "1,295", "1,330-1,360", "1,380-1,430", "1,440-1,520"],
                    ["Google review velocity / mo", "current + 20-30%", "30-50", "45-65", "50-80"],
                    ["Star average", "4.9&#9733;", "hold", "hold", "hold"],
                    ["Organic keywords ranking", "51", "65-85", "100-140", "160-220"],
                    ["Estimated organic visits / mo", "184", "240-300", "380-500", "600-850"],
                    ["Service-city pages in top 3", "1", "2-3", "4-6", "6-9"],
                    ["Google Maps impressions / mo", "baseline", "+20%", "+50%", "+90%"],
                    ["GBP calls / mo", "baseline", "+15%", "+35%", "+60-80%"],
                    ["Inbound quote forms / mo", "baseline", "+10%", "+30%", "+50-80%"],
                 ]},
                {"type": "spacer", "height": 14},
                {"type": "callout",
                 "head": "WHERE THE UPSIDE REALLY SITS",
                 "body": ["The single biggest dollar-per-effort move is closing the gap on 5-10 service+city queries "
                          "already ranking at #7-#11. These are pages that already exist, that Google already trusts "
                          "to some degree, and that need depth (schema + per-city proof + tighter internal linking) "
                          "rather than rebuild. Each page that moves from #11 to top-3 produces an order-of-magnitude "
                          "jump in local clicks. Six service-city pages moving into top 3 in 90 days is the difference "
                          "between today&rsquo;s 184 monthly organic visits and a steady 600+."]},
            ],
        },
        {
            "id": "11", "title": "NEXT STEPS",
            "question": "What we&rsquo;d love to do with you",
            "blocks": [
                {"type": "paragraph",
                 "text": "Thanks for trusting us with this Quick Audit. Three ways forward, in order of speed:"},
                {"type": "spacer", "height": 6},
                {"type": "callout", "head": "1. DO IT YOURSELF",
                 "body": ["This document is enough to run the playbook in-house. Every Tier 1 item is doable with "
                          "no outside help. We&rsquo;re happy to be the help-desk on Slack if you want to send us "
                          "a screenshot now and then."]},
                {"type": "spacer", "height": 8},
                {"type": "callout", "head": "2. DONE-WITH-YOU (RECOMMENDED)",
                 "body": ["BlitzMetrics&rsquo; Local Service Spotlight team takes Tier 1 + Tier 2 off your plate. "
                          "You stay in the driver&rsquo;s seat for content (the founder video, the customer stories, "
                          "the field-job Reels) and we handle the directory cleanup, schema, location-page deepening, "
                          "review automation, backlink audit, and GBP optimization. Typical engagement: 90 days, "
                          "$X-X-XX retainer band, KPI-based check-ins every 30 days."]},
                {"type": "spacer", "height": 8},
                {"type": "callout", "head": "3. DONE-FOR-YOU",
                 "body": ["Full Content Factory engagement &mdash; monthly retainer covers content production, ads "
                          "management (LSA + Google Ads + Meta), review ops, monthly performance reviews, and a "
                          "quarterly Quick Audit re-grade. This is what ARDMOR Windows, Plumbing Pros, and Miley "
                          "Legal run with us today."]},
                {"type": "spacer", "height": 16},
                {"type": "centered",
                 "text": "Reach Dennis directly: dennis@blitzmetrics.com  &bull;  blitzmetrics.com  &bull;  linkedin.com/in/dennisyu"},
                {"type": "centered",
                 "text": "Local Service Spotlight: localservicespotlight.com"},
            ],
        },
        {
            "id": "12", "title": "APPENDIX",
            "question": "Sources, methodology, and supporting data",
            "blocks": [
                {"type": "paragraph",
                 "text": ("Every claim in this audit is backed by a public source. This appendix lists the data "
                          "points we pulled and the platforms we pulled them from, so you can audit our audit.")},
                {"type": "spacer", "height": 8},
                {"type": "h3", "text": "Methodology"},
                {"type": "paragraph",
                 "text": ("This Quick Audit follows BlitzMetrics&rsquo; six-check framework: Footprint, Reviews &amp; "
                          "Reputation, Social, Website, Brand Search, Keyword Rankings. Data was pulled on May 28, 2026, "
                          "from live sources. Scoring uses a 0-100 weighted index across roughly 40 individual signals "
                          "per pillar.")},
                {"type": "h3", "text": "Sources &amp; tools"},
                {"type": "data_table",
                 "header": ["Source", "What we pulled"],
                 "col_widths": [2.3, 4.3],
                 "rows": [
                    ["Ahrefs Site Explorer (2026-05-28)", "DR (8), referring domains (345 live; 1,085 all-time), backlinks (3,240 live; 9,055 all-time), organic keywords (51), top organic pages, organic competitors"],
                    ["Google Business Profile / Google Maps (Orem, navigated live)", "Place ID, 1,295 reviews at 4.9&#9733;, primary category &lsquo;Plumber,&rsquo; hours, recent photos, April 2026 owner post, owner-reply rhythm"],
                    ["Yelp (Orem + SLC listings)", "Per-location review counts (61 + 157), photos, phone numbers"],
                    ["Better Business Bureau", "Profile presence, accreditation status (Not Accredited)"],
                    ["Facebook, Instagram, LinkedIn, Twitter, YouTube, Pinterest", "Channel inventory, follower count (IG 1,363), brand-history copy, contact numbers"],
                    ["expertservicesutah.com (homepage, About Us, Reviews)", "CMS, tracking stack, service-city navigation, blog, schema detection, on-page content quality"],
                    ["Local Salt Lake / Utah County competitor scan", "Any Hour, Western, True Pros, SameDay, Just Right Air, Royal, Blue Best, K-Tech, Llewellyn, Told, Roto-Rooter, Parley&rsquo;s, S&amp;L, Valley"],
                 ]},
            ],
        },
        {
            "id": "13", "title": "GLOSSARY",
            "blocks": [
                {"type": "data_table",
                 "header": ["Term", "Definition"],
                 "col_widths": [1.6, 5.0],
                 "rows": [
                    ["NAP", "Name, Address, Phone &mdash; the three identity fields Google uses to verify a local business across the web."],
                    ["DR (Domain Rating)", "Ahrefs metric, 0-100. Measures the strength of a domain&rsquo;s backlink profile."],
                    ["E-E-A-T", "Experience, Expertise, Authority, Trust. Google&rsquo;s quality framework for evaluating content credibility."],
                    ["GBP", "Google Business Profile (formerly Google My Business)."],
                    ["Knowledge Panel", "The information panel that appears on the right side of brand searches in Google."],
                    ["Local Pack / Map Pack", "The three-business map result that appears for &lsquo;[service] near me&rsquo; queries."],
                    ["LSA", "Google Local Services Ads &mdash; pay-per-lead format with the Google Guarantee badge."],
                    ["Schema / Structured Data", "Machine-readable annotations that help search engines understand a page&rsquo;s content."],
                 ]},
                {"type": "spacer", "height": 20},
                {"type": "centered", "color": "text_muted", "size": 9,
                 "text": "<i>Prepared by BlitzMetrics &mdash; Local Service Spotlight. This audit is informational and "
                         "reflects publicly observable data as of May 28, 2026. We&rsquo;re happy to walk through any "
                         "finding live.</i>"},
            ],
        },
    ],
}

import sys
out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/es_audit.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(spec, f, indent=2, ensure_ascii=False)
print(f"Wrote spec: {out}")
