"""
Quick Audit — PDF renderer (generalized, JSON-driven).

Reads a structured `audit-spec.json` and produces a Dennis-style PDF using the
Local Service Spotlight color palette. Used by the quick-audit scheduled
task in Step 14 (PDF render).

USAGE
-----
    python3 render_audit_pdf.py --spec /tmp/<slug>_audit.json --out /path/to.pdf

JSON SPEC SCHEMA
----------------
The spec is a single JSON object with three top-level keys:

{
  "meta":            { ... cover-page + footer metadata ... },
  "sections":        [ { id, title, question?, blocks: [...] }, ... ],
  "exec_summary":    { ... convenience block for the standardized Section 01 ... }
}

`meta` fields (all strings unless noted):
  business_name              "Expert Services"
  business_descriptor        "Plumbing, Heating, Air & Electrical"
  business_location_label    "Utah (Salt Lake + Utah Counties)"
  contact_name               "Owner / Operations Lead"  (or person + role)
  contact_role               (optional)
  address_lines              ["1190 N 1200 W, Orem, UT 84057", ...]   (list)
  phone                      "(385) 446-5727"
  website                    "expertservicesutah.com"
  issue_date                 "May 28, 2026"
  order_number               "F2F79621"
  auditor_org                "BlitzMetrics  •  Local Service Spotlight"
  auditor_contact_line       "Local Service Spotlight  •  dennis@..."
  footer_brand_line          "Expert Services Quick Audit  |  Prepared by BlitzMetrics..."

`exec_summary` fields (drive the Section 01 page; renderer wires them together):
  lede                       "..." (paragraph text)
  overall_grade:             { letter, name, oneliner }
  pillars:                   [ { letter, title, text }, ... 6 rows ]
  scores:                    [ { pillar, score }, ... 6 rows ]
  bottom_line                "..." (paragraph text)

`sections` is a list (rendered in order, page-break between each). Each section:
  { "id": "03",
    "title": "FOOTPRINT & LISTINGS",
    "question": "Is the basic information consistent?",  // optional
    "blocks": [ ... ] }

Block types (each block is a dict with "type" plus type-specific fields):

  {"type":"h3",           "text":"..."}
  {"type":"paragraph",    "text":"..."}
  {"type":"spacer",       "height": 12}                  // points
  {"type":"grade_banner", "letter":"D","pillar":"Footprint","oneliner":"..."}
  {"type":"stat_callout", "stats":[["1,295","Google reviews"], ...]}
  {"type":"data_table",   "header":["A","B"], "rows":[["x","y"], ...],
                          "col_widths":[2.5, 4.1]}        // inches, optional
  {"type":"callout",      "head":"BOTTOM LINE","body":["...", "..."]}
  {"type":"bullets",      "items":["...","..."]}
  {"type":"centered",     "text":"...","color":"deep_teal","size":10}

The Section 01 (Executive Summary) is auto-built from `exec_summary` and does
not require explicit blocks. If the spec includes a section with id "01", its
blocks are rendered AFTER the auto-built exec summary content.

HTML-ish formatting inside text fields is supported (reportlab Paragraph
flavor): <b>...</b>, <i>...</i>, <font color="#hex">, &mdash;, &#9733;, etc.
"""

import argparse
import json
import sys

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
)
from reportlab.lib.enums import TA_CENTER


# ---------- LSS palette ----------

DEEP_TEAL  = colors.HexColor("#1B4D5C")
MED_TEAL   = colors.HexColor("#22698A")
PALE_TINT  = colors.HexColor("#EAF2F8")
AMBER      = colors.HexColor("#F5A623")
ORANGE     = colors.HexColor("#D87830")
RED        = colors.HexColor("#C0392B")
TEXT_DARK  = colors.HexColor("#1E293B")
TEXT_BODY  = colors.HexColor("#334155")
TEXT_MUTED = colors.HexColor("#7A7A7A")
NEAR_WHITE = colors.HexColor("#F7F9FA")
BORDER     = colors.HexColor("#E0E0E0")
WHITE      = colors.white

GRADE_COLORS = {
    "A": DEEP_TEAL,
    "B": MED_TEAL,
    "C": AMBER,
    "D": ORANGE,
    "F": RED,
}

NAMED_COLORS = {
    "deep_teal": DEEP_TEAL,
    "med_teal":  MED_TEAL,
    "amber":     AMBER,
    "orange":    ORANGE,
    "red":       RED,
    "text_dark": TEXT_DARK,
    "text_body": TEXT_BODY,
    "text_muted": TEXT_MUTED,
}


