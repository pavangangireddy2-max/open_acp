# AI Engineer Ladder — career framework v2 for content-department domain teams.
# Source: knowledge/raw/corpora/remixed-0bb5468a.html ("SDE Learning Systems Career
# Framework", March 2026). v2 renames titles to Pavan's "AI Engineer – [Domain]
# Learning Systems" pattern and wires every progression area + rating line to named
# KPI rows in the tracker / team views. Descriptors are carried verbatim from source.
# Outputs: role_cards.xlsx (editable master, 5 tabs) + role_cards.html (artifact).
import json, re, html as H
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

SRC = "/Users/pavan/Desktop/projects/open_acp/knowledge/raw/corpora/remixed-0bb5468a.html"
src = open(SRC, encoding="utf-8").read()

def clean(x):
    x = re.sub(r"<br\s*/?>", "\n", x)
    x = re.sub(r"<[^>]+>", "", x)
    return H.unescape(x).replace(" ", " ").strip()

# ---------------------------------------------------------------- parse source
comp_boxes = [(clean(a), clean(b), clean(c)) for a, b, c in re.findall(
    r'<div class="comp-box">\s*<div class="role-level">(.*?)</div>\s*'
    r'<div class="comp-range">(.*?)</div>\s*<div class="note">(.*?)</div>', src, re.S)]
assert len(comp_boxes) == 5, comp_boxes

# Section text/tables come from the pre-parsed JSON (h3 headings separated into
# "sub" there — the flat regex walk can't do that); comp boxes are div-based and
# absent from the JSON, hence the direct extraction above.
sections = {s["h2"]: s for s in
            json.load(open("role_cards_source.json", encoding="utf-8"))["sections"]}

AREAS_T   = sections["21 Progression Areas"]["tables"]          # 4 tables, hdr + rows
PORTF     = sections["Portfolio Metrics by Level"]["tables"][0]
COMPLEX   = sections["Domain Complexity Reference"]["tables"][0]
PRODUCTS  = sections["Product Baselines (Student Reach)"]["tables"][0]
DOMAINS   = sections["Complete Domain List"]["tables"][0]
SCALE     = sections["Performance Rating Framework (SDE Lead Level)"]["tables"][0]
RT        = sections["Performance Rating Framework (SDE Lead Level)"]["text"]
KEYTERMS  = sections["Key Terms"]["tables"][0]
assert sum(len(t) - 1 for t in AREAS_T) == 21 and len(RT) == 21

CATS = ["Foundation", "Core Creation and Quality", "Operational Excellence",
        "Collaboration and Stakeholders"]
AREAS = []  # (category, area, assoc, e1, e2, lead)
for cat, t in zip(CATS, AREAS_T):
    for r in t[1:]:
        AREAS.append((cat, r[0], r[1], r[2], r[3], r[4]))

def parse_lines(lines):
    out = []
    for ln in lines:
        m = re.match(r"(.+?) \((\d+)%\): (.+)", ln)
        out.append((m.group(1), int(m.group(2)), m.group(3)))
    return out

PILLARS = [  # (name, weight, sublines, kpi reads aligned to sublines)
    ("Performance", 50, parse_lines(RT[1:5]), [
        "Summative + Formative Skill Assessment Achievement · org KRA 1 SPI Score Bands",
        "Content Issue Resolution Efficiency · Content Issue Recurrence Rate",
        "Industry Update Adherence · Tech Stack Freshness Rate",
        "Pedagogy Initiative Impact · Agentic Production Coverage"]),
    ("Role Competence", 25, parse_lines(RT[5:10]), [
        "Content Issue Recurrence Rate · Module-Quiz Score Bands · Engagement-Matrix Cell Migration",
        "Agentic Production Coverage",
        "Cost per Learning Hour · Cost per MCQ · Cost per Coding Question",
        "Learning Content Hours Delivered · Practice & Assessment Content Pieces Delivered",
        "Cross-functional Sprint Delivery Rate · Stakeholder Content Request Fulfillment Rate"]),
    ("Develop the Best", 15, parse_lines(RT[10:15]), [None] * 5),
    ("Culture and Values", 10, parse_lines(RT[15:20]), [None] * 5),
]
CALC = RT[20]

