# Quick Audit — Grading Approach v1

**Supersedes:** `MVS_QuickAudit-Grading-Rubric_v1.md` (strict deduction-formula rubric). The rubric is preserved for reference but is not the production grading method.

**Method:** Anchored reasoning. The agent observes a concrete signal list per pillar, anchors to a known example (Apparel Junction or RiteWay), then writes a letter grade, a 0-100 score, and a one-paragraph rationale. Hard-cap floors apply for catastrophic gaps. Everything is shown work.

---

## 1. Why this and not a formula

Strict deduction formulas read as defensible but break down on the things that matter most:

- **Industry context.** TikTok presence is critical for an apparel shop and irrelevant for a B2B law firm. A rigid formula deducts the same in both.
- **Holistic fit.** A best-in-class business with one weird gap shouldn't be dragged down to a B by summed small penalties. A grader recognizes the gap as a footnote on an otherwise-A business.
- **Dennis's actual workflow.** The Apparel Junction grades are judgment calls, not summed deductions. Matching the format includes matching the grading style.

Anchored reasoning recovers what formulas were trying to deliver — reproducibility, defensibility, multi-auditor consistency — through different mechanics:

- **Signals are visible.** The agent must enumerate 5-10 concrete data points per pillar before assigning a grade. No vibes-grading on hidden observations.
- **Anchors are explicit.** Every grade cites which example it calibrated against ("similar to Apparel Junction's Footprint D — slightly better on X").
- **Reasoning is written.** One paragraph per pillar, kept in a working-notes file that travels with the audit and gets compared to next quarter's re-grade.
- **Hard caps protect the floor.** Catastrophic gaps (no GBP, dead site) can't be reasoned around — they cap at F.

The 0-100 score is the output of judgment, not arithmetic. It exists because Dennis's format includes a scorecard.

---

## 2. Letter bands (verbal definitions)

| Letter | Score band | Definition |
|---|---|---|
| **A** | 85-100 | Best-in-class. Specific gaps only — there's nothing structurally wrong, and the business is ahead of most or all benchmarked peers. A reader should be able to say "if my listing looked like this I'd be happy." |
| **B** | 70-84 | Solid. Clear identifiable gaps with clear fixes. Business is roughly at peer parity, with two or three concrete moves that would push it above peers. |
| **C** | 50-69 | Functional but underperforming. The basics work, but a meaningful segment of opportunity is being missed. Behind most benchmarked peers. |
| **D** | 30-49 | Major gaps. Multiple table-stakes are missing. Behind every benchmarked peer on at least one important axis. |
| **F** | 0-29 | Catastrophic. The pillar is actively losing the business deals. Either nonexistent or so broken it has negative value. |

The score within a band is a judgment call too. "Mid-D = ~40" — pick the integer that feels right given the signal list.

---

## 3. Hard-cap floors (catastrophic gaps)

These are the only places the agent's judgment is overridden:

| Situation | Pillar effect |
|---|---|
| No GBP found / no claimed Google listing | Footprint capped at F (≤29). Brand Search capped at D (≤49). |
| GBP suspended | Footprint capped at F (≤29). |
| Website unreachable / SSL broken / 5xx errors on homepage | Website Performance capped at F (≤29). Keyword Rankings capped at F (≤29). |
| No reviews on any platform (Google, Yelp, Birdeye, BBB) | Reviews & Reputation capped at F (≤29). |
| Zero ranking keywords AND zero referring domains (Ahrefs) | Keyword Rankings capped at F (≤29). |
| No social channels of any kind | Social Media capped at F (≤29). |

Below the cap, the grade can be even lower if the agent reasons it should be. The cap is a ceiling, not a floor.

When a data source fails (Ahrefs MCP, PSI API), the affected pillar is marked "data unavailable" in the visible signal list and the agent grades on what it can observe, with the caveat called out in the audit body.

---

## 4. The workflow per pillar

For each of the six pillars, the agent does this in order:

### Step A — Enumerate signals

Pull 5-10 concrete data points relevant to the pillar. Each signal is a single line: the data point + the source.

Example (Footprint):
```
- GBP claimed: yes (per Maps panel)
- GBP primary category: "Embroidery & Crochet"
- GBP secondary categories: 0 visible
- Phone on own contact page: (817) 264-6564
- Phone on GBP: (817) 264-6564
- Phone on Birdeye: (817) 264-6564
- Phone on BBB: (817) 899-2158 — MISMATCH
- Phone on Yelp: (817) 264-6564
- Birdeye claim status: unclaimed
- BBB claim status: unclaimed
- Yelp claim status: claimed
- Hours on own page: Mon-Fri 9-5:30; Sat by appt
- Hours on GBP: Mon-Fri 9-5
- Hours on Birdeye: Mon-Fri 9-6
- Apple Maps presence: not verified
- Bing Places presence: not verified
```

