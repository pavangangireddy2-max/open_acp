# Content OS — one site, four altitudes. Level 1 (the HOD one-pager) is embedded
# in full; Levels 2–4 are reference sections that LINK to the standalone artifacts
# (KPI tracker, KPI Flow Map, AI Engineer Ladder, Career Growth Map) instead of
# re-rendering their content — directive 2026-08-26: from the second section,
# reference the URLs only, so the site stays lean and a child-artifact republish
# no longer forces a site rebuild (only xlsx content changes do — both masters
# stay base64-embedded and offered through the viewer's `downloads` runtime
# capability; the artifact already stores capabilities={downloads: true}, and a
# republish OMITS the capabilities field to carry it forward). Download buttons
# ship hidden and unhide only where the capability resolves — local preview stays
# buttonless.
import base64
import json
import re

ART = "/Users/pavan/Desktop/projects/open_acp/docs/handoff/artifacts/"
try:  # repo may be unreachable (e.g. macOS folder access revoked) — fall back to cwd copies
    open(ART + "hod_kpi_onepager.html", encoding="utf-8").close()
except OSError:
    ART = ""

def load_artifact(fname):
    h = open(ART + fname, encoding="utf-8").read()
    css = re.search(r"<style[^>]*>(.*?)</style>", h, re.S).group(1)
    after = h.split("</style>", 1)[1]
    scripts = re.findall(r"<script[^>]*>.*?</script>", after, re.S)
    body = re.sub(r"<script[^>]*>.*?</script>", "", after, flags=re.S).strip()
    assert "<title>" not in body and "<style" not in body
    return css, body, scripts

FAMILY_BODY = ("font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; "
               "background: #ffffff; padding: 40px 20px; color: #1a1a1a; line-height: 1.5;")

def scope(css, sel):
    m = re.search(r"body\s*\{([^}]*)\}", css)
    assert m and " ".join(m.group(1).split()) == FAMILY_BODY, f"unexpected body in {sel}"
    assert "html" not in re.findall(r"(?:^|\})\s*([a-z]+)\s*\{", css)
    css = css.replace(m.group(0), "")
    return f"{sel} {{\n{css}\n}}"

op_css, op_body, op_scripts = load_artifact("hod_kpi_onepager.html")
assert not op_scripts

URLS = {
    "onepager":  "https://claude.ai/code/artifact/cd52be82-3fd5-4264-a7aa-5b4e5e132ed9",
    "tracker":   "https://claude.ai/code/artifact/44869dfd-506f-4f4c-9d2b-0581b8e065d1",
    "kpimap":    "https://claude.ai/code/artifact/81cb774c-3cc4-4715-9f2b-b1fafdb72c4a",
    "ladder":    "https://claude.ai/code/artifact/dc3ab90d-c4a4-448d-bdb5-fb43a9235734",
    "careermap": "https://claude.ai/code/artifact/a051587e-381c-4712-a501-9cfceaf75756",
}

# ---- downloadable masters: base64-embedded, saved via the viewer's
# ---- `downloads` capability. Buttons ship hidden; the script unhides them
# ---- only when claude.use("downloads") resolves (null → affordance absent).
XLSX_B64 = {f: base64.b64encode(open(ART + f, "rb").read()).decode("ascii")
            for f in ("kra_training_sheet.xlsx", "role_cards.xlsx")}

def dlbtn(name):
    return f'<button class="dlbtn" type="button" data-file="{name}" hidden>⬇ {name}</button>'

DL_SCRIPT = """<script>
(async () => {
  const XLSX = """ + json.dumps(XLSX_B64) + """;
  const dl = (window.claude && window.claude.use) ? await window.claude.use("downloads") : null;
  if (!dl) {                     // this view can't save files — say so instead of hiding silently
    document.querySelectorAll(".dlnote").forEach(n => { n.hidden = false; });
    return;
  }
  document.querySelectorAll(".dlwrap").forEach(w => { w.hidden = false; });
  document.querySelectorAll(".dlbtn").forEach(b => {
    b.hidden = false;
    b.addEventListener("click", async () => {
      const name = b.dataset.file, label = b.textContent;
      b.disabled = true;
      try {
        await dl.save({ filename: name, data: Uint8Array.from(atob(XLSX[name]), c => c.charCodeAt(0)) });
        b.textContent = "saved \\u2713";
      } catch (e) {
        const code = e && e.code;
        b.textContent = code === "declined" ? label
          : "couldn't save" + (code ? " (" + code + ")" : "") + " \\u2014 try again";
      }
      setTimeout(() => { b.textContent = label; b.disabled = false; }, 2600);
    });
  });
})();
</script>"""