# ---------------------------------------------------------------- v2 additions
NEW_TITLE = {"Associate SDE": "Associate AI Engineer", "SDE 1": "AI Engineer 1",
             "SDE 2": "AI Engineer 2", "SDE Lead": "AI Engineer Lead", "SDE 3": "AI Engineer 3"}

def retitle_example(note):
    return re.sub(r'(Associate SDE|SDE Lead|SDE [123]), Learning Systems - ([^"]+)',
                  lambda m: f"{NEW_TITLE[m.group(1)]} – {m.group(2)} Learning Systems", note)

LEVELS = []  # (new_title_pattern, old_title, comp, exp, note, surface)
SURFACE = [
    "Contributes to this team's Section B rows under review — no rows answered for yet; growth is read through review evidence.",
    "Answers for the Section B velocity + quality rows of the modules they own (their content hours, pieces, issue-recurrence share).",
    "Answers for a domain slice of Section B — effectiveness, velocity and Evaluation Environment Coverage for their courses; first Section C asks raised in their name.",
    "Answers for the team's full Section B at review and supports the Section A lane numbers; the rating framework below applies as written.",
    "Shapes org-tracker rows and cross-domain standards; portfolio spans teams — reads through §5 department KPIs and org KRAs, not one team view.",
]
for (title, comp, note), surf in zip(comp_boxes, SURFACE):
    old = title.split(",")[0].strip()
    scope = title[title.find("["):title.find("]") + 1] if "[" in title else "[Domain]"
    scope = scope.replace("Domain Name", "Domain")  # normalize the placeholder token
    LEVELS.append((f"{NEW_TITLE[old]} – {scope} Learning Systems",
                   title, comp, retitle_example(note), surf))

