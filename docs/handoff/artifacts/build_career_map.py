#!/usr/bin/env python3
# build_career_map.py — generates career_map.html ("Career Growth Map" artifact 🧗)
# The AI Engineer ladder read against the frozen KPI system: climb band (5 levels +
# PM operating seat, widening metric surface), then one canvas — 21 progression
# areas → the frozen rows that evidence them → the Lead rating math (19 lines →
# 4 pillars → final). Every wire comes from build_role_cards.py (WIRING / PILLARS /
# SURFACE / PM_ROLE, ast-extracted so this stays in lockstep with the shipped
# ladder) resolved against kra_training_sheet.xlsx row names. Unresolvable reads
# fail the build loudly — no silent drops.
import ast, json, re, html as H, openpyxl

XLSX = "kra_training_sheet.xlsx"
OUT  = "career_map.html"

def first_readable(*paths):
    for p in paths:
        try:
            open(p, encoding="utf-8").close()
            return p
        except OSError:
            continue
    raise OSError(f"none readable: {paths}")

ART = "/Users/pavan/Desktop/projects/open_acp/docs/handoff/artifacts"
RC_PATH  = first_readable(f"{ART}/build_role_cards.py", "build_role_cards.py")
SRC_PATH = first_readable(f"{ART}/role_cards_source.json", "role_cards_source.json")

# ---------------- ladder structures, ast-extracted from the shipped builder ----------------
tree = ast.parse(open(RC_PATH, encoding="utf-8").read())
lits, pillars_node = {}, None
for node in ast.walk(tree):
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        nm = node.targets[0].id
        if nm in ("WIRING", "SURFACE", "NEW_TITLE", "PM_ROLE"):
            lits[nm] = ast.literal_eval(node.value)
        elif nm == "PILLARS":
            pillars_node = node.value
WIRING, SURFACE, NEW_TITLE, PM_ROLE = lits["WIRING"], lits["SURFACE"], lits["NEW_TITLE"], lits["PM_ROLE"]
assert len(WIRING) == 21 and len(SURFACE) == 5 and pillars_node is not None

sections = {s["h2"]: s for s in json.load(open(SRC_PATH, encoding="utf-8"))["sections"]}
RT      = sections["Performance Rating Framework (SDE Lead Level)"]["text"]
AREAS_T = sections["21 Progression Areas"]["tables"]
assert len(RT) == 21 and sum(len(t) - 1 for t in AREAS_T) == 21
CALC = RT[20]

def parse_lines(lines):
    out = []
    for ln in lines:
        m = re.match(r"(.+?) \((\d+)%\): (.+)", ln)
        assert m, f"unparsable rating line: {ln!r}"
        out.append((m.group(1), int(m.group(2)), m.group(3)))
    return out

PILLARS = []  # (name, weight, [(subname, subweight, descriptor)], [reads-string|None per subline])
for t in pillars_node.elts:
    name, weight = ast.literal_eval(t.elts[0]), ast.literal_eval(t.elts[1])
    sl = t.elts[2].args[0].slice            # parse_lines(RT[lo:up]) — reuse the shipped slice
    sublines = parse_lines(RT[sl.lower.value:sl.upper.value])
    r = t.elts[3]
    try:
        reads = ast.literal_eval(r)
    except ValueError:                       # [None] * 5
        reads = ast.literal_eval(r.left) * r.right.value
    assert len(reads) == len(sublines)
    PILLARS.append((name, weight, sublines, reads))
assert [w for _, w, _, _ in PILLARS] == [50, 25, 15, 10]
for _, _, subs, _ in PILLARS:
    assert sum(w for _, w, _ in subs) == 100

# per-level progression text per area (Associate / SDE1 / SDE2 / Lead), verbatim
CATS = ["Foundation", "Core Creation and Quality", "Operational Excellence", "Collaboration and Stakeholders"]
AREA_LEVELS = {}
for cat, t in zip(CATS, AREAS_T):
    for r in t[1:]:
        AREA_LEVELS[r[0]] = (r[1], r[2], r[3], r[4])
assert set(AREA_LEVELS) == {a for _, a, _, _ in WIRING}

# ---------------- frozen rows from the tracker workbook ----------------
wb = openpyxl.load_workbook(XLSX, data_only=False)
org = wb["KPI Tracker FY26-27"]
FLAG_RE = re.compile(r"\s*\[(CASCADE|SAMPLE|CROSS-FUNCTION)\]")
kras, org_metrics, cur_kra_key, cur = {}, [], None, None
for r in range(3, org.max_row + 1):
    b = org.cell(r, 2).value
    if b:
        first = str(b).split("\n")[0].strip()
        mk = re.match(r"(KRA \d+)\s*[—-]\s*(.+)", first)
        if mk:
            cur_kra_key = mk.group(1)
            w = re.search(r"(\d+)\s*%", str(b)[len(first):])
            kras.setdefault(cur_kra_key, {"name": mk.group(2).strip(), "weight": (w.group(1) + "%") if w else ""})
    F, G = org.cell(r, 6).value, org.cell(r, 7).value
    if not G:
        cur = None
        continue
    if F:
        name = re.sub(r"\s+", " ", FLAG_RE.sub("", str(F))).strip()
        cur = {"name": name, "kra": cur_kra_key,
               "lane": str(org.cell(r, 12).value or "").strip(),
               "desc": str(org.cell(r, 8).value or "").strip(),
               "unit": str(org.cell(r, 13).value or "").strip(),
               "freq": str(org.cell(r, 14).value or "").strip()}
        org_metrics.append(cur)