# ---------- Styles ----------

_base = getSampleStyleSheet()

H_COVER_TAG       = ParagraphStyle("CoverTag", parent=_base["Normal"], fontName="Helvetica-Bold", fontSize=11, textColor=DEEP_TEAL, spaceAfter=8, leading=14)
H_COVER_TITLE     = ParagraphStyle("CoverTitle", parent=_base["Normal"], fontName="Helvetica-Bold", fontSize=44, textColor=TEXT_DARK, spaceAfter=10, leading=50)
H_COVER_SUB       = ParagraphStyle("CoverSub", parent=_base["Normal"], fontName="Helvetica", fontSize=14, textColor=TEXT_BODY, spaceAfter=24, leading=20)
H_COVER_LABEL     = ParagraphStyle("CoverLabel", parent=_base["Normal"], fontName="Helvetica-Bold", fontSize=9, textColor=DEEP_TEAL, spaceAfter=4, leading=12)
H_COVER_LABEL_VAL = ParagraphStyle("CoverLabelVal", parent=_base["Normal"], fontName="Helvetica", fontSize=11, textColor=TEXT_DARK, spaceAfter=14, leading=15)
H_COVER_TAGLINE   = ParagraphStyle("CoverTagline", parent=_base["Normal"], fontName="Helvetica-Oblique", fontSize=12, textColor=TEXT_MUTED, alignment=TA_CENTER, leading=16)
H_SECTION_Q       = ParagraphStyle("SectionQuestion", parent=_base["Normal"], fontName="Helvetica-Oblique", fontSize=12, textColor=TEXT_MUTED, leading=16, spaceAfter=14)
H_H3              = ParagraphStyle("H3", parent=_base["Normal"], fontName="Helvetica-Bold", fontSize=11, textColor=DEEP_TEAL, leading=14, spaceBefore=10, spaceAfter=6)
P_BODY            = ParagraphStyle("Body", parent=_base["Normal"], fontName="Helvetica", fontSize=10, textColor=TEXT_BODY, leading=14, spaceAfter=8)
P_BODY_TIGHT      = ParagraphStyle("BodyTight", parent=P_BODY, spaceAfter=4)
P_BULLET          = ParagraphStyle("Bullet", parent=P_BODY, leftIndent=14, bulletIndent=0, spaceAfter=5)
P_CALLOUT         = ParagraphStyle("Callout", parent=_base["Normal"], fontName="Helvetica", fontSize=10, textColor=TEXT_DARK, leading=14, leftIndent=10, rightIndent=10, spaceBefore=6, spaceAfter=6)
P_CALLOUT_HEAD    = ParagraphStyle("CalloutHead", parent=_base["Normal"], fontName="Helvetica-Bold", fontSize=10, textColor=DEEP_TEAL, leading=14, leftIndent=10, rightIndent=10, spaceBefore=6, spaceAfter=2)
P_TABLE_HEAD      = ParagraphStyle("TableHead", parent=_base["Normal"], fontName="Helvetica-Bold", fontSize=9, textColor=WHITE, leading=11)
P_TABLE_CELL      = ParagraphStyle("TableCell", parent=_base["Normal"], fontName="Helvetica", fontSize=9, textColor=TEXT_DARK, leading=12)
P_STAT_NUM        = ParagraphStyle("StatNum", parent=_base["Normal"], fontName="Helvetica-Bold", fontSize=28, textColor=DEEP_TEAL, leading=32, alignment=TA_CENTER)
P_STAT_LABEL      = ParagraphStyle("StatLabel", parent=_base["Normal"], fontName="Helvetica-Bold", fontSize=8, textColor=TEXT_MUTED, leading=10, alignment=TA_CENTER)


# ---------- Block helpers ----------

def _grade_box(letter, width=0.6*inch, height=0.6*inch, font_size=22):
    color = GRADE_COLORS.get(letter, TEXT_MUTED)
    tbl = Table(
        [[Paragraph(f'<font color="white" size="{font_size}"><b>{letter}</b></font>',
                    ParagraphStyle("g", alignment=TA_CENTER, leading=font_size+2))]],
        colWidths=[width], rowHeights=[height])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), color),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("BOX", (0,0), (-1,-1), 0, color),
    ]))
    return tbl

def block_h3(text):
    return Paragraph(text, H_H3)

def block_paragraph(text):
    return Paragraph(text, P_BODY)

def block_spacer(height=12):
    return Spacer(1, height)

