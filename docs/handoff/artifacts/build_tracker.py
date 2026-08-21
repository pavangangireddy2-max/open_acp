#!/usr/bin/env python3
"""KPI Tracker FY26-27 builder.

- Extends kra_data.json with the TRACKER section (single data source).
- Adds/replaces the "KPI Tracker FY26-27" sheet in kra_training_sheet.xlsx IN PLACE
  (other three sheets untouched, so the Dependent-metrics rename and any HOD edits survive).
- Splices the same table into kra_training_sheet.html between TRACKER:START/END markers.
Idempotent: safe to re-run after data edits.
"""
import json, math
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

SP = Path(__file__).parent
XLSX, HTML, DATA = SP / "kra_training_sheet.xlsx", SP / "kra_training_sheet.html", SP / "kra_data.json"

def F(size=10, **kw): return Font(name="Arial", size=size, **kw)

HUES  = ["2A78D6", "EB6834", "1BAF7A", "EDA100", "E87BA4"]
BANDS = ["DFEBF9", "FCE8E1", "DDF3EB", "FCF1D9", "FCEBF1"]
TINTS = ["F2F7FD", "FEF6F3", "F1FAF7", "FEF9F0", "FEF7FA"]

# ---------------------------------------------------------------- tracker data
TRACKER = [
  # ---- KRA 1
  {"kra": 0, "category": "Delivery", "product": "NIAT", "metric": "Program Delivery Gap", "marker": "CASCADE",
   "desc": "% deviation of the executed schedule vs the designed schedule, across the journey steps (lectures, quizzes, practice releases, assets)",
   "unit": "%", "freq": "Monthly", "lane": "Product Learning Experience",
   "remark": "CASCADE — feeds KRA 1 + KRA 3, tracked once (no double count). Lower is better — variance reads inverted.",
   "rows": [{"cohort": "All", "kpi": "Delivery:NIAT::Program Delivery Gap", "budget": 0}]},
  {"kra": 0, "category": "Business Impact", "product": "NIAT", "metric": "Module-Quiz Score Bands", "marker": "",
   "desc": "Share of the batch in each module-quiz band (10-pt scale) — one band stricter than the org bands",
   "unit": "%", "freq": "Monthly", "lane": "Learning Domains",
   "remark": "Four band rows per batch sum to 100; the <5.0 rows target 0 (lower is better). B4 rows go live with the batch's first module quiz.",
   "rows": [
     {"cohort": "B3", "kpi": "Business Impact:NIAT:B3::% in Module-Quiz Band ≥8.0",    "budget": 30},
     {"cohort": "B3", "kpi": "Business Impact:NIAT:B3::% in Module-Quiz Band 7.0–8.0", "budget": 40},
     {"cohort": "B3", "kpi": "Business Impact:NIAT:B3::% in Module-Quiz Band 5.0–7.0", "budget": 30},
     {"cohort": "B3", "kpi": "Business Impact:NIAT:B3::% in Module-Quiz Band <5.0",    "budget": 0},
     {"cohort": "B4", "kpi": "Business Impact:NIAT:B4::% in Module-Quiz Band ≥8.0",    "budget": 30},
     {"cohort": "B4", "kpi": "Business Impact:NIAT:B4::% in Module-Quiz Band 7.0–8.0", "budget": 40},
     {"cohort": "B4", "kpi": "Business Impact:NIAT:B4::% in Module-Quiz Band 5.0–7.0", "budget": 30},
     {"cohort": "B4", "kpi": "Business Impact:NIAT:B4::% in Module-Quiz Band <5.0",    "budget": 0}]},
  {"kra": 0, "category": "Business Impact", "product": "NIAT", "metric": "Content–Assessment Alignment", "marker": "",
   "desc": "|avg module-quiz score − avg skill-assessment score| — the taught-vs-tested gap",
   "unit": "pp", "freq": "Per cycle", "lane": "Learning Domains",
   "remark": "Lower is better — variance reads inverted. Tightens to ≤5 pp after 3 clean cycles (cycle = semester).",
   "rows": [
     {"cohort": "B3", "kpi": "Business Impact:NIAT:B3::Content–Assessment Alignment", "budget": 10},
     {"cohort": "B4", "kpi": "Business Impact:NIAT:B4::Content–Assessment Alignment", "budget": 10}]},
  {"kra": 0, "category": "Business Impact", "product": "All", "metric": "Engagement-Matrix Cell Migration", "marker": "SAMPLE",
   "desc": "% of learners in the HE×HV (high-effort × high-value) cell; the full 3×3 matrix stays diagnostic",
   "unit": "%", "freq": "Per cycle · read monthly", "lane": "Learning Platform",
   "remark": "SAMPLE — from ~4% baseline; budget confirms when the LE dashboard lands. Alt pick: M×M 10 → 20.",
   "rows": [{"cohort": "All", "kpi": "Business Impact:All::% Learners in HE×HV Cell", "budget": 10}]},
  # ---- KRA 2
  {"kra": 1, "category": "Quality & Reliability", "product": "All", "metric": "Content Issue Resolution Efficiency", "marker": "",
   "desc": "% of content issues resolved within the 2-day TAT — resolved = fix live + students notified",
   "unit": "%", "freq": "Monthly", "lane": "Agentic Content Platform",
   "remark": "The % climbs over the year; the 2-day TAT itself doesn't move.",
   "rows": [{"cohort": "All", "kpi": "Quality & Reliability:All::Content Issue Resolution Efficiency", "budget": 80}]},
  {"kra": 1, "category": "Quality & Reliability", "product": "All", "metric": "Content Issue Recurrence", "marker": "",
   "desc": "% of resolved content issues that recur — root-cause close: instance fixed · artifact changed · tripwire added · broadcast sent",
   "unit": "%", "freq": "Quarterly", "lane": "Agentic Content Platform",
   "remark": "Lower is better — variance reads inverted.",
   "rows": [{"cohort": "All", "kpi": "Quality & Reliability:All::Content Issue Recurrence", "budget": 2}]},
  {"kra": 1, "category": "Business Impact", "product": "All", "metric": "Learning Environment Satisfaction", "marker": "",
   "desc": "Student rating of the learning environment — driven by the four platform rows below",
   "unit": "score /5", "freq": "Monthly", "lane": "Developer Platform",
   "remark": "",
   "rows": [{"cohort": "All", "kpi": "Business Impact:All::Learning Environment Satisfaction", "budget": 4.5}]},
  {"kra": 1, "category": "Quality & Reliability", "product": "All", "metric": "Availability & Saturation Detection", "marker": "",
   "desc": "% of critical-service saturations alerted, detection ≤10 min (IDE, compiler, workflows)",
   "unit": "%", "freq": "Monthly", "lane": "Developer Platform",
   "remark": "",
   "rows": [{"cohort": "All", "kpi": "Quality & Reliability:All::Availability & Saturation Detection", "budget": 100}]},
  {"kra": 1, "category": "Quality & Reliability", "product": "All", "metric": "Tail-Latency User Impact", "marker": "",
   "desc": "% of students beyond P99 latency limits — IDE launch / submit / publish <60 s",
   "unit": "%", "freq": "Monthly", "lane": "Developer Platform",
   "remark": "Lower is better — variance reads inverted.",
   "rows": [{"cohort": "All", "kpi": "Quality & Reliability:All::Tail-Latency User Impact", "budget": 0}]},
  {"kra": 1, "category": "Quality & Reliability", "product": "All", "metric": "Platform Issue Resolution Efficiency", "marker": "",
   "desc": "% of platform issues resolved within the 2-day TAT (internal same-day)",
   "unit": "%", "freq": "Monthly", "lane": "Developer Platform",
   "remark": "",
   "rows": [{"cohort": "All", "kpi": "Quality & Reliability:All::Platform Issue Resolution Efficiency", "budget": 80}]},
  {"kra": 1, "category": "Quality & Reliability", "product": "All", "metric": "Platform Issue Recurrence", "marker": "",
   "desc": "% of resolved platform issues that recur (quarter)",
   "unit": "%", "freq": "Quarterly", "lane": "Developer Platform",
   "remark": "Lower is better — variance reads inverted.",
   "rows": [{"cohort": "All", "kpi": "Quality & Reliability:All::Platform Issue Recurrence", "budget": 2}]},
  {"kra": 1, "category": "Business Impact", "product": "NIAT", "metric": "Journey Step Health", "marker": "",
   "desc": "% of the 11 journey steps green — NIAT first, then per product",
   "unit": "%", "freq": "Monthly", "lane": "Product Learning Experience",
   "remark": "Q1 baseline sets the budget — blank until then (org-tracker precedent).",
   "rows": [{"cohort": "All", "kpi": "Business Impact:NIAT::Journey Step Health", "budget": None}]},
  {"kra": 1, "category": "Quality & Reliability", "product": "NIAT", "metric": "Product Issue Resolution Efficiency", "marker": "CROSS-DEPT",
   "desc": "% of student-reported product issues resolved within TAT — resolved across departments, we route; fix live + students notified",
   "unit": "%", "freq": "Monthly", "lane": "Product Learning Experience",
   "remark": "Q1 baseline sets the TAT target — blank until then.",
   "rows": [{"cohort": "All", "kpi": "Quality & Reliability:NIAT::Product Issue Resolution Efficiency", "budget": None}]},
  {"kra": 1, "category": "Quality & Reliability", "product": "NIAT", "metric": "Product Issue Recurrence", "marker": "CROSS-DEPT",
   "desc": "% of resolved product issues that recur at student-journey level (quarter)",
   "unit": "%", "freq": "Quarterly", "lane": "Product Learning Experience",
   "remark": "Lower is better — variance reads inverted.",
   "rows": [{"cohort": "All", "kpi": "Quality & Reliability:NIAT::Product Issue Recurrence", "budget": 2}]},
  # ---- KRA 3
  {"kra": 2, "category": "Business Impact", "product": "NIAT", "metric": "BOS Credit Acceptance", "marker": "",
   "desc": "% of proposed credits accepted first-pass by the university BOS",
   "unit": "%", "freq": "Per cycle", "lane": "Product Learning Experience",
   "remark": "Cohort rows split where targets differ: B3 85 · B4 90.",
   "rows": [
     {"cohort": "B3", "kpi": "Business Impact:NIAT:B3::BOS Credit Acceptance", "budget": 85},
     {"cohort": "B4", "kpi": "Business Impact:NIAT:B4::BOS Credit Acceptance", "budget": 90}]},
  {"kra": 2, "category": "Quality & Reliability", "product": "NIAT", "metric": "University Communication TAT", "marker": "",
   "desc": "% of university requests answered within TAT — ack ≤1 business day, standard 3-day TAT",
   "unit": "%", "freq": "Monthly", "lane": "Product Learning Experience",
   "remark": "University-request log builds in month 1.",
   "rows": [{"cohort": "—", "kpi": "Quality & Reliability:NIAT::University Communication TAT", "budget": 90}]},
  {"kra": 2, "category": "Quality & Reliability", "product": "NIAT", "metric": "University Curriculum & Framework Compliance", "marker": "",
   "desc": "% of submission cycles fully compliant — approved BOS syllabus + NHQRF / Woolf / AICTE / UGC",
   "unit": "%", "freq": "Per cycle", "lane": "Product Learning Experience",
   "remark": "",
   "rows": [{"cohort": "All", "kpi": "Quality & Reliability:NIAT::University Curriculum & Framework Compliance", "budget": 100}]},
  # ---- KRA 4
  {"kra": 3, "category": "Quality & Reliability", "product": "NIAT", "metric": "Industry Update Adherence", "marker": "",
   "desc": "% of GRIT-tested skills covered in live course content — Learning–GRIT delta → 0",
   "unit": "%", "freq": "Quarterly", "lane": "Learning Domains",
   "remark": "",
   "rows": [{"cohort": "All", "kpi": "Quality & Reliability:NIAT::Industry Update Adherence", "budget": 100}]},
  {"kra": 3, "note": "GRIT-feature KPIs — org-owned, pending definition with the GRIT owner (Sundar); rows enter the tracker when defined."},
  # ---- KRA 5
  {"kra": 4, "note": "Employability mapping deliberately not forced — skill mastery is the long lever; rows enter the tracker when the mapping is agreed."},
]