# ---- site chrome -----------------------------------------------------------
SITE_CSS = """  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #ffffff; color: #1a1a1a; line-height: 1.5; }
  #topnav { position: sticky; top: 0; z-index: 60; background: #ffffff; border-bottom: 2px solid #000;
    display: flex; align-items: center; gap: 18px; padding: 10px 20px; flex-wrap: wrap; }
  #topnav .brand { font-weight: 800; letter-spacing: .02em; }
  #topnav a { color: #1a1a1a; text-decoration: none; font-size: .9em; padding: 2px 2px; border-bottom: 2px solid transparent; }
  #topnav a:hover, #topnav a:focus-visible { border-bottom-color: #000; outline: none; }
  #topnav .lvl-no { color: #666; font-variant-numeric: tabular-nums; margin-right: 3px; }
  .site-section { scroll-margin-top: 58px; }
  .pad { padding: 40px 20px; }
  .hero { max-width: 1180px; margin: 0 auto; }
  .hero h1 { font-size: 2.4em; font-weight: 800; margin: 18px 0 10px; }
  .hero .tag { color: #666; font-size: 1.02em; max-width: 74ch; }
  .flow { max-width: 880px; margin: 34px auto 8px; }
  .fcard { display: block; color: inherit; text-decoration: none; border: 1px solid #ccc; border-radius: 5px;
    padding: 14px 16px; display: grid; grid-template-columns: 138px 1fr; gap: 14px; background: #fff; }
  .fcard:hover, .fcard:focus-visible { border-color: #000; outline: none; }
  .fcard .lv { font-weight: 800; font-size: .84em; letter-spacing: .06em; text-transform: uppercase; }
  .fcard .lv .n { display: block; font-size: 2em; line-height: 1.1; }
  .fcard .what { font-size: .92em; }
  .fcard .what b { display: block; margin-bottom: 2px; font-size: 1.05em; }
  .fcard .meta { color: #666; font-size: .88em; margin-top: 4px; }
  .conn { display: flex; justify-content: space-between; align-items: center; padding: 6px 18px; font-size: .82em; }
  .conn .down { color: #004085; }
  .conn .up { color: #0e6e5c; }
  .legendline { text-align: center; color: #666; font-size: .85em; margin-top: 14px; }
  .legendline .down { color: #004085; } .legendline .up { color: #0e6e5c; }
  .band { background: #000; color: #fff; padding: 26px 20px; }
  .band .in { max-width: 1180px; margin: 0 auto; display: flex; flex-wrap: wrap; gap: 8px 22px; align-items: baseline; }
  .band .lv { font-size: .8em; letter-spacing: .12em; text-transform: uppercase; color: #bbb; }
  .band .nm { font-size: 1.35em; font-weight: 800; }
  .band .desc { color: #ddd; font-size: .92em; flex-basis: 100%; max-width: 90ch; }
  .band .links { margin-left: auto; display: flex; gap: 10px; }
  .band a { color: #fff; font-size: .82em; text-decoration: none; border: 1px solid #666; border-radius: 3px; padding: 2px 9px; white-space: nowrap; }
  .band a:hover, .band a:focus-visible { border-color: #fff; outline: none; }
  .band .chipfile { color: #bbb; font-size: .82em; border: 1px dashed #555; border-radius: 3px; padding: 2px 9px; white-space: nowrap; }
  .refsec { padding: 34px 20px 46px; }
  .refin { max-width: 1180px; margin: 0 auto; }
  .reflead { color: #444; font-size: .95em; max-width: 90ch; margin-bottom: 18px; }
  .refs { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 12px; max-width: 980px; }
  .refcard { display: grid; grid-template-columns: 44px 1fr auto; gap: 12px; align-items: center;
    border: 1px solid #ccc; border-radius: 5px; padding: 14px 16px; color: inherit; text-decoration: none; background: #fff; }
  .refcard:hover, .refcard:focus-visible { border-color: #000; outline: none; }
  .refcard .re { font-size: 1.7em; line-height: 1; }
  .refcard .rt { font-size: .9em; color: #444; }
  .refcard .rt b { display: block; font-size: 1.06em; color: #1a1a1a; margin-bottom: 2px; }
  .refcard .ro { color: #004085; font-size: .82em; white-space: nowrap; }
  .refnote { color: #666; font-size: .85em; margin-top: 14px; max-width: 90ch; }
  footer { border-top: 2px solid #000; margin-top: 20px; padding: 30px 20px 46px; }
  footer .in { max-width: 1180px; margin: 0 auto; font-size: .88em; color: #444; }
  footer h3 { font-size: 1em; margin-bottom: 8px; }
  footer ul { list-style: none; }
  footer li { margin: 3px 0; }
  footer .mono { font-family: ui-monospace, 'SF Mono', Menlo, monospace; font-size: .92em; }
  footer a { color: #004085; }
  .dlbtn { font: inherit; font-size: .82em; cursor: pointer; white-space: nowrap;
    border: 1px solid #0e6e5c; border-radius: 3px; background: #0e6e5c; color: #fff; padding: 2px 9px; }
  .dlbtn:hover, .dlbtn:focus-visible { background: #0b574a; border-color: #0b574a; outline: none; }
  .dlbtn[disabled] { opacity: .65; cursor: default; }
  @media (max-width: 700px) { .fcard { grid-template-columns: 1fr; gap: 6px; } }"""

