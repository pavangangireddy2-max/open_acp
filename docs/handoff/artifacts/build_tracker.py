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
  "jsh":    "Product Managers + DA/DEs + CSI team + Pedagogy Experts (journey design)",
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
   "desc": "% deviation of the executed schedule vs the designed schedule, across the journey steps (lectures, quizzes, practice releases, assets) — existence only: a step that never runs counts here, not in Journey Step Health",
   "dep": dep(0),
   "funnel": fun(0) + " · also: delivered = approved plan → university trust → Univ Relations CSAT (feeds KRA 3)",
   "functions": FX["pdg"], "unit": "%", "freq": "Weekly", "lane": "Product Learning Experience",
   "remark": "CASCADE — feeds KRA 1 + KRA 3, tracked once (no double count). Lower is better — variance reads inverted. Assembled KPI — each dependent step carries a named owner (col I); we orchestrate, route, escalate: red 2 consecutive weeks → HOD-to-HOD.",
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
   "desc": "|avg module-quiz score − avg biweekly skill-assessment score| — the taught-vs-tested gap",
   "dep": dep(2), "funnel": fun(2), "functions": FX["align"],
   "unit": "pp", "freq": "Monthly", "lane": "Learning Domains",
   "remark": "Lower is better — variance reads inverted. Tightens to ≤5 pp after 3 clean cycles (cycle = semester).",
   "rows": [
     {"cohort": "B3", "kpi": "Business Impact:NIAT:B3::Content–Assessment Alignment", "budget": 10},
     {"cohort": "B4", "kpi": "Business Impact:NIAT:B4::Content–Assessment Alignment", "budget": 10}]},
  {"kra": 0, "category": "Business Impact", "product": "All", "metric": "Engagement-Matrix Cell Migration", "marker": "SAMPLE",
   "desc": "% of learners in the HE×HV (high-effort × high-value) cell; the full 3×3 matrix stays diagnostic",
   "dep": dep(3), "funnel": fun(3), "functions": FX["cell"],
   "unit": "%", "freq": "Per cycle · read monthly", "lane": "Learning Platform",
   "remark": "SAMPLE — from ~4% baseline; budget confirms when the LE dashboard lands. Alt pick: M×M 10 → 20. Arbitration with Score Bands: both red → the bleeding cell names the lane — high effort + low value = content not converting effort (Learning Domains); effort itself draining = engagement problem (Learning Platform).",
   "rows": [{"cohort": "All", "kpi": "Business Impact:All::% Learners in HE×HV Cell", "budget": 10}]},
  {"kra": 0, "note": "Summative & Formative Achievement — ORG scoreboard, tracked not owned: same 30/40/30 on assessment scores, per batch. Steps 1–3 held → assessments run → the 75% lands → SPI Bands."},
  # ---- KRA 2
  {"kra": 1, "category": "Content Efficiency", "product": "All", "metric": "Content Issue Resolution Efficiency", "marker": "",
   "desc": "% of content issues resolved within the 2-day TAT — resolved = fix live + students notified",
   "dep": dep(5), "funnel": fun(5), "functions": FX["cissue"],
   "unit": "%", "freq": "Monthly", "lane": "Learning Domains",
   "remark": "The % climbs over the year; the 2-day TAT itself doesn't move.",
   "rows": [{"cohort": "All", "kpi": "Content Efficiency:All::Content Issue Resolution Efficiency", "budget": 80}]},
  {"kra": 1, "category": "Content Efficiency", "product": "All", "metric": "Content Issue Recurrence", "marker": "",
   "desc": "% of resolved content issues that recur — root-cause close: instance fixed · artifact changed · tripwire added · broadcast sent",
   "dep": dep(6), "funnel": fun(6), "functions": FX["cissue"],
   "unit": "%", "freq": "Quarterly", "lane": "Learning Domains",
   "remark": "Lower is better — variance reads inverted.",
   "rows": [{"cohort": "All", "kpi": "Content Efficiency:All::Content Issue Recurrence", "budget": 2}]},
  {"kra": 1, "category": "Content Efficiency", "product": "All", "metric": "Agentic Production Coverage", "marker": "",
   "desc": "% of authorable content production (questions, slides, cheatsheets, reading material, translations) flowing through registered agentic workflows — machine first drafts, humans as reviewers not authors; blended rollup, excludes on-camera and live-delivery work",
   "dep": "per-type coverage % (questions · slides · cheatsheets · reading material · translations) · registered-workflow count (pipeline registry) · human-review pass rate · cost-per-item trend (Content–Central)",
   "funnel": "more production through governed pipelines → faster fixes + consistent quality at scale (CIRE / CIR run through these pipes) → Academics CSAT",
   "functions": "Content–Central + DA/DEs — pipelines & production workflows; domain teams publish through them",
   "unit": "%", "freq": "Monthly", "lane": "Agentic Content Platform",
   "remark": "ACP's tracker row now CIRE/CIR sit with Learning Domains — this lane builds the pipes; the issue KPIs score the fixes. Target 90% blended (§5); read with cost-per-item + Content Issue Recurrence. Functions cell draft for red-pen. Absorbs the retired R&D Initiative Impact — initiative counting folds into coverage % + cost-per-item + recurrence; mirrored in FS & CS Core Section A at the same 90.",
   "rows": [{"cohort": "All", "kpi": "Content Efficiency:All::Agentic Production Coverage", "budget": 90}]},
  {"kra": 1, "category": "Content Effectiveness", "product": "All", "metric": "Learning Environment Satisfaction", "marker": "",
   "desc": "Student rating of the learning environment — driven by the four platform rows below",
   "dep": dep(7), "funnel": fun(7), "functions": FX["eng"],
   "unit": "score /5", "freq": "Monthly", "lane": "Developer Platform",
   "remark": "Umbrella for the four Developer Platform rows below. Verbatims route like CROSS-FUNCTION: reliability complaints → Developer Platform backlog · capability gaps → Learning Platform capability registry.",
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
   "desc": "% of the journey steps that ran this month finishing green (one-pager §11 thresholds) — NIAT first, then per product. Health of what ran: a step that never ran counts in PDG, not here",
   "dep": dep(12), "funnel": fun(12), "functions": FX["jsh"],
   "unit": "%", "freq": "Monthly", "lane": "Product Learning Experience",
   "remark": "Q1 baseline sets the budget — blank until then (org-tracker precedent). Assembled KPI — steps owned per col I (§11 owner column); we orchestrate, route, escalate.",
   "rows": [{"cohort": "All", "kpi": "Program Delivery:NIAT::Journey Step Health", "budget": None}]},
  {"kra": 1, "category": "Content Efficiency", "product": "NIAT", "metric": "Product Issue Resolution Efficiency", "marker": "CROSS-FUNCTION",
   "desc": "% of student-reported product issues resolved within TAT — resolved across functions, we route; fix live + students notified",
   "dep": dep(13), "funnel": fun(13), "functions": FX["prod"],
   "unit": "%", "freq": "Monthly", "lane": "Product Learning Experience",
   "remark": "Q1 baseline sets the TAT target — blank until then.",
   "rows": [{"cohort": "All", "kpi": "Content Efficiency:NIAT::Product Issue Resolution Efficiency", "budget": None}]},
  {"kra": 1, "category": "Content Efficiency", "product": "NIAT", "metric": "Product Issue Recurrence", "marker": "CROSS-FUNCTION",
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
  {"kra": 2, "category": "University Alignment", "product": "NIAT", "metric": "University Curriculum & Framework Compliance", "marker": "",
   "desc": "% of submission cycles fully compliant — approved BOS syllabus + NHQRF / Woolf / AICTE / UGC",
   "dep": dep(18), "funnel": fun(18), "functions": FX["comp"],
   "unit": "%", "freq": "Per cycle", "lane": "Product Learning Experience",
   "remark": "",
   "rows": [{"cohort": "All", "kpi": "University Alignment:NIAT::University Curriculum & Framework Compliance", "budget": 100}]},
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
  ["Content–Central (production ops)", "Content–Central",
   "Agentic Production Coverage — the agentic pipelines & production workflows the domain teams publish through"],
  ["Engineering", "Engineering",
   "LES + its four drivers (DP lane) · Content Issue pair tooling/routing (ACP lane) · Cell Migration build (LP lane)"],
  ["Product Managers", "Product Managers",
   "Program Delivery Gap (feeds KRA 1 + 3) · Engagement-Matrix Cell Migration · Journey Step Health · Product Issue pair"],
  ["Pedagogy Experts", "Pedagogy Experts",
   "Module-Quiz Score Bands · Content–Assessment Alignment · Journey Step Health (journey design at the CSI team)"],
  ["DA/DEs", "DA/DE",
   "score analysis (bands, alignment) · LE dashboard (cell migration) · Journey Step Health instrumentation · Agentic Production Coverage instrumentation"],
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
for name in list(wb.sheetnames):  # prefix match also clears openpyxl "…View1" dedup ghosts
    if name.startswith(("KRA-KPI Map", "KPI Tracker FY26-27", "Session Index",
                        "CSI Team View", "FullStack & CS Core View", "Content–Central View")):
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
ROWMAP = []
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
        cohort_top = {}
        while i < n:
            j = i
            while j + 1 < n and b["rows"][j + 1]["cohort"] == b["rows"][i]["cohort"]:
                j += 1
            if j > i:
                ws.merge_cells(start_row=r0 + i, start_column=5, end_row=r0 + j, end_column=5)
            put(r0 + i, 5, b["rows"][i]["cohort"], center=True)
            for q in range(i, j + 1):
                cohort_top[r0 + q] = r0 + i
            i = j + 1
        for i, rr in enumerate(b["rows"]):
            r = r0 + i
            sno += 1
            ROWMAP.append({"sno": sno, "r": r, "r0": r0, "cr": cohort_top[r], "metric": b["metric"],
                           "functions": b["functions"], "dlen": len(b["desc"])})
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
    fml = f'=COUNTIF({rng},"*{pat}*")'
    if pat == "Content":  # bare-Content rooms only; Content–Central has its own row
        fml = f'=COUNTIF({rng},"*Content*")-COUNTIF({rng},"*Content–Central*")'
    si.cell(row=r, column=3, value=fml).font = F(10, bold=True)
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
lg["B3"] = ("A lane is an accountability grouping of KPIs, NOT a team — the lane lead answers for the number at review. "
            "Learning Domains (domain curriculum, pedagogy & question banks) · Learning Platform (shared study / practice / "
            "revision / assessment capabilities) · Product Learning Experience (product-specific learning experiences + "
            "university delivery & compliance) · Agentic Content Platform (AI platforms & automation for content production) · "
            "Developer Platform (IDE, compiler & platform services) · Shared/PMO (department-wide programs). "
            "Category (col C) = what it measures · Lane (col L) = who is accountable · Functions (col K) = who does the work.")
lg["B7"] = ("[ORG] org-owned scoreboard, tracked not owned · [CROSS-FUNCTION] resolved across functions, we route · "
            "[SAMPLE] illustrative numbers until baselines land · [CASCADE] same KPI feeds two KRAs.")
lg["B4"] = ("The teams that actively build the learning system (HOD one-pager §2 key terms): Content, Engineering, "
            "Product Managers, Pedagogy Experts, DA/DEs, Graphic Designers, Video Editors, Product Designers, "
            "Packaging Teams (Content Systems & Infra), SDIs — plus the CSI team on delivery- and university-facing rows. Draft for red-pen.")
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
lg["A21"] = "Team views (tabs 4–5)"
lg["B21"] = ("Functional Operating Views — one satellite tab per team, docked to the tracker, never merged. Section A "
            "mirrors the tracker rows the team is on the hook for (live formulas — numbers are edited on the tracker tab "
            "only). Section B = KPIs the team owns, budgets & actuals here, each with a Ladders-to call: direct (an org "
            "KRA number) · enabling (a dept §5 KPI) · hygiene (guardrail, no ladder by design). Section C = asks of "
            "counterparties. Pilots: CSI team · FullStack & CS Core.")
lg["A22"] = "Lane ↔ working teams"
lg["B22"] = ("Worked by (primary) — staffing, never ownership (col L stays the accountability; many-to-many): "
             "Learning Domains — Content domain teams + Pedagogy Experts (lesson-plan design, the in-classroom "
             "experience) + DA/DEs · Learning Platform — Product Managers + Engineering + DA/DEs · Product Learning "
             "Experience — CSI team + Product Managers + Pedagogy Experts (journey design) · Agentic Content Platform "
             "— Content–Central + DA/DEs · Developer Platform — Engineering · Shared/PMO — PMO. Program Ops, "
             "Instructors dept and Mentors are counterparties reached through asks (§7 / team-view Section C), not lane staff.")
lg["A23"] = "Domain product boundary"
lg["B23"] = ("Domain-specific product work — evaluation environments and domain-specific learning-platform capabilities, "
             "incl. domain-specific learner-facing AI tutors/agents — is raised and accepted by domain SMEs, built by "
             "Product Managers + Engineering, and its KPIs sit in the domain team's Section B under Domain Product "
             "Enablement (Learning Domains accountability). Generic/reusable capabilities rest with the Learning Platform "
             "lane, product-owned. ACP boundary: ACP = content-facing production pipelines · domain product work = "
             "learner-facing systems. Section-B-first: an org-tracker row waits until the environment registry sets a baseline.")
lg["A20"] = "Metric categories (col C)"
lg["B20"] = ("Org Head-Abstract vocabulary — Business Impact · Content Effectiveness · Content Velocity · Content Efficiency · Content Relevance · Stakeholder Alignment · Executive Ops — plus three department extensions: Program Delivery · University Alignment · Platform Reliability. Category = what the KPI measures; Lane (col L) = who is accountable; Functions (col K) = who does the work.")
lg["A24"] = "Metric evolution (pre-agreed)"
lg["B24"] = ("Forward moves recorded so the sheet evolves without relitigating. (1) R&D Initiative Impact — retired Aug 2026, "
             "absorbed by Agentic Production Coverage (org row, mirrored in FS & CS Core Section A at 90) + the cost-per-item "
             "rows + Content Issue Recurrence; initiative counting is no longer a KPI anywhere. (2) Evaluation Environment "
             "Coverage + Domain Capability Delivery — at ~90% registry coverage or after two review cycles, the pair folds "
             "into one funnel KPI: raised → accepted → delivered rate + TAT, with capabilities-raised/quarter as a "
             "non-budgeted context line. (3) Pedagogy Initiative Impact — becomes Domain Learning-Value Uplift (ability/band "
             "improvement across the domain's courses per cycle, HE×HV machinery, semester/quarter windows) once per-course "
             "ability instruments are confirmed.")
for r in (1, 3, 4, 7, 8, 17, 18, 19, 20, 21, 22, 23, 24):
    lg.cell(row=r, column=1).font = F(10, bold=True)
    lg.cell(row=r, column=1).alignment = Alignment(vertical="top", wrap_text=True)
    lg.cell(row=r, column=2).font = F(10)
    lg.cell(row=r, column=2).alignment = Alignment(vertical="top", wrap_text=True)
    lg.row_dimensions[r].height = 55
lg.row_dimensions[3].height = 70
lg.row_dimensions[21].height = 70
lg.row_dimensions[22].height = 84
lg.row_dimensions[24].height = 120

# ---------------------------------------------------------------- team views (tabs 4-5): docked to the tracker, never merged
TRK = "KPI Tracker FY26-27"
def tcell(col, r): return f"'{TRK}'!{col}{r}"
def tref(col, r):  return '=IF({0}="","",{0})'.format(tcell(col, r))

def fx_tokens(s):
    # em-dash splits, en-dash doesn't: "Content–Central" stays one token
    for d in ("—", "·", ",", ":", ";", "(", ")"):
        s = s.replace(d, "+")
    return [t.strip() for t in s.split("+") if t.strip()]
def a_rows(match, twins):
    return [rm for rm in ROWMAP if match in fx_tokens(rm["functions"]) or rm["metric"] in twins]

TEAM_VIEWS = [
 {"tab": "CSI Team View", "hue": 0, "team": "CSI team",
  "sub": ("Curriculum Systems & Infrastructure — Product Learning Experience lane. Section A mirrors the department tracker "
          "(live formulas — numbers are edited on the KPI Tracker tab only) · Section B is owned here, budgets & actuals live "
          "on this tab · Section C = asks of counterparties."),
  "match": "CSI team", "twins": [],
  "own": [
   ("Content Efficiency", "Cost per BOS Approval (NIAT)",
    "Average cost incurred per approved BOS across university partners. Includes CSI team payroll and non-payroll costs (travel, liaison activities) attributed to BOS approval work.",
    "enabling → dept Cost per BOS Approval (§5 Content Efficiency) — the economics of the KRA-3 BOS engine",
    "INR", "Quarterly", "Q1 ref: B ₹14,040 (quarterly)."),
   ("Content Efficiency", "Cost per Vernacular Content Hour (NIAT + Academy)",
    "Average cost to produce one hour of vernacular-language content, tracked centrally by the CSI team. Includes CSI payroll and AI tooling costs attributed to vernacular production.",
    "enabling → dept Cost per Vernacular Content Hour (§5 Content Efficiency) — central track; FS&CS Core carries the production-side twin",
    "INR", "Monthly", ""),
   ("Executive Ops", "Operations & Growth Cost",
    "Average cost across executive ops, operational efficiency, market analysis and hiring activities. Tracked at team scope, not per product.",
    "hygiene — team run-cost guardrail; no org ladder by design",
    "INR", "Monthly", ""),
  ],
  "asks": [
   ("Conduction adherence", "Program Ops",
    "Zero schedule deviation on lectures / quizzes / assessments + attendance drive — feeds Program Delivery Gap & Journey Step Health (§7 ask; exact thresholds pending)."),
   ("Learning-assets SLA", "Instructors dept",
    "PPT + recorded video ready & loaded ≥1 month ahead of delivery — feeds the assets leg of Program Delivery Gap."),
   ("University response windows", "Univ Relations",
    "BOS meeting windows + response SLAs on university communications — feeds BOS Credit Acceptance & University Communication TAT."),
  ]},
 {"tab": "FullStack & CS Core View", "hue": 2, "team": "FullStack & CS Core",
  "sub": ("Learning Domains lane — Content function. Section A mirrors the department tracker (live formulas — numbers are "
          "edited on the KPI Tracker tab only) · Section B is owned here, budgets & actuals live on this tab · Section C = "
          "asks of counterparties."),
  "match": "Content", "twins": ["Engagement-Matrix Cell Migration", "Learning Environment Satisfaction", "Agentic Production Coverage"],
  "own": [
   ("Business Impact", "Summative Skill Assessment Achievement Rate",
    "Students scoring above the defined passing threshold in summative skill assessments across owned domains. Passing threshold set by the team per domain context (default reference: 70%).",
    "direct → org KRA 1 — the summative achievement number itself (org scoreboard; the tracker reads it via module-quiz Bands + Alignment)",
    "%", "Quarterly", "Q1 ref: B 35 (quarterly) · default threshold 70%."),
   ("Business Impact", "Formative Skill Assessment Achievement Rate",
    "Students scoring above the defined passing threshold in formative skill assessments across owned domains. Passing threshold set by the team per domain context (default reference: 70%).",
    "enabling → Summative SA Achievement (row above) + tracker Content–Assessment Alignment — the early-warning formative read",
    "%", "Monthly", "Q1 Jul: B 23 · A 33.4 — 75% cap used as the Skill Assessments cut-off."),
   ("Business Impact", "Graded Assessment Achievement Rate (NIAT)",
    "Students scoring above the defined passing threshold in university-conducted graded assessments — Mid-1, Mid-2 and End Semester exams — delivered in collaboration with the university.",
    "enabling → dept Business Impact (§5) — university-conducted exams: NIAT SPI & university trust",
    "%", "Monthly", ""),
   ("Business Impact", "Weekly Active Users (Launchpad)",
    "Total prospective learner leads generated in the period through content-driven channels (organic, referral, campaigns, partnerships).",
    "enabling → dept Business Impact (§5) — Launchpad top-of-funnel",
    "Count", "Monthly (wkly avg)", ""),
   ("Content Effectiveness", "Pedagogy Initiative Impact",
    "Implemented pedagogy initiatives with measurable learning-outcome improvement. Outcome baseline must be defined and agreed before the initiative is launched.",
    "enabling → module-quiz Bands + org KRA 2 Academics CSAT — pedagogy initiatives move the learning numbers",
    "Count", "Quarterly", "Owned by the domain SME on this team; embedded Pedagogy Experts contribute to the initiatives. Pre-agreed outcome form: becomes Domain Learning-Value Uplift — ability/band improvement across this domain's courses per cycle (HE×HV machinery) — once per-course ability instruments are confirmed."),
   ("Content Effectiveness", "Learner Accessed Content Completion Rate",
    "Video units: for each learner, % of video units they opened that they also completed; averaged across learners. Excludes units with zero opens.",
    "enabling → tracker Engagement-Matrix Cell Migration — video-stickiness leg of the value axis; access-conditioned, so conduction effects are stripped",
    "%", "Monthly", ""),
   ("Content Effectiveness", "Practice Attempt-to-Completion Rate",
    "Practice units: for each learner, % of coding/project exercises attempted that they also completed. Surfaces environment friction (IDE, playground, cloud setup) vs difficulty-related drop-off.",
    "enabling → tracker Journey Step Health steps 6–7 (practice return & completion) + Learning Environment Satisfaction",
    "%", "Monthly", "Q1 Jul: B 38."),
   ("Content Velocity", "Learning Content Hours Delivered",
    "Total learning content hours created per month across all formats (video, text, interactive). Content serving multiple products counted once.",
    "enabling → dept Content Velocity (§5) — capacity for B4 & new stacks",
    "Hours", "Monthly", "Q1 Jul: B 50 · A 46."),
   ("Content Velocity", "Vernacular Content Hours Delivered",
    "Total vernacular-language learning content hours created per month. Tracked separately from English hours — effort per vernacular hour differs significantly.",
    "enabling → dept Content Velocity (§5) — vernacular capacity",
    "Hours", "Monthly", "Q1 Jul: B 0 — no vernacular slate yet."),
   ("Content Velocity", "Practice & Assessment Content Pieces Delivered",
    "Total practice and assessment pieces delivered monthly across owned domains (MCQs, coding questions, projects, case studies).",
    "enabling → dept Content Velocity (§5) — practice depth behind Journey Step Health steps 5–7",
    "Count", "Monthly", "Q1 Jul: B 1,600 · A 1,499 (Aug B: 1,000)."),
   ("Content Velocity", "Branding Content Assets Delivered",
    "Total branded content pieces produced monthly (thumbnails, banners, promo assets).",
    "enabling → dept Content Velocity (§5)",
    "Count", "Monthly", "Q1 Jul: B 0."),
   ("Content Efficiency", "Cost per Learning Hour Produced",
    "Average cost to produce one hour of learning content. Includes people, tools and infra involved in creation. Tracks creation efficiency — not delivery cost.",
    "enabling → dept Cost per Learning Hour (§5 Content Efficiency)",
    "INR", "Monthly", "Q1 Jul: B ₹10,000 · A ₹6,803 — 46 h across 4 products."),
   ("Content Efficiency", "Cost per Vernacular Content Hour",
    "Average cost to produce one hour of vernacular-language content. Includes team bandwidth involved in creation (contract basis, tools & infrastructure).",
    "enabling → dept Cost per Vernacular Content Hour (§5) — production-side twin of CSI's central track",
    "INR", "Monthly", "Q1 Jul: B 0 · A 0."),
   ("Content Efficiency", "Cost per MCQ Generated",
    "Average cost to develop one objective question, including both manual and AI-assisted production.",
    "enabling → dept Cost per MCQ (§5 Content Efficiency)",
    "INR", "Monthly", "Q1 Jul: B ₹40 · A ₹26 — 1,347 MCQs across 2 products."),
   ("Content Efficiency", "Cost per Coding Question",
    "Average cost to develop one coding question, including test-case design and evaluation-engine configuration.",
    "enabling → dept Cost per Coding Question (§5 Content Efficiency)",
    "INR", "Monthly", "Q1 Jul: B ₹400 · A ₹163 — 131 coding questions across 3 products."),
   ("Content Efficiency", "Cost per Branding Content Asset",
    "Average cost to create one branded content piece.",
    "enabling → dept Cost per Branding Asset (§5 Content Efficiency)",
    "INR", "Monthly", "Q1 Jul: B 0 · A 0."),
   ("Content Efficiency", "Platform Runtime Cost per Active Learner",
    "Total platform delivery costs (cloud compute, code-execution infra, cloud IDE hosting, GenAI API calls) divided by active learners in the period. Tracks delivery-cost efficiency as usage scales.",
    "enabling → dept Platform Runtime Cost per Active Learner (§5) — the team's share of delivery cost",
    "INR", "Monthly", ""),
   ("Content Relevance", "Tech Stack Freshness Rate",
    "% of tools, frameworks, libraries and environments referenced in content (and configured in IDEs, playgrounds, cloud setups) matching the current stable or LTS version at audit.",
    "enabling → tracker Industry Update Adherence — the freshness audit behind relevance",
    "%", "Monthly", "Q1 Jul: B 100 · A 100."),
   ("Stakeholder Alignment", "Stakeholder Content Request Fulfillment Rate",
    "Requests from Sales, Placements, Program Ops, Assessments and Instructors fulfilled within agreed timeframes across all products.",
    "enabling → dept Stakeholder Alignment (§5)",
    "%", "Monthly", "Q1 Jul: B 90 · A 90."),
   ("Stakeholder Alignment", "Cross-functional Sprint Delivery Rate",
    "% of committed tickets across Product, Pedagogy, Engineering, UI/UX and DA/DE — scoped and approved by this team — delivered within the committed sprint.",
    "enabling → dept Stakeholder Alignment (§5)",
    "%", "Monthly", "Q1 Jul: B 100 · A 100."),
   ("Domain Product Enablement", "Evaluation Environment Coverage",
    "% of practice/assessment item types in this domain's live curriculum with a production-ready evaluation environment (code judges, test harnesses, notebook/cloud envs). Domain configuration — item types, test cases, judges — by this team's SMEs; platform build by Product Managers + Engineering.",
    "enabling → Practice Attempt-to-Completion (environment-friction leg) + tracker Journey Step Health steps 6–7 + Learning Environment Satisfaction",
    "%", "Quarterly", "Baseline first: build the item-type × environment registry, then set the budget (APC precedent). Pre-agreed evolution: at ~90% coverage or after two cycles, EEC + DCD fold into one funnel KPI — raised → accepted → delivered rate + TAT, with capabilities-raised/quarter as a non-budgeted context line."),
   ("Domain Product Enablement", "Domain Capability Delivery",
    "Domain-specific learning-platform capabilities shipped vs committed per cycle. Raised and specified by this team's SMEs; built by Product Managers + Engineering; accountability stays here — the ask and the acceptance are domain-owned.",
    "enabling → dept Platform Capability Configuration Coverage (§5) + the LP capability registry",
    "%", "Quarterly", "Generic/reusable capabilities rest with the Learning Platform lane (product-owned), not here. Folds into the raised → accepted → delivered funnel with EEC when the trigger lands (see EEC remark + Legend)."),
   ("Executive Ops", "Operations & Growth Cost",
    "Average cost across executive ops, operational efficiency, market analysis and hiring activities. Tracked at team scope, not per product.",
    "hygiene — team run-cost guardrail; no org ladder by design",
    "INR", "Monthly", "Q1 Jul: A ₹300,863."),
   ("Executive Ops", "Creative Resource Utilisation Rate",
    "% of allocated Graphic Designer and Video Editor bandwidth utilised against planned branding and content-asset deliverables within a cycle. Primarily tracked and managed by Project Managers.",
    "hygiene — creative bandwidth guardrail (PM-managed); no org ladder by design",
    "%", "Monthly", "Q1 Jul: A 100% — fully utilised, at times stretched."),
  ],
  "asks": [
   ("Assessment blueprints per cycle", "Assessments team",
    "Skill-assessment blueprints + knowledge points shared before authoring each cycle; changes communicated — feeds Content–Assessment Alignment (§7 ask)."),
   ("Engagement & LE dashboards", "Learning Platform / DA-DEs",
    "Monthly LE + engagement-matrix cuts per domain — budgets for Cell Migration and module-quiz Bands come from here. Course-completion cuts included as a read-only view: completion is conduction-driven (Program Ops); the team's owned stickiness KPIs are Learner-Accessed Completion + Practice Attempt-to-Completion."),
   ("Domain-specific capability build", "Learning Platform (PMs + Engineering)",
    "Build slots for domain-raised capabilities and evaluation environments — SMEs here raise and accept; PMs + Engineering build. Boundary: generic/reusable capability = Learning Platform lane (product-owned) · domain-specific instance = KPI here, in Learning Domains · ACP = content-facing production pipelines, domain product work = learner-facing systems."),
   ("Classroom signal loop", "Instructors dept + Program Ops",
    "Structured instructor feedback + conduction context per module — feeds content iteration and Content Issue routing."),
  ]},
 {"tab": "Content–Central View", "hue": 3, "team": "Content–Central",
  "sub": ("Shared/PMO lane — the central two-person team: a Business Ops owner (shared-team delivery + Agentic Content "
          "Platform builds; reports to the HOD) with a PMO manager reporting to them — role titles pending. Section A "
          "mirrors the department tracker (live formulas — numbers are edited on the KPI Tracker tab only) · Section B is "
          "owned here, budgets & actuals live on this tab · Section C = asks of counterparties."),
  "match": "Content–Central", "twins": [],
  "a_notes": {"Agentic Production Coverage":
    " · Central read: units-at-bar — how many of the 5 learning-domain units hold ≥ 90 (a count, not a blended average); "
    "each domain owns its own slice in its own view (FS & CS Core wired, others as their views land)."},
  "own": [
   ("Business Ops — Shared Teams", "Shared-Team Deliverables Landed",
    "Of the deliverables the shared-resource teams (Product, Engineering, DA/DEs, Product Design) committed to content work "
    "for the period, the % delivered and accepted. Acceptance sits with the requesting unit — Central verifies the register, "
    "not the work.",
    "enabling → dept Stakeholder Alignment (§5) — the delivery contract with the embedded shared teams",
    "%", "Monthly", "Baseline first: Q1 builds the committed-deliverables register per shared team; budget set after one "
    "full cycle. Owned by the Business Ops lead."),
   ("Business Ops — Shared Teams", "Shared-Team Spend vs Plan",
    "Actual spend on shared-resource team allocations vs planned spend for the period. Reads over- and under-runs early; "
    "the value-for-spend judgment stays with the Business Ops owner at the monthly review.",
    "enabling → dept Content Efficiency (§5) — the ₹ side of the shared-team delivery contract",
    "%", "Monthly", "Baseline first: plan numbers come from the allocation agreed with each function head; tolerance band "
    "set after one full cycle. Owned by the Business Ops lead."),
   ("Business Ops — Shared Teams", "Creative Resource Utilisation — All Units",
    "Of the Graphic Designer & Video Editor bandwidth allocated across all sub-departments, the % actually used against "
    "planned deliverables in the cycle. Central reads the aggregate and the skew — which units are stretched, which "
    "under-use; day-to-day management stays with unit PMs. Low = planning gaps · over = scope creep or under-resourcing.",
    "enabling → dept Creative Resource Utilisation (§5, PMO lane) — the dept KPI lands its team owner here; domain views "
    "keep their own slice (FS: Creative Resource Utilisation Rate)",
    "%", "Monthly", "Baseline first: Q1 builds the allocation register per unit; unit PMs supply the reads, the PMO manager "
    "collects at the check-in, the Business Ops lead owns the judgment. FS Q1 Jul reference: A 100% — fully utilised, at "
    "times stretched."),
   ("Business Ops — Shared Teams", "Cross-functional Resource Utilisation — All Units",
    "Of the embedded function bandwidth (Engineering, Product, Pedagogy, DA/DEs, Product Design) allocated into units, the "
    "% actually used on committed work in the cycle — across every sub-department and function. Read the same way: low = "
    "planning gaps · over = scope creep or under-resourcing.",
    "enabling → dept Cross-functional Resource Utilisation (§5, PMO lane) — the dept KPI lands its team owner here",
    "%", "Monthly", "Baseline first: same allocation register; unit PMs supply the reads, the PMO manager collects at the "
    "check-in, the Business Ops lead owns the judgment."),
   ("Agentic Content Platform", "Shared Tool Adoption",
    "% of shipped shared ACP tools (content-generation workflows, MCP servers, production pipelines built for all domains) "
    "that every learning-domain unit is publishing through within a month of shipping. Adopted = used in live production, "
    "not a trial.",
    "enabling → tracker Agentic Production Coverage — adoption is how all units reach the 90 bar",
    "%", "Monthly", "Bar: ALL learning domains within a month of shipping — an unadopted shared tool is shelfware. Owned by "
    "the Business Ops lead (ACP builder hat)."),
   ("PMO", "Check-ins Run",
    "% of scheduled monthly unit check-ins with the HOD held on schedule, with the pre-read circulated a day before. Covers "
    "every sub-department and embedded function on the check-in calendar (~10 units).",
    "hygiene — operating-rhythm guardrail; no org ladder by design",
    "%", "Monthly", "Run by the PMO manager; unit PMs supply the pre-read inputs — orchestration here, the work stays with "
    "the units."),
   ("PMO", "Actions Closed",
    "% of actions logged in a monthly check-in that are closed before that unit's next check-in. The follow-through half of "
    "the cadence — check-ins that close loops, not meetings that merely happen.",
    "hygiene — operating-rhythm guardrail; no org ladder by design",
    "%", "Monthly", "Run by the PMO manager. Deferred companions (spend → outcome map · tracker freshness · finance "
    "turnaround) join after the start set runs a cycle or two."),
  ],
  "asks": [
   ("Execution-management KPI tracking", "Product, Engineering, Product Design & Pedagogy function heads",
    "Own execution KPIs (roadmap predictability, on-time delivery, budget adherence…) for teams embedded with us, tracked "
    "in their home functions — Central consumes the read at the monthly check-in; feeds Shared-Team Deliverables Landed "
    "(§7 ask)."),
   ("Creative delivery-management tracking", "Graphic Design & Video Editing team heads",
    "Delivery-management KPIs for the design & video pipeline (on-time %, asset turnaround TAT, rework rate…) stay with "
    "the creative team heads; domain PMs manage day-to-day utilisation (FS view carries Creative Resource Utilisation) — "
    "§7 ask, reviewed quarterly."),
  ]},
]

def build_team_view(tv):
    tvs = wb.create_sheet(tv["tab"])
    hue  = "FF" + HUES[tv["hue"]]
    band = "FF" + BANDS[tv["hue"]]
    tint = "FF" + TINTS[tv["hue"]]
    tvs.sheet_properties.tabColor = hue
    for col, w in zip("ABCDEFGHIJKLMN", (5, 6, 16, 10, 9, 28, 46, 28, 9, 10, 11, 11, 10, 32)):
        tvs.column_dimensions[col].width = w
    tvs.freeze_panes = "G4"

    tvs.merge_cells("A1:N1")
    c = tvs.cell(row=1, column=1, value=f'{tv["team"]} — Functional Operating View · FY 2026-27')
    c.font = F(13, bold=True); c.fill = PatternFill("solid", start_color=band)
    c.alignment = Alignment(vertical="center"); tvs.row_dimensions[1].height = 24
    tvs.merge_cells("A2:N2")
    c = tvs.cell(row=2, column=1, value=tv["sub"])
    c.font = F(9, italic=True, color="FF555555")
    c.alignment = Alignment(vertical="center", wrap_text=True); tvs.row_dimensions[2].height = 30
    for j, h in enumerate(("S. No", "Sect", "Metric category", "Product", "Cohort", "KPI name", "Description",
                           "Ladders to", "Unit", "Freq", "Budgeted", "Actual", "Variance", "Remarks"), 1):
        c = tvs.cell(row=3, column=j, value=h)
        c.font = F(9, bold=True); c.fill = PatternFill("solid", start_color=band)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = Border(left=thin, right=thin, top=thin, bottom=med)
    tvs.row_dimensions[3].height = 20

    rowp = [4]  # mutable row pointer
    def hdr(txt):
        r = rowp[0]
        tvs.merge_cells(start_row=r, start_column=1, end_row=r, end_column=14)
        c = tvs.cell(row=r, column=1, value=txt)
        c.font = F(10, bold=True, color="FFFFFFFF"); c.fill = PatternFill("solid", start_color=hue)
        c.alignment = Alignment(vertical="center", wrap_text=True)
        for cc in range(1, 15):
            tvs.cell(row=r, column=cc).border = Border(left=thin, right=thin, top=med, bottom=thin)
        tvs.row_dimensions[r].height = 26
        rowp[0] = r + 1

    def body_row(vals, *, fill=None, dlen=0, center_cols=(1, 2, 4, 5, 9, 10, 11, 12, 13), merge_detail=False):
        r = rowp[0]
        if merge_detail:
            tvs.merge_cells(start_row=r, start_column=7, end_row=r, end_column=14)
        for cc in range(1, 15):
            c = tvs.cell(row=r, column=cc)
            if cc in vals: c.value = vals[cc]
            c.font = F(9, bold=(cc == 6))
            if fill: c.fill = PatternFill("solid", start_color=fill)
            c.alignment = Alignment(horizontal="center" if cc in center_cols else "left",
                                    vertical="top", wrap_text=True)
            c.border = Border(left=thin, right=thin, top=thin, bottom=thin)
        tvs.row_dimensions[r].height = min(92, max(30, 6 + 13 * (dlen // 50 + 1)))
        rowp[0] = r + 1
        return r

    hdr("A — Inherited: org-KRA rows this team is on the hook for (live mirror — numbers live on the KPI Tracker tab; edit there)")
    for rm in a_rows(tv["match"], tv["twins"]):
        body_row({1: "T%d" % rm["sno"], 2: "A",
                  3: tref("C", rm["r0"]), 4: tref("D", rm["r0"]), 5: tref("E", rm["cr"]),
                  6: tref("G", rm["r"]), 7: tref("H", rm["r0"]),
                  8: (("inherited — team-sheet twin" if rm["metric"] in tv["twins"] else "inherited — via Functions (col K)")
                      + tv.get("a_notes", {}).get(rm["metric"], "")),
                  9: tref("M", rm["r0"]), 10: tref("N", rm["r0"]), 11: tref("O", rm["r"]),
                  12: tref("P", rm["r"]), 13: tref("Q", rm["r"]), 14: tref("R", rm["r0"])},
                 fill=tint, dlen=rm["dlen"])

    hdr("B — Owned: functional KPIs this team runs (budgets & actuals live here) — Ladders-to key: "
        "direct = an org-KRA number · enabling = a dept §5 KPI · hygiene = guardrail by design")
    for i, (cat, name, desc, ladder, unit, freq, rem) in enumerate(tv["own"], 1):
        prod = "All"
        for tag in ("NIAT + Academy", "NIAT", "Launchpad", "Academy", "Intensive"):
            if name.endswith(f"({tag})"):
                prod, name = tag, name[: -len(tag) - 2].rstrip()
                break
        r = body_row({1: i, 2: "B", 3: cat, 4: prod, 5: "All", 6: name, 7: desc, 8: ladder,
                      9: unit, 10: freq, 14: rem},
                     dlen=max(len(desc), len(ladder)))
        vc = tvs.cell(row=r, column=13)
        vc.value = f'=IF(AND(ISNUMBER(K{r}),ISNUMBER(L{r})),K{r}-L{r},"")'
        vc.font = F(9, bold=True); vc.alignment = Alignment(horizontal="center", vertical="top")

    hdr("C — Asks: what this team needs from counterparties (thin interface contracts — reviewed monthly)")
    for i, (ask, who, detail) in enumerate(tv["asks"], 1):
        body_row({1: i, 2: "C", 3: who, 6: ask, 7: detail}, fill=tint, dlen=0, merge_detail=True)
        tvs.row_dimensions[rowp[0] - 1].height = 40

for tv in TEAM_VIEWS:
    build_team_view(tv)

wb.save(XLSX)

# ---------------------------------------------------------------- html page
TAG = {"CASCADE": "tag-cascade", "SAMPLE": "tag-sample", "CROSS-FUNCTION": "tag-xdept", "ORG": "tag-org"}
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
            'kra_training_sheet.xlsx (6 tabs — incl. team views: CSI &middot; FullStack &amp; CS Core &middot; '
            'Content&ndash;Central)</div>')
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
            '<span class="tag tag-xdept">CROSS-FUNCTION</span> resolved across functions, we route &middot; '
            '<span class="tag tag-sample">SAMPLE</span> illustrative until baselines land &middot; '
            '<span class="tag tag-cascade">CASCADE</span> same KPI feeds two KRAs.</div>')
body.append('  <div class="key-point"><strong>Lanes (col L):</strong> the accountability groupings KPIs report under — '
            'a lane is not a team; its lead answers for the number at review. <strong>Learning Domains</strong> — domain '
            'curriculum, pedagogy &amp; question banks across the 13 domains &middot; <strong>Learning Platform</strong> — '
            'shared study / practice / revision / assessment capabilities across products &middot; <strong>Product Learning '
            'Experience</strong> — product-specific learning experiences plus university delivery &amp; compliance &middot; '
            '<strong>Agentic Content Platform</strong> — AI platforms &amp; automation for curriculum creation and content '
            'ops &middot; <strong>Developer Platform</strong> — IDE, compiler &amp; platform services students code on '
            '&middot; <strong>Shared / PMO</strong> — department-wide programs run from the HOD office. <strong>One line to '
            'keep the axes apart:</strong> Metric category (col C) = <em>what</em> the KPI measures &middot; Lane (col L) = '
            '<em>who is accountable</em> for the number &middot; Functions (col K) = <em>who does the work</em> that moves '
            'it.</div>')
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
    hits = sum(1 for b in TRACKER if "rows" in b and pat in b["functions"])
    if pat == "Content":
        hits -= sum(1 for b in TRACKER if "rows" in b and "Content–Central" in b["functions"])
    counts.append(hits)
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
            'internal operating view. Downloadable editable master: <strong>kra_training_sheet.xlsx</strong> — 6 tabs: KPI '
            'Tracker FY26-27 (training columns in a collapsible group, collapsed by default) &middot; Session Index &middot; '
            'Legend &middot; team views (CSI &middot; FullStack &amp; CS Core &middot; Content&ndash;Central), same color '
            'coding. Variance = Budgeted &minus; Actual (org Head-Abstract convention). Functions vocabulary '
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