assert len(org_metrics) == 19, [m["name"] for m in org_metrics]

ws = wb["FullStack & CS Core View"]
hdr = next(r for r in range(1, 8) if "KPI name" in [str(ws.cell(r, c).value or "") for c in range(1, 16)])
cols = {str(ws.cell(hdr, c).value or ""): c for c in range(1, 16)}
assert "Product" in cols, sorted(cols)
fs_rows = []
for r in range(hdr + 1, ws.max_row + 1):
    name = ws.cell(r, cols["KPI name"]).value
    if not name or str(name).startswith("=") or str(ws.cell(r, cols["Sect"]).value or "").strip() != "B":
        continue
    budg = ws.cell(r, cols["Budgeted"]).value
    fs_rows.append({"name": str(name).strip(),
                    "cat": str(ws.cell(r, cols["Metric category"]).value or "").strip(),
                    "product": str(ws.cell(r, cols["Product"]).value or "").strip(),
                    "desc": str(ws.cell(r, cols["Description"]).value or "").strip(),
                    "unit": str(ws.cell(r, cols["Unit"]).value or "").strip(),
                    "freq": str(ws.cell(r, cols["Freq"]).value or "").strip(),
                    "budget": "" if budg is None else str(budg)})
assert len(fs_rows) == 29, len(fs_rows)

# ---------------- resolve every ladder read to a frozen row ----------------
NORM = lambda s: re.sub(r"[–—]", "-", s or "").casefold().strip()
FS_BY_NAME  = {r["name"]: i for i, r in enumerate(fs_rows)}
ORG_BY_NAME = {m["name"]: i for i, m in enumerate(org_metrics)}
ALIAS = {  # ladder shorthand -> frozen row(s); "Summative + Formative" fans out to both rows
    "Summative + Formative Achievement": [("fs", "Summative Skill Assessment Achievement Rate"),
                                          ("fs", "Formative Skill Assessment Achievement Rate")],
    "Summative + Formative Skill Assessment Achievement": [("fs", "Summative Skill Assessment Achievement Rate"),
                                                           ("fs", "Formative Skill Assessment Achievement Rate")],
    "org KRA 1 SPI Score Bands": [("kra", "KRA 1")],
    "Graded Assessment Achievement Rate (NIAT)": [("fs", "Graded Assessment Achievement Rate")],
    "Weekly Active Users (Launchpad)": [("fs", "Weekly Active Users")],
    "University Curriculum Compliance": [("org", "University Curriculum & Framework Compliance")],
    "Content Issue Recurrence Rate": [("org", "Content Issue Recurrence")],
    "Cost per Learning Hour": [("fs", "Cost per Learning Hour Produced")],
    "Cost per MCQ": [("fs", "Cost per MCQ Generated")],
}
def resolve(key):
    """-> list of node ids (f#, g#, k1)."""
    if key in ALIAS:
        pairs = ALIAS[key]
    elif key in FS_BY_NAME:
        pairs = [("fs", key)]
    elif key in ORG_BY_NAME:
        pairs = [("org", key)]
    else:
        hits = ([("fs", n) for n in FS_BY_NAME if NORM(key) in NORM(n)] +
                [("org", n) for n in ORG_BY_NAME if NORM(key) in NORM(n)])
        assert len(hits) == 1, f"read {key!r} resolved to {hits}"
        pairs = hits
    out = []
    for kind, nm in pairs:
        if kind == "fs":
            out.append(f"f{FS_BY_NAME[nm]}")
        elif kind == "org":
            out.append(f"g{ORG_BY_NAME[nm]}")
        else:
            out.append("k1")
    return out

# evidence edges: area -> row
ev_edges, wired, review = [], [], []
for ai, (cat, area, reads, note) in enumerate(WIRING):
    (wired if reads else review).append(area)
    for key in reads:
        for tid in resolve(key):
            ev_edges.append((f"a{ai}", tid))
assert len(wired) == 14 and len(review) == 7, (wired, review)
assert len(ev_edges) == 32, len(ev_edges)

# rating-read edges: row -> subline
SUBS = []       # (sid, pillar_idx, name, weight, descriptor, reads_keys)
rd_edges = []
si = 0
for pi, (pname, pw, sublines, reads) in enumerate(PILLARS):
    for (sname, sw, sdesc), rstr in zip(sublines, reads):
        keys = [k.strip() for k in rstr.split("·")] if rstr else []
        for key in keys:
            for tid in resolve(key):
                rd_edges.append((tid, f"s{si}"))
        SUBS.append((f"s{si}", pi, sname, sw, sdesc, keys))
        si += 1
assert si == 19 and len(rd_edges) == 24, (si, len(rd_edges))

tr_edges = [(f"s{i}", f"p{pi}") for i, (_, pi, *_ ) in enumerate(SUBS)] + [(f"p{i}", "fin") for i in range(4)]
assert len(tr_edges) == 23

edges = [(s, t, "ev") for s, t in ev_edges] + [(s, t, "rd") for s, t in rd_edges] + [(s, t, "tr") for s, t in tr_edges]