### Step B — Anchor to a known example

State which anchor calibrates this grade. Two anchors are stable enough to use today:

- **Apparel Junction** (issued 2026-05-28) — D overall (38). Pillar grades: Footprint D (42), Reviews C (55), Social D (38), Website D (40), Brand Search D (35), Keyword Rankings F (18).
- **RiteWay Heating, Cooling & Plumbing** (issued 2026-05-22, regraded under this approach) — A overall (~90). Strong across every pillar.

State the anchor like: *"This business's Footprint signal list reads close to Apparel Junction's — phone mismatch on one major directory, two unclaimed majors, wrong GBP primary. Slightly better than Apparel Junction because Apple Maps is verified. Lands in upper D."*

If neither anchor fits well (e.g., this business is mid-tier and both anchors are extremes), say so explicitly and grade by the verbal band definitions. New anchors get added to this document as they accumulate.

### Step C — Assign letter and 0-100 score

Write the letter (A/B/C/D/F) and a single integer in the band. The integer is judgment, not arithmetic.

### Step D — Write the rationale

One paragraph (3-5 sentences). Must cite specific signals and the anchor. Example:

```
Footprint lands at D (42) — same band as Apparel Junction. The phone is consistent on
seven of eight checked directories but mismatches on BBB (817-899-2158 vs the canonical
817-264-6564). Birdeye and BBB are both unclaimed, leaving strangers to shape the first
impression on two major review surfaces. The GBP primary category reads "Embroidery &
Crochet" when the business is actually a screen-printing-and-embroidery shop — a
direct hit to Maps ranking eligibility. Apple Maps and Bing Places presence couldn't be
verified in this run, so those deductions are deferred.
```

### Step E — Record to the Grading Notes file

Append Steps A-D to `<BusinessName>_Grading-Notes_v1.md`. This file is the working artifact that next quarter's re-grade reads before regrading. It does not ship to the prospect.

---

## 5. Overall Grade

The Overall Grade is the rounded average of the six pillar scores, mapped to the §2 letter bands. Apparel Junction: (42+55+38+40+35+18)/6 = 38 → D. Use the integer average; don't redo the judgment.

**Sanity-check rule:** After computing the average, ask whether the Overall feels right for the business. If the gut says "this is obviously a D but my average gave a C" or vice versa, that means one of the pillar grades is probably wrong. Don't tune the Overall to taste — go back and find the pillar that was over- or under-graded. Reasoning grades should rarely produce a wrong Overall.

---

## 6. Anchored examples — the calibration set

These are the live anchors. Treat them like reference photos a colorist works from.

### Anchor A — Apparel Junction (Custom Embroidery, Arlington TX) — Overall D

**Why D, not C:** 34 years in business with no Knowledge Panel, 3 ranking keywords, 1 monthly organic visit, NAP inconsistent, two unclaimed major directories, AI-generic blog content, no video, fragmented domains. Every pillar except Reviews fails table-stakes. Multiple deals lost to a 1-star Yellow Pages result and a "Not Rated" BBB page. The business is producing real work but the digital storefront doesn't reflect it.

**Pillar grades:**
- Footprint D (42) — phone mismatch on BBB; Birdeye and BBB unclaimed; wrong GBP primary category.
- Reviews C (55) — 4.1★ is solid; 31 lifetime reviews is poor; 0 in the last 12 months is the killer; behind every benchmarked peer on volume.
- Social D (38) — FB and IG exist but dormant; no video anywhere; founder LinkedIn untapped; missing TikTok/YouTube/Pinterest.
- Website D (40) — three fragmented domains, InkSoft subpath storefront, no schema, anonymous blog author, AI-generic content, no service-city pages.
- Brand Search D (35) — own domain not in top 3 on brand SERP; Knowledge Panel missing; 1-star Yellow Pages result on page 1; BBB "Not Rated" on page 1; DR 21.
- Keyword Rankings F (18) — 3 ranking keywords; 1 monthly visit; none commercial-intent (all customer-specific subdomains).

### Anchor B — RiteWay Heating, Cooling & Plumbing (HVAC + Plumbing, Tucson AZ) — Overall A (~90)