# ---------------------------------------------------------------- persist data
data = json.loads(DATA.read_text())
data["TRACKER"] = TRACKER
DATA.write_text(json.dumps(data, ensure_ascii=False))
KRAS = data["KRAS"]

# ---------------------------------------------------------------- xlsx
COLS = ["S. No.", "KRA", "Metric category", "Product", "Cohort", "Metric name",
        "KPI name (naming convention)", "Description", "Unit", "Frequency",
        "Lane (KPI owner)", "Budgeted", "Actual", "Variance", "Remarks"]
WIDTHS = [6, 26, 17, 8, 8, 26, 40, 46, 9, 15, 22, 10, 9, 10, 40]
CENTER_COLS = {1, 4, 5, 9, 12, 13, 14}  # S.No, Product, Cohort, Unit, B, A, V

wb = load_workbook(XLSX)
if "KPI Tracker FY26-27" in wb.sheetnames:
    del wb["KPI Tracker FY26-27"]
ws = wb.create_sheet("KPI Tracker FY26-27")

thin = Side(style="thin", color="FFCCCCCC")
med  = Side(style="medium", color="FF555555")
BLACK = PatternFill("solid", fgColor="FF000000")

for i, w in enumerate(WIDTHS):
    ws.column_dimensions[chr(65 + i)].width = w