# which rows the ladder touches
used = {t for s, t in ev_edges} | {s for s, _ in rd_edges}
org_used = sorted({int(t[1:]) for t in used if t.startswith("g")})
assert {org_metrics[i]["name"] for i in org_used} == {
    "Content Issue Resolution Efficiency", "Content Issue Recurrence", "Module-Quiz Score Bands",
    "Engagement-Matrix Cell Migration", "University Curriculum & Framework Compliance",
    "Industry Update Adherence", "Agentic Production Coverage"}, [org_metrics[i]["name"] for i in org_used]
unused_fs = [r["name"] for i, r in enumerate(fs_rows) if f"f{i}" not in used]
assert set(unused_fs) == {"Branding Content Assets Delivered", "Cost per Vernacular Content Hour",
                          "Cost per Branding Content Asset", "Platform Runtime Cost per Active Learner",
                          "Roadmap Items Completion"}, unused_fs

# reverse index for tooltips: row -> areas / rating lines that read it
read_by = {}
for ai, (cat, area, reads, note) in enumerate(WIRING):
    for key in reads:
        for tid in resolve(key):
            read_by.setdefault(tid, [[], []])[0].append(area)
for sid, pi, sname, *_ , keys in SUBS:
    for key in keys:
        for tid in resolve(key):
            read_by.setdefault(tid, [[], []])[1].append(sname)

# ---------------- geometry ----------------
X_AREA, W_AREA = 14, 330
X_KPI,  W_KPI  = 470, 360
X_SUB,  W_SUB  = 950, 340
X_PIL,  W_PIL  = 1352, 146
X_FIN,  W_FIN  = 1552, 118
WIDTH = 1684
AH, KH, SH, GAP, CATH = 38, 42, 42, 8, 22
Y0 = 70

nodes = {}  # id -> dict(x, y, w, h, kind, ...)

# middle column first — it is the tallest and anchors vertical centering
labels = []  # (x, y, cls, text)
y = Y0
labels.append((X_KPI, y + 11, "blk", "FS & CS CORE TEAM VIEW — SECTION B (ALL 29 OWNED ROWS)"))
y += 26
cur_cat = None
for i, r in enumerate(fs_rows):
    if r["cat"] != cur_cat:
        cur_cat = r["cat"]
        y += 4
        labels.append((X_KPI, y + 11, "cat", cur_cat.upper()))
        y += CATH
    nodes[f"f{i}"] = {"x": X_KPI, "y": y, "w": W_KPI, "h": KH, "kind": "kpi", "fs": r,
                      "mut": f"f{i}" not in used}
    y += KH + GAP
y += 18
labels.append((X_KPI, y + 11, "blk", "ORG TRACKER — ROWS THE LADDER READS (7 OF 19)"))
y += 26
for i in org_used:
    nodes[f"g{i}"] = {"x": X_KPI, "y": y, "w": W_KPI, "h": KH, "kind": "kpi", "org": org_metrics[i]}
    y += KH + GAP
y += 18
nodes["k1"] = {"x": X_KPI, "y": y, "w": W_KPI, "h": 56, "kind": "kra"}
y += 56
mid_bottom = y
span = mid_bottom - Y0

# left column — 21 areas in 4 groups, vertically centered against the middle
left_h = 21 * (AH + GAP) + 4 * (CATH + 4) + 3 * 10
y = Y0 + (span - left_h) / 2
cur_cat = None
for ai, (cat, area, reads, note) in enumerate(WIRING):
    if cat != cur_cat:
        if cur_cat is not None:
            y += 10
        cur_cat = cat
        labels.append((X_AREA, y + 11, "cat", cat.upper()))
        y += CATH + 4
    nodes[f"a{ai}"] = {"x": X_AREA, "y": y, "w": W_AREA, "h": AH, "kind": "area",
                       "area": area, "cat": cat, "reads": reads, "note": note, "rev": not reads}
    y += AH + GAP

# right column — 19 rating lines in 4 pillar groups, centered likewise
right_h = 19 * (SH + GAP) + 4 * (CATH + 4)
y = Y0 + (span - right_h) / 2
cur_pi = None
group_ys = {}
for sid, pi, sname, sw, sdesc, keys in SUBS:
    if pi != cur_pi:
        cur_pi = pi
        labels.append((X_SUB, y + 11, "cat", PILLARS[pi][0].upper() + f" — {PILLARS[pi][1]}%"))
        y += CATH + 4
    nodes[sid] = {"x": X_SUB, "y": y, "w": W_SUB, "h": SH, "kind": "sub",
                  "pi": pi, "name": sname, "w%": sw, "desc": sdesc, "keys": keys}
    group_ys.setdefault(pi, []).append(y + SH / 2)
    y += SH + GAP
for pi in range(4):
    cy = sum(group_ys[pi]) / len(group_ys[pi])
    nodes[f"p{pi}"] = {"x": X_PIL, "y": cy - 23, "w": W_PIL, "h": 46, "kind": "pil", "pi": pi}
fin_cy = sum(nodes[f"p{i}"]["y"] + 23 for i in range(4)) / 4
nodes["fin"] = {"x": X_FIN, "y": fin_cy - 30, "w": W_FIN, "h": 60, "kind": "fin"}
HEIGHT = int(mid_bottom + 40)

# ---------------- tooltips ----------------
esc = lambda s: H.escape(str(s), quote=True)
def cut(s, n):
    return s if len(s) <= n else s[:n - 1].rstrip() + "…"
