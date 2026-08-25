# AI Engineer Ladder — career framework v3 for content-department domain teams.
# Source: knowledge/raw/corpora/remixed-0bb5468a.html ("SDE Learning Systems Career
# Framework", March 2026). v2 renamed titles to Pavan's "AI Engineer – [Domain]
# Learning Systems" pattern and wired every progression area + rating line to named
# KPI rows. v3 (Aug 2026, talk-first approved): Associate = 6-month internship that
# manages agents from day one; AI Engineer 1 + 2 merged into one AI Engineer band;
# Senior AI Engineer added (the 2× force-multiplier bar); promotion gates + stay
# bars + the A1–A4 Agent Scope scale; Learning Systems Design elevated to 4 reads;
# two matrix rows (▲) rewritten agent-first. Everything else stays verbatim from
# source; comp for the changed rungs is parked with HR — no invented numbers.
# Outputs: role_cards.xlsx (editable master, 8 tabs) + role_cards.html (artifact).
import json, re, html as H
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

SRC = "/Users/pavan/Desktop/projects/open_acp/knowledge/raw/corpora/remixed-0bb5468a.html"
CACHE = "comp_boxes_cache.json"  # comp boxes only — refreshed whenever SRC is readable
try:
    src = open(SRC, encoding="utf-8").read()
except OSError:  # raw source is untracked / folder access unavailable — use the cache
    src = None

def clean(x):
    x = re.sub(r"<br\s*/?>", "\n", x)
    x = re.sub(r"<[^>]+>", "", x)
    return H.unescape(x).replace(" ", " ").strip()

# ---------------------------------------------------------------- parse source
if src is not None:
    comp_boxes = [(clean(a), clean(b), clean(c)) for a, b, c in re.findall(
        r'<div class="comp-box">\s*<div class="role-level">(.*?)</div>\s*'
        r'<div class="comp-range">(.*?)</div>\s*<div class="note">(.*?)</div>', src, re.S)]
    json.dump([list(b) for b in comp_boxes],
              open(CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
else:
    comp_boxes = [tuple(b) for b in json.load(open(CACHE, encoding="utf-8"))]
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

AREA_OVERRIDES = {  # v3 (▲): the two agent-first matrix rewrites — Intern / AI Engineer / Senior / Lead
    "Production Systems": (
        "Manages and improves the agents they run: accuracy, retrieval quality, cost metrics held inside budget (A1–A2).",
        "Builds new content agents end-to-end — at least 2–3 built and adopted, impact visible in the metrics (A3).",
        "Orchestrates systems of agents carrying production: multi-agent workflows, escalation design, agents other people run (A4).",
        "Runs the team's agent fleet through people: fleet health, standards, and the coverage number answered for at review."),
    "Learning Systems Design": (
        "Sees how learning is measured up close: item stats, quiz score bands, eval outcomes for the modules they support.",
        "Instruments their own modules: formative and summative signals watched, weak items found and fixed, learning deltas shown.",
        "Invents new ways to teach that take advantage of agentic AI — and applies rigorous measurement to prove users are "
        "developing new skills and retaining them. Raises the EEC / DCD asks from the SME seat.",
        "Makes invention repeatable: eval environments and capability delivery answered for, measurement standards set for the team."),
}
AREAS = [(cat, area) + AREA_OVERRIDES.get(area, tuple(rest)) for cat, area, *rest in AREAS]

# Source descriptors occasionally name the old titles inline ("mentoring from SDE 1+").
# The ladder carries no lineage language, so those are retitled in place too.
INLINE_RETITLE = [("SDE 1+", "AI Engineers and above"), ("Associate SDE", "Associate AI Engineer"),
                  ("SDE Lead", "AI Engineer Lead"), ("SDE 3", "AI Engineer 3"),
                  ("SDE 2", "Senior AI Engineer"), ("SDE 1", "AI Engineer")]

def retitle_text(s):
    for old, new in INLINE_RETITLE:
        s = s.replace(old, new)
    return s

AREAS = [(cat, area) + tuple(retitle_text(c) for c in cells) for cat, area, *cells in AREAS]

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
    ("Develop the Best", 15, parse_lines(RT[10:15]), [
        "Power Performers Created",
        None,
        "Hires Made · Cost per Hire",
        "Team Retention Rate",
        None]),
    ("Culture and Values", 10, parse_lines(RT[15:20]), [None] * 5),
]
CALC = RT[20]

# ------------------------------------------------------------ v2/v3 additions
NEW_TITLE = {"Associate SDE": "Associate AI Engineer", "SDE 1": "AI Engineer",
             "SDE 2": "Senior AI Engineer", "SDE Lead": "AI Engineer Lead", "SDE 3": "AI Engineer 3"}

def retitle_example(note):
    return re.sub(r'(Associate SDE|SDE Lead|SDE [123]), Learning Systems - ([^"]+)',
                  lambda m: f"{NEW_TITLE[m.group(1)]} – {m.group(2)} Learning Systems", note)

LEVELS = []  # (new_title_pattern, old_title, comp, v3_role, src_note, surface)
SURFACE = [
    "Contributes on sample surfaces along the internship ramp — no rows answered for; growth is read through ramp evidence (A1→A2 on the Agent Scope scale).",
    "Answers for the Section B velocity + quality rows of the modules they own (their content hours, pieces, issue-recurrence share) — a topic surface of ≈ 100 topics at FullStack / GenAI complexity, refreshed every 6 months, with 2–3 content agents built and adopted (A3).",
    "Answers for a domain slice ≈ 2× an AI Engineer's complexity-weighted topic surface — by depth, breadth, or leverage (A4 agent systems); first Section C asks raised in their name.",
    "Answers for the team's full Section B at review and supports the Section A lane numbers; span ~5–8 members; the rating framework below applies as written.",
    "Shapes org-tracker rows and cross-domain standards; portfolio spans teams — reads through §5 department KPIs and org KRAs, not one team view.",
]
V3_COMP = {  # comp overrides for the changed rungs — numbers parked with HR (talk-first, Aug 2026).
             # Format is "band | tenure": the site keeps only the right side of the pipe.
    0: "Internship stipend — set by HR | 6-month internship",
    1: "9–24L, band under HR review (the full IC span) | ≥1 year in role before Senior eligibility",
    2: "Band under HR review — new rung | reached through the 2× gate below",
}
V3_ROLE = [  # v3 card bodies (the "what you manage" identity); source scope notes stay in the xlsx.
    "6-month internship — manages agents under supervision from day one: runs existing pipelines, reviews outputs, "
    "tunes prompts, handles escalations (A1), then shows measurable improvement on an agent's numbers (A2). Produces "
    "representative content items manually during the ramp — the domain floor. Converts through the gate below.",
    "Manages agents. Owns modules end-to-end and builds new content agents — 2–3 built and adopted by year-end, "
    "impact visible in the metrics (A3). One band, covering the full individual-contributor span before Senior.",
    "Manages agent systems and mentors humans — the force-multiplier rung. Holds ≈2× an AI Engineer's "
    "complexity-weighted surface by depth, breadth, or leverage; orchestrating systems of agents (A4) is the "
    "leverage route. Invents new ways to teach with agentic AI and proves them with rigorous measurement.",
    "Manages humans who manage agents. Runs the team: full Section B answered for at review; people outcomes — "
    "ratings, retention, growth, hiring — define the title. Span ~5–8 members (number with HR).",
    None,  # AI Engineer 3 — unchanged rung: the card shows the source scope, examples retitled
]
for i, ((title, comp, note), surf) in enumerate(zip(comp_boxes, SURFACE)):
    old = title.split(",")[0].strip()
    scope = title[title.find("["):title.find("]") + 1] if "[" in title else "[Domain]"
    scope = scope.replace("Domain Name", "Domain")  # normalize the placeholder token
    src_note = retitle_example(note)
    LEVELS.append((f"{NEW_TITLE[old]} – {scope} Learning Systems", title,
                   V3_COMP.get(i, comp), V3_ROLE[i] or src_note, src_note, surf))

WIRING = [  # (category, area, [kpi rows], note)
    ("Foundation", "Scope of Work", [],
     "Calibration, not a metric — read through the Portfolio Metrics matrix + domain complexity multipliers below."),
    ("Foundation", "Influence", [],
     "Review evidence — influence is work adopted beyond your lane: SOPs and agents other teams run, "
     "team-view Section C asks raised → accepted → delivered, §7 counterparty standing."),
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
     "Adherence = planned updates land on schedule; freshness = the 6-month topic-refresh audit behind relevance. "
     "A topic is PPT + recorded session + practice + quiz content (catalogue hours ≈ topic count) and every refresh "
     "is planned as a from-scratch rebuild — this row is what makes a rung's surface size arguable."),
    ("Core Creation and Quality", "Production Systems",
     ["Agentic Production Coverage"],
     "Publishing through ACP pipelines; cost rows below read the efficiency it buys. The Agent Scope scale "
     "grades the work — operate and improve (A1–A2), build (A3), orchestrate (A4); agent-ops observability "
     "lives here: the day starts and ends in the pipeline dashboards."),
    ("Core Creation and Quality", "Learning Systems Design",
     ["Evaluation Environment Coverage", "Domain Capability Delivery",
      "Summative + Formative Achievement", "Module-Quiz Score Bands"],
     "The Domain Product Enablement pair — raised/accepted by SMEs, built by PMs + Engineering, "
     "accountability in Learning Domains — plus the measurement proof: achievement and quiz-band reads "
     "shared with Content Effectiveness / Content Quality (the APC double-read precedent). Also reads: "
     "Learning Environment Satisfaction, PAtC env-friction leg."),
    ("Core Creation and Quality", "GenAI Orchestration & Content Automation",
     ["Agentic Production Coverage", "Cost per MCQ Generated", "Cost per Coding Question"],
     "Mandatory from day one — the internship runs on it. Orchestration shows up as coverage plus falling "
     "unit costs; prompt craftsmanship and AI operational literacy are named expectations here."),
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
     ["Cost of Operations", "Creative Resource Utilisation Rate"],
     "Hygiene guardrails from the Team Ops & People block — run by the team's PM; no org ladder by design. "
     "SOPs runnable by others are the review evidence — the bus-factor guard."),
    ("Collaboration and Stakeholders", "Cross-Functionality",
     ["Cross-functional Sprint Delivery Rate"],
     "Plus the health of Section C asks the person is party to."),
    ("Collaboration and Stakeholders", "Stakeholder Collaboration",
     ["Stakeholder Content Request Fulfillment Rate"],
     "Ladders to dept Stakeholder Alignment (§5)."),
    ("Collaboration and Stakeholders", "Cross-Product Work", [],
     "Read through the Product column — Section B rows carried per product (NIAT · Academy · Launchpad slots)."),
    ("Collaboration and Stakeholders", "Mentorship", ["Power Performers Created"],
     "Rating Pillar 3 (Develop the Best) — first direct read: members made next-level-ready, counted per "
     "appraisal cycle. Feedback quality and growth opportunities stay review-based."),
]
assert len(WIRING) == 21