# headers: two rows, A..K merged vertically, FY banner over L..O
for i, name in enumerate(COLS[:11]):
    c = chr(65 + i)
    ws.merge_cells(f"{c}1:{c}2")
    ws[f"{c}1"] = name
ws.merge_cells("L1:O1")
ws["L1"] = "FY 2026-27 — annual"
for c, name in zip("LMNO", COLS[11:]):
    ws[f"{c}2"] = name
for r in (1, 2):
    for i in range(15):
        cell = ws.cell(row=r, column=i + 1)
        cell.fill = BLACK
        cell.font = F(10, bold=True, color="FFFFFFFF")
        cell.alignment = Alignment(horizontal="center" if r == 1 and i >= 11 else "left",
                                   vertical="center", wrap_text=True)
ws["L1"].alignment = Alignment(horizontal="center", vertical="center")
ws.row_dimensions[1].height = 24
ws.row_dimensions[2].height = 18
ws.freeze_panes = "G3"

def put(r, c, v, *, bold=False, italic=False, color="FF1A1A1A", center=False, num=False):
    cell = ws.cell(row=r, column=c)
    cell.value = v
    cell.font = F(10, bold=bold, italic=italic, color=color)
    cell.alignment = Alignment(horizontal="center" if center else "left", vertical="top", wrap_text=True)
    return cell