LEVEL_SHORT = ["Associate AI Engineer", "AI Engineer 1", "AI Engineer 2", "AI Engineer Lead"]
tips = {}
for nid, n in nodes.items():
    k = n["kind"]
    if k == "area":
        wired_line = (f'wired to {len({t for s, t in ev_edges if s == nid})} frozen row'
                      + ("s" if len({t for s, t in ev_edges if s == nid}) != 1 else "")
                      if n["reads"] else "review-based — no direct row, by design")
        climb = "".join(f'<div class="tsub"><b>{esc(lv)}:</b> {esc(cut(tx, 150))}</div>'
                        for lv, tx in zip(LEVEL_SHORT, AREA_LEVELS[n["area"]]))
        tips[nid] = (f'<b>{esc(n["area"])}</b><div class="tcat">{esc(n["cat"])} · {esc(wired_line)}</div>'
                     f'<div class="tdesc">{esc(n["note"])}</div>'
                     f'<div class="tmeta" style="margin-top:4px"><b>The climb (verbatim, trimmed):</b></div>{climb}'
                     f'<div class="tlad">Full per-level text lives in the AI Engineer Ladder cards.</div>')
    elif k == "kpi" and "fs" in n:
        r = n["fs"]
        prod = f' · Product: {esc(r["product"])}' if r["product"] else ""
        meta = " · ".join(x for x in (r["unit"], r["freq"]) if x) + (f' · budget {esc(r["budget"])}' if r["budget"] else "")
        areas, subs2 = read_by.get(nid, [[], []])
        if areas or subs2:
            reads = ((f'<div class="tmeta"><b>Evidences:</b> {esc(" · ".join(dict.fromkeys(areas)))}</div>' if areas else "")
                     + (f'<div class="tmeta"><b>Read by rating line:</b> {esc(" · ".join(dict.fromkeys(subs2)))}</div>' if subs2 else ""))
        elif r["name"] == "Roadmap Items Completion":
            reads = '<div class="thyg">No ladder read — the PM operating seat runs this row (with the rest of the Team Ops &amp; People block); the Lead answers for it at review.</div>'
        else:
            reads = '<div class="thyg">No ladder read — a team row the career framework doesn\'t cite. Fine if deliberate; red-pen if not.</div>'
        tips[nid] = (f'<b>{esc(r["name"])}</b><div class="tcat">FS &amp; CS Core team view · Section B · {esc(r["cat"])}{prod}</div>'
                     f'<div class="tdesc">{esc(cut(r["desc"], 220))}</div><div class="tmeta">{esc(meta)}</div>{reads}')
    elif k == "kpi":
        m = n["org"]
        areas, subs2 = read_by.get(nid, [[], []])
        reads = ((f'<div class="tmeta"><b>Evidences:</b> {esc(" · ".join(dict.fromkeys(areas)))}</div>' if areas else "")
                 + (f'<div class="tmeta"><b>Read by rating line:</b> {esc(" · ".join(dict.fromkeys(subs2)))}</div>' if subs2 else ""))
        apc = ('<div class="tlad">Mirrored into FS Section A at budget 90 — the team answers for it there.</div>'
               if m["name"] == "Agentic Production Coverage" else "")
        tips[nid] = (f'<b>{esc(m["name"])}</b><div class="tcat">Org tracker · {esc(m["kra"])} — {esc(kras[m["kra"]]["name"])} · Lane: {esc(m["lane"])}</div>'
                     f'<div class="tdesc">{esc(cut(m["desc"], 220))}</div>'
                     f'<div class="tmeta">{esc(" · ".join(x for x in (m["unit"], m["freq"]) if x))}</div>{reads}{apc}')
    elif k == "kra":
        tips[nid] = (f'<b>KRA 1 — {esc(kras["KRA 1"]["name"])}</b><div class="tcat">Org KRA · weight {esc(kras["KRA 1"]["weight"])}</div>'
                     f'<div class="tdesc">Read directly by the rating\'s top Performance line — achievement is judged where the org judges it.</div>')
    elif k == "sub":
        of_final = n["w%"] * PILLARS[n["pi"]][1] / 100
        of_final = f"{of_final:g}"
        reads = (f'<div class="tmeta"><b>Reads:</b> {esc(" · ".join(n["keys"]))}</div>' if n["keys"]
                 else '<div class="thyg">Review-based line — judged in the appraisal conversation, no named row by design.</div>')
        tips[nid] = (f'<b>{esc(n["name"])}</b><div class="tcat">{esc(PILLARS[n["pi"]][0])} · {n["w%"]}% of the pillar = {of_final}% of the final rating</div>'
                     f'<div class="tdesc">{esc(n["desc"])}</div>{reads}')
    elif k == "pil":
        pname, pw, subs3, _ = PILLARS[n["pi"]]
        tips[nid] = (f'<b>{esc(pname)}</b><div class="tcat">{pw}% of the final rating · {len(subs3)} lines</div>'
                     f'<div class="tdesc">Rolls up its lines by their weights; touches the KPI column only through them.</div>')
    elif k == "fin":
        tips[nid] = (f'<b>Final Rating</b><div class="tcat">applies at AI Engineer Lead</div>'
                     f'<div class="tdesc">{esc(CALC)}</div>'
                     f'<div class="tlad">Below Lead the same 21 areas are read at review depth (see the climb band). '
                     f'For the Team Ops &amp; People rows, KPIs cascade Lead → PM: the PM runs them day to day, the Lead answers at review.</div>')