LEVELS = [
    ("org", "1", "Organization", "🎯 HOD one-pager",
     "What the org holds this department to — the KRAs, and the department KPI baseline that answers them.",
     "Read by: Founders &middot; HOD. The contract everything below serves.",
     URLS["onepager"], None),
    ("dept", "2", "Department", "🧭 KPI tracker",
     "The 28 rows the department runs on — metric category says <em>what</em>, lane says <em>who answers</em>, cadence says <em>when</em>.",
     "Read by: HOD &middot; lane leads &middot; PMs. Master: kra_training_sheet.xlsx.",
     URLS["tracker"], "kra_training_sheet.xlsx"),
    ("team", "3", "Team", "Team scorecards",
     "One team's slice: Section A inherited from the tracker &middot; Section B owned &middot; Section C asks of other teams. Pilot: FullStack &amp; CS Core.",
     "Read by: team leads &middot; SMEs. Views live as tabs in the tracker master xlsx.",
     None, "kra_training_sheet.xlsx"),
    ("ind", "4", "Individual", "🪜 AI Engineer Ladder",
     "An internship rung plus four employee levels, the team's Project Manager card, stay bars, 21 progression areas, and the rating rubric — every area wired to the same KPI rows the levels above run on.",
     "Read by: every engineer &middot; their manager. Master: role_cards.xlsx.",
     URLS["ladder"], "role_cards.xlsx"),
]

def band(key, no, name, art, desc, meta, url, master):
    links = []
    if url:
        links.append(f'<a href="{url}" target="_blank" rel="noopener">standalone artifact ↗</a>')
    if master:
        links.append(f'<span class="chipfile">master: {master}</span>')
        links.append(dlbtn(master))
    return (f'<div class="band" id="{key}-band"><div class="in">'
            f'<span class="lv">Level {no} · {name}</span><span class="nm">{art}</span>'
            f'<span class="links">{"".join(links)}</span>'
            f'<span class="desc">{desc}</span></div></div>')

def refcard(emoji, name, url, sub):
    return (f'<a class="refcard" href="{url}" target="_blank" rel="noopener">'
            f'<span class="re">{emoji}</span><span class="rt"><b>{name}</b>{sub}</span>'
            f'<span class="ro">open ↗</span></a>')