row = 3
sno = 0
kra_ranges = []   # (kra_idx, first_row, last_row)
for k in range(5):
    blocks = [b for b in TRACKER if b["kra"] == k]
    kra_first = row
    tint = PatternFill("solid", fgColor="FF" + TINTS[k])
    for b in blocks:
        if "note" in b:
            ws.merge_cells(start_row=row, start_column=3, end_row=row, end_column=15)
            put(row, 3, b["note"], italic=True, color="FF777777")
            for cc in range(1, 16):
                ws.cell(row=row, column=cc).fill = tint
            ws.row_dimensions[row].height = 30
            row += 1
            continue
        n = len(b["rows"])
        r0 = row
        # shared columns (merge when the block has several KPI rows)
        shared = {3: b["category"], 4: b["product"], 6: b["metric"] + (f"  [{b['marker']}]" if b["marker"] else ""),
                  8: b["desc"], 9: b["unit"], 10: b["freq"], 11: b["lane"], 15: b["remark"]}
        for cc, v in shared.items():
            if n > 1:
                ws.merge_cells(start_row=r0, start_column=cc, end_row=r0 + n - 1, end_column=cc)
            put(r0, cc, v, bold=(cc == 6), center=(cc in (4, 9)))
        # cohort runs
        i = 0
        while i < n:
            j = i
            while j + 1 < n and b["rows"][j + 1]["cohort"] == b["rows"][i]["cohort"]:
                j += 1
            if j > i:
                ws.merge_cells(start_row=r0 + i, start_column=5, end_row=r0 + j, end_column=5)
            put(r0 + i, 5, b["rows"][i]["cohort"], center=True)
            i = j + 1
        # per-KPI rows
        for i, rr in enumerate(b["rows"]):
            r = r0 + i
            sno += 1
            put(r, 1, sno, center=True)
            put(r, 7, rr["kpi"])
            if rr["budget"] is not None:
                put(r, 12, rr["budget"], center=True, bold=True)
            ws.cell(row=r, column=14).value = f'=IF(AND(ISNUMBER(L{r}),ISNUMBER(M{r})),L{r}-M{r},"")'
            ws.cell(row=r, column=14).font = F(10)
            ws.cell(row=r, column=14).alignment = Alignment(horizontal="center", vertical="top")
            for cc in range(1, 16):
                ws.cell(row=r, column=cc).fill = tint
        # block height heuristic
        lines = max(math.ceil(len(b["desc"]) / 50), math.ceil(len(b["remark"]) / 43) if b["remark"] else 1,
                    math.ceil(len(b["metric"]) / 24), 2)
        per = max(24, (lines * 13 + 6) / n)
        for i in range(n):
            ws.row_dimensions[r0 + i].height = per
        row = r0 + n
    kra_ranges.append((k, kra_first, row - 1))