# ---------------- svg ----------------
def trunc(s, w, px=6.35):
    lim = int(w / px)
    return s if len(s) <= lim else s[:lim - 1].rstrip() + "…"

S = [f'<svg id="g" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Career growth map">']
for x, w, t, sub in ((X_AREA, W_AREA, "21 PROGRESSION AREAS", "what growth is made of · dashed = review-based"),
                     (X_KPI, W_KPI, "THE FROZEN ROWS", "where each area shows up as a number"),
                     (X_SUB, W_SUB, "RATING LINES — AI ENGINEER LEAD", "19 lines, weighted inside each pillar"),
                     (X_PIL, W_PIL + W_FIN + 54, "PILLARS → FINAL", "50 / 25 / 15 / 10")):
    S.append(f'<text x="{x}" y="34" class="colh">{esc(t)}</text>')
    if sub:
        S.append(f'<text x="{x}" y="50" class="colsub">{esc(sub)}</text>')

def bez(s, t):
    a, b = nodes[s], nodes[t]
    x1, y1 = a["x"] + a["w"], a["y"] + a["h"] / 2
    x2, y2 = b["x"], b["y"] + b["h"] / 2
    dx = (x2 - x1) * 0.45
    return f"M{x1:.0f},{y1:.0f} C{x1+dx:.0f},{y1:.0f} {x2-dx:.0f},{y2:.0f} {x2:.0f},{y2:.0f}"
for i, (s, t, k) in enumerate(edges):
    col = "#9a9a94" if k == "tr" else "#0D9488"
    dash = ' stroke-dasharray="6 5"' if k == "rd" else ""
    S.append(f'<path id="e{i}" class="edge e-{k}" d="{bez(s,t)}" stroke="{col}"{dash} data-s="{s}" data-t="{t}"/>')

for x, yy, cls, text in labels:
    S.append(f'<text x="{x+2}" y="{yy}" class="{ "blklab" if cls == "blk" else "catlab" }">{esc(text)}</text>')

for nid, n in nodes.items():
    x, yy, w, h, k = n["x"], n["y"], n["w"], n["h"], n["kind"]
    cls = f"node nk-{k}" + (" rev" if n.get("rev") else "") + (" mut" if n.get("mut") else "") + (" fsr" if k == "kpi" and "fs" in n else "")
    S.append(f'<g class="{cls}" id="{nid}" tabindex="0">')
    S.append(f'<rect x="{x:.0f}" y="{yy:.0f}" width="{w}" height="{h}" rx="7"/>')
    if k == "area":
        nsub = (f'wired to {len({t for s2, t in ev_edges if s2 == nid})} frozen rows' if n["reads"] else "review-based — by design")
        if len(n["reads"]) == 1:
            nsub = "wired to 1 frozen row"
        S.append(f'<text x="{x+12}" y="{yy+15}" class="nname">{esc(trunc(n["area"], w-22))}</text>')
        S.append(f'<text x="{x+12}" y="{yy+29}" class="nsub">{esc(nsub)}</text>')
    elif k == "kpi" and "fs" in n:
        r = n["fs"]
        prod = f'{r["product"]} · ' if r["product"] and r["product"] != "All" else ""
        sub = ("no ladder read — team row only" if n.get("mut")
               else prod + " · ".join(x for x in (r["unit"], r["freq"]) if x))
        S.append(f'<text x="{x+12}" y="{yy+16}" class="nname">{esc(trunc(r["name"], w-22))}</text>')
        S.append(f'<text x="{x+12}" y="{yy+31}" class="nsub">{esc(trunc(sub, w-22, 5.4))}</text>')
    elif k == "kpi":
        m = n["org"]
        S.append(f'<text x="{x+12}" y="{yy+16}" class="nname">{esc(trunc(m["name"], w-22))}</text>')
        S.append(f'<text x="{x+12}" y="{yy+31}" class="nsub">{esc(trunc("org tracker · Lane: " + m["lane"], w-22, 5.4))}</text>')
    elif k == "kra":
        S.append(f'<text x="{x+12}" y="{yy+22}" class="kname">KRA 1</text>')
        S.append(f'<text x="{x+12}" y="{yy+39}" class="ksub">{esc(trunc(kras["KRA 1"]["name"], w-20, 5.6))}</text>')
    elif k == "sub":
        S.append(f'<text x="{x+12}" y="{yy+16}" class="nname">{esc(trunc(n["name"], w-22))}</text>')
        wsub = f'{n["w%"]}% of {PILLARS[n["pi"]][0]}' + ("" if n["keys"] else " · review-based")
        S.append(f'<text x="{x+12}" y="{yy+31}" class="nsub">{esc(trunc(wsub, w-22, 5.4))}</text>')
    elif k == "pil":
        pname, pw, subs3, _ = PILLARS[n["pi"]]
        S.append(f'<text x="{x+12}" y="{yy+18}" class="nname">{esc(trunc(pname, w-22))}</text>')
        S.append(f'<text x="{x+12}" y="{yy+33}" class="nsub">{pw}% of final · {len(subs3)} lines</text>')
    elif k == "fin":
        S.append(f'<text x="{x+12}" y="{yy+22}" class="kname">Final Rating</text>')
        S.append(f'<text x="{x+12}" y="{yy+38}" class="ksub">applies at Lead</text>')
        S.append(f'<text x="{x+12}" y="{yy+52}" class="ksub2">cascades Lead → PM</text>')
    S.append("</g>")