# ------------------------------------------------- v3 progression machinery
PRINCIPLE = ("All content production runs through agents — humans design, review, and improve the systems "
             "that produce. Named exception, so the claim stays honest: the video production pipeline "
             "(recording, editing, review) — agenticity not required there. This principle is what makes the "
             "first two rungs' job descriptions true, and it turns Agentic Production Coverage from a metric "
             "into a mandate.")

AGENT_SCOPE = [  # the A1–A4 scale — grades agent work without colliding with role levels
    ("A1", "Operate", "Run an existing agent pipeline: review outputs, tune prompts, handle escalations; "
                      "keep accuracy and cost inside budget."),
    ("A2", "Improve", "Move an agent's numbers: evals, retrieval quality, unit-cost reduction — with a "
                      "before/after you can show."),
    ("A3", "Build", "Design and ship a new content agent end-to-end whose impact holds in the metrics. "
                    "AI Engineer bar: at least 2–3 built and adopted."),
    ("A4", "Orchestrate", "Systems of agents carrying production: multi-agent workflows, escalation design "
                          "(when agents act alone, when they hand to humans), agents other people run."),
]
AGENT_SCOPE_MAP = ("Intern converts having shown A1 + A2 · AI Engineer reaches A3 within the year · Senior "
                   "operates at A4 (the leverage route) · Lead runs the team's agent fleet through people · "
                   "AI Engineer 3 sets the org's agent architecture.")