last = row - 1
# KRA band cells
for k, r1, r2 in kra_ranges:
    ws.merge_cells(start_row=r1, start_column=2, end_row=r2, end_column=2)
    cell = put(r1, 2, f"{KRAS[k][0]}\n{KRAS[k][1]}", bold=True)
    band = PatternFill("solid", fgColor="FF" + BANDS[k])
    for r in range(r1, r2 + 1):
        ws.cell(row=r, column=2).fill = band

# borders: thin grid, medium top on each KRA first row, thick hue accent on KRA cells
for r in range(1, last + 1):
    for c in range(1, 16):
        ws.cell(row=r, column=c).border = Border(left=thin, right=thin, top=thin, bottom=thin)
for k, r1, r2 in kra_ranges:
    for c in range(1, 16):
        cell = ws.cell(row=r1, column=c)
        cell.border = Border(left=thin, right=thin, top=med, bottom=thin)
    accent = Side(style="thick", color="FF" + HUES[k])
    for r in range(r1, r2 + 1):
        b = ws.cell(row=r, column=2).border
        ws.cell(row=r, column=2).border = Border(left=accent, right=thin, top=b.top, bottom=thin)

# legend additions (once)
lg = wb["Legend & Notes"]
labels = {lg.cell(row=r, column=1).value for r in range(1, lg.max_row + 1)}
if "KPI Tracker FY26-27 (tab 4)" not in labels:
    add = [
        ("KPI Tracker FY26-27 (tab 4)",
         "Annual tracker in the org Head-Abstract format — one Budgeted / Actual / Variance / Remarks set for FY 2026-27, "
         "Actual updated at each KPI's frequency. Variance = Budgeted − Actual (org convention): negative = beat on "
         "higher-is-better rows; rows flagged 'lower is better' read inverted."),
        ("Tracker conventions",
         "KPI name follows Category:Product:Cohort::Name; per-batch rows split into B3 / B4. Budgets are numeric — the "
         "≤ / ≥ direction lives in Description and Remarks. Blank Budgeted = first-quarter baseline sets it. The tracker's "
         "Budgeted is the number of record; the map's KPI target mirrors it, never the reverse."),
    ]
    r = lg.max_row + 2
    for lab, txt in add:
        lg.cell(row=r, column=1, value=lab).font = F(10, bold=True)
        lg.cell(row=r, column=1).alignment = Alignment(vertical="top", wrap_text=True)
        lg.cell(row=r, column=2, value=txt).font = F(10)
        lg.cell(row=r, column=2).alignment = Alignment(vertical="top", wrap_text=True)
        lg.row_dimensions[r].height = 55
        r += 1