S.append("</svg>")
SVG = "\n".join(S)

# ---------------- edge-list table ----------------
def node_name(nid):
    n = nodes[nid]
    return {"area": lambda: "Area · " + n["area"],
            "kpi":  lambda: ("FS Section B · " + n["fs"]["name"]) if "fs" in n else ("Org · " + n["org"]["name"]),
            "kra":  lambda: "KRA 1 — " + kras["KRA 1"]["name"],
            "sub":  lambda: f'Rating line · {n["name"]} ({n["w%"]}%)',
            "pil":  lambda: f'Pillar · {PILLARS[n["pi"]][0]} ({PILLARS[n["pi"]][1]}%)',
            "fin":  lambda: "Final Rating"}[n["kind"]]()
KINDL = {"ev": "is evidenced by", "rd": "is read by rating line", "tr": "rolls into"}
rows_html = "".join(f"<tr><td>{esc(node_name(s))}</td><td>{KINDL[k]}</td><td>{esc(node_name(t))}</td></tr>"
                    for s, t, k in edges)

# ---------------- climb band ----------------
BEAM = [("reads: review evidence", 12), ("answers: your modules' rows", 34),
        ("answers: a domain slice", 58), ("answers: full Section B — 29 rows", 100),
        ("shapes: §5 + org tracker", 100)]
OLD_ORDER = ["Associate SDE", "SDE 1", "SDE 2", "SDE Lead", "SDE 3"]
rungs = []
for i, old in enumerate(OLD_ORDER):
    lab, pct = BEAM[i]
    ext = " ext" if i == 4 else ""
    rungs.append(f'''<div class="rung">
      <div class="eyeb">LEVEL {i+1}</div><h3>{esc(NEW_TITLE[old])}</h3>
      <p>{esc(SURFACE[i])}</p>
      <div class="beam{ext}"><i style="width:{pct}%"></i></div><div class="beamlab">{esc(lab)}</div>
    </div>''')
rungs.append(f'''<div class="rung pm">
      <div class="eyeb">OPERATING SEAT — NOT A RUNG</div><h3>Project Manager</h3>
      <p>Reports to the team's AI Engineer Lead. Runs the 7 Team Ops &amp; People rows day to day — the Lead answers for them at review (KPIs cascade Lead → PM). Progression &amp; rating for this seat: not designed yet.</p>
      <div class="beamlab" style="color:#8a8a84">operates: Team Ops &amp; People block</div>
    </div>''')
BAND = "\n".join(rungs)

review_subs = [f'{n} ({PILLARS[pi][0]})' for _, pi, n, _, _, k2 in SUBS if not k2]

# ---------------- html ----------------
EDGE_JSON = json.dumps([{"s": s, "t": t, "k": k} for s, t, k in edges]).replace("</", "<\\/")
TIP_JSON = json.dumps(tips).replace("</", "<\\/")