GATES = [  # (transition, [numbered requirements]) — approved Aug 2026; becomes the standing
           # Progression Policy document when Pavan calls for it.
    ("Conversion gate — Associate AI Engineer → AI Engineer, at 6 months", [
        "Runs assigned agent pipelines end-to-end without supervision — prompts tuned, outputs reviewed, "
        "escalations handled (A1–A2 shown).",
        "Judgment demonstrated: the responsible reviewer — their mentoring AI Engineer or Senior — confirms "
        "the intern's reviews catch what their own review would catch, sampled on real work through the ramp; "
        "they can tell good output from plausible output.",
        "Domain floor: has produced representative content items manually during the ramp — you can't review "
        "what you can't do.",
        "Decided by: supervising Senior / AI Engineer Lead proposes with ramp evidence; HOD confirms. "
        "Package set by HR at conversion."]),
    ("AI Engineer → Senior AI Engineer — the 2× bar", [
        "Surface ≈ 2× an AI Engineer's — courses × complexity, any mix of depth, breadth, or leverage "
        "(A4 agent systems are the leverage route).",
        "Quality held: all their Section B rows at budget, 2+ consecutive cycles.",
        "Leverage visible: Agentic Production Coverage contribution plus falling cost rows for their courses.",
        "People growing: mentorship evidence (Power Performers Created) — guiding work, not owning ratings.",
        "AI Engineer Lead proposes with row evidence; HOD + calibration confirm. Minimum 1 year in role."]),
    ("Senior AI Engineer → AI Engineer Lead — people outcomes define the title", [
        "A Lead seat exists — the span rule creates them: ~5–8 members per Lead (number with HR).",
        "Already answering beyond their slice: full-Section-B literacy shown at reviews, Section A lane "
        "awareness.",
        "People outcomes proven as a mentor: retention and growth of the people they guided.",
        "Accepts the accountability that defines the title: ratings, retention, growth and hiring for members.",
        "HOD + PM-head calibration confirm."]),
    ("AI Engineer Lead → AI Engineer 3 — the org seat", [
        "Org-level surface already held: org-tracker rows shaped, cross-domain standards authored and adopted.",
        "Their team runs without them day to day — the bus-factor test, passed.",
        "By org need, not tenure. HOD proposes; founders / PM-head calibration confirm."]),
]

STAY_LEAD = ("The gates say how you climb; this says what keeping the seat means. One rule under every bar: "
             "your rung's eight scored rows at budget — 100%, no governance breach. Below budget more than "
             "twice in 12 months breaks the bar; two consecutive cycles below starts a structured gap "
             "conversation with your Lead — what's missing, the plan, the timeline. A conversation, not a "
             "demotion. The tables below are those eight rows, per rung — the same grid the merit rating "
             "scores: four output rows, four governance rows, 12.5% each.")

STAY_KEY = ("How to read the gate column: Mandatory = the rung's defining requirement · Breach blocks = a "
            "breach zeroes that 12.5% slice and blocks eligibility for the cycle · ⚑ = a number not locked "
            "yet (a proposed default, adjustable).")

STAY_LEGEND = ("Domain chips — build complexity sets the topic count behind the same ≈ 200 CWT per cycle: "
               "{lo|Low 1.0× — English · Aptitude · Mathematics} {md|Medium 1.5× — Programming · CS Core · "
               "DevOps} {hi|High 2.0× — FullStack · GenAI} {vh|Very High 2.5× — System Design · DS & Algo · "
               "DS / ML} · {lc|low-churn} marks the two slots that swap on low-refresh domains (note below).")

# Chip tokens {lo|..} {md|..} {hi|..} {vh|..} {lc|..} render as colored chips in the html and as
# plain text in the xlsx: lo/md/hi/vh = the four build-complexity classes, lc = the low-churn slot
# swap. Content unchanged from the 25 Aug stay-bar ship — every ₹ / % / default stays Pavan-adjustable.
STAY = [  # (level, context line, footer line, rows); row = ("A"|"B", row name, bar to hold, gate)
    ("Associate AI Engineer (internship)",
     "A readiness scorecard — read ready / not ready. Interns answer for no team rows by design.",
     "Ramp cadence: A1 shown, then A2 — never more than one month behind the ramp plan across the six.",
     [("A", "Agent Pipeline Operation (A1)",
       "Assigned pipelines run unsupervised — two consecutive months", "Mandatory"),
      ("A", "Agent Improvement Delta (A2)",
       "≥ 1 documented before/after on an agent's accuracy, retrieval quality or unit cost", "Mandatory"),
      ("A", "Domain floor output",
       "⚑ propose: 25% of an AI Engineer's monthly share, produced hands-on (FS: ≈ 12 hrs · 400 pieces)",
       "Mandatory"),
      ("A", "Review judgment",
       "The responsible reviewer signs off their review calls on real work", "Mandatory"),
      ("B", "Content Issue Recurrence — their items", "≤ 2%", "Breach blocks"),
      ("B", "Unit costs — their pipelines",
       "Objective practice item (FIB, MCQ, MMCQ — any type) ≤ ₹3 · coding question on the domain scale "
       "{hi|~₹200 FullStack / GenAI} {vh|up to ₹300 DS & Algo}", "Breach blocks"),
      ("B", "Worklog & Status Hygiene", "100% — worklogs complete, statuses current", "Breach blocks"),
      ("B", "Culture & Values pillar", "In band", "Breach blocks")]),
    ("AI Engineer",
     None,
     "Rating floor: Performance + Role Competence pillars in band.",
     [("A", "Tech Stack Freshness Rate {lc|low-churn: slot → Learning Systems Design impact}",
       "100% of the ≈ 200 CWT surface each 6-month cycle — {lo|200 topics} {md|133 topics} "
       "{hi|100 topics} {vh|80 topics}", "Below 90% blocks ⚑"),
      ("A", "Learning Content Hours + Practice & Assessment Pieces",
       "Their CWT share of the team budget (FS team: 50 hrs · 1,600 pieces a month)", "At budget"),
      ("A", "Agentic Production Coverage",
       "90% — with 2–3 content agents built and adopted (A3) by year-end", "Agents mandatory"),
      ("A", "Summative + Formative Achievement {lc|low-churn: slot → Pedagogy Initiative Impact}",
       "Summative 35% quarterly · Formative 23% monthly, on their modules", "At budget"),
      ("B", "Content Issue Resolution Efficiency", "80% inside the 2-day TAT", "Breach blocks"),
      ("B", "Content Issue Recurrence", "≤ 2%", "Breach blocks"),
      ("B", "Unit costs",
       "CpLH ≤ ₹10,000 · objective practice item (FIB, MCQ, MMCQ — any type) ≤ ₹3 · coding question "
       "under ₹100 baseline {hi|~₹200 FullStack / GenAI} {vh|up to ₹300 DS & Algo}", "Breach blocks"),
      ("B", "Sprint Delivery + Stakeholder Fulfillment", "Sprint 100% · stakeholder 90%", "Breach blocks")]),
    ("Senior AI Engineer",
     None,
     None,
     [("A", "Complexity-weighted surface",
       "≈ 400 CWT held at budget — 2× an AI Engineer; Senior isn't a medal, it's a load, and the slice "
       "doesn't quietly shrink", "Mandatory"),
      ("A", "Learning Systems Design impact",
       "⚑ review evidence until budgets land (engagement-experience contribution + drop-off/completion delta)",
       "Review-based"),
      ("A", "Agent Orchestration (A4)",
       "90% production coverage attributable to multi-agent systems they own", "Mandatory"),
      ("A", "Pedagogy Initiative Impact", "⚑ review evidence until a budget lands", "Review-based"),
      ("B", "Their Section B rows", "All at budget, 2+ consecutive cycles", "Breach blocks"),
      ("B", "Content Issue Recurrence — wider slice", "≤ 2%", "Breach blocks"),
      ("B", "Unit-cost trend — their courses", "At or below budget, and falling", "Breach blocks"),
      ("B", "Mentorship on record",
       "≥ 1 power performer contributed, trailing 12 months (adjustable)", "Breach blocks")]),
    ("AI Engineer Lead",
     None,
     None,
     [("A", "Team Section B in-band rate",
       "⚑ propose: ≥ 85% of the team's owned rows at budget (FS pilot: 29 rows)", "Mandatory"),
      ("A", "Team Tech Stack Freshness", "100% across the team's whole surface", "Below 90% blocks ⚑"),
      ("A", "Team Agentic Production Coverage", "90% — run through people, not personally", "Mandatory"),
      ("A", "Business impact — the team's domains",
       "Summative 35% · Formative 23% · SPI band contribution", "At budget"),
      ("B", "Team Retention Rate", "≥ 90%, trailing 12 months (adjustable)", "Breach blocks"),
      ("B", "Power Performers Created", "≥ 1 per appraisal cycle (adjustable)", "Breach blocks"),
      ("B", "Cost of Operations + Roadmap",
       "At plan ⚑ · ≥ 90% ⚑ — run by the team's PM, answered for by the Lead", "Breach blocks"),
      ("B", "Stakeholder Fulfillment + Sprint Delivery", "Stakeholder 90% · sprint 100%", "Breach blocks")]),
    ("AI Engineer 3",
     "Reads through department KPIs and org KRAs, not one team view — the bar stays directional until those "
     "budgets land: the standards they authored still adopted and alive · portfolio Section B healthy across "
     "teams · a Lead bench ready behind them · places the org's learning-systems bets.",
     None,
     []),
]
for _lvl, _ctx, _foot, _rows in STAY:  # every rung with a table carries exactly the 4+4 grid
    assert not _rows or (sum(1 for c, *_ in _rows if c == "A") == 4 and
                         sum(1 for c, *_ in _rows if c == "B") == 4), _lvl