wb.save(XLSX)

# ---------------------------------------------------------------- html
TAG = {"CASCADE": "tag-cascade", "SAMPLE": "tag-sample", "CROSS-DEPT": "tag-xdept", "ORG": "tag-org"}
def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

out = []
out.append('<!-- TRACKER:START -->')
out.append('  <h2>3. KPI Tracker — FY 2026-27 (annual)</h2>')
out.append('  <div class="sectionlead">The post-training scoreboard — &sect;1 decomposed to one trackable number per row, '
           'in the org Head-Abstract tracker format (tab 4 of the workbook). One annual Budgeted / Actual / Variance set; '
           '<strong>Variance = Budgeted &minus; Actual</strong> (org convention), so negative = beat on higher-is-better rows, '
           'and rows flagged <em>lower is better</em> read inverted. Budgets are numeric — the &le;/&ge; direction lives in the '
           'description and remarks; blank Budgeted = first-quarter baseline sets it. The tracker&rsquo;s Budgeted is the number '
           'of record — &sect;1 targets mirror it.</div>')
out.append('  <div class="scroll">')
out.append('  <table style="min-width:1680px">')
out.append('    <tr>'
           '<th class="c" rowspan="2" style="width:3%">S. No.</th>'
           '<th rowspan="2" style="width:11%">KRA</th>'
           '<th rowspan="2" style="width:6%">Metric category</th>'
           '<th class="c" rowspan="2" style="width:4%">Product</th>'
           '<th class="c" rowspan="2" style="width:4%">Cohort</th>'
           '<th rowspan="2" style="width:10%">Metric name</th>'
           '<th rowspan="2" style="width:14%">KPI name (naming convention)</th>'
           '<th rowspan="2" style="width:16%">Description</th>'
           '<th class="c" rowspan="2" style="width:4%">Unit</th>'
           '<th rowspan="2" style="width:5%">Frequency</th>'
           '<th rowspan="2" style="width:7%">Lane (KPI owner)</th>'
           '<th class="c" colspan="4">FY 2026-27 — annual</th></tr>')
out.append('    <tr><th class="c" style="width:4%">Budgeted</th><th class="c" style="width:3%">Actual</th>'
           '<th class="c" style="width:4%">Variance</th><th style="width:12%">Remarks</th></tr>')
out.append('    <tbody>')