WIRING = [  # (category, area, [kpi rows], note)
    ("Foundation", "Scope of Work", [],
     "Calibration, not a metric — read through the Portfolio Metrics matrix + domain complexity multipliers below."),
    ("Foundation", "Influence", [],
     "Read through interfaces: team-view Section C asks raised and honoured, §7 counterparty standing."),
    ("Core Creation and Quality", "Content Quality",
     ["Content Issue Resolution Efficiency", "Content Issue Recurrence Rate", "Module-Quiz Score Bands"],
     "The Learning Domains quality loop — recurrence is the tell that a fix actually held."),
    ("Core Creation and Quality", "Content Effectiveness",
     ["Learner Accessed Content Completion Rate", "Practice Attempt-to-Completion Rate",
      "Engagement-Matrix Cell Migration", "Summative + Formative Achievement"],
     "Access-conditioned stickiness pair + the matrix — conduction effects stripped by design."),
    ("Core Creation and Quality", "Curriculum Design",
     ["Pedagogy Initiative Impact", "University Curriculum Compliance"],
     "PII is SME-owned (Pedagogy Experts contribute); compliance rows apply on university-facing work."),
    ("Core Creation and Quality", "Content Velocity",
     ["Learning Content Hours Delivered", "Vernacular Content Hours Delivered",
      "Practice & Assessment Content Pieces Delivered"],
     "The per-level hours ladder in the matrix is the personal share of these team rows."),
    ("Core Creation and Quality", "Industry Upgrades",
     ["Industry Update Adherence", "Tech Stack Freshness Rate"],
     "Adherence = planned updates land on schedule; freshness = the audit behind relevance."),
    ("Core Creation and Quality", "Production Systems",
     ["Agentic Production Coverage"],
     "Publishing through ACP pipelines; cost rows below read the efficiency it buys."),
    ("Core Creation and Quality", "Learning Systems Design",
     ["Evaluation Environment Coverage", "Domain Capability Delivery"],
     "The Domain Product Enablement pair — raised/accepted by SMEs, built by PMs + Engineering, "
     "accountability in Learning Domains. Reads: Learning Environment Satisfaction, PAtC env-friction leg."),
    ("Core Creation and Quality", "GenAI Orchestration & Content Automation",
     ["Agentic Production Coverage", "Cost per MCQ Generated", "Cost per Coding Question"],
     "Mandatory from AI Engineer 1 — orchestration shows up as coverage plus falling unit costs."),
    ("Core Creation and Quality", "Business Impact",
     ["Summative Skill Assessment Achievement Rate", "Formative Skill Assessment Achievement Rate",
      "Graded Assessment Achievement Rate (NIAT)", "Weekly Active Users (Launchpad)"],
     "The Section B Business Impact block; ladders to org KRAs 1, 4 and 5."),
    ("Operational Excellence", "Problem Solving", [], "Review evidence — no direct KPI by design."),
    ("Operational Excellence", "Execution",
     ["Cross-functional Sprint Delivery Rate", "Stakeholder Content Request Fulfillment Rate"],
     "Committed-vs-delivered is the execution read."),
    ("Operational Excellence", "Learnability", [],
     "Review evidence — GenAI adoption surfaces indirectly in Agentic Production Coverage contribution."),
    ("Operational Excellence", "Communication", [], "Review evidence — no direct KPI by design."),
    ("Operational Excellence", "Ambiguity Handling", [], "Review evidence — no direct KPI by design."),
    ("Operational Excellence", "Best Practices",
     ["Operations & Growth Cost", "Creative Resource Utilisation Rate"],
     "Hygiene guardrails (PM-managed reads) — no org ladder by design."),
    ("Collaboration and Stakeholders", "Cross-Functionality",
     ["Cross-functional Sprint Delivery Rate"],
     "Plus the health of Section C asks the person is party to."),
    ("Collaboration and Stakeholders", "Stakeholder Collaboration",
     ["Stakeholder Content Request Fulfillment Rate"],
     "Ladders to dept Stakeholder Alignment (§5)."),
    ("Collaboration and Stakeholders", "Cross-Product Work", [],
     "Read through the Product column — Section B rows carried per product (NIAT · Academy · Launchpad slots)."),
    ("Collaboration and Stakeholders", "Mentorship", [],
     "Rating Pillar 3 (Develop the Best) — deliberately review-based, no KPI row."),
]
assert len(WIRING) == 21

BRIDGE = [
    ("Functions", "§10 embedded functions + the content domain teams. “Packaging Teams” = Content Systems & Infra teams (Pavan, Aug 2026)."),
    ("Stakeholders", "§7 counterparties — reached through team-view Section C asks, never staffed into lanes."),
    ("Leadership", "Unchanged — Founders, HODs."),
    ("Peer Content Teams", "The other §10 sub-departments (domain teams)."),
    ("Support Teams", "Unchanged — HR, Finance, L&D, Facilities."),
    ("“Owns” / P&L language", "Translated to the axis rule: Lane (col L) = accountability · Functions (col K) = who works. "
     "A Lead answers for the team's Section B; lane numbers stay with lane leads."),
]

FS_PILOT = {
    "team": "FullStack & CS Core",
    "titles": ["Associate AI Engineer – FullStack Learning Systems",
               "AI Engineer 1 – FullStack Learning Systems",
               "AI Engineer 2 – FullStack & CS Core Learning Systems",
               "AI Engineer Lead – FullStack & CS Core Learning Systems"],
    "complexity": "High (2.0x) — FullStack · Medium (1.5x) — CS Core",
    "domains": [r for r in DOMAINS[1:] if r[0] in ("Full Stack", "CS Core")],
    "surface": "Metric surface = the FullStack & CS Core team view: Section A 19 mirrored tracker rows · "
               "Section B 24 owned rows (incl. the Domain Product Enablement pair) · Section C 4 asks.",
}

# ---------------------------------------------------------------- xlsx
TEAL, TEAL_MID, TEAL_TINT = "FF0E6E5C", "FF7CBFB1", "FFE6F2EF"
INK, MUTED = "FF1A1A1A", "FF666666"
THIN = Border(*[Side(style="thin", color="FFCCCCCC")] * 4)