def chip_txt(s):  # xlsx / plain-text rendering: chip tokens → their text
    return re.sub(r"\{(?:lo|md|hi|vh|lc)\|([^}]*)\}", r"\1", s)

STAY_NOTES = [  # rendered under the stay-bar table in both outputs
    "Low-refresh domains (English, Aptitude, Mathematics, Programming, CS Core, DS & Algo, DevOps, System "
    "Design) run the same bar with two occupants swapped: Tech Stack Freshness → Learning Systems Design "
    "impact · Business Impact → Pedagogy Initiative Impact. The refresh audit still runs — 100% of the "
    "surface audited each cycle, rebuilt where the audit calls.",
    "Cost bars scale with domain complexity, and every number here is adjustable as real costs land: an "
    "objective practice item (FIB, MCQ, MMCQ — any type) ≤ ₹3 · a coding question under ₹100 baseline — "
    "~₹200 where a question is effectively a project (FullStack, GenAI), up to ₹300 where it ships "
    "editorials, brute-force and efficient solutions (DS & Algo).",
]
CWT_DEF = ("CWT — complexity-weighted topics: topic count × the domain complexity multiplier. ≈ 200 CWT per "
           "AI Engineer per 6-month cycle (= ≈ 100 topics at FullStack / GenAI 2.0×); a Senior holds ≈ 400.")

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
    "titles": ["Associate AI Engineer – FullStack Learning Systems (6-month internship)",
               "AI Engineer – FullStack Learning Systems",
               "Senior AI Engineer – FullStack & CS Core Learning Systems",
               "AI Engineer Lead – FullStack & CS Core Learning Systems"],
    "complexity": "High (2.0x) — FullStack · Medium (1.5x) — CS Core",
    "domains": [r for r in DOMAINS[1:] if r[0] in ("Full Stack", "CS Core")],
    "surface": "Metric surface = the FullStack & CS Core team view: Section A 19 mirrored tracker rows · "
               "Section B 29 owned rows (incl. the Domain Product Enablement pair and the Team Ops & People "
               "block) · Section C 4 asks.",
}

# The team's operating seat — added August 2026 with the Team Ops & People metric
# block. Not a ladder level: the maker levels own content and systems; the PM runs
# the operating rhythm. Comp band deliberately not set here.
PM_ROLE = {
    "title": "Project Manager – [Domain] Learning Systems",
    "pilot": "Project Manager – FullStack & CS Core Learning Systems",
    "reports": "The team's AI Engineer Lead. KPIs cascade Lead → PM: the Lead answers for the numbers at review; "
               "the PM runs them day to day. Team shape guardrail: ~5–8 makers per Lead (number with HR).",
    "comp": "Band pending — defined with HR when the seat is staffed.",
    "rows": ["Cost of Operations", "Roadmap Items Completion", "Hires Made", "Cost per Hire",
             "Team Retention Rate", "Power Performers Created", "Creative Resource Utilisation Rate"],
    "rows_note": "The Team Ops & People block of the team view — the FullStack & CS Core pilot carries all 7 "
                 "(CSI: 6, without the creative-utilisation row). Three of these are also the Lead's "
                 "Develop-the-Best rating reads: the PM operates the rows, the Lead answers for them.",
    "interfaces": "Content–Central PMO: the PM feeds the monthly check-in — complete worklogs and current ClickUp "
                  "statuses are what the PMO's Worklog & Status Hygiene — All Units read counts. Worklog capture "
                  "is the load-bearing activity: it makes deliverable costing computable.",
    "scope_note": "Progression and rating for the PM seat itself: not designed yet — this card fixes the seat, "
                  "the reporting line and the metric surface first.",
}
PM_OPS = [  # the Cost of Operations register — verbatim intent from Pavan, Aug 2026
    "Monthly manager–reportee one-on-ones",
    "Scheduling roadmap review meetings + Head approval",
    "Day-to-day ops — standups, learning hours",
    "Scheduling monthly check-in meets & documenting them in the right place",
    "Maintaining team assets (laptops, systems)",
    "Ensuring ClickUp adoption",
    "Keeping deliverable statuses up to date",
    "Monthly worklog capture → deliverable costs computed for the check-in",
    "Generating newsletters monthly",
    "Conducting team outings",
    "Conducting cycle-wise appraisal meetings",
]

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
ws = sheet("Ladder", (26, 22, 46, 46, 46))
r = title_row(ws, 1, "AI Engineer Ladder — content-department domain teams · August 2026 · five levels: a 6-month "
                     "internship rung, three employee rungs to Lead, then the org seat. Comp for the changed rungs "
                     "sits with HR.", 5)