html_out = f"""<meta charset="utf-8">
<title>Career Growth Map</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  :root {{ --fs:#0D9488; --ink:#1a1a1a; --sub:#666; --line:#d8d8d3; --bg:#ffffff; }}
  body {{ font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; background:var(--bg); color:var(--ink); padding:36px 20px 60px; line-height:1.5; }}
  .container {{ max-width:1700px; margin:0 auto; }}
  h1 {{ font-size:1.9em; font-weight:700; }}
  .subtitle {{ color:var(--sub); margin:4px 0 18px; max-width:78ch; }}
  .seclab {{ font-size:.74em; font-weight:800; letter-spacing:.09em; color:#8a8a84; margin:18px 0 8px; }}
  .band {{ display:flex; gap:10px; overflow-x:auto; padding-bottom:4px; }}
  .rung {{ flex:1 0 236px; max-width:300px; border:1px solid var(--line); border-radius:10px; padding:12px 14px; background:#fff; }}
  .rung.pm {{ border-style:dashed; background:#fcfcfa; }}
  .rung .eyeb {{ font-size:.66em; letter-spacing:.08em; font-weight:800; color:#8a8a84; }}
  .rung h3 {{ font-size:.95em; margin:2px 0 6px; }}
  .rung p {{ font-size:.76em; color:var(--sub); line-height:1.45; }}
  .beam {{ height:8px; border-radius:4px; background:#eeeeea; margin-top:10px; position:relative; overflow:hidden; }}
  .beam i {{ position:absolute; left:0; top:0; bottom:0; border-radius:4px; background:var(--fs); }}
  .beam.ext i {{ background:linear-gradient(90deg, var(--fs) 72%, #6BB8AE 72%); }}
  .beamlab {{ font-size:.7em; color:var(--fs); font-weight:700; margin-top:5px; }}
  .lg {{ font-size:.78em; color:var(--sub); display:flex; gap:16px; flex-wrap:wrap; align-items:center; margin-bottom:12px; }}
  .lg svg {{ vertical-align:middle; }}
  .wrap {{ overflow-x:auto; border:1px solid #eeeeea; border-radius:10px; background:#fff; }}
  svg#g {{ display:block; }}
  .colh {{ font-size:12.5px; font-weight:800; letter-spacing:.06em; fill:var(--ink); }}
  .colsub {{ font-size:10.5px; fill:var(--sub); }}
  .catlab {{ font-size:9.5px; font-weight:700; letter-spacing:.09em; fill:#8a8a84; }}
  .blklab {{ font-size:10.5px; font-weight:800; letter-spacing:.08em; fill:var(--fs); }}
  .edge {{ fill:none; stroke-width:1.6; opacity:.38; transition:opacity .15s, stroke-width .15s; }}
  .node rect {{ fill:#fff; stroke:var(--line); stroke-width:1.2; transition:opacity .15s; cursor:pointer; }}
  .node text {{ pointer-events:none; }}
  .nk-area rect {{ stroke:#b9b9b2; }}
  .nk-area.rev rect {{ stroke-dasharray:4 3; fill:#fcfcfa; }}
  .nk-kpi.fsr rect {{ stroke:var(--fs); }}
  .nk-kpi rect {{ fill:#fafaf8; }}
  .nk-kpi.mut rect {{ stroke:#e0e0da; fill:#fbfbf9; }}
  .nk-kpi.mut .nname, .nk-kpi.mut .nsub {{ fill:#9a9a94; }}
  .nk-sub rect {{ fill:#fff; }}
  .nk-pil rect {{ fill:#f5f5f2; stroke:#d2d2cc; }}
  .nk-kra rect, .nk-fin rect {{ fill:var(--ink); stroke:var(--ink); }}
  .kname {{ fill:#fff; font-size:13px; font-weight:800; }}
  .ksub {{ fill:#fff; font-size:10.5px; font-weight:600; }}
  .ksub2 {{ fill:#bbb; font-size:9.5px; }}
  .nname {{ font-size:12px; font-weight:600; fill:var(--ink); }}
  .nsub {{ font-size:10px; fill:var(--sub); }}
  svg.sel .edge {{ opacity:.05; }}
  svg.sel .edge.hi {{ opacity:.95; stroke-width:2.4; }}
  svg.sel .node {{ opacity:.16; }}
  svg.sel .node.hi {{ opacity:1; }}
  svg.sel .node.hi rect {{ stroke-width:2; }}
  #tip {{ position:fixed; z-index:9; max-width:400px; background:#fff; border:1px solid var(--ink); border-radius:8px; padding:10px 12px; font-size:.8em; box-shadow:0 6px 24px rgba(0,0,0,.14); display:none; pointer-events:none; }}
  #tip b {{ font-size:1.02em; }}
  .tcat {{ color:var(--sub); font-size:.9em; margin:2px 0 6px; }}
  .tdesc {{ margin-bottom:6px; }}
  .tmeta {{ color:var(--sub); font-size:.92em; }}
  .tsub {{ color:var(--sub); font-size:.92em; margin-top:2px; }}
  .tlad {{ margin-top:6px; padding-top:6px; border-top:1px dashed var(--line); font-style:italic; color:#444; }}
  .thyg {{ margin-top:6px; color:#8a6d00; }}
  details {{ margin-top:22px; font-size:.86em; }}
  summary {{ cursor:pointer; font-weight:600; }}
  details table {{ border-collapse:collapse; margin-top:10px; width:100%; font-size:.95em; }}
  details td {{ border:1px solid var(--line); padding:5px 8px; }}
  .tscroll {{ overflow-x:auto; }}
  .foot {{ margin-top:22px; color:var(--sub); font-size:.8em; max-width:110ch; }}
  .foot p {{ margin-bottom:6px; }}
</style>
<div class="container">
  <h1>Career Growth Map</h1>
  <p class="subtitle">The AI Engineer ladder read against the frozen KPI system. The climb band shows how the metric surface widens level by level; the canvas below wires the 21 progression areas to the named rows that evidence them, and those same rows into the Lead's rating math. Hover or click anything to light up its full path.</p>
  <div class="seclab">THE CLIMB — ONE LADDER, WIDENING METRIC SURFACE ({esc(NEW_TITLE["Associate SDE"])} → {esc(NEW_TITLE["SDE 3"])} – [Domain] Learning Systems)</div>
  <div class="band">{BAND}</div>
  <div class="seclab">THE WIRING — AREAS → FROZEN ROWS → RATING MATH</div>
  <div class="lg">
    <span><svg width="34" height="10"><line x1="0" y1="5" x2="34" y2="5" stroke="#0D9488" stroke-width="2"/></svg> area is evidenced by this row</span>
    <span><svg width="34" height="10"><line x1="0" y1="5" x2="34" y2="5" stroke="#0D9488" stroke-width="2" stroke-dasharray="6 4"/></svg> rating line reads this row</span>
    <span><svg width="34" height="10"><line x1="0" y1="5" x2="34" y2="5" stroke="#9a9a94" stroke-width="2"/></svg> rolls up by weight</span>
    <span><svg width="30" height="14"><rect x="1" y="1" width="28" height="12" rx="4" fill="#fcfcfa" stroke="#999" stroke-dasharray="4 3"/></svg> review-based — no row by design</span>
    <span><svg width="30" height="14"><rect x="1" y="1" width="28" height="12" rx="4" fill="#fbfbf9" stroke="#e0e0da"/></svg> team row with no ladder read</span>
  </div>
  <div class="wrap">{SVG}</div>
  <div id="tip"></div>
  <details><summary>Every connection as a list (for checking)</summary>
    <div class="tscroll"><table><tbody>{rows_html}</tbody></table></div>
  </details>
  <div class="foot">
    <p><b>Review-based areas (dashed, no row by design):</b> {esc(" · ".join(review))}. Each carries its own read — hover for it.</p>
    <p><b>Review-based rating lines:</b> {esc(" · ".join(review_subs))}. Judged in the appraisal conversation, not by a row.</p>
    <p><b>Team rows the ladder never cites (muted):</b> {esc(" · ".join(n for n in unused_fs if n != "Roadmap Items Completion"))} — plus <b>Roadmap Items Completion</b>, which the PM operating seat runs. Fine if deliberate; red-pen anything you want wired.</p>
    <p><b>The rating math applies at AI Engineer Lead</b> and cascades Lead → PM for the Team Ops &amp; People rows. Below Lead, the same 21 areas are read at review depth per the climb band. Pilot team: FullStack &amp; CS Core; CSI and Content–Central cards are queued separately. Comp bands deliberately live in the AI Engineer Ladder artifact, not here.</p>
    <p>Generated from build_role_cards.py (WIRING · PILLARS · SURFACE · PM_ROLE), role_cards_source.json and kra_training_sheet.xlsx · 22 Aug 2026.</p>
  </div>
</div>
<script>
const EDGES = {EDGE_JSON};
const TIPS = {TIP_JSON};
const svg = document.getElementById('g'), tip = document.getElementById('tip');
const down = {{}}, up = {{}};
EDGES.forEach((e, i) => {{ (down[e.s] = down[e.s] || []).push([e.t, i]); (up[e.t] = up[e.t] || []).push([e.s, i]); }});
function reach(id) {{
  const ns = new Set([id]), es = new Set();
  const walk = (start, adj) => {{ const q = [start], seen = new Set([start]);
    while (q.length) {{ const c = q.pop(); (adj[c] || []).forEach(([n, i]) => {{ es.add(i); ns.add(n); if (!seen.has(n)) {{ seen.add(n); q.push(n); }} }}); }} }};
  walk(id, down); walk(id, up);
  return [ns, es];
}}
let pinned = null;
function light(id) {{
  svg.classList.add('sel');
  svg.querySelectorAll('.hi').forEach(el => el.classList.remove('hi'));
  const [ns, es] = reach(id);
  ns.forEach(n => {{ const el = document.getElementById(n); if (el) el.classList.add('hi'); }});
  es.forEach(i => document.getElementById('e' + i).classList.add('hi'));
}}
function clearLight() {{ if (pinned) return; svg.classList.remove('sel'); svg.querySelectorAll('.hi').forEach(el => el.classList.remove('hi')); }}
svg.querySelectorAll('.node').forEach(g => {{
  g.addEventListener('mouseenter', () => {{ if (!pinned) light(g.id); showTip(g.id); }});
  g.addEventListener('mouseleave', () => {{ clearLight(); tip.style.display = 'none'; }});
  g.addEventListener('click', ev => {{ ev.stopPropagation(); pinned = (pinned === g.id) ? null : g.id; if (pinned) light(g.id); else clearLight(); }});
  g.addEventListener('focus', () => {{ if (!pinned) light(g.id); showTip(g.id, true); }});
  g.addEventListener('blur', () => {{ clearLight(); tip.style.display = 'none'; }});
}});
document.body.addEventListener('click', () => {{ pinned = null; svg.classList.remove('sel'); svg.querySelectorAll('.hi').forEach(el => el.classList.remove('hi')); }});
function showTip(id, focusMode) {{
  const h = TIPS[id]; if (!h) {{ tip.style.display = 'none'; return; }}
  tip.innerHTML = h; tip.style.display = 'block';
  if (focusMode) {{ const r = document.getElementById(id).getBoundingClientRect(); place(r.right, r.top); }}
}}
function place(x, y) {{
  const pad = 14, w = tip.offsetWidth, h = tip.offsetHeight;
  let L = x + pad, T = y + pad;
  if (L + w > innerWidth - 8) L = x - w - pad;
  if (T + h > innerHeight - 8) T = Math.max(8, innerHeight - h - 8);
  tip.style.left = Math.max(8, L) + 'px'; tip.style.top = T + 'px';
}}
svg.addEventListener('mousemove', ev => {{ if (tip.style.display === 'block') place(ev.clientX, ev.clientY); }});
</script>
"""
open(OUT, "w", encoding="utf-8").write(html_out)

print(f"OK {OUT}: {len(html_out):,} chars · nodes: {len(nodes)} "
      f"(21 areas / {len(fs_rows)} FS / {len(org_used)} org / 1 KRA / 19 lines / 4 pillars / 1 final) · "
      f"edges: {len(edges)} (ev {len(ev_edges)} · rd {len(rd_edges)} · tr {len(tr_edges)}) · "
      f"canvas {WIDTH}×{HEIGHT} · wired {len(wired)}/review {len(review)} · muted FS {len(unused_fs)}")
assert len(nodes) == 21 + 29 + 7 + 1 + 19 + 4 + 1, len(nodes)
assert html_out.count('class="edge') == len(edges)
assert ">None<" not in html_out and "UNMAPPED" not in html_out