wb = Workbook()
wb.remove(wb.active)

def F(sz=9, bold=False, color=INK, italic=False):
    return Font(name="Calibri", size=sz, bold=bold, color=color, italic=italic)

def sheet(name, widths):
    ws = wb.create_sheet(name)
    ws.sheet_properties.tabColor = TEAL
    for col, w in zip("ABCDEFGHIJ", widths):
        ws.column_dimensions[col].width = w
    return ws

def put(ws, r, c, v, *, sz=9, bold=False, color=INK, fill=None, wrap=True, italic=False):
    cell = ws.cell(row=r, column=c, value=v)
    cell.font = F(sz, bold, color, italic)
    cell.alignment = Alignment(vertical="top", wrap_text=wrap)
    cell.border = THIN
    if fill:
        cell.fill = PatternFill("solid", start_color=fill)
    return cell

def title_row(ws, r, txt, ncols):
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=ncols)
    c = put(ws, r, 1, txt, sz=11, bold=True, color="FFFFFFFF", fill=TEAL)
    for cc in range(1, ncols + 1):
        ws.cell(row=r, column=cc).fill = PatternFill("solid", start_color=TEAL)
    return r + 1

def hdr_row(ws, r, cells):
    for c, v in enumerate(cells, 1):
        put(ws, r, c, v, bold=True, fill=TEAL_TINT)
    return r + 1

# Tab 1 — Ladder
ws = sheet("Ladder", (26, 30, 16, 60, 60))
r = title_row(ws, 1, "AI Engineer Ladder — content-department domain teams · v2 August 2026 "
                     "(titles renamed from the March 2026 SDE framework; descriptors verbatim)", 5)