r = hdr_row(ws, r, ("Title", "Comp | Tenure", "Role", "Scope (framework descriptor)", "Metric surface"))
for new, old, comp, role, src_note, surf in LEVELS:
    put(ws, r, 1, new, bold=True)
    put(ws, r, 2, comp)
    put(ws, r, 3, role)
    put(ws, r, 4, src_note)
    put(ws, r, 5, surf)
    ws.row_dimensions[r].height = max(60, 14 * (max(len(role), len(src_note)) // 60 + 1))
    r += 1

# Tab 2 — Gates & Scope (v3)
ws = sheet("Gates & Scope", (32, 120))
r = title_row(ws, 1, "Progression machinery — the production principle, the A1–A4 Agent Scope scale, "
                     "promotion gates, and stay bars. Becomes the standing Progression Policy document "
                     "when formalized.", 2)
put(ws, r, 1, "Production principle", bold=True)
put(ws, r, 2, PRINCIPLE)
ws.row_dimensions[r].height = 52
r += 2
r = hdr_row(ws, r, ("Agent Scope", "Definition"))
for code, nm, desc in AGENT_SCOPE:
    put(ws, r, 1, f"{code} — {nm}", bold=True)
    put(ws, r, 2, desc)
    ws.row_dimensions[r].height = 28
    r += 1
put(ws, r, 1, "Role mapping", bold=True, color=MUTED)
put(ws, r, 2, AGENT_SCOPE_MAP)
ws.row_dimensions[r].height = 28
r += 2
r = hdr_row(ws, r, ("Promotion gate", "Requirements (all of them)"))
for trans, lines in GATES:
    put(ws, r, 1, trans, bold=True)
    put(ws, r, 2, "\n".join(f"{i}. {ln}" for i, ln in enumerate(lines, 1)))
    ws.row_dimensions[r].height = 15 + 26 * len(lines)
    r += 1
r += 1
r = hdr_row(ws, r, ("Level", "Holding the role (the stay bar)"))
put(ws, r, 1, "One rule", bold=True, color=MUTED)
put(ws, r, 2, STAY_LEAD)
ws.row_dimensions[r].height = 56
r += 1
put(ws, r, 1, "Per-rung matrices", bold=True, color=MUTED)
put(ws, r, 2, "See the Stay Bars tab — each rung's eight rows in the merit-matrix format "
              "(Category · Row · Bar · Gate · Weight), with the domain-scaled numbers spelled out.")
ws.row_dimensions[r].height = 28
r += 1

# Tab 3 — Stay Bars (per-rung, merit-matrix format — 25 Aug readability pass)
ws = sheet("Stay Bars", (18, 38, 58, 18, 8))
r = title_row(ws, 1, "Holding the role — each rung's stay bar as its eight scored rows "
                     "(4 output + 4 governance × 12.5%). " + STAY_LEAD, 5)
put(ws, r, 1, "Key", bold=True, color=MUTED)
put(ws, r, 2, STAY_KEY + "  " + chip_txt(STAY_LEGEND), italic=True, color=MUTED)
ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=5)
ws.row_dimensions[r].height = 42
r += 2
for lvl, ctx, foot, stay_rows in STAY:
    put(ws, r, 1, lvl, bold=True, sz=10)
    put(ws, r, 2, chip_txt(ctx) if ctx else "", italic=True, color=MUTED)
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=5)
    ws.row_dimensions[r].height = 30 if ctx else 16
    r += 1
    if stay_rows:
        r = hdr_row(ws, r, ("Category", "Row", "Bar — hold at 100%", "Gate", "Weight"))
        for cat, nm, bar, gate in stay_rows:
            put(ws, r, 1, "A — Output" if cat == "A" else "B — Governance",
                color=("0B4F43" if cat == "A" else "8A2C18"), bold=True)
            put(ws, r, 2, chip_txt(nm), bold=True)
            put(ws, r, 3, chip_txt(bar))
            put(ws, r, 4, chip_txt(gate))
            put(ws, r, 5, "12.5%")
            ws.row_dimensions[r].height = max(26, 13 * (len(chip_txt(bar)) // 56 + 1) + 4)
            r += 1
    if foot:
        put(ws, r, 1, "Note", color=MUTED, italic=True)
        put(ws, r, 2, foot, italic=True, color=MUTED)
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=5)
        ws.row_dimensions[r].height = 16
        r += 1
    r += 1
for note in STAY_NOTES + [CWT_DEF]:
    put(ws, r, 1, "Note", color=MUTED, italic=True)
    put(ws, r, 2, note, italic=True, color=MUTED)
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=5)
    ws.row_dimensions[r].height = max(15, 14 * (len(note) // 110 + 1))
    r += 1

# Tab 4 — Progression Areas
ws = sheet("Progression Areas", (24, 22, 34, 34, 34, 34))
r = title_row(ws, 1, "21 progression areas × 4 levels — carried verbatim from the framework except the rows "
                     "marked ▲ (rewritten agent-first). AI Engineer 3 sits above Lead (org-wide scope); "
                     "the matrix deliberately stops at Lead.", 6)
r = hdr_row(ws, r, ("Category", "Area", "Associate AI Engineer (Intern)", "AI Engineer", "Senior AI Engineer", "AI Engineer Lead"))
for cat, area, a, e1, e2, ld in AREAS:
    put(ws, r, 1, cat, color=MUTED)
    put(ws, r, 2, area + (" ▲" if area in AREA_OVERRIDES else ""), bold=True)
    for c, v in enumerate((a, e1, e2, ld), 3):
        put(ws, r, c, v)
    ws.row_dimensions[r].height = max(40, 13 * (max(len(x) for x in (a, e1, e2, ld)) // 34 + 1))
    r += 1

# Tab 5 — KPI Wiring
ws = sheet("KPI Wiring", (24, 26, 62, 62))
r = title_row(ws, 1, "Progression area → named KPI rows (tracker / FullStack & CS Core team view). Every area "
                     "cites the rows it moves, or says why it deliberately has none.", 4)
r = hdr_row(ws, r, ("Category", "Area", "Wired to (KPI rows)", "Note"))
for cat, area, rows, note in WIRING:
    put(ws, r, 1, cat, color=MUTED)
    put(ws, r, 2, area, bold=True)
    put(ws, r, 3, " · ".join(rows) if rows else "— (by design)", color=TEAL if rows else MUTED)
    put(ws, r, 4, note)
    ws.row_dimensions[r].height = max(28, 13 * (len(note) // 60 + 1))
    r += 1

# Tab 6 — Rating Framework
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

# Tab 7 — Calibration
ws = sheet("Calibration", (26, 34, 34, 34, 34))
r = title_row(ws, 1, "Calibration: portfolio by level · domain complexity · product baselines · "
                     "domain catalogue · vocabulary bridge (2026 doc → KPI system)", 5)
r = hdr_row(ws, r, tuple(PORTF[0][:1] + ["Associate AI Engineer (Intern)", "AI Engineer", "Senior AI Engineer", "AI Engineer Lead"]))
for row in PORTF[1:]:
    put(ws, r, 1, row[0], bold=True)
    for c, v in enumerate(row[1:], 2):
        put(ws, r, c, v)
    r += 1
put(ws, r, 1, "How to read it", bold=True, color=MUTED)
ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=5)
put(ws, r, 2, "The AI Engineer column calibrates entry into the band; the Senior column is the 2× bar "
              "expressed in portfolio terms.")
r += 2
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

# Tab 8 — Project Manager
ws = sheet("Project Manager", (24, 120))
r = title_row(ws, 1, "Project Manager — the team's operating seat (added August 2026 with the Team Ops & People "
                     "metric block). Not a ladder level: reports to the AI Engineer Lead.", 2)
r = hdr_row(ws, r, ("Field", "Detail"))
for label, val in (
        ("Title pattern", PM_ROLE["title"]),
        ("Pilot instance", PM_ROLE["pilot"]),
        ("Reports to", PM_ROLE["reports"]),
        ("Comp", PM_ROLE["comp"]),
        ("Owns (metric surface)", " · ".join(PM_ROLE["rows"]) + ". " + PM_ROLE["rows_note"]),
        ("Interfaces", PM_ROLE["interfaces"]),
        ("Progression / rating", PM_ROLE["scope_note"])):
    put(ws, r, 1, label, bold=True)
    put(ws, r, 2, val)
    ws.row_dimensions[r].height = max(15, 13 * (len(val) // 115 + 1))
    r += 1
r += 1
r = hdr_row(ws, r, ("#", "Ops register — the activities inside Cost of Operations (so nothing is forgotten)"))
for i, act in enumerate(PM_OPS, 1):
    put(ws, r, 1, str(i))
    put(ws, r, 2, act)
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
  .staytbl { min-width: 900px; }
  .staytbl td.cat { font-weight: 600; white-space: nowrap; width: 1%; }
  .staytbl td.catA { background: #f2f8f6; color: #0b4f43; }
  .staytbl td.catB { background: #fdf1ee; color: #8a2c18; }
  .staytbl td.gA { color: #0b4f43; font-weight: 600; white-space: nowrap; }
  .staytbl td.gB { color: #8a2c18; font-weight: 600; white-space: nowrap; }
  .dchip { display: inline-block; font-size: .88em; font-weight: 600; padding: 0 7px; border-radius: 9px;
    margin: 1px 3px 1px 0; white-space: nowrap; border: 1px solid transparent; }
  .dc-lo { background: #eef7f4; color: #134237; border-color: #cfe6df; }
  .dc-md { background: #d9ece7; color: #134237; border-color: #b9d9d1; }
  .dc-hi { background: #b3d9d0; color: #113b31; border-color: #93c6ba; }
  .dc-vh { background: #7cbfb1; color: #0c322a; border-color: #5da997; }
  .dc-lc { background: #eceef8; color: #3a4a8c; border-color: #c8cdea; }
  .stayfoot { font-size: .82em; color: #666; margin: -18px 0 24px; max-width: 90ch; }
  .ladder { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin: 18px 0 8px; }
  .lvl { border: 1px solid #ccc; border-radius: 4px; overflow: hidden; display: flex; flex-direction: column; }
  .lvl-head { padding: 10px 12px; }
  .lvl-head .t { font-weight: 700; font-size: .95em; line-height: 1.25; }
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
  .gate { border: 1px solid #ccc; border-radius: 4px; margin-bottom: 12px; overflow: hidden; }
  .gate-h { padding: 9px 12px; background: #f4f4f4; border-bottom: 1px solid #ddd; font-weight: 700; font-size: .92em; }
  .gate ol { padding: 10px 14px 10px 32px; font-size: .86em; margin: 0; }
  .gate li { margin: 3px 0; }
  @media (max-width: 980px) { .ladder { grid-template-columns: 1fr; } }"""

B = []
B.append('<h1>AI Engineer Ladder</h1>')
B.append('<div class="subtitle">Career framework for content-department domain teams &middot; August 2026 &middot; '
         'titles follow the <strong>AI Engineer &ndash; [Domain] Learning Systems</strong> pattern &middot; five '
         'levels, from a 6-month internship to the org seat &middot; editable master: '
         '<strong>role_cards.xlsx</strong> (8 tabs)</div>')
B.append('<div class="key-point"><strong>How to read the cards:</strong> every progression area and rating line is '
         'wired to named KPI rows — anything in a <span class="kpi">mono chip</span> is a live row on the KPI tracker '
         'or the team view, so reviews read off the sheets instead of impressions. Areas with no chip say so '
         '<em>by design</em>. Every transition has a written gate, every rung a stay bar, and the A1&ndash;A4 Agent '
         'Scope scale grades the agent work; comp for the changed rungs sits with HR.</div>')
B.append('<div class="key-point"><strong>Production principle:</strong> all content production runs through agents — '
         'humans design, review, and improve the systems that produce. Named exception, so the claim stays honest: '
         'the video production pipeline (recording, editing, review) — agenticity not required there. This is what '
         'makes the first two rungs&rsquo; job descriptions true, and it turns '
         '<span class="kpi">Agentic Production Coverage</span> from a metric into a mandate.</div>')

B.append('<h2>The ladder</h2>')
B.append('<div class="sectionlead">Five levels, linear — an internship rung, then four employee rungs; AI Engineer 3 '
         'sits above Lead (org-wide scope) and the progression matrix below deliberately stops at Lead. Comp: Lead and '
         'AI Engineer 3 keep inherited bands; the changed rungs are with HR — no invented numbers. Strip the comp line '
         'before wide sharing if needed.</div>')
B.append('<div class="ladder">')
for (new, old, comp, role, src_note, surf), (bg, fg) in zip(LEVELS, RAMP):
    B.append(f'<div class="lvl"><div class="lvl-head" style="background:{bg};color:{fg}">'
             f'<div class="t">{esc(new)}</div></div>'
             f'<div class="lvl-comp">{esc(comp)}</div>'
             f'<div class="lvl-body">{esc(role)}</div>'
             f'<div class="lvl-surf"><strong>Answers for:</strong> {esc(surf)}</div></div>')
B.append('</div>')

B.append('<h2>Agent Scope — the A1&ndash;A4 scale</h2>')
B.append('<div class="sectionlead">Role levels say what you answer for; the A-scale grades the agent work itself. '
         'The gates and stay bars below cite it.</div>')
B.append('<div class="scroll"><table style="max-width:980px"><tr><th style="width:16%">Scope</th><th>What it means</th></tr>')
for code, nm, desc in AGENT_SCOPE:
    B.append(f'<tr><td><strong>{code} — {esc(nm)}</strong></td><td>{esc(desc)}</td></tr>')
B.append('</table></div>')
B.append(f'<div class="key-point"><strong>Role mapping:</strong> {esc(AGENT_SCOPE_MAP)}</div>')

B.append('<h2>Promotion gates</h2>')
B.append('<div class="sectionlead">Each transition has a written gate — all requirements, plus who proposes and who '
         'confirms. These blocks become the standing Progression Policy document when formalized.</div>')
for trans, lines in GATES:
    B.append(f'<div class="gate"><div class="gate-h">{esc(trans)}</div><ol>' +
             "".join(f'<li>{esc(ln)}</li>' for ln in lines) + '</ol></div>')

def chip_html(s):  # chip tokens → colored spans (escape first; tokens carry no &<>)
    return re.sub(r"\{(lo|md|hi|vh|lc)\|([^}]*)\}",
                  lambda m: f'<span class="dchip dc-{m.group(1)}">{m.group(2)}</span>', esc(s))

B.append('<h2>Holding the role — the stay bars</h2>')
B.append(f'<div class="sectionlead">{esc(STAY_LEAD)}</div>')
B.append(f'<div class="sectionlead" style="margin-top:-10px">{esc(STAY_KEY)}</div>')
B.append(f'<div class="sectionlead" style="margin-top:-10px">{chip_html(STAY_LEGEND)}</div>')
for lvl, ctx, foot, stay_rows in STAY:
    B.append(f'<h3 style="margin:24px 0 8px;font-size:1.05em">{esc(lvl)}</h3>')
    if not stay_rows:
        B.append(f'<p style="font-size:.9em;max-width:90ch;margin:0 0 24px">{esc(ctx)}</p>')
        continue
    if ctx:
        B.append(f'<div class="sectionlead" style="margin:0 0 10px">{esc(ctx)}</div>')
    B.append('<div class="scroll"><table class="staytbl"><tr><th style="width:12%">Category</th>'
             '<th style="width:25%">The row</th><th>The bar — hold at 100%</th>'
             '<th style="width:13%">Gate</th><th style="width:7%">Weight</th></tr>')
    for i, (cat, nm, bar, gate) in enumerate(stay_rows):
        catcell = ''
        if i == 0 or stay_rows[i - 1][0] != cat:
            label = "A — Output" if cat == "A" else "B — Governance"
            catcell = f'<td class="cat cat{cat}" rowspan="4">{label}</td>'
        B.append(f'<tr>{catcell}<td><strong>{chip_html(nm)}</strong></td><td>{chip_html(bar)}</td>'
                 f'<td class="g{cat}">{esc(gate)}</td><td>12.5%</td></tr>')
    B.append('</table></div>')
    if foot:
        B.append(f'<div class="stayfoot">{esc(foot)}</div>')
for note in STAY_NOTES:
    B.append(f'<p class="muted" style="font-size:.85em;max-width:90ch;margin:-6px 0 14px">{esc(note)}</p>')
B.append('<p class="muted" style="font-size:.85em;max-width:90ch;margin:-2px 0 26px"><strong>' +
         esc(CWT_DEF).replace(" — complexity-weighted topics:", "</strong> — complexity-weighted topics:", 1) + '</p>')

B.append('<h2>21 progression areas</h2>')
B.append('<div class="sectionlead">Grouped into 4 categories; all areas matter, weight varies by level. Carried '
         'verbatim from the framework except the rows marked ▲ — rewritten agent-first.</div>')
for cat in CATS:
    rows = [a for a in AREAS if a[0] == cat]
    B.append(f'<h3 style="margin:20px 0 10px;font-size:1.05em">{esc(cat)} ({len(rows)})</h3>')
    B.append('<div class="scroll"><table class="wide"><tr><th style="width:13%">Area</th>'
             '<th>Associate AI Engineer (Intern)</th><th>AI Engineer</th><th>Senior AI Engineer</th><th>AI Engineer Lead</th></tr>')
    for _, area, a, e1, e2, ld in rows:
        mark = ' <span title="rewritten agent-first">▲</span>' if area in AREA_OVERRIDES else ''
        B.append(f'<tr><td><strong>{esc(area)}</strong>{mark}</td><td>{esc(a)}</td><td>{esc(e1)}</td>'
                 f'<td>{esc(e2)}</td><td>{esc(ld)}</td></tr>')
    B.append('</table></div>')

B.append('<h2>KPI wiring</h2>')
B.append('<div class="sectionlead">Each area cites the rows it moves, or says why it deliberately has none. Rows live '
         'on the KPI tracker and the FullStack &amp; CS Core team view (the pilot).</div>')
B.append('<div class="scroll"><table class="wide"><tr><th style="width:15%">Category</th><th style="width:17%">Area</th>'
         '<th style="width:38%">Wired to</th><th>Note</th></tr>')
for cat, area, rows, note in WIRING:
    B.append(f'<tr><td class="muted">{esc(cat)}</td><td><strong>{esc(area)}</strong></td>'
             f'<td>{chips(rows)}</td><td>{esc(note)}</td></tr>')
B.append('</table></div>')

B.append('<h2>Performance rating — AI Engineer Lead</h2>')
B.append(f'<div class="sectionlead">{esc(RT[0])} {esc(CALC)}. The rating samples the surface; the role answers for '
         'all of it.</div>')
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
    f"<th>{esc(h)}</th>" for h in [PORTF[0][0], "Associate AI Engineer (Intern)", "AI Engineer", "Senior AI Engineer", "AI Engineer Lead"]) + "</tr>")
for row in PORTF[1:]:
    B.append("<tr><td><strong>" + esc(row[0]) + "</strong></td>" + "".join(f"<td>{esc(v)}</td>" for v in row[1:]) + "</tr>")
B.append('</table></div>')
B.append('<p class="muted" style="font-size:.85em;margin:-16px 0 22px">The AI Engineer column calibrates entry into '
         'the band; the Senior column is the 2&times; bar expressed in portfolio terms.</p>')
for tab, cap in ((COMPLEX, "Domain complexity"), (PRODUCTS, "Product baselines (student reach)"), (DOMAINS, "Domain catalogue")):
    B.append(f'<h3 style="margin:20px 0 10px;font-size:1.05em">{cap}</h3>')
    B.append('<div class="scroll"><table><tr>' + "".join(f"<th>{esc(h)}</th>" for h in tab[0]) + "</tr>")
    for row in tab[1:]:
        B.append("<tr><td><strong>" + esc(row[0]) + "</strong></td>" + "".join(f"<td>{esc(v)}</td>" for v in row[1:]) + "</tr>")
    B.append('</table></div>')

B.append('<div class="key-point"><strong>Topic surface — how a rung&rsquo;s load is argued:</strong> a topic is PPT + '
         'recorded video session + practice content + quiz content, so a domain&rsquo;s catalogue hours are ≈ its '
         'topic count. Every topic is refreshed on a 6-month cycle and planned as a from-scratch rebuild. That puts '
         'one AI Engineer&rsquo;s surface at ≈ 100 topics of FullStack / GenAI complexity per cycle, and a '
         'Senior&rsquo;s at ≈ 2&times; that, complexity-weighted — the cards write this as <strong>CWT</strong> '
         '(complexity-weighted topics: topic count &times; the domain multiplier, ≈ 200 per AI Engineer, ≈ 400 '
         'for a Senior). Lighter-refresh domains — English, Aptitude, '
         'programming fundamentals, CS Core, Mathematics, DS &amp; Algo — carry roughly double the topic count, and '
         'those seats are weighed harder on <strong>Learning Systems Design</strong> and <strong>Production '
         'Systems</strong>: refreshing costs less there, so invention and agent building are where the load belongs. '
         'Read on the team view as <span class="kpi">Tech Stack Freshness Rate</span>.</div>')

B.append('<h2>Pilot: FullStack &amp; CS Core</h2>')
fp = FS_PILOT
B.append('<div class="key-point"><strong>Instantiated titles:</strong> ' +
         " &middot; ".join(f'<span class="kpi">{esc(t)}</span>' for t in fp["titles"]) +
         f'<br><strong>Complexity:</strong> {esc(fp["complexity"])} &middot; <strong>Catalogue:</strong> ' +
         " · ".join(f'{esc(r[0])} — {esc(r[1])}h · {esc(r[2])}' for r in fp["domains"]) +
         f'<br>{esc(fp["surface"])}</div>')

B.append('<h2>Project Manager — the operating role</h2>')
B.append('<div class="sectionlead">Not a sixth ladder level — a parallel operating seat, one per domain team, added '
         'August 2026 with the Team Ops &amp; People metric block. The maker levels above own the content and the '
         'systems; the PM runs the team&rsquo;s operating rhythm.</div>')
pm_ifc = esc(PM_ROLE["interfaces"]).replace(
    "Worklog &amp; Status Hygiene — All Units",
    '<span class="kpi">Worklog &amp; Status Hygiene — All Units</span>')
pm_rows = [
    ("Title pattern", f'<strong>{esc(PM_ROLE["title"])}</strong>'),
    ("Pilot instance", f'<span class="kpi">{esc(PM_ROLE["pilot"])}</span>'),
    ("Reports to", esc(PM_ROLE["reports"])),
    ("Comp", esc(PM_ROLE["comp"])),
    ("Owns (metric surface)", chips(PM_ROLE["rows"]) +
     f'<div style="margin-top:4px" class="muted">{esc(PM_ROLE["rows_note"])}</div>'),
    ("Runs (ops register)", '<ol style="padding-left:18px">' +
     "".join(f'<li>{esc(a)}</li>' for a in PM_OPS) + '</ol>'),
    ("Interfaces", pm_ifc),
    ("Progression / rating", f'<span class="nodesign">{esc(PM_ROLE["scope_note"])}</span>'),
]
B.append('<div class="scroll"><table style="max-width:980px"><tr><th style="width:18%">Field</th><th>Detail</th></tr>')
for label, val in pm_rows:
    B.append(f'<tr><td><strong>{label}</strong></td><td>{val}</td></tr>')
B.append('</table></div>')

B.append('<h2>Vocabulary bridge</h2>')
B.append('<div class="scroll"><table><tr><th style="width:22%">2026 doc term</th><th>In the KPI system</th></tr>')
for term, mapping in BRIDGE:
    B.append(f'<tr><td><strong>{esc(term)}</strong></td><td>{esc(mapping)}</td></tr>')
B.append('</table></div>')

B.append('<div class="footnote">Source: the department&rsquo;s March 2026 career framework — descriptors, rating '
         'weights and calibration tables carried verbatim except the two matrix rows marked ▲; titles renamed and KPI '
         'wiring added (August 2026); the internship rung, the Senior force-multiplier rung, '
         'promotion gates, stay bars and the Agent Scope scale added August 2026. The rating samples the '
         'surface; the role answers for all of it. Comp: Lead and AI Engineer 3 keep inherited bands; the changed '
         'rungs are with HR — no invented numbers. '
         'Defaults taken pending red-pen: comp bands included (artifact is private; strip for wide sharing) &middot; '
         'level names Associate (internship) / Engineer / Senior / Lead / 3 &middot; FullStack &amp; CS Core as pilot. '
         'Companion sheets: KPI tracker (kra_training_sheet.xlsx) &middot; HOD one-pager. Other domain teams get cards '
         'when their team views land; CSI and Content&ndash;Central role cards are queued separately; the gate blocks '
         'above become the standing Progression Policy document when called for.</div>')

html = ('<title>AI Engineer Ladder</title>\n<style>\n' + STYLE + '\n</style>\n'
        '<div class="container">\n' + "\n".join(B) + '\n</div>\n')
open("role_cards.html", "w", encoding="utf-8").write(html)

print("xlsx tabs:", wb.sheetnames)
print("levels:", len(LEVELS), "| areas:", len(AREAS), "| wiring:", len(WIRING),
      "| pillars:", [(p[0], p[1], len(p[2])) for p in PILLARS])
print("html chars:", len(html), "| kpi chips:", html.count('class="kpi"'))
