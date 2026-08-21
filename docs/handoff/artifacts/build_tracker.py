#!/usr/bin/env python3
"""Merged KRA-KPI sheet builder — the tracker IS the training sheet.

- One xlsx sheet "KPI Tracker FY26-27" (tab 1): org Head-Abstract tracker columns
  + three training columns (Dependent metrics · Funnel · Functions) in a collapsed
  column group. Session Index (tab 2) recounts off it; Legend (tab 3) patched.
- One HTML table on the artifact page, training columns behind a toggle.
- Functions vocabulary from the HOD one-pager §2 key terms.
Reads/extends kra_data.json (ROWS supplies dependent metrics + funnel text).
Idempotent — safe to re-run.
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

data = json.loads(DATA.read_text())
KRAS, ROWS = data["KRAS"], data["ROWS"]
def dep(i): return ROWS[i][3]
def fun(i): return ROWS[i][5]

# Functions that move it — vocabulary from the HOD one-pager §2 key terms:
# Content, Engineering, Product Managers, Pedagogy Experts, Graphic Designers,
# Video Editors, DA/DEs, Product Designers, Packaging Teams, SDIs (+ CSI team).
FX = {
  "pdg":    "CSI team + Product Managers — counterparty: Program Ops · assets leg: Graphic Designers, Video Editors, SDIs, Packaging Teams",
  "bands":  "Content + Pedagogy Experts + DA/DEs",
  "align":  "Content + Pedagogy Experts + DA/DEs",
  "cell":   "Product Managers + Engineering + DA/DEs",
  "cissue": "Content + Engineering",
  "eng":    "Engineering",
  "jsh":    "Product Managers + DA/DEs + CSI team",
  "prod":   "Product Managers + CSI team",
  "bos":    "CSI team + Content",
  "tat":    "CSI team",
  "comp":   "CSI team + Content",
  "iua":    "Content",
}

# ---------------------------------------------------------------- tracker data
TRACKER = [
  # ---- KRA 1
  {"kra": 0, "category": "Program Delivery", "product": "NIAT", "metric": "Program Delivery Gap", "marker": "CASCADE",
   "desc": "% deviation of the executed schedule vs the designed schedule, across the journey steps (lectures, quizzes, practice releases, assets)",
   "dep": dep(0),
   "funnel": fun(0) + " · also: delivered = approved plan → university trust → Univ Relations CSAT (feeds KRA 3)",
   "functions": FX["pdg"], "unit": "%", "freq": "Monthly", "lane": "Product Learning Experience",
   "remark": "CASCADE — feeds KRA 1 + KRA 3, tracked once (no double count). Lower is better — variance reads inverted.",
   "rows": [{"cohort": "All", "kpi": "Program Delivery:NIAT::Program Delivery Gap", "budget": 0}]},
  {"kra": 0, "category": "Business Impact", "product": "NIAT", "metric": "Module-Quiz Score Bands", "marker": "",
   "desc": "Share of the batch in each module-quiz band (10-pt scale) — one band stricter than the org bands",
   "dep": dep(1), "funnel": fun(1), "functions": FX["bands"],
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
   "dep": dep(2), "funnel": fun(2), "functions": FX["align"],
   "unit": "pp", "freq": "Per cycle", "lane": "Learning Domains",
   "remark": "Lower is better — variance reads inverted. Tightens to ≤5 pp after 3 clean cycles (cycle = semester).",
   "rows": [
     {"cohort": "B3", "kpi": "Business Impact:NIAT:B3::Content–Assessment Alignment", "budget": 10},
     {"cohort": "B4", "kpi": "Business Impact:NIAT:B4::Content–Assessment Alignment", "budget": 10}]},
  {"kra": 0, "category": "Business Impact", "product": "All", "metric": "Engagement-Matrix Cell Migration", "marker": "SAMPLE",
   "desc": "% of learners in the HE×HV (high-effort × high-value) cell; the full 3×3 matrix stays diagnostic",
   "dep": dep(3), "funnel": fun(3), "functions": FX["cell"],
   "unit": "%", "freq": "Per cycle · read monthly", "lane": "Learning Platform",
   "remark": "SAMPLE — from ~4% baseline; budget confirms when the LE dashboard lands. Alt pick: M×M 10 → 20.",
   "rows": [{"cohort": "All", "kpi": "Business Impact:All::% Learners in HE×HV Cell", "budget": 10}]},
  {"kra": 0, "note": "Summative & Formative Achievement — ORG scoreboard, tracked not owned: same 30/40/30 on assessment scores, per batch. Steps 1–3 held → assessments run → the 75% lands → SPI Bands."},
  # ---- KRA 2
  {"kra": 1, "category": "Content Efficiency", "product": "All", "metric": "Content Issue Resolution Efficiency", "marker": "",
   "desc": "% of content issues resolved within the 2-day TAT — resolved = fix live + students notified",
   "dep": dep(5), "funnel": fun(5), "functions": FX["cissue"],
   "unit": "%", "freq": "Monthly", "lane": "Agentic Content Platform",
   "remark": "The % climbs over the year; the 2-day TAT itself doesn't move.",
   "rows": [{"cohort": "All", "kpi": "Content Efficiency:All::Content Issue Resolution Efficiency", "budget": 80}]},
  {"kra": 1, "category": "Content Efficiency", "product": "All", "metric": "Content Issue Recurrence", "marker": "",
   "desc": "% of resolved content issues that recur — root-cause close: instance fixed · artifact changed · tripwire added · broadcast sent",
   "dep": dep(6), "funnel": fun(6), "functions": FX["cissue"],
   "unit": "%", "freq": "Quarterly", "lane": "Agentic Content Platform",
   "remark": "Lower is better — variance reads inverted.",
   "rows": [{"cohort": "All", "kpi": "Content Efficiency:All::Content Issue Recurrence", "budget": 2}]},
  {"kra": 1, "category": "Content Effectiveness", "product": "All", "metric": "Learning Environment Satisfaction", "marker": "",
   "desc": "Student rating of the learning environment — driven by the four platform rows below",
   "dep": dep(7), "funnel": fun(7), "functions": FX["eng"],
   "unit": "score /5", "freq": "Monthly", "lane": "Developer Platform",
   "remark": "",
   "rows": [{"cohort": "All", "kpi": "Content Effectiveness:All::Learning Environment Satisfaction", "budget": 4.5}]},
  {"kra": 1, "category": "Platform Reliability", "product": "All", "metric": "Availability & Saturation Detection", "marker": "",
   "desc": "% of critical-service saturations alerted, detection ≤10 min (IDE, compiler, workflows)",
   "dep": dep(8), "funnel": fun(8), "functions": FX["eng"],
   "unit": "%", "freq": "Monthly", "lane": "Developer Platform",
   "remark": "",
   "rows": [{"cohort": "All", "kpi": "Platform Reliability:All::Availability & Saturation Detection", "budget": 100}]},
  {"kra": 1, "category": "Platform Reliability", "product": "All", "metric": "Tail-Latency User Impact", "marker": "",
   "desc": "% of students beyond P99 latency limits — IDE launch / submit / publish <60 s",
   "dep": dep(9), "funnel": fun(9), "functions": FX["eng"],
   "unit": "%", "freq": "Monthly", "lane": "Developer Platform",
   "remark": "Lower is better — variance reads inverted.",
   "rows": [{"cohort": "All", "kpi": "Platform Reliability:All::Tail-Latency User Impact", "budget": 0}]},
  {"kra": 1, "category": "Platform Reliability", "product": "All", "metric": "Platform Issue Resolution Efficiency", "marker": "",
   "desc": "% of platform issues resolved within the 2-day TAT (internal same-day)",
   "dep": dep(10), "funnel": fun(10), "functions": FX["eng"],
   "unit": "%", "freq": "Monthly", "lane": "Developer Platform",
   "remark": "",
   "rows": [{"cohort": "All", "kpi": "Platform Reliability:All::Platform Issue Resolution Efficiency", "budget": 80}]},
  {"kra": 1, "category": "Platform Reliability", "product": "All", "metric": "Platform Issue Recurrence", "marker": "",
   "desc": "% of resolved platform issues that recur (quarter)",
   "dep": dep(11), "funnel": fun(11), "functions": FX["eng"],
   "unit": "%", "freq": "Quarterly", "lane": "Developer Platform",
   "remark": "Lower is better — variance reads inverted.",
   "rows": [{"cohort": "All", "kpi": "Platform Reliability:All::Platform Issue Recurrence", "budget": 2}]},
  {"kra": 1, "category": "Program Delivery", "product": "NIAT", "metric": "Journey Step Health", "marker": "",
   "desc": "% of the 11 journey steps green — NIAT first, then per product",
   "dep": dep(12), "funnel": fun(12), "functions": FX["jsh"],
   "unit": "%", "freq": "Monthly", "lane": "Product Learning Experience",
   "remark": "Q1 baseline sets the budget — blank until then (org-tracker precedent).",
   "rows": [{"cohort": "All", "kpi": "Program Delivery:NIAT::Journey Step Health", "budget": None}]},
  {"kra": 1, "category": "Content Efficiency", "product": "NIAT", "metric": "Product Issue Resolution Efficiency", "marker": "CROSS-DEPT",
   "desc": "% of student-reported product issues resolved within TAT — resolved across departments, we route; fix live + students notified",
   "dep": dep(13), "funnel": fun(13), "functions": FX["prod"],
   "unit": "%", "freq": "Monthly", "lane": "Product Learning Experience",
   "remark": "Q1 baseline sets the TAT target — blank until then.",
   "rows": [{"cohort": "All", "kpi": "Content Efficiency:NIAT::Product Issue Resolution Efficiency", "budget": None}]},
  {"kra": 1, "category": "Content Efficiency", "product": "NIAT", "metric": "Product Issue Recurrence", "marker": "CROSS-DEPT",
   "desc": "% of resolved product issues that recur at student-journey level (quarter)",
   "dep": dep(14), "funnel": fun(14), "functions": FX["prod"],
   "unit": "%", "freq": "Quarterly", "lane": "Product Learning Experience",
   "remark": "Lower is better — variance reads inverted.",
   "rows": [{"cohort": "All", "kpi": "Content Efficiency:NIAT::Product Issue Recurrence", "budget": 2}]},
  # ---- KRA 3
  {"kra": 2, "category": "University Alignment", "product": "NIAT", "metric": "BOS Credit Acceptance", "marker": "",
   "desc": "% of proposed credits accepted first-pass by the university BOS",
   "dep": dep(15), "funnel": fun(15), "functions": FX["bos"],
   "unit": "%", "freq": "Per cycle", "lane": "Product Learning Experience",
   "remark": "Cohort rows split where targets differ: B3 85 · B4 90.",
   "rows": [
     {"cohort": "B3", "kpi": "University Alignment:NIAT:B3::BOS Credit Acceptance", "budget": 85},
     {"cohort": "B4", "kpi": "University Alignment:NIAT:B4::BOS Credit Acceptance", "budget": 90}]},
  {"kra": 2, "note": "Program Delivery Gap feeds this KRA too — tracked once as row 1 (CASCADE): delivered = approved plan → university trust → Univ Relations CSAT."},
  {"kra": 2, "category": "University Alignment", "product": "NIAT", "metric": "University Communication TAT", "marker": "",
   "desc": "% of university requests answered within TAT — ack ≤1 business day, standard 3-day TAT",
   "dep": dep(17), "funnel": fun(17), "functions": FX["tat"],
   "unit": "%", "freq": "Monthly", "lane": "Product Learning Experience",
   "remark": "University-request log builds in month 1.",
   "rows": [{"cohort": "—", "kpi": "University Alignment:NIAT::University Communication TAT", "budget": 90}]},
  {"kra": 2, "category": "Content Relevance", "product": "NIAT", "metric": "University Curriculum & Framework Compliance", "marker": "",
   "desc": "% of submission cycles fully compliant — approved BOS syllabus + NHQRF / Woolf / AICTE / UGC",
   "dep": dep(18), "funnel": fun(18), "functions": FX["comp"],
   "unit": "%", "freq": "Per cycle", "lane": "Product Learning Experience",
   "remark": "",
   "rows": [{"cohort": "All", "kpi": "Content Relevance:NIAT::University Curriculum & Framework Compliance", "budget": 100}]},
  # ---- KRA 4
  {"kra": 3, "category": "Content Relevance", "product": "NIAT", "metric": "Industry Update Adherence", "marker": "",
   "desc": "% of GRIT-tested skills covered in live course content — Learning–GRIT delta → 0",
   "dep": dep(19), "funnel": fun(19), "functions": FX["iua"],
   "unit": "%", "freq": "Quarterly", "lane": "Learning Domains",
   "remark": "",
   "rows": [{"cohort": "All", "kpi": "Content Relevance:NIAT::Industry Update Adherence", "budget": 100}]},
  {"kra": 3, "note": "GRIT-feature KPIs — org-owned, pending definition with the GRIT owner (Sundar); rows enter the tracker when defined."},
  # ---- KRA 5
  {"kra": 4, "note": "Employability mapping deliberately not forced — skill mastery is the long lever; rows enter the tracker when the mapping is agreed."},
]

# Session-index rooms: (display name, COUNTIF pattern, rows text)
FUNCTIONS = [
  ["Content", "Content",
   "Module-Quiz Score Bands · Content–Assessment Alignment · Content Issue pair (fixes) · BOS curriculum artifacts · Compliance · Industry Update Adherence"],
  ["Engineering", "Engineering",
   "LES + its four drivers (DP lane) · Content Issue pair tooling/routing (ACP lane) · Cell Migration build (LP lane)"],
  ["Product Managers", "Product Managers",
   "Program Delivery Gap (feeds KRA 1 + 3) · Engagement-Matrix Cell Migration · Journey Step Health · Product Issue pair"],
  ["Pedagogy Experts", "Pedagogy Experts",
   "Module-Quiz Score Bands · Content–Assessment Alignment"],
  ["DA/DEs", "DA/DE",
   "score analysis (bands, alignment) · LE dashboard (cell migration) · Journey Step Health instrumentation"],
  ["CSI team", "CSI team",
   "Program Delivery Gap (feeds KRA 1 + 3) · Journey Step Health · Product Issue pair · BOS · University Communication TAT · Compliance"],
  ["Asset production — Graphic Designers · Video Editors · SDIs · Packaging Teams", "Graphic Designers",
   "Program Delivery Gap assets leg — learning assets (PPT + recorded video) ready & loaded ≥1 month ahead"],
]

data["TRACKER"], data["FUNCTIONS"] = TRACKER, FUNCTIONS
DATA.write_text(json.dumps(data, ensure_ascii=False))

# ---------------------------------------------------------------- xlsx
COLS = ["S. No.", "KRA", "Metric category", "Product", "Cohort", "Metric name",
        "KPI name (naming convention)", "Description", "Dependent metrics",
        "Funnel → org KPI", "Functions that move it", "Lane (KPI owner)",
        "Unit", "Frequency", "Budgeted", "Actual", "Variance", "Remarks"]
WIDTHS = [6, 26, 16, 8, 8, 24, 36, 40, 44, 40, 26, 20, 8, 13, 10, 9, 10, 36]
NCOL = 18
C_DEP, C_FUNNEL, C_FX = 9, 10, 11          # the collapsible training cluster I:K
C_BUD, C_ACT, C_VAR, C_REM = 15, 16, 17, 18

wb = load_workbook(XLSX)
for name in ("KRA-KPI Map", "KPI Tracker FY26-27", "Session Index"):
    if name in wb.sheetnames:
        del wb[name]
ws = wb.create_sheet("KPI Tracker FY26-27", 0)

thin = Side(style="thin", color="FFCCCCCC")
med  = Side(style="medium", color="FF555555")
BLACK = PatternFill("solid", fgColor="FF000000")

for i, w in enumerate(WIDTHS):
    ws.column_dimensions[chr(65 + i)].width = w

for i, name in enumerate(COLS[:14]):
    c = chr(65 + i)
    ws.merge_cells(f"{c}1:{c}2")
    ws[f"{c}1"] = name
ws.merge_cells("O1:R1")
ws["O1"] = "FY 2026-27 — annual"
for c, name in zip("OPQR", COLS[14:]):
    ws[f"{c}2"] = name
for r in (1, 2):
    for i in range(NCOL):
        cell = ws.cell(row=r, column=i + 1)
        cell.fill = BLACK
        cell.font = F(10, bold=True, color="FFFFFFFF")
        cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
ws["O1"].alignment = Alignment(horizontal="center", vertical="center")
ws.row_dimensions[1].height = 24
ws.row_dimensions[2].height = 18
ws.freeze_panes = "G3"

def put(r, c, v, *, bold=False, italic=False, color="FF1A1A1A", center=False):
    cell = ws.cell(row=r, column=c)
    cell.value = v
    cell.font = F(10, bold=bold, italic=italic, color=color)
    cell.alignment = Alignment(horizontal="center" if center else "left", vertical="top", wrap_text=True)
    return cell

row, sno = 3, 0
kra_ranges = []
for k in range(5):
    blocks = [b for b in TRACKER if b["kra"] == k]
    kra_first = row
    tint = PatternFill("solid", fgColor="FF" + TINTS[k])
    for b in blocks:
        if "note" in b:
            ws.merge_cells(start_row=row, start_column=3, end_row=row, end_column=NCOL)
            put(row, 3, b["note"], italic=True, color="FF777777")
            for cc in range(1, NCOL + 1):
                ws.cell(row=row, column=cc).fill = tint
            ws.row_dimensions[row].height = 30
            row += 1
            continue
        n = len(b["rows"])
        r0 = row
        shared = {3: b["category"], 4: b["product"],
                  6: b["metric"] + (f"  [{b['marker']}]" if b["marker"] else ""),
                  8: b["desc"], C_DEP: b["dep"], C_FUNNEL: b["funnel"], C_FX: b["functions"],
                  12: b["lane"], 13: b["unit"], 14: b["freq"], C_REM: b["remark"]}
        for cc, v in shared.items():
            if n > 1:
                ws.merge_cells(start_row=r0, start_column=cc, end_row=r0 + n - 1, end_column=cc)
            put(r0, cc, v, bold=(cc == 6), center=(cc in (4, 13)))
        i = 0
        while i < n:
            j = i
            while j + 1 < n and b["rows"][j + 1]["cohort"] == b["rows"][i]["cohort"]:
                j += 1
            if j > i:
                ws.merge_cells(start_row=r0 + i, start_column=5, end_row=r0 + j, end_column=5)
            put(r0 + i, 5, b["rows"][i]["cohort"], center=True)
            i = j + 1
        for i, rr in enumerate(b["rows"]):
            r = r0 + i
            sno += 1
            put(r, 1, sno, center=True)
            put(r, 7, rr["kpi"])
            if rr["budget"] is not None:
                put(r, C_BUD, rr["budget"], center=True, bold=True)
            vc = ws.cell(row=r, column=C_VAR)
            vc.value = f'=IF(AND(ISNUMBER(O{r}),ISNUMBER(P{r})),O{r}-P{r},"")'
            vc.font = F(10)
            vc.alignment = Alignment(horizontal="center", vertical="top")
            for cc in range(1, NCOL + 1):
                ws.cell(row=r, column=cc).fill = tint
        lines = max(math.ceil(len(b["desc"]) / 48), math.ceil(len(b["dep"]) / 52),
                    math.ceil(len(b["funnel"]) / 47), math.ceil(len(b["functions"]) / 30),
                    math.ceil(len(b["remark"]) / 42) if b["remark"] else 1,
                    math.ceil(len(b["metric"]) / 22), 2)
        per = max(24, (lines * 13 + 6) / n)
        for i in range(n):
            ws.row_dimensions[r0 + i].height = per
        row = r0 + n
    kra_ranges.append((k, kra_first, row - 1))

last = row - 1
for k, r1, r2 in kra_ranges:
    ws.merge_cells(start_row=r1, start_column=2, end_row=r2, end_column=2)
    put(r1, 2, f"{KRAS[k][0]}\n{KRAS[k][1]}", bold=True)
    band = PatternFill("solid", fgColor="FF" + BANDS[k])
    for r in range(r1, r2 + 1):
        ws.cell(row=r, column=2).fill = band

for r in range(1, last + 1):
    for c in range(1, NCOL + 1):
        ws.cell(row=r, column=c).border = Border(left=thin, right=thin, top=thin, bottom=thin)
for k, r1, r2 in kra_ranges:
    for c in range(1, NCOL + 1):
        ws.cell(row=r1, column=c).border = Border(left=thin, right=thin, top=med, bottom=thin)
    accent = Side(style="thick", color="FF" + HUES[k])
    for r in range(r1, r2 + 1):
        b = ws.cell(row=r, column=2).border
        ws.cell(row=r, column=2).border = Border(left=accent, right=thin, top=b.top, bottom=thin)

# collapsible training cluster I:K — grouped + hidden (collapsed) by default
for c in "IJK":
    ws.column_dimensions[c].outline_level = 1
    ws.column_dimensions[c].hidden = True

# ---------------------------------------------------------------- session index
si = wb.create_sheet("Session Index", 1)
si.column_dimensions["A"].width = 30
si.column_dimensions["B"].width = 95
si.column_dimensions["C"].width = 12
hdr = ["Function (training room)", "Your rows in the tracker", "Row count"]
for c, name in enumerate(hdr, start=1):
    cell = si.cell(row=1, column=c, value=name)
    cell.fill = BLACK
    cell.font = F(10, bold=True, color="FFFFFFFF")
    cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
si.row_dimensions[1].height = 20
si.freeze_panes = "A2"
rng = f"'KPI Tracker FY26-27'!$K$3:$K${last}"
for i, (name, pat, rows_txt) in enumerate(FUNCTIONS):
    r = 2 + i
    si.cell(row=r, column=1, value=name).font = F(10, bold=True)
    si.cell(row=r, column=2, value=rows_txt).font = F(10)
    si.cell(row=r, column=3, value=f'=COUNTIF({rng},"*{pat}*")').font = F(10, bold=True)
    for c in range(1, 4):
        si.cell(row=r, column=c).alignment = Alignment(
            horizontal="center" if c == 3 else "left", vertical="top", wrap_text=True)
    si.row_dimensions[r].height = 30
note_r = 2 + len(FUNCTIONS)
si.merge_cells(start_row=note_r, start_column=1, end_row=note_r, end_column=3)
nc = si.cell(row=note_r, column=1,
             value="Counts are per metric — a band/cohort block counts once (the Functions cell spans its rows). "
                   "Functions vocabulary from the HOD one-pager §2 key terms; edit column K on the tracker and the counts recompute.")
nc.font = F(10, italic=True, color="FF777777")
nc.alignment = Alignment(vertical="top", wrap_text=True)
si.row_dimensions[note_r].height = 30
for r in range(1, note_r + 1):
    for c in range(1, 4):
        si.cell(row=r, column=c).border = Border(left=thin, right=thin, top=thin, bottom=thin)

# ---------------------------------------------------------------- legend patches
lg = wb["Legend & Notes"]
lg["B1"] = ("A KRA (Key Result Area) is an org outcome NIAT is judged on — it carries the target. One merged sheet: "
            "each numbered row is one trackable KPI under the KRA it moves; muted rows are context (org-owned or pending). "
            "Training columns — Dependent metrics · Funnel · Functions — sit in a collapsed column group.")
lg["B4"] = ("The teams that actively build the learning system (HOD one-pager §2 key terms): Content, Engineering, "
            "Product Managers, Pedagogy Experts, DA/DEs, Graphic Designers, Video Editors, Product Designers, "
            "Packaging Teams, SDIs — plus the CSI team on delivery- and university-facing rows. Draft for red-pen.")
lg["B8"] = ("Everything is editable. Cells most expected to change: Functions column (K on the tracker, draft for red-pen), "
            "SAMPLE budgets, blank Q1-baseline budgets.")
lg["A17"] = "KPI Tracker FY26-27 (tab 1)"
lg["B17"] = ("The single merged sheet — org Head-Abstract format with one Budgeted / Actual / Variance / Remarks set for "
             "FY 2026-27, Actual updated at each KPI's frequency. Variance = Budgeted − Actual (org convention): negative "
             "= beat on higher-is-better rows; rows flagged 'lower is better' read inverted.")
lg["B18"] = ("KPI name follows Category:Product:Cohort::Name; per-batch rows split into B3 / B4. Budgets are numeric — "
             "the ≤ / ≥ direction lives in Description and Remarks. Blank Budgeted = first-quarter baseline sets it. "
             "One sheet, so there is no separate target column to keep in sync.")
lg["A19"] = "Training columns (I–K)"
lg["B19"] = ("Dependent metrics · Funnel · Functions are a collapsible column group, collapsed by default — expand with "
             "the +/− control above the columns. Collapsed = the org-format tracker; expanded = the training view.")
lg["A20"] = "Metric categories (col C)"
lg["B20"] = ("Org Head-Abstract vocabulary — Business Impact · Content Effectiveness · Content Velocity · Content Efficiency · Content Relevance · Stakeholder Alignment · Executive Ops — plus three department extensions: Program Delivery · University Alignment · Platform Reliability. Category = what the KPI measures; Lane (col L) = who is accountable; Functions (col K) = who does the work.")
for r in (1, 4, 8, 17, 18, 19, 20):
    lg.cell(row=r, column=1).font = F(10, bold=True)
    lg.cell(row=r, column=1).alignment = Alignment(vertical="top", wrap_text=True)
    lg.cell(row=r, column=2).font = F(10)
    lg.cell(row=r, column=2).alignment = Alignment(vertical="top", wrap_text=True)
    lg.row_dimensions[r].height = 55

wb.save(XLSX)

# ---------------------------------------------------------------- html page
TAG = {"CASCADE": "tag-cascade", "SAMPLE": "tag-sample", "CROSS-DEPT": "tag-xdept", "ORG": "tag-org"}
def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

STYLE = """  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #ffffff; padding: 40px 20px; color: #1a1a1a; line-height: 1.5; }
  .container { max-width: 1320px; margin: 0 auto; }
  h1 { font-size: 2em; margin-bottom: 8px; font-weight: 700; }
  .subtitle { font-size: 1em; color: #666; margin-bottom: 30px; }
  h2 { font-size: 1.4em; margin: 40px 0 20px 0; padding-bottom: 8px; border-bottom: 2px solid #000; font-weight: 700; }
  .sectionlead { color: #666; font-size: 0.92em; margin: -12px 0 16px; }
  .scroll { overflow-x: auto; }
  table { width: 100%; border-collapse: collapse; margin-bottom: 30px; font-size: 0.85em; min-width: 1100px; }
  th { background: #000; color: #fff; padding: 9px; text-align: left; font-weight: 600; border: 1px solid #000; }
  td { padding: 9px; border: 1px solid #ccc; vertical-align: top; }
  td.kra { font-weight: 600; }
  td.kra .num { display: block; margin-top: 4px; }
  td.kra .lead { display: block; margin-top: 4px; font-weight: 400; }
  .num { font-variant-numeric: tabular-nums; font-weight: 600; }
  .lead { color: #555; font-size: 0.95em; font-weight: 400; }
  .team { display: inline-block; font-size: 0.82em; font-weight: 600; letter-spacing: .03em;
    border: 1px solid #999; color: #444; padding: 1px 7px; border-radius: 3px; background: #fff; }
  .tag { display: inline-block; font-size: 0.72em; font-weight: 600; letter-spacing: .04em;
    padding: 1px 7px; border-radius: 3px; vertical-align: 1px; white-space: nowrap; }
  .tag-org { background: #1a1a1a; color: #fff; }
  .tag-xdept { background: #f3e1e1; color: #a34040; }
  .tag-sample { background: #fff3cd; color: #856404; }
  .tag-cascade { background: #e7f3ff; color: #004085; }
  .key-point { background: #e7f3ff; border-left: 3px solid #004085; padding: 12px; margin: 20px 0; }
  strong { font-weight: 600; }
  .footnote { font-size: 0.85em; color: #666; margin-top: 30px; border-top: 1px solid #ccc; padding-top: 12px; }
  th.c, td.c { text-align: center; }
  .kpiname { font-family: ui-monospace, 'SF Mono', Menlo, monospace; font-size: .9em; }
  .toggle-btn { font-size: .88em; font-weight: 600; border: 1px solid #999; background: #fff; color: #444;
    padding: 5px 14px; border-radius: 3px; cursor: pointer; margin-bottom: 12px; }
  .toggle-btn:hover { background: #f2f2f2; }
  #trk .tc { display: none; }
  #trk.train .tc { display: table-cell; }
  #trk { min-width: 1500px; }
  #trk.train { min-width: 2250px; }"""

body = []
body.append('  <h1>NIAT Org KPIs as KRAs — Department KPI Tracker</h1>')
body.append('  <div class="subtitle">Training sheet and FY 2026-27 tracker, merged &middot; August 2026 &middot; one row per '
            'trackable KPI, grouped under the org KRA it moves &middot; training columns fold out &middot; editable workbook: '
            'kra_training_sheet.xlsx (3 tabs)</div>')
body.append('  <div class="key-point"><strong>How to read this sheet:</strong> a <strong>KRA</strong> (Key Result Area) is an '
            'organizational outcome NIAT is judged on — it carries the target; each KRA block keeps its color family (a reading '
            'aid — identity is always in the text). Each numbered row is <strong>one trackable KPI</strong> — per-batch rows split '
            'into B3 / B4, band metrics decompose into one row per band. <strong>Variance = Budgeted &minus; Actual</strong> (org '
            'Head-Abstract convention): negative = beat on higher-is-better rows; rows flagged <em>lower is better</em> read '
            'inverted. Blank Budgeted = first-quarter baseline sets it. The three <strong>training columns</strong> — '
            '<strong>Dependent metrics</strong> (the trigger metrics that compose or precede the KPI), the <strong>Funnel</strong> '
            '(causal chain to the org KPI), and <strong>Functions that move it</strong> (the real teams, per the HOD one-pager '
            'key terms; <strong>Lane</strong> stays the accountability owner, not a team) — are collapsed by default: toggle them '
            'here, expand the column group in the workbook. Markers: '
            '<span class="tag tag-org">ORG</span> org-owned scoreboard, tracked not owned &middot; '
            '<span class="tag tag-xdept">CROSS-DEPT</span> resolved across departments, we route &middot; '
            '<span class="tag tag-sample">SAMPLE</span> illustrative until baselines land &middot; '
            '<span class="tag tag-cascade">CASCADE</span> same KPI feeds two KRAs.</div>')
body.append('  <h2>1. KRA &rarr; KPI Tracker — FY 2026-27</h2>')
body.append('  <div class="sectionlead">The sheet people live in after training — muted rows are context (org-owned or pending), '
            'so nothing from the training story is lost.</div>')
body.append('  <button id="tbtn" class="toggle-btn" onclick="tt()">Show training columns — Dependent metrics &middot; Funnel '
            '&middot; Functions &#9662;</button>')
body.append('  <div class="scroll">')
body.append('  <table id="trk">')
body.append('    <tr>'
            '<th class="c" rowspan="2">S. No.</th>'
            '<th rowspan="2" style="min-width:150px">KRA</th>'
            '<th rowspan="2">Metric category</th>'
            '<th class="c" rowspan="2">Product</th>'
            '<th class="c" rowspan="2">Cohort</th>'
            '<th rowspan="2" style="min-width:130px">Metric name</th>'
            '<th rowspan="2" style="min-width:190px">KPI name (naming convention)</th>'
            '<th rowspan="2" style="min-width:200px">Description</th>'
            '<th class="tc" rowspan="2" style="min-width:240px">Dependent metrics</th>'
            '<th class="tc" rowspan="2" style="min-width:220px">Funnel &rarr; org KPI</th>'
            '<th class="tc" rowspan="2" style="min-width:150px">Functions that move it</th>'
            '<th rowspan="2">Lane (KPI owner)</th>'
            '<th class="c" rowspan="2">Unit</th>'
            '<th rowspan="2">Frequency</th>'
            '<th class="c" colspan="4">FY 2026-27 — annual</th></tr>')
body.append('    <tr><th class="c">Budgeted</th><th class="c">Actual</th><th class="c">Variance</th>'
            '<th style="min-width:170px">Remarks</th></tr>')
body.append('    <tbody>')

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
            tr += f'<td colspan="16" style="font-style:italic;color:#777">{esc(b["note"])}</td></tr>'
            body.append('    ' + tr)
            first_of_kra = False
            continue
        n = len(b["rows"])
        metric_html = f'<strong>{esc(b["metric"])}</strong>'
        if b["marker"]:
            metric_html += f' <span class="tag {TAG[b["marker"]]}">{esc(b["marker"])}</span>'
        sh = {
            3:  f'<td rowspan="{n}">{esc(b["category"])}</td>',
            4:  f'<td class="c" rowspan="{n}">{esc(b["product"])}</td>',
            6:  f'<td rowspan="{n}">{metric_html}</td>',
            8:  f'<td rowspan="{n}"><span class="lead">{esc(b["desc"])}</span></td>',
            9:  f'<td class="tc" rowspan="{n}"><span class="lead">{esc(b["dep"])}</span></td>',
            10: f'<td class="tc" rowspan="{n}"><span class="lead">{esc(b["funnel"])}</span></td>',
            11: f'<td class="tc" rowspan="{n}">{esc(b["functions"])}</td>',
            12: f'<td rowspan="{n}"><span class="team">{esc(b["lane"])}</span></td>',
            13: f'<td class="c" rowspan="{n}">{esc(b["unit"])}</td>',
            14: f'<td rowspan="{n}">{esc(b["freq"])}</td>',
            18: f'<td rowspan="{n}"><span class="lead">{esc(b["remark"]) if b["remark"] else "&mdash;"}</span></td>',
        }
        runs = []
        i = 0
        while i < n:
            j = i
            while j + 1 < n and b["rows"][j + 1]["cohort"] == b["rows"][i]["cohort"]:
                j += 1
            runs.append((i, j - i + 1, b["rows"][i]["cohort"]))
            i = j + 1
        run_starts = {st: (ln, ch) for st, ln, ch in runs}
        for i, rr in enumerate(b["rows"]):
            sno += 1
            style = f'background:#{tint}' + (';border-top:2px solid #555' if first_of_kra and i == 0 else '')
            budget = rr["budget"]
            btxt = '&mdash;' if budget is None else f'{budget:g}'
            kpi_td = f'<td class="kpiname">{esc(rr["kpi"])}</td>'
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
                cells += [sh[6], kpi_td, sh[8], sh[9], sh[10], sh[11], sh[12], sh[13], sh[14], bav, sh[18]]
            else:
                cells += [kpi_td, bav]
            body.append(f'    <tr style="{style}">' + ''.join(cells) + '</tr>')
        first_of_kra = False
body.append('    </tbody>')
body.append('  </table>')
body.append('  </div>')

# session index (counts computed at metric level, matching the merged-cell COUNTIF)
counts = []
for name, pat, _ in FUNCTIONS:
    counts.append(sum(1 for b in TRACKER if "rows" in b and pat in b["functions"]))
body.append('  <h2>2. Session index — by function (the training rooms)</h2>')
body.append('  <div class="sectionlead">Functions are where people actually sit — vocabulary from the HOD one-pager &sect;2 key '
            'terms. Counts are per metric (a band or cohort block counts once). The Functions column is a draft for red-pen — '
            'edit column K in the workbook and the counts recompute.</div>')
body.append('  <table style="min-width:0">')
body.append('    <tr><th style="width:26%">Function (training room)</th><th>Your rows in the tracker</th>'
            '<th class="c" style="width:10%">Row count</th></tr>')
body.append('    <tbody>')
for (name, pat, rows_txt), cnt in zip(FUNCTIONS, counts):
    body.append(f'    <tr><td><strong>{esc(name)}</strong></td><td>{esc(rows_txt)}</td>'
                f'<td class="c num">{cnt}</td></tr>')
body.append('    </tbody>')
body.append('  </table>')

body.append('  <div class="footnote">Training companion to the HOD one-pager (&sect;6 scoreboard + mechanism trees) and the '
            'internal operating view. Downloadable editable master: <strong>kra_training_sheet.xlsx</strong> — 3 tabs: KPI '
            'Tracker FY26-27 (training columns in a collapsible group, collapsed by default) &middot; Session Index &middot; '
            'Legend, same color coding. Variance = Budgeted &minus; Actual (org Head-Abstract convention). Functions vocabulary '
            'from the HOD one-pager &sect;2 key terms — draft for red-pen. SAMPLE numbers pend LE-dashboard baselines. Colors '
            'follow a CVD-validated categorical palette. Curriculum / Content Department &middot; 2026-08-21.</div>')

page = ("<title>NIAT Org KPIs as KRAs — Department KPI Training Sheet</title>\n"
        "<style>\n" + STYLE + "\n</style>\n"
        '<div class="container">\n' + "\n".join(body) + "\n</div>\n"
        "<script>\n"
        "function tt(){var t=document.getElementById('trk'),b=document.getElementById('tbtn');"
        "t.classList.toggle('train');var on=t.classList.contains('train');"
        "b.innerHTML=on?'Hide training columns \\u25B4':'Show training columns \\u2014 Dependent metrics \\u00B7 Funnel \\u00B7 Functions \\u25BE';}\n"
        "</script>\n")
HTML.write_text(page)

# ---------------------------------------------------------------- verify
wb2 = load_workbook(XLSX)
t = wb2["KPI Tracker FY26-27"]
snos = [t.cell(row=r, column=1).value for r in range(3, t.max_row + 1) if isinstance(t.cell(row=r, column=1).value, int)]
formulas = sum(1 for r in range(3, t.max_row + 1) if str(t.cell(row=r, column=C_VAR).value or "").startswith("=IF"))
notes = sum(1 for r in range(3, t.max_row + 1)
            if t.cell(row=r, column=1).value is None and t.cell(row=r, column=3).value)
print("sheets:", wb2.sheetnames)
print("numbered rows:", len(snos), "| max sno:", max(snos), "| note rows:", notes, "| variance formulas:", formulas)
print("grouped/hidden cols:", [c for c in "IJK" if t.column_dimensions[c].hidden and t.column_dimensions[c].outline_level == 1])
si2 = wb2["Session Index"]
print("session formulas:", [si2.cell(row=r, column=3).value for r in range(2, 2 + len(FUNCTIONS))][:2], "...")
print("computed counts:", dict(zip([f[0].split(" —")[0] for f in FUNCTIONS], counts)))
print("legend rows:", wb2["Legend & Notes"].max_row)
print("stale map refs in xlsx:", sum(1 for sh in wb2 for row_ in sh.iter_rows() for c in row_
      if isinstance(c.value, str) and "KRA-KPI Map" in c.value))
print("html bytes:", len(page), "| tc cells:", page.count('class="tc"'), "| toggle:", "tt()" in page)