def refsection(key, lead, cards, note):
    return (f'<div class="site-section refsec" id="{key}"><div class="refin">'
            f'<div class="reflead">{lead}</div>'
            f'<div class="refs">{"".join(cards)}</div>'
            f'<div class="refnote">{note}</div>'
            f'</div></div>')

# ---- Levels 2–4: reference sections (URLs only — content lives in the artifacts)
DEPT_SEC = refsection("dept",
    "Not re-rendered here — the department layer lives in its own artifacts, updated in place. "
    "The tracker is the operating sheet; the flow map draws how every row connects.",
    [refcard("🧭", "KPI tracker", URLS["tracker"],
             "The 28 department rows — metric category, lane, cadence, budgets — plus the legend that "
             "decodes them."),
     refcard("🕸️", "KPI Flow Map", URLS["kpimap"],
             "Every KPI drawn as a node — team rows ladder into department rows into org KRAs.")],
    "The live grid with budget / actual / variance columns is the master xlsx — "
    "<span class=\"mono\">kra_training_sheet.xlsx</span>, download from the band above or the footer.")

TEAM_SEC = refsection("team",
    "A team view has three sections: <strong>A — inherited</strong> from the tracker (the rows this team "
    "works on; the number answers at department level) · <strong>B — owned</strong> (the team's functional "
    "KPIs, each naming the row it ladders to) · <strong>C — asks</strong> of other teams, named, so "
    "dependencies are contracts instead of surprises. Every view carries Product + Cohort columns.",
    [refcard("🕸️", "KPI Flow Map", URLS["kpimap"],
             "The same map, read from the team end — where each owned row goes when it ladders up.")],
    "The team views themselves are tabs in <span class=\"mono\">kra_training_sheet.xlsx</span> — "
    "FullStack &amp; CS Core (the pilot every domain team copies) · CSI · Content&ndash;Central. "
    "Download from the band above or the footer.")

IND_SEC = refsection("ind",
    "Careers wire to the same rows the levels above run on — the ladder carries the levels, stay bars, "
    "progression areas and the rating rubric; the growth map draws it all as one picture.",
    [refcard("🪜", "AI Engineer Ladder", URLS["ladder"],
             "Five levels with stay bars, the A1&ndash;A4 agent scale, 21 progression areas, the rating "
             "rubric and the Project Manager card."),
     refcard("🧗", "Career Growth Map", URLS["careermap"],
             "The ladder as one drawn map — rungs, progression areas and the evidence wires between them.")],
    "Editable master: <span class=\"mono\">role_cards.xlsx</span> (8 tabs) — download from the band above "
    "or the footer. Comp bands are deliberately kept off this site.")

NAV = ('<nav id="topnav"><span class="brand">Content OS</span>'
       '<a href="#map">The map</a>'
       + "".join(f'<a href="#{k}"><span class="lvl-no">{n}</span>{nm}</a>'
                 for k, n, nm, *_ in LEVELS)
       + '</nav>')

HERO = ['<div class="pad site-section" id="map"><div class="hero">']
HERO.append('<h1>Content OS</h1>')
HERO.append('<div class="tag">The Content &amp; Curriculum department, end to end, on one page. Four altitudes: '
            'the organization sets the targets, the department runs the tracker, teams own their scorecards, and '
            'individual careers are wired to the very same rows. <strong>Targets cascade down; numbers ladder back '
            'up the same wires.</strong> Scroll, or jump to your altitude.</div>')
HERO.append('<div class="flow">')
for i, (key, no, name, art, desc, meta, url, master) in enumerate(LEVELS):
    if i:
        HERO.append('<div class="conn"><span class="down">▼ targets cascade</span>'
                    '<span class="up">numbers ladder up ▲</span></div>')
    HERO.append(f'<a class="fcard" href="#{key}"><span class="lv">Level<span class="n">{no}</span>{name}</span>'
                f'<span class="what"><b>{art}</b>{desc}<div class="meta">{meta}</div></span></a>')