sno = 0
for k in range(5):
    blocks = [b for b in TRACKER if b["kra"] == k]
    total = sum(len(b["rows"]) if "rows" in b else 1 for b in blocks)
    tint, band, hue = TINTS[k], BANDS[k], HUES[k]
    kra_td = (f'<td class="kra" rowspan="{total}" style="background:#{band};border-left:4px solid #{hue}">'
              f'{esc(KRAS[k][0])}<span class="num">{esc(KRAS[k][1])}</span></td>')
    first_of_kra = True
    for b in blocks:
        if "note" in b:
            tr = f'<tr style="background:#{tint}{";border-top:2px solid #555" if first_of_kra else ""}"><td class="c"></td>'
            if first_of_kra:
                tr += kra_td
            tr += f'<td colspan="13" style="font-style:italic;color:#777">{esc(b["note"])}</td></tr>'
            out.append('    ' + tr)
            first_of_kra = False
            continue
        n = len(b["rows"])
        metric_html = f'<strong>{esc(b["metric"])}</strong>'
        if b["marker"]:
            metric_html += f' <span class="tag {TAG[b["marker"]]}">{esc(b["marker"])}</span>'
        shared = [
            (3,  f'<td rowspan="{n}">{esc(b["category"])}</td>'),
            (4,  f'<td class="c" rowspan="{n}">{esc(b["product"])}</td>'),
            (6,  f'<td rowspan="{n}">{metric_html}</td>'),
            (8,  f'<td rowspan="{n}"><span class="lead">{esc(b["desc"])}</span></td>'),
            (9,  f'<td class="c" rowspan="{n}">{esc(b["unit"])}</td>'),
            (10, f'<td rowspan="{n}">{esc(b["freq"])}</td>'),
            (11, f'<td rowspan="{n}"><span class="team">{esc(b["lane"])}</span></td>'),
            (15, f'<td rowspan="{n}"><span class="lead">{esc(b["remark"]) if b["remark"] else "&mdash;"}</span></td>'),
        ]
        # cohort runs
        runs = []
        i = 0
        while i < n:
            j = i
            while j + 1 < n and b["rows"][j + 1]["cohort"] == b["rows"][i]["cohort"]:
                j += 1
            runs.append((i, j - i + 1, b["rows"][i]["cohort"]))
            i = j + 1
        run_starts = {st: (ln, ch) for st, ln, ch in runs}
        sh = dict(shared)
        for i, rr in enumerate(b["rows"]):
            sno += 1
            style = f'background:#{tint}' + (';border-top:2px solid #555' if first_of_kra and i == 0 else '')
            budget = rr["budget"]
            btxt = '&mdash;' if budget is None else (f'{budget:g}')
            kpi_td = f'<td style="font-family:ui-monospace,\'SF Mono\',Menlo,monospace;font-size:.88em">{esc(rr["kpi"])}</td>'
            bav = (f'<td class="c num">{btxt}</td>'
                   '<td class="c"></td>'
                   '<td class="c" style="color:#999">&mdash;</td>')
            cells = [f'<td class="c num">{sno}</td>']
            if first_of_kra and i == 0:
                cells.append(kra_td)
            if i == 0:
                cells += [sh[3], sh[4]]
            if i in run_starts:
                ln, ch = run_starts[i]
                cells.append(f'<td class="c" rowspan="{ln}"><strong>{esc(ch)}</strong></td>')
            if i == 0:
                # column order: Metric(6) · KPI(7) · Desc(8) · Unit(9) · Freq(10) · Lane(11) · B/A/V · Remarks(15)
                cells += [sh[6], kpi_td, sh[8], sh[9], sh[10], sh[11], bav, sh[15]]
            else:
                cells += [kpi_td, bav]
            out.append(f'    <tr style="{style}">' + ''.join(cells) + '</tr>')
        first_of_kra = False
out.append('    </tbody>')
out.append('  </table>')
out.append('  </div>')
out.append('<!-- TRACKER:END -->')
fragment = "\n".join(out)

html = HTML.read_text()
if "<!-- TRACKER:START -->" in html:
    pre = html.split("<!-- TRACKER:START -->")[0]
    post = html.split("<!-- TRACKER:END -->")[1]
    html = pre + fragment + post
else:
    html = html.replace('  <div class="footnote">', fragment + '\n\n  <div class="footnote">')
html = html.replace(
    "(same three views: map &middot; session index &middot; legend, same color coding)",
    "(same four tabs: map &middot; session index &middot; legend &middot; KPI Tracker FY26-27, same color coding; "
    "the tracker follows the org Head-Abstract format — variance = Budgeted &minus; Actual)")
HTML.write_text(html)

# ---------------------------------------------------------------- verify
wb2 = load_workbook(XLSX)
t = wb2["KPI Tracker FY26-27"]
snos = [t.cell(row=r, column=1).value for r in range(3, t.max_row + 1) if isinstance(t.cell(row=r, column=1).value, int)]
formulas = sum(1 for r in range(3, t.max_row + 1)
               if str(t.cell(row=r, column=14).value or "").startswith("=IF"))
budgets = [t.cell(row=r, column=12).value for r in range(3, t.max_row + 1)]
print("sheets:", wb2.sheetnames)
print("numbered rows:", len(snos), "| max sno:", max(snos), "| variance formulas:", formulas)
print("blank budgets (baseline rows):", sum(1 for r in range(3, t.max_row + 1)
      if isinstance(t.cell(row=r, column=1).value, int) and t.cell(row=r, column=12).value is None))
print("last row:", t.max_row, "| html rows:", html.count('<td class="c num">'), "| tracker section in html:", "TRACKER:START" in html)
print("legend rows:", wb2["Legend & Notes"].max_row)