r = hdr_row(ws, r, ("Title (v2 pattern)", "Formerly", "Comp | Experience", "Scope (source, examples retitled)", "Metric surface (v2)"))
for new, old, comp, note, surf in LEVELS:
    put(ws, r, 1, new, bold=True)
    put(ws, r, 2, old, color=MUTED)
    put(ws, r, 3, comp)
    put(ws, r, 4, note)
    put(ws, r, 5, surf)
    ws.row_dimensions[r].height = max(52, 14 * (len(note) // 78 + 1))
    r += 1

# Tab 2 — Progression Areas
ws = sheet("Progression Areas", (24, 22, 34, 34, 34, 34))
r = title_row(ws, 1, "21 progression areas × 4 levels — verbatim from source. AI Engineer 3 sits above "
                     "Lead (org-wide scope); the matrix deliberately stops at Lead.", 6)
r = hdr_row(ws, r, ("Category", "Area", "Associate AI Engineer", "AI Engineer 1", "AI Engineer 2", "AI Engineer Lead"))
for cat, area, a, e1, e2, ld in AREAS:
    put(ws, r, 1, cat, color=MUTED)
    put(ws, r, 2, area, bold=True)
    for c, v in enumerate((a, e1, e2, ld), 3):
        put(ws, r, c, v)
    ws.row_dimensions[r].height = max(40, 13 * (max(len(x) for x in (a, e1, e2, ld)) // 34 + 1))
    r += 1

# Tab 3 — KPI Wiring
ws = sheet("KPI Wiring", (24, 26, 62, 62))
r = title_row(ws, 1, "Progression area → named KPI rows (tracker / FullStack & CS Core team view). "
                     "The v2 addition: every area now cites live rows, or says why it deliberately has none.", 4)
r = hdr_row(ws, r, ("Category", "Area", "Wired to (KPI rows)", "Note"))
for cat, area, rows, note in WIRING:
    put(ws, r, 1, cat, color=MUTED)
    put(ws, r, 2, area, bold=True)
    put(ws, r, 3, " · ".join(rows) if rows else "— (by design)", color=TEAL if rows else MUTED)
    put(ws, r, 4, note)
    ws.row_dimensions[r].height = max(28, 13 * (len(note) // 60 + 1))
    r += 1

# Tab 4 — Rating Framework
ws = sheet("Rating Framework", (26, 9, 58, 58))
r = title_row(ws, 1, "Performance rating — AI Engineer Lead level. 4 pillars, weighted; target 3.0+ on 5. "
                     "Each line now reads from named KPI rows.", 4)
for name, wt, subs, reads in PILLARS:
    r = hdr_row(ws, r, (f"Pillar: {name}", f"{wt}%", "What it measures (verbatim)", "Reads from (KPI rows)"))
    for (nm, swt, desc), rd in zip(subs, reads):
        put(ws, r, 1, nm, bold=True)
        put(ws, r, 2, f"{swt}%")
        put(ws, r, 3, desc)
        put(ws, r, 4, rd if rd else "Review-based — no KPI row by design", color=TEAL if rd else MUTED)
        ws.row_dimensions[r].height = max(28, 13 * (len(desc) // 56 + 1))
        r += 1
put(ws, r, 1, "Calculation", bold=True)
ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=4)
put(ws, r, 2, CALC)
r += 2
r = hdr_row(ws, r, ("Rating", "Label", "Meaning", ""))
for sc in SCALE[1:]:
    put(ws, r, 1, sc[0]); put(ws, r, 2, sc[1]); put(ws, r, 3, sc[2]); put(ws, r, 4, "")
    r += 1

# Tab 5 — Calibration
ws = sheet("Calibration", (26, 34, 34, 34, 34))
r = title_row(ws, 1, "Calibration: portfolio by level · domain complexity · product baselines · "
                     "domain catalogue · vocabulary bridge (2026 doc → KPI system)", 5)
r = hdr_row(ws, r, tuple(PORTF[0][:1] + ["Associate AI Engineer", "AI Engineer 1", "AI Engineer 2", "AI Engineer Lead"]))
for row in PORTF[1:]:
    put(ws, r, 1, row[0], bold=True)
    for c, v in enumerate(row[1:], 2):
        put(ws, r, c, v)
    r += 1
r += 1
r = hdr_row(ws, r, tuple(COMPLEX[0] + [""] * (5 - len(COMPLEX[0]))))
for row in COMPLEX[1:]:
    for c, v in enumerate(row, 1):
        put(ws, r, c, v, bold=(c == 1))
    r += 1
r += 1
r = hdr_row(ws, r, tuple(PRODUCTS[0] + [""] * (5 - len(PRODUCTS[0]))))
for row in PRODUCTS[1:]:
    for c, v in enumerate(row, 1):
        put(ws, r, c, v, bold=(c == 1))
    r += 1
r += 1
r = hdr_row(ws, r, tuple(DOMAINS[0] + [""] * (5 - len(DOMAINS[0]))))
for row in DOMAINS[1:]:
    for c, v in enumerate(row, 1):
        put(ws, r, c, v, bold=(c == 1))
    r += 1
r += 1
r = hdr_row(ws, r, ("2026 doc term", "In the KPI system", "", "", ""))
for term, mapping in BRIDGE:
    put(ws, r, 1, term, bold=True)
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=5)
    put(ws, r, 2, mapping)
    ws.row_dimensions[r].height = max(15, 13 * (len(mapping) // 120 + 1))
    r += 1

wb.save("role_cards.xlsx")

# ---------------------------------------------------------------- html
RAMP = [("#d9ece7", "#134237"), ("#b3d9d0", "#113b31"), ("#7cbfb1", "#0c322a"),
        ("#3f9682", "#ffffff"), ("#0e6e5c", "#ffffff")]

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def chips(rows):
    if not rows:
        return '<span class="nodesign">— by design</span>'
    return " ".join(f'<span class="kpi">{esc(x)}</span>' for x in rows)

STYLE = """  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #ffffff; padding: 40px 20px; color: #1a1a1a; line-height: 1.5; }
  .container { max-width: 1180px; margin: 0 auto; }
  h1 { font-size: 2em; margin-bottom: 8px; font-weight: 700; }
  .subtitle { font-size: 1em; color: #666; margin-bottom: 30px; max-width: 72ch; }
  h2 { font-size: 1.4em; margin: 44px 0 18px 0; padding-bottom: 8px; border-bottom: 2px solid #000; font-weight: 700; }
  .sectionlead { color: #666; font-size: 0.92em; margin: -8px 0 18px; max-width: 78ch; }
  .key-point { background: #e6f2ef; border-left: 3px solid #0e6e5c; padding: 12px 14px; margin: 20px 0; font-size: .93em; }
  .scroll { overflow-x: auto; }
  table { width: 100%; border-collapse: collapse; margin-bottom: 26px; font-size: 0.85em; }
  table.wide { min-width: 1050px; }
  th { background: #000; color: #fff; padding: 8px 9px; text-align: left; font-weight: 600; border: 1px solid #000; }
  td { padding: 8px 9px; border: 1px solid #ccc; vertical-align: top; }
  .muted { color: #666; }
  .kpi { font-family: ui-monospace, 'SF Mono', Menlo, monospace; font-size: .84em; display: inline-block;
    background: #e6f2ef; color: #0b4f43; border: 1px solid #a8cfc6; border-radius: 3px;
    padding: 0 6px; margin: 1px 2px 1px 0; white-space: nowrap; }
  .nodesign { color: #888; font-style: italic; font-size: .92em; }
  .ladder { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin: 18px 0 8px; }
  .lvl { border: 1px solid #ccc; border-radius: 4px; overflow: hidden; display: flex; flex-direction: column; }
  .lvl-head { padding: 10px 12px; }
  .lvl-head .t { font-weight: 700; font-size: .95em; line-height: 1.25; }
  .lvl-head .was { font-size: .76em; opacity: .75; margin-top: 3px; }
  .lvl-comp { padding: 7px 12px; font-size: .82em; font-weight: 600; border-bottom: 1px solid #e2e2e2;
    background: #fafafa; font-variant-numeric: tabular-nums; }
  .lvl-body { padding: 10px 12px; font-size: .8em; color: #333; flex: 1; }
  .lvl-surf { padding: 9px 12px; font-size: .78em; color: #0b4f43; background: #f2f8f6; border-top: 1px solid #e2e2e2; }
  .pillar { border: 1px solid #ccc; border-radius: 4px; margin-bottom: 14px; overflow: hidden; }
  .pillar-head { display: flex; align-items: baseline; gap: 12px; padding: 9px 12px; background: #f4f4f4;
    border-bottom: 1px solid #ddd; }
  .pillar-head .nm { font-weight: 700; }
  .pillar-head .wt { font-weight: 700; color: #0e6e5c; font-variant-numeric: tabular-nums; }
  .subline { display: grid; grid-template-columns: 210px 46px 1fr; gap: 10px; padding: 8px 12px;
    border-bottom: 1px solid #eee; font-size: .86em; align-items: start; }
  .subline:last-child { border-bottom: none; }
  .subline .swt { color: #0e6e5c; font-weight: 600; font-variant-numeric: tabular-nums; }
  .bar { height: 4px; background: #e4e4e4; border-radius: 2px; margin-top: 5px; }
  .bar i { display: block; height: 4px; background: #0e6e5c; border-radius: 2px; }
  .footnote { font-size: 0.85em; color: #666; margin-top: 34px; border-top: 1px solid #ccc; padding-top: 12px; max-width: 90ch; }
  @media (max-width: 980px) { .ladder { grid-template-columns: 1fr; } }"""

B = []
B.append('<h1>AI Engineer Ladder</h1>')
B.append('<div class="subtitle">Career framework for content-department domain teams &middot; v2, August 2026 &middot; '
         'titles follow the <strong>AI Engineer &ndash; [Domain] Learning Systems</strong> pattern &middot; descriptors '
         'carried verbatim from the March 2026 SDE Learning Systems framework &middot; editable master: '
         '<strong>role_cards.xlsx</strong> (5 tabs)</div>')
B.append('<div class="key-point"><strong>What changed in v2:</strong> titles renamed to the AI Engineer pattern; every '
         'progression area and rating line is wired to named KPI rows — anything in a '
         '<span class="kpi">mono chip</span> is a live row on the KPI tracker or the team view, so reviews read off the '
         'sheets instead of impressions. Areas with no chip say so <em>by design</em>. Level content, comp bands and the '
         'rating weights are unchanged from the source framework.</div>')

B.append('<h2>The ladder</h2>')
B.append('<div class="sectionlead">Five levels, linear — AI Engineer 3 sits above Lead (30L+ vs 24&ndash;30L, org-wide '
         'scope); the progression matrix below deliberately stops at Lead. Comp bands included; strip this column before '
         'wide sharing if needed.</div>')
B.append('<div class="ladder">')
for (new, old, comp, note, surf), (bg, fg) in zip(LEVELS, RAMP):
    B.append(f'<div class="lvl"><div class="lvl-head" style="background:{bg};color:{fg}">'
             f'<div class="t">{esc(new)}</div><div class="was">formerly {esc(old)}</div></div>'
             f'<div class="lvl-comp">{esc(comp)}</div>'
             f'<div class="lvl-body">{esc(note)}</div>'
             f'<div class="lvl-surf"><strong>Answers for:</strong> {esc(surf)}</div></div>')
B.append('</div>')

B.append('<h2>21 progression areas</h2>')
B.append('<div class="sectionlead">Grouped into 4 categories; all areas matter, weight varies by level. Verbatim from source.</div>')
for cat in CATS:
    rows = [a for a in AREAS if a[0] == cat]
    B.append(f'<h3 style="margin:20px 0 10px;font-size:1.05em">{esc(cat)} ({len(rows)})</h3>')
    B.append('<div class="scroll"><table class="wide"><tr><th style="width:13%">Area</th>'
             '<th>Associate AI Engineer</th><th>AI Engineer 1</th><th>AI Engineer 2</th><th>AI Engineer Lead</th></tr>')
    for _, area, a, e1, e2, ld in rows:
        B.append(f'<tr><td><strong>{esc(area)}</strong></td><td>{esc(a)}</td><td>{esc(e1)}</td>'
                 f'<td>{esc(e2)}</td><td>{esc(ld)}</td></tr>')
    B.append('</table></div>')

B.append('<h2>KPI wiring</h2>')
B.append('<div class="sectionlead">The v2 addition: each area cites the rows it moves, or says why it deliberately has '
         'none. Rows live on the KPI tracker and the FullStack &amp; CS Core team view (the pilot).</div>')
B.append('<div class="scroll"><table class="wide"><tr><th style="width:15%">Category</th><th style="width:17%">Area</th>'
         '<th style="width:38%">Wired to</th><th>Note</th></tr>')
for cat, area, rows, note in WIRING:
    B.append(f'<tr><td class="muted">{esc(cat)}</td><td><strong>{esc(area)}</strong></td>'
             f'<td>{chips(rows)}</td><td>{esc(note)}</td></tr>')
B.append('</table></div>')

B.append('<h2>Performance rating — AI Engineer Lead</h2>')
B.append(f'<div class="sectionlead">{esc(RT[0])} {esc(CALC)}.</div>')
for name, wt, subs, reads in PILLARS:
    B.append(f'<div class="pillar"><div class="pillar-head"><span class="nm">{esc(name)}</span>'
             f'<span class="wt">{wt}%</span></div>')
    for (nm, swt, desc), rd in zip(subs, reads):
        chip = chips(rd.split(" · ")) if rd else '<span class="nodesign">review-based — no KPI row by design</span>'
        B.append(f'<div class="subline"><div><strong>{esc(nm)}</strong><div class="bar"><i style="width:{swt}%"></i></div></div>'
                 f'<div class="swt">{swt}%</div><div>{esc(desc)}<div style="margin-top:4px">{chip}</div></div></div>')
    B.append('</div>')
B.append('<div class="scroll"><table style="max-width:560px"><tr><th>Rating</th><th>Label</th><th>Meaning</th></tr>')
for sc in SCALE[1:]:
    B.append(f'<tr><td class="muted">{esc(sc[0])}</td><td><strong>{esc(sc[1])}</strong></td><td>{esc(sc[2])}</td></tr>')
B.append('</table></div>')

B.append('<h2>Calibration</h2>')
B.append('<div class="sectionlead">Portfolio expectations by level, domain complexity multipliers, and product reach — '
         'the sizing inputs behind every card.</div>')
B.append('<div class="scroll"><table class="wide"><tr>' + "".join(
    f"<th>{esc(h)}</th>" for h in [PORTF[0][0], "Associate AI Engineer", "AI Engineer 1", "AI Engineer 2", "AI Engineer Lead"]) + "</tr>")
for row in PORTF[1:]:
    B.append("<tr><td><strong>" + esc(row[0]) + "</strong></td>" + "".join(f"<td>{esc(v)}</td>" for v in row[1:]) + "</tr>")
B.append('</table></div>')
for tab, cap in ((COMPLEX, "Domain complexity"), (PRODUCTS, "Product baselines (student reach)"), (DOMAINS, "Domain catalogue")):
    B.append(f'<h3 style="margin:20px 0 10px;font-size:1.05em">{cap}</h3>')
    B.append('<div class="scroll"><table><tr>' + "".join(f"<th>{esc(h)}</th>" for h in tab[0]) + "</tr>")
    for row in tab[1:]:
        B.append("<tr><td><strong>" + esc(row[0]) + "</strong></td>" + "".join(f"<td>{esc(v)}</td>" for v in row[1:]) + "</tr>")
    B.append('</table></div>')

B.append('<h2>Pilot: FullStack &amp; CS Core</h2>')
fp = FS_PILOT
B.append('<div class="key-point"><strong>Instantiated titles:</strong> ' +
         " &middot; ".join(f'<span class="kpi">{esc(t)}</span>' for t in fp["titles"]) +
         f'<br><strong>Complexity:</strong> {esc(fp["complexity"])} &middot; <strong>Catalogue:</strong> ' +
         " · ".join(f'{esc(r[0])} — {esc(r[1])}h · {esc(r[2])}' for r in fp["domains"]) +
         f'<br>{esc(fp["surface"])}</div>')

B.append('<h2>Vocabulary bridge</h2>')
B.append('<div class="scroll"><table><tr><th style="width:22%">2026 doc term</th><th>In the KPI system</th></tr>')
for term, mapping in BRIDGE:
    B.append(f'<tr><td><strong>{esc(term)}</strong></td><td>{esc(mapping)}</td></tr>')
B.append('</table></div>')

B.append('<div class="footnote">Source: SDE Learning Systems Career Framework (March 2026) — descriptors, comp bands, '
         'rating weights and calibration tables carried verbatim; titles renamed and KPI wiring added in v2 (August 2026). '
         'Defaults taken pending red-pen: comp bands included (artifact is private; strip for wide sharing) &middot; '
         'level names Associate / 1 / 2 / Lead / 3 &middot; FullStack &amp; CS Core as pilot. Companion sheets: KPI tracker '
         '(kra_training_sheet.xlsx) &middot; HOD one-pager. Other domain teams get cards when their team views land.</div>')

html = ('<title>AI Engineer Ladder</title>\n<style>\n' + STYLE + '\n</style>\n'
        '<div class="container">\n' + "\n".join(B) + '\n</div>\n')
open("role_cards.html", "w", encoding="utf-8").write(html)

print("xlsx tabs:", wb.sheetnames)
print("levels:", len(LEVELS), "| areas:", len(AREAS), "| wiring:", len(WIRING),
      "| pillars:", [(p[0], p[1], len(p[2])) for p in PILLARS])
print("html chars:", len(html), "| kpi chips:", html.count('class="kpi"'))