def block_grade_banner(letter, pillar, oneliner):
    color = GRADE_COLORS.get(letter, TEXT_MUTED)
    return Table(
        [[
            Paragraph(f'<font color="white" size="28"><b>{letter}</b></font>',
                      ParagraphStyle("gb", alignment=TA_CENTER, leading=32)),
            [
                Paragraph(f'<font color="white" size="10"><b>GRADE: {pillar.upper()}</b></font>',
                          ParagraphStyle("pn", leading=12, spaceAfter=3, textColor=WHITE)),
                Paragraph(f'<font color="white" size="10">{oneliner}</font>',
                          ParagraphStyle("po2", leading=13, textColor=WHITE)),
            ],
        ]],
        colWidths=[0.8*inch, 5.8*inch],
        style=TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), color),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("LEFTPADDING", (1,0), (1,0), 14),
            ("TOPPADDING", (0,0), (-1,-1), 10),
            ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ]))

def block_stat_callout(stats):
    n = len(stats)
    cells = [[Paragraph(str(num), P_STAT_NUM),
              Paragraph(str(label).upper(), P_STAT_LABEL)] for num, label in stats]
    tbl = Table([cells], colWidths=[6.6*inch/n]*n)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), PALE_TINT),
        ("BOX", (0,0), (-1,-1), 0.5, BORDER),
        ("INNERGRID", (0,0), (-1,-1), 0.5, BORDER),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 16),
        ("BOTTOMPADDING", (0,0), (-1,-1), 16),
    ]))
    return tbl

def block_data_table(header, rows, col_widths=None):
    head = [Paragraph(h, P_TABLE_HEAD) for h in header]
    body = [[Paragraph(str(c), P_TABLE_CELL) for c in r] for r in rows]
    data = [head] + body
    cw = [w*inch for w in col_widths] if col_widths else None
    tbl = Table(data, colWidths=cw, repeatRows=1)
    style = [
        ("BACKGROUND", (0,0), (-1,0), DEEP_TEAL),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,0), 7),
        ("BOTTOMPADDING", (0,0), (-1,0), 7),
        ("TOPPADDING", (0,1), (-1,-1), 5),
        ("BOTTOMPADDING", (0,1), (-1,-1), 5),
        ("LINEBELOW", (0,0), (-1,-1), 0.3, BORDER),
        ("BOX", (0,0), (-1,-1), 0.5, BORDER),
    ]
    for i in range(2, len(data), 2):
        style.append(("BACKGROUND", (0,i), (-1,i), NEAR_WHITE))
    tbl.setStyle(TableStyle(style))
    return tbl

def block_callout(head, body):
    content = [Paragraph(head, P_CALLOUT_HEAD)]
    for p in body:
        content.append(Paragraph(p, P_CALLOUT))
    tbl = Table([[content]], colWidths=[6.6*inch])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), PALE_TINT),
        ("LINEBEFORE", (0,0), (-1,-1), 3, DEEP_TEAL),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ]))
    return tbl

def block_bullets(items):
    return [Paragraph(f"&bull; {item}", P_BULLET) for item in items]

def block_centered(text, color="deep_teal", size=10):
    style = ParagraphStyle("ctr", parent=P_BODY, fontSize=size,
                           textColor=NAMED_COLORS.get(color, DEEP_TEAL),
                           alignment=TA_CENTER)
    return Paragraph(text, style)


# ---------- Exec-summary-specific helpers ----------

def big_grade_block(letter, name, oneliner):
    color = GRADE_COLORS.get(letter, TEXT_MUTED)
    return Table(
        [[
            _grade_box(letter, width=1.4*inch, height=1.4*inch, font_size=44),
            [
                Paragraph(
                    f'<font color="{color.hexval()}" size="14"><b>{letter} &mdash; {name}</b></font>',
                    ParagraphStyle("g", leading=18, spaceAfter=4)),
                Paragraph(oneliner, ParagraphStyle("go", parent=P_BODY, leading=14,
                                                   fontSize=10, textColor=TEXT_DARK)),
            ],
        ]],
        colWidths=[1.6*inch, 5.0*inch],
        style=TableStyle([
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("LEFTPADDING", (1,0), (1,0), 14),
            ("BACKGROUND", (0,0), (-1,-1), NEAR_WHITE),
            ("BOX", (0,0), (-1,-1), 0.5, BORDER),
            ("LINEBEFORE", (1,0), (1,0), 4, GRADE_COLORS.get(letter, TEXT_MUTED)),
        ]))