**Why A, not B:** 67 years in business since 1959, 12,680 Google reviews at 4.9★, DR 35 with 650 referring domains, BBB A+ accredited since 1976, brand SERP fully owned, multi-type LocalBusiness schema, ~200 active Google ads, multi-market expansion (Tucson + Phoenix). The bottleneck is non-brand head-keyword targeting and one GBP primary-category question — both fixes, not structural problems.

**Pillar grades (predicted under this approach):**
- Footprint A (~92) — NAP consistent; all major directories claimed; only friction is the GBP primary-category question (Plumber vs HVAC contractor in an HVAC-first brand).
- Reviews A (100) — 12,680 reviews at 4.9★ is best-in-class for the market.
- Social B (~84) — FB, IG, YouTube, LinkedIn co all active; IG name drift ("AC & Plumbing" drops "Heating"); founder LinkedIn presence unconfirmed.
- Website B+ (~85) — strong schema, GTM in place, but CallRail missing and service-city landing pages not confirmed; PSI unavailable in this audit run.
- Brand Search A (~90) — own domain #1 on brand SERP; Knowledge Panel renders; no risk items; DR 35.
- Keyword Rankings A (~90) — 795 ranking keywords; 147 in top-3; 3,039 monthly visits; multiple service-city wins. Only friction is missing the very top head terms ("ac repair tucson," "plumber tucson").

When new audits land between these two, the agent reasons toward whichever anchor fits best on each pillar.

---

## 7. Grading discipline (non-negotiables)

1. **Enumerate signals before grading.** No grade gets written without 5-10 concrete data points in the signal list. This is the part formulas were trying to enforce — keep it.
2. **Show the anchor.** Every grade cites the anchor it calibrated against. "Closest to Apparel Junction's Footprint" or "Closer to RiteWay's Reviews, just shy of A."
3. **Hard caps are hard.** No reasoning around a catastrophic gap. No GBP → Footprint capped at F.
4. **Never fabricate signals to justify a grade.** If a signal can't be collected, mark it "data unavailable" and grade on what's observable.
5. **One paragraph of rationale per pillar.** No skipping. The rationale is what makes quarterly re-grades meaningful.
6. **Write to the Grading Notes file.** Not the audit body. The audit body shows the grade and a one-sentence read; the working file holds the receipts.

---

## 8. Quarterly re-grade workflow

When re-auditing a client at +90 days, +180 days, etc.:

1. Read the prior `Grading-Notes_v1.md`. Note the previous signal list and the rationale per pillar.
2. Run the new audit and enumerate the current signal list per pillar.
3. Diff the lists. Did the gaps actually close (BBB now claimed, GBP primary corrected, service-city pages live, review velocity up)?
4. Assign the new grade by the same anchored-reasoning process.
5. Write the new rationale citing both the current signals and the prior signal list. ("Footprint moved from D to B because BBB is now claimed, the GBP primary category is fixed, Apple Maps is verified — three of the four D-signals from May 2026 are closed.")
6. Append to the Grading Notes file (don't overwrite — keep history).

That history is the proof that the engagement is producing improvement. It's also the data that lets us tune anchors and add new ones.

---

## 9. Adding new anchors

Two anchors (Apparel Junction + RiteWay) is a thin calibration set. The agent should propose new anchors when:

- A graded audit lands in a band that's poorly served by the current anchors (e.g., a mid-C business when both anchors are at the extremes).
- A pillar consistently grades differently than gut would say across multiple runs.
- A new industry vertical produces enough audits that an industry-specific anchor would help (e.g., "Legal Services A-tier anchor," "Restaurants D-tier anchor").

New anchors live in §6 of this document. Adding one is a deliberate update — name the business, date, full per-pillar signal list, and rationale. Review with Dennis before adding.

---

## 10. What changed from v1 (the strict rubric)

For anyone who saw the rubric:

- Removed: per-pillar deduction tables with cap rules.
- Removed: "subtract 12 for unclaimed major directory" arithmetic.
- Kept: 5-letter scale and score bands.
- Kept: hard-cap floors for catastrophic gaps (now §3).
- Kept: HARD STOP handling for data unavailability.
- Kept: Apparel Junction and RiteWay as worked examples (now §6).
- Added: explicit signal-enumeration step (§4 Step A).
- Added: required anchor citation (§4 Step B).
- Added: rationale paragraph requirement (§4 Step D).
- Added: Grading Notes companion file (§4 Step E, §8).
- Added: new-anchor process (§9).

The previous rubric document remains in the folder for reference. Production grading uses this approach.