HERO.append('</div>')
HERO.append('<div class="legendline"><span class="down">▼ cascade</span> = budgets and targets set at the level '
            'above &nbsp;·&nbsp; <span class="up">▲ ladder up</span> = every lower row names the higher row it '
            'moves (&ldquo;ladders to&rdquo;)</div>')
HERO.append('</div></div>')

FOOTER = f"""<footer><div class="in">
<h3>Behind this site</h3>
<ul>
<li>Editable masters: <span class="mono">kra_training_sheet.xlsx</span> (tracker + legend + CSI, FullStack &amp; CS Core and Content&ndash;Central team views) · <span class="mono">role_cards.xlsx</span> (ladder, 8 tabs)<span class="dlwrap" hidden> — download: {dlbtn("kra_training_sheet.xlsx")} {dlbtn("role_cards.xlsx")}</span><span class="dlnote" hidden> — <em>this view can&rsquo;t save files (the viewer didn&rsquo;t grant the file-save capability), so the download buttons are hidden; the same two sheets are attached in the Claude chat and live in the repo</em></span> — in <span class="mono">docs/handoff/artifacts/</span> with the builders and CHANGELOG.</li>
<li>Standalone artifacts, each updated in place (Level 1 is embedded above; Levels 2&ndash;4 link out rather than re-rendering): <a href="{URLS["onepager"]}" target="_blank" rel="noopener">HOD one-pager</a> · <a href="{URLS["tracker"]}" target="_blank" rel="noopener">KPI tracker</a> · <a href="{URLS["kpimap"]}" target="_blank" rel="noopener">KPI Flow Map</a> · <a href="{URLS["ladder"]}" target="_blank" rel="noopener">AI Engineer Ladder</a> · <a href="{URLS["careermap"]}" target="_blank" rel="noopener">Career Growth Map</a>.</li>
<li>Each artifact link opens subject to that artifact's own sharing settings.</li>
<li>Comp bands are deliberately kept off this site — they live in the standalone ladder artifact and <span class="mono">role_cards.xlsx</span>.</li>
</ul>
</div></footer>"""

# ---- wide tables scroll in their own container (page never h-scrolls) -------
def wrap_tables(body):
    tags = re.findall(r"</?table", body)
    assert tags and len(tags) % 2 == 0
    assert all(t == ("<table" if i % 2 == 0 else "</table") for i, t in enumerate(tags))
    body = body.replace("<table", '<div class="tscroll"><table')
    return body.replace("</table>", "</table></div>")

for _c in (op_css, SITE_CSS, op_body):
    assert "tscroll" not in _c
op_body = wrap_tables(op_body)

page = []
page.append("<title>Content OS</title>")
page.append("<style>")
page.append(SITE_CSS)
page.append(scope(op_css, "#org"))
page.append("#org { padding: 40px 20px; }")
page.append(".tscroll { overflow-x: auto; }")
page.append("</style>")
page.append(NAV)
page.extend(HERO)
page.append(band(*LEVELS[0]))
page.append(f'<div class="site-section" id="org">\n{op_body}\n</div>')
page.append(band(*LEVELS[1]))
page.append(DEPT_SEC)
page.append(band(*LEVELS[2]))
page.append(TEAM_SEC)
page.append(band(*LEVELS[3]))
page.append(IND_SEC)
page.append(FOOTER)
page.append(DL_SCRIPT)

out = "\n".join(page) + "\n"
assert out.count('class="dlbtn"') == 5          # dept + team + ind bands, footer ×2
assert out.count('class="dlnote"') == 1         # capability-absent fallback, footer only
assert out.count('class="refcard"') == 5        # tracker, kpimap ×2, ladder, careermap
for u in URLS.values():
    assert out.count(u) >= 2 or u == URLS["careermap"], u   # band/card + footer
open("content_os.html", "w", encoding="utf-8").write(out)
print("chars:", len(out), "| braces:", out.count("{") == out.count("}"),
    "| sections:", [k for k, *_ in LEVELS],
    "| refcards:", out.count('class="refcard"'),
    "| dlbtns:", out.count('class="dlbtn"'),
    "| b64 chars:", {k: len(v) for k, v in XLSX_B64.items()})