def pillar_summary_row(letter, title, text):
    return Table(
        [[
            _grade_box(letter, width=0.55*inch, height=0.55*inch, font_size=18),
            [
                Paragraph(f'<font color="{TEXT_DARK.hexval()}" size="11"><b>{title}</b></font>',
                          ParagraphStyle("pt", leading=14, spaceAfter=2)),
                Paragraph(text, ParagraphStyle("po", parent=P_BODY_TIGHT, fontSize=9.5,
                                               textColor=TEXT_BODY, leading=12.5)),
            ],
        ]],
        colWidths=[0.75*inch, 5.85*inch],
        style=TableStyle([
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("LEFTPADDING", (1,0), (1,0), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ("TOPPADDING", (0,0), (-1,-1), 6),
            ("LINEBELOW", (0,0), (-1,-1), 0.5, BORDER),
        ]))


# ---------- Section header + page chrome ----------

def section_header(num, title, question=None):
    parts = []
    tbl = Table(
        [[Paragraph(num, ParagraphStyle("sn", fontName="Helvetica-Bold",
                                         fontSize=44, textColor=PALE_TINT, leading=44)),
          Paragraph(title, ParagraphStyle("st", fontName="Helvetica-Bold",
                                           fontSize=18, textColor=DEEP_TEAL, leading=22))]],
        colWidths=[0.9*inch, 5.7*inch],
        style=TableStyle([
            ("VALIGN", (0,0), (-1,-1), "BOTTOM"),
            ("BOTTOMPADDING", (0,0), (-1,-1), 2),
            ("LINEBELOW", (0,0), (-1,-1), 1.5, DEEP_TEAL),
        ]))
    parts.append(tbl)
    if question:
        parts.append(Spacer(1, 6))
        parts.append(Paragraph(question, H_SECTION_Q))
    else:
        parts.append(Spacer(1, 12))
    return parts


def page_chrome_factory(footer_line):
    def on_page(canv, doc):
        canv.saveState()
        canv.setStrokeColor(BORDER)
        canv.setLineWidth(0.3)
        canv.line(0.6*inch, 0.55*inch, 7.9*inch, 0.55*inch)
        canv.setFont("Helvetica", 8)
        canv.setFillColor(TEXT_MUTED)
        canv.drawString(0.6*inch, 0.4*inch, footer_line)
        canv.drawRightString(7.9*inch, 0.4*inch, f"Page {doc.page}")
        canv.restoreState()
    return on_page

def on_cover_page(canv, doc):
    canv.saveState()
    canv.setFillColor(DEEP_TEAL)
    canv.rect(0, LETTER[1]-0.4*inch, LETTER[0], 0.4*inch, stroke=0, fill=1)
    canv.setFillColor(AMBER)
    canv.rect(0, LETTER[1]-0.45*inch, LETTER[0], 0.05*inch, stroke=0, fill=1)
    canv.setFillColor(DEEP_TEAL)
    canv.rect(0, 0, LETTER[0], 0.3*inch, stroke=0, fill=1)
    canv.restoreState()


# ---------- Cover + Exec Summary builders ----------

def cover_page(meta):
    flow = []
    flow.append(Spacer(1, 0.6*inch))
    flow.append(Paragraph("QUICK AUDIT  |  DIGITAL &amp; SOCIAL", H_COVER_TAG))
    flow.append(Spacer(1, 0.15*inch))
    flow.append(Paragraph(meta["business_name"], H_COVER_TITLE))
    flow.append(Paragraph(
        f"{meta['business_descriptor']}  |  {meta['business_location_label']}",
        H_COVER_SUB))
    flow.append(Spacer(1, 0.6*inch))

    flow.append(Paragraph("PREPARED FOR", H_COVER_LABEL))
    address_html = "<br/>".join(meta.get("address_lines", []))
    contact_role = meta.get("contact_role")
    prepared_for_lines = [meta["contact_name"]]
    if contact_role:
        prepared_for_lines.append(contact_role)
    if address_html:
        prepared_for_lines.append(address_html)
    if meta.get("phone") or meta.get("website"):
        prepared_for_lines.append(
            f"{meta.get('phone','')}  &bull;  {meta.get('website','')}")
    flow.append(Paragraph("<br/>".join(prepared_for_lines), H_COVER_LABEL_VAL))

    flow.append(Spacer(1, 0.3*inch))
    flow.append(Paragraph("PREPARED BY", H_COVER_LABEL))
    prepared_by = [
        meta["auditor_org"],
        f"Issued: {meta['issue_date']}  &bull;  Order #{meta['order_number']}",
        meta["auditor_contact_line"],
    ]
    flow.append(Paragraph("<br/>".join(prepared_by), H_COVER_LABEL_VAL))

    flow.append(Spacer(1, 1.0*inch))
    flow.append(Paragraph("Six checks. One page-one verdict. Then the fix.",
                          H_COVER_TAGLINE))
    flow.append(PageBreak())
    return flow

def exec_summary_block(exec_data):
    flow = []
    flow.extend(section_header("01", "EXECUTIVE SUMMARY"))
    flow.append(Paragraph("What we found in 5 minutes", H_H3))
    flow.append(Paragraph(exec_data["lede"], P_BODY))
    flow.append(Spacer(1, 10))

    flow.append(Paragraph("Overall Grade", H_H3))
    og = exec_data["overall_grade"]
    flow.append(big_grade_block(og["letter"], og["name"], og["oneliner"]))
    flow.append(Spacer(1, 16))

    flow.append(Paragraph("The Six Checks", H_H3))
    for p in exec_data["pillars"]:
        flow.append(pillar_summary_row(p["letter"], p["title"], p["text"]))
    flow.append(Spacer(1, 14))

    flow.append(Paragraph("Quick Reference Scores", H_H3))
    score_rows = [[s["pillar"], s["score"]] for s in exec_data["scores"]]
    flow.append(block_data_table(["Pillar", "Score"], score_rows,
                                 col_widths=[5.0, 1.6]))
    flow.append(Spacer(1, 14))

    if exec_data.get("bottom_line"):
        bl = exec_data["bottom_line"]
        if isinstance(bl, str):
            bl = [bl]
        flow.append(block_callout("BOTTOM LINE", bl))
    flow.append(PageBreak())
    return flow


# ---------- Generic block dispatcher ----------

def render_block(block):
    t = block["type"]
    if t == "h3":
        return [block_h3(block["text"])]
    if t == "paragraph":
        return [block_paragraph(block["text"])]
    if t == "spacer":
        return [block_spacer(block.get("height", 12))]
    if t == "grade_banner":
        return [block_grade_banner(block["letter"], block["pillar"], block["oneliner"])]
    if t == "stat_callout":
        return [block_stat_callout(block["stats"])]
    if t == "data_table":
        return [block_data_table(block["header"], block["rows"],
                                  col_widths=block.get("col_widths"))]
    if t == "callout":
        body = block["body"]
        if isinstance(body, str):
            body = [body]
        return [block_callout(block["head"], body)]
    if t == "bullets":
        return block_bullets(block["items"])
    if t == "centered":
        return [block_centered(block["text"],
                                color=block.get("color", "deep_teal"),
                                size=block.get("size", 10))]
    raise ValueError(f"Unknown block type: {t}")


def render_section(section):
    flow = []
    flow.extend(section_header(section["id"], section["title"], section.get("question")))
    for block in section.get("blocks", []):
        flow.extend(render_block(block))
    flow.append(PageBreak())
    return flow


# ---------- Top-level build ----------

def build_from_spec(spec, output_path):
    meta = spec["meta"]
    doc = SimpleDocTemplate(
        output_path, pagesize=LETTER,
        leftMargin=0.6*inch, rightMargin=0.6*inch,
        topMargin=0.75*inch, bottomMargin=0.75*inch,
        title=f"{meta['business_name']} Quick Audit",
        author=meta.get("auditor_org", "BlitzMetrics"))

    story = []
    story.extend(cover_page(meta))
    if "exec_summary" in spec:
        story.extend(exec_summary_block(spec["exec_summary"]))
    for section in spec.get("sections", []):
        if section.get("id") == "01" and "exec_summary" in spec:
            # exec_summary already rendered; treat blocks as additional content
            if section.get("blocks"):
                for block in section["blocks"]:
                    story.extend(render_block(block))
                story.append(PageBreak())
            continue
        story.extend(render_section(section))

    footer_line = meta.get(
        "footer_brand_line",
        f"{meta['business_name']} Quick Audit  |  Prepared by BlitzMetrics — Local Service Spotlight")
    on_page = page_chrome_factory(footer_line)

    def layout(canv, doc_):
        if doc_.page == 1:
            on_cover_page(canv, doc_)
        else:
            on_page(canv, doc_)

    doc.build(story, onFirstPage=layout, onLaterPages=layout)


# ---------- CLI ----------

def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--spec", required=True, help="Path to audit-spec.json")
    parser.add_argument("--out",  required=True, help="Output PDF path")
    args = parser.parse_args()

    with open(args.spec, "r", encoding="utf-8") as f:
        spec = json.load(f)
    build_from_spec(spec, args.out)
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
