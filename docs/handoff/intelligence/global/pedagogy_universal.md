# Open ACP — Pedagogy Intelligence (Standalone Handoff)

> **Standalone handoff document.** The complete pedagogy intelligence — coverage inventory,
> the full extracted principles file (inlined verbatim in §3), stack-specific overlays,
> an eval set, and implementation examples. No repo access required to use this.
> Generated 2026-07-06.

---

## 1. What this is and how it was derived

NxtWave's exemplar slide decks (the "brand corpus") were analyzed to extract **descriptive pedagogy intelligence**: the principles, strategies, session flows, and slide-level patterns the real content actually uses. Method:

1. Every deck's text layer was extracted (`pdftotext -layout`); each analyst read the text in full, then **visually spot-checked 5–19 representative pages per deck** to confirm patterns text can't show (progressive reveals, diagrams, side-by-side layouts, color idioms, callouts).
2. One analyst per domain-chunk ran independently (C++ ×3 chunks, Python, DSA, HTML/CSS, ReactJS, GenAI), each mapping findings onto the existing schema and proposing only genuinely novel patterns, with every claim grounded in a specific deck/slide.
3. Findings were synthesized into one file (`universal_principles.yaml`, now **version 4**) — inlined in full in §3. Analysts' confirmatory evidence was preferred over novelty; near-duplicate patterns were folded into existing keys instead of added.

**Interpretation rule:** the patterns are **DESCRIPTIVE** (observed in decks produced under real time constraints), not prescriptive mandates. Treat rules as strong defaults, and the `observed_in` lines as the evidence trail.

---

## 2. Coverage inventory — exactly what was analyzed

### 2.1 Corpus totals

- **34 PDFs, 2,170 pages** in the corpus; **32 session decks analyzed** + 2 guide/asset decks.
- All decks were re-exported clean from Google Slides on 2026-07-06 after the on-disk copies were found corrupt (recovery recipe: `https://docs.google.com/presentation/d/<ID>/export/pdf`; IDs tracked in `knowledge/raw/brand/download_list.txt`).

### 2.2 Deck-by-deck table

| # | deck | domain | pages | actual content | analysis status |
|---|---|---|---|---|---|
| 1 | sample_cpp_s1 | C++ | 101 | Intro to C++ (car analogy, Python bridge, first program) | analyzed (v1 core) |
| 2 | cpp_s2 | C++ | 70 | Operators, type conversion, conditionals (bridge course) | analyzed (v3) |
| 3 | cpp_s3 | C++ | 46 | Loops and arrays (bridge course) | analyzed (v3) |
| 4 | cpp_s4 | C++ | 36 | Functions (bridge course, C++ vs Python) | analyzed (v3) |
| 5 | cpp_s5 | C++ | 82 | STL: Pair & Vector (+ iterators, safe .at()) | analyzed (v3) |
| 6 | cpp_s6 | C++ | 77 | STL: Deque & Stack (+ SpecialStack capstone) | analyzed (v3) |
| 7 | cpp_s7 | C++ | 68 | STL: Queue & Priority Queue (+ Emergency Room capstone) | analyzed (v3) |
| 8 | cpp_s8 | C++ | 80 | STL: Sets (Set → Multiset → Unordered Set) | analyzed (v3) |
| 9 | cpp_s9 | C++ | 103 | STL: Maps (Map → Multimap → Unordered Map) | analyzed (v3) |
| 10 | cpp_s10 | C++ | 80 | Utility functions (sort, max/min_element, find, permutations) | analyzed (v3) |
| 11 | sample_python_s1 | Python | 47 | Intro / how to learn a programming language | analyzed (v1 core) |
| 12 | sample_python_s2 | Python | 29 | First program, JS→Python bridge | analyzed (v1 core) |
| 13 | sample_python_s3 | Python | 60 | Coding-practice platform walkthrough | analyzed (v1 core) |
| 14 | python_s4 | Python | 48 | Variables & data types (JS side-by-side) | analyzed (v3) |
| 15 | python_s5 | Python | 62 | Strings, type conversion, input/output | analyzed (v3) |
| 16 | sample_dsa_s1 | DSA | 27 | DS & algorithms intro (bookshelf/recipe analogies) | analyzed (v1 core) |
| 17 | dsa_s2 | DSA | 44 | Time complexity (step counting → Big O) | analyzed (v3) |
| 18 | dsa_s3 | DSA | 20 | Space complexity (+ optimization refactor) | analyzed (v3) |
| 19 | dsa_s4 | DSA | 9 | Pseudocode (short primer) | analyzed (v3) |
| 20 | htmlcss_s1 | HTML/CSS | 29 | Introduction to HTML (Tourism card build) | analyzed (v3) |
| 21 | htmlcss_css_part1 | HTML/CSS | 37 | **Introduction to CSS Part 1** (ruleset, div, class) — user-recovered | analyzed (v4) |
| 22 | htmlcss_s2 | HTML/CSS | 41 | Introduction to CSS Part 2 (color, background-color) | analyzed (v3) |
| 23 | htmlcss_s3 | HTML/CSS | 47 | CSS Part 2 revised cut (near-duplicate of s2 + announcements) | analyzed (v3) |
| 24 | sample_react_project | ReactJS | 44 | Introduction to React JS (MERN map, vanilla→React→JSX) | analyzed (v2) |
| 25 | react_s2 | ReactJS | 33 | JSX intro (largely overlaps #24) | analyzed (v3) |
| 26 | react_s3 | ReactJS | 32 | Components & Props | analyzed (v3) |
| 27 | react_s4 | ReactJS | 56 | Components & Props recap + Creating a React App (Vite/NPM) | analyzed (v3) |
| 28 | sample_genai_project | GenAI | 14 | Track intro ("AI-curious to AI-confident", 4 capstone pipelines) | analyzed (v2) |
| 29 | genai_s2 | GenAI | 71 | Exploring GenAI capabilities (search, deep research, voice, model taxonomy) | analyzed (v3) |
| 30 | genai_s3 | GenAI | 66 | Productivity tools (Gamma, Code2Tutorial, ChatGPT features) | analyzed (v3) |
| 31 | genai_s4 | GenAI | 109 | Prompt engineering fundamentals (CRAFT, shots, templates, roles) | analyzed (v3) |
| 32 | genai_s5 | GenAI | 150 | No-code workflow build (n8n + Make.com social-media automation) | analyzed (v3) |
| 33 | slide_prep_guide | guide | 101 | Slide preparation guide (30–40 words/slide etc.) | analyzed (v1 core) |
| 34 | coding_illustrations | assets | 251 | Branded illustration asset library | catalogued (v1) |

Per-domain page totals: C++ 743 · GenAI 410 · Python 246 · ReactJS 165 · HTML/CSS 154 · DSA 100 · guides/assets 352.

### 2.3 Known caveats and gaps (be honest with downstream agents)

1. `genai_s4`/`genai_s5` exports contain duplicated/reordered slide runs (working merges) — their session flows were reconstructed by content grouping, not raw page order.
2. ReactJS filenames don't match content: `react_s2` = JSX intro, `react_s3`/`react_s4` = Components & Props (+Vite). **No React deck covers Lists/State/Events/Routing.**
3. `htmlcss_s2` and `htmlcss_s3` are near-duplicates (same "Part 2" session, s3 is a longer revised cut).
4. True HTML/CSS session order: `htmlcss_s1` (HTML intro) → `htmlcss_css_part1` (CSS Part 1) → `htmlcss_s2/s3` (CSS Part 2).
5. **Two frontend-track decks are referenced by recap slides but absent from the corpus** (no Drive IDs known): "Getting Started with Frontend" and "Leveraging Gen AI for accelerated learning" (Perplexity/NotebookLM meta-skill session).
6. `dsa_s4` is genuinely short (9p pseudocode primer) — thin evidence, flagged as such.
7. Quiz Time! slides are branded transition slides; actual quiz questions are delivered live and are not in the decks.

### 2.4 Do we need every stack → course → session → PDF? (sampling guidance)

**No.** Evidence from this run: the last six C++ decks were almost purely *confirmatory* (they re-observed existing patterns); genuinely new patterns came only from **new domains** (HTML/CSS, GenAI) or **new session archetypes** (complexity analysis, no-code workflow build, tool walkthrough). Practical rule for extending coverage:

- **Universal principles** (§3 `principles`/`strategies`) transfer across stacks — do not re-derive per stack.
- For a **new stack**, sample 2–4 decks that span its distinct **session archetypes** (e.g. concept session, practice session, project/build session). Stop when a deck stops yielding new patterns (the "loop-until-dry" signal).
- Only expect NEW patterns when the stack has a genuinely different **delivery form** (markup-with-rendered-output, no-code tool orchestration, math-proof-style derivations, etc.).
- Prioritize closing archetype gaps over adding more decks of a covered archetype. Current highest-value gaps: React state/lists/events sessions, a DSA algorithm-technique session (sorting/searching walkthrough), the two missing frontend-track decks.

---

## 3. The full pedagogy intelligence (universal_principles.yaml v4, verbatim)

```yaml
# Universal Pedagogy Principles
# These apply to ALL content types and ALL domain stacks
#
# Provenance (see knowledge/analyses/style/ for per-deck analyses):
#   - Core principles are heavily C++-derived (C++ S1 + STL/Loops/Operators/Functions),
#     with Python S1-S3, DSA S1, and generic ReactJS input.
#   - 2026-07-06 (v2): added project-building / framework / GenAI patterns from the two
#     intact sample decks (sample_react_project 44p, sample_genai_project 14p).
#   - 2026-07-06 (v3): the previously-corrupt numbered decks were re-exported clean and
#     fully analyzed (24 decks, one analyst per domain-chunk). Coverage now spans:
#       C++ S2-S10 (operators/loops/functions + STL sets/maps/pair/vector/deque/stack/
#         queue/PQ + utility algorithms); Python S4-S5 (variables/types, strings & I/O);
#         DSA S2-S4 (time/space complexity, pseudocode); HTML/CSS S1-S3 (HTML intro, CSS
#         color/background) — HTML/CSS previously had ZERO source; ReactJS S2-S4
#         (JSX/intro, components & props, Vite app setup); GenAI S2-S5 (capabilities tour,
#         productivity tools, prompt engineering, no-code workflow-automation build).
#   - 2026-07-06 (v4): added the previously-missing "Introduction to CSS | Part 1" deck
#     (user-provided file, 37p → knowledge/raw/brand/htmlcss_css_part1.pdf; no Drive ID).
#     Closes the CSS-syntax-fundamentals gap: ruleset/selector/property/value, container
#     div, class attribute — the material htmlcss_s2/s3 only recapped. True session
#     order: htmlcss_s1 (HTML intro) → css_part1 → htmlcss_s2/s3 (both "Part 2").
#   - CAVEATS: some re-exported decks (genai_s4/s5) contain duplicated/reordered slide
#     runs (working merges) — flows below are reconstructed by content grouping, not raw
#     page order. ReactJS filenames don't match content (react_s2 = JSX intro,
#     react_s3/s4 = Components&Props + Vite; none cover Lists/State/Routing).
#     The HTML/CSS track's recap slides reference two further sessions NOT in the corpus:
#     "Getting Started with Frontend" and "Leveraging Gen AI for accelerated learning".
#   - Visual patterns below are DESCRIPTIVE (observed in decks produced under time
#     constraints), not prescriptive mandates — treat as "observed", weigh accordingly.

version: 4

# ─── CORE PRINCIPLES ────────────────────────────────────────────────────────────

principles:

  incremental_learning_progression:
    description: "Build knowledge in small, sequenced steps — never jump cognitive levels"
    observed_in:
      - "Python S1: driving analogy → common aspects → differences → conclusion — before touching code"
      - "C++ S1: same driving analogy reused (bridge from known), then three key areas → syntax last"
      - "Python S2: recap previous session → agenda → first program → comparison table → operations"
      - "DSA S1: definition → real-life analogy → examples → applications → benefits → takeaways"
      - "C++ Loops: For loop flowchart → syntax comparison → iteration trace table → code example — visual before textual before executable"
      - "C++ Operators: Operators comparison tables → key differences → type conversion → conditionals — each builds on the prior concept"
      - "C++ STL Pair & Vector: STL overview (4 components) → Pair (simple container) → Vector (complex container) → iterators — each topic builds on the prior"
      - "C++ STL Sets: Set (unique+sorted) → Multiset (duplicate+sorted) → Unordered Set (unique+unordered) — each variant introduced by contrast with the previous"
    rules:
      - "Start every concept with what the learner already knows (prior knowledge activation)"
      - "Introduce ONE new concept per slide/section — never two"
      - "Build complexity gradually: simple case → general case → edge cases"
      - "Each session builds on the previous — mandatory recap at start"
      - "When transitioning to a new language/framework, explicitly bridge from the known one"

  analogy_before_abstraction:
    description: "Use real-world analogies before formal definitions"
    observed_in:
      - "Python S1: 'Driving a car' analogy for learning programming languages (8 slides before code)"
      - "C++ S1: same car analogy reused — proving it's a deliberate pedagogical pattern"
      - "DSA S1: 'Bookshelf in a library' for data structures, 'recipe in a cookbook' for algorithms, 'ingredients in containers' for data organization"
      - "ReactJS: component trees shown as visual diagrams before code"
      - "C++ STL Queue: FIFO concept shown with people-in-line illustration (numbered 1-6) BEFORE any code"
      - "C++ STL Priority Queue: VIP queue analogy (VIP vs Regular passengers) BEFORE formal max-heap definition — structurally maps: VIP = higher priority = served first regardless of arrival order"
      - "C++ STL Vector: Array limitation (fixed size) introduced via character dialogue BEFORE vector definition — motivates WHY vectors exist"
      - "GenAI S4: LLM introduced as 'a new intern who doesn't know what to do unless you explain' BEFORE defining prompt engineering"
      - "GenAI S2: 'different AI models are like different tools in a toolbox' BEFORE the model-category taxonomy"
      - "GenAI S5: an AI workflow framed as 'creating a recipe for the AI to follow' before the build"
      - "CSS Part 1: 'Real World Example — Container' — loose boxes → one packed box → loaded truck illustration shown BEFORE the div syntax"
    rules:
      - "Every abstract concept must have a concrete analogy BEFORE the formal definition"
      - "Analogies should use everyday objects (cars, bookshelves, recipes, containers)"
      - "Reuse analogies across sessions when introducing related concepts in new languages"
      - "The analogy must map structurally to the concept — not just be a loose metaphor"

  bridge_from_known_to_unknown:
    description: "When introducing new concepts, always start from what the learner already knows"
    observed_in:
      - "Python S2: JavaScript vs Python comparison table on slide 10 (they know JS)"
      - "C++ S1: Python vs C++ side-by-side for print, comments, variables, data types — 30+ slides of comparison"
      - "C++ S1: 'Three key areas to focus' — abstractions (same), problem-solving (same), syntax (different) — minimizing perceived difficulty"
      - "ReactJS: Regular JS → React JS progression (show vanilla JS first, then React equivalent)"
      - "C++ Functions: Every function concept shown as C++ vs Python side-by-side (definition, calling, pass by value/reference)"
      - "C++ Loops: For/While/Do-While each shown as C++ syntax left, Python syntax right, with dashed orange separator"
      - "C++ Operators: Comparison tables for Logical, Arithmetic, Relational, Assignment operators — Python column vs C++ column"
      - "C++ STL Vector: Every operation (declaration, indexing, push_back/append, pop_back/pop, size/len, erase/del, insert, reverse, clear, swap) shown C++ left, Python right"
      - "C++ STL Vector: 'To better comprehend the significance of vectors, let's consider the concept of arrays' — bridges from arrays (known) to vectors (new)"
      - "C++ STL Priority Queue: Max-Heap taught first, then Min-Heap introduced as variation — bridges from default to parameterized"
      - "ReactJS S1 (sample): build 'Hello World' the vanilla-DOM way first (document.createElement/appendChild), then rebuild the IDENTICAL result with React (React.createElement/createRoot/render) — whole-artifact bridge, not line-by-line"
      - "ReactJS S1 (sample): JSX introduced as a 'compiles to' equivalent of the React.createElement call the learner just wrote — new syntax bridged to the API they already learned"
      - "Python S4-S5: nearly every concept shown JavaScript-left vs Python-right (variables, int/float/str/bool/None, constants, type checking) + a JS→Py conversion-API map (String()→str, Number()/parseInt()→int, Boolean()→bool)"
      - "ReactJS S3: passing props framed as 'like declaring attributes for any HTML tag' — bridges props to the already-known HTML-attribute mental model"
    rules:
      - "When learners know Language A and are learning Language B, ALWAYS show A vs B comparison"
      - "Use side-by-side code comparison slides (Language A on left, Language B on right)"
      - "Highlight what's SAME first (reduces anxiety), then what's DIFFERENT (focused learning)"
      - "Explicitly state transfer: 'The problem-solving approach is the same across all languages'"
      - "Use Python comparison selectively — Vector uses it (direct equivalent: list), but Queue/Priority Queue/Sets drop it when Python equivalents would confuse more than help"
      - "For a new framework/library: build the target artifact the KNOWN way first (vanilla), run it, show output; then rebuild the same artifact the new way and prove identical output (matched-output proof)"
      - "Introduce a framework's ergonomic syntax (e.g. JSX) as a compile-target of the lower-level API just taught — 'this sugar becomes that call'"

  contextual_and_applied_learning:
    description: "Every concept must connect to real-world application"
    observed_in:
      - "DSA S1: search engines, social media, e-commerce, healthcare, finance as DSA applications"
      - "C++ S1: desktop apps, mobile apps, gaming, big data, cloud, web — with named companies"
      - "ReactJS: Meta/Facebook, Netflix, Airbnb as companies using React"
      - "C++ S1: 'F-35 fighter jet uses C++ for avionics', 'NASA uses C++ for flight software'"
      - "HTML/CSS S1: opens with frontend importance + MNC-salary framing before any markup (career lever for a job-track skill)"
      - "GenAI S2: each capability mapped across Agriculture/Sports/Education/Fashion domains; deep-research shown as an industry use-case wheel"
      - "GenAI S5: manual-vs-workflow time contrast ('30-45 min per article' vs '< 2 min of human effort')"
    rules:
      - "After introducing a concept, immediately show 2-3 real-world applications"
      - "Use named companies and specific products (not generic 'many companies use X')"
      - "Include surprising/impressive facts to build motivation ('NASA uses C++ for flight software')"
      - "Show industry trends and download statistics to validate technology choices"

  cognitive_load_management:
    description: "Strictly limit information density to prevent overload"
    observed_in:
      - "Slide Prep Guide: max 30-40 words per slide, 3-4 lines ideal"
      - "All PPTs: one concept per slide, progressive reveal (multiple slides for one topic)"
      - "C++ S1: data type table split across 2 slides instead of cramming into 1"
      - "Python S3: coding practice walkthrough uses 15+ slides for one question"
      - "C++ Loops: Do-while loop explained across 5 progressive annotation slides — same code shown 5 times, each highlighting ONE different line with a callout box"
      - "C++ Operators: Array declaration syntax revealed across 3 slides — first highlights 'type', then 'array_name', then '[array_size]'"
      - "C++ STL Queue: Push operation shown across 3 progressive slides (push 10 → push 20 → push 30), one element per slide"
      - "C++ STL Priority Queue: Push operation shown across 5 progressive slides (push 50 → 30 → 20 → 10 → 5), maintaining visual container state on every slide"
      - "C++ STL Vector: Iterator concept taught across 4 slides — begin() → *it dereference → end() → end()-1 — each slide adds one annotation to the same code"
      - "CSS Part 1: the SAME HTML panel re-shown across 3 consecutive slides while only the caption evolves — 'All The Elements At Once!' → 'Wrapping: grouping elements at one place' → 'we use container element' — vocabulary staged one term per slide over a static code panel"
    rules:
      - "Maximum 30-40 words per slide — enforced, not suggested"
      - "One idea per slide — if you need more space, add another slide"
      - "Progressive reveal: show code in stages (declare → input → output → full program)"
      - "Break complex topics into multiple slides with clear visual progression"
      - "Watch time drop at 25 minutes → design for 20-minute attention blocks with breaks"
      - "Maximum 3-4 new concepts per 15-minute block"

  skill_mastery_through_deliberate_practice:
    description: "Learning is solidified through structured practice, not passive consumption"
    observed_in:
      - "Python S3: entire session dedicated to coding practice walkthrough"
      - "C++ S1: practice questions section at the end with worked solutions (area of circle, simple interest)"
      - "All sessions end with Key Takeaways that double as a self-check"
      - "Difficulty levels (Easy/Medium/Hard) explicitly shown in coding practice"
      - "C++ Functions: Practice section with 3 graduated problems — Swap Two Numbers → Find Maximum → Sum of Digits → Calculator (increasing complexity)"
    rules:
      - "At least 40% of session time must be active practice (not lecture)"
      - "Practice problems must be progressive: Easy → Medium → Hard"
      - "Provide worked solutions — but encourage trying BEFORE looking ('Before looking at the Tutorial, make sure you try harder')"
      - "Each practice problem should map to a specific learning objective"
      - "Include self-assessment mechanisms (test cases, AI tutor, comparison with solution)"

# ─── LEARNING STRATEGIES ────────────────────────────────────────────────────────

strategies:

  spaced_repetition:
    description: "Revisit previously learned material at increasing intervals"
    observed_in:
      - "Every session starts with a Recap slide reviewing the previous session"
      - "Key Takeaways at end mirror the Agenda at start (bookend pattern)"
      - "Feedback slides every 4 sessions — a checkpoint to revisit cumulative learning"
      - "C++ PPTs constantly reference Python equivalents — reinforcing Python while teaching C++"
    rules:
      - "Mandatory Recap slide at start of every session"
      - "Recap should use bullet points summarizing previous session's key concepts"
      - "When teaching new language, constantly reference the first language learned (reinforcement)"
      - "Module quizzes every 4 sessions as spaced repetition checkpoints"
      - "Key Takeaways must be split into parts (Part 1/2, 2/2) if content is substantial"

  active_recall:
    description: "Force retrieval from memory rather than passive review"
    observed_in:
      - "C++ S1: 'What are the differences between the two cars?' — question BEFORE showing the answer"
      - "C++ S1: 'Does driving a new car require a different set of fundamental skills?' — Socratic questioning"
      - "DSA S1: 'But what if we had a big sentence?' — posing a problem before the solution"
      - "Coding practice: show problem → attempt → fail → debug → succeed"
      - "C++ Functions/Loops/Operators: 'Quiz Time!' slides after every major concept section — 2-3 per session, not just end-of-session"
    rules:
      - "Ask questions BEFORE providing answers (Socratic method)"
      - "Use 'Think about this...' slides before revealing the solution"
      - "In coding: show the problem, let them think, THEN show the approach"
      - "Classroom quizzes every 15-20 minutes to force recall"

  concept_interleaving:
    description: "Mix related concepts rather than teaching in isolation"
    observed_in:
      - "C++ S1: interleaves data types with input/output operations — doesn't teach all types first then all I/O"
      - "Python S2: interleaves arithmetic operations with print statements"
      - "ReactJS: interleaves JavaScript fundamentals with React concepts"
    rules:
      - "Don't teach all theory first then all practice — interleave them"
      - "When introducing a new concept, immediately connect it to the previous one"
      - "Side-by-side comparisons within a session (not 'compare later')"
      - "Practice problems should combine concepts from current AND previous sessions"

  progressive_code_reveal:
    description: "Show code building up step by step, not as a complete block"
    observed_in:
      - "C++ S1: boilerplate code revealed over 5 slides (#include → main() → code area → return 0 → explained)"
      - "C++ data types: declare variable → take input → print output — 3 separate slides per data type"
      - "ReactJS: vanilla JS → add React imports → React.createElement → render — multi-slide progression"
      - "Python S2: 'Hello World' in JS first, then Python equivalent"
      - "C++ Loops: Do-while progressive annotation — full code shown but each line highlighted with dashed-arrow callout explaining one aspect per slide"
      - "C++ Operators: Array syntax 'type array_name[array_size]' revealed in 3 separate slides highlighting each component"
      - "ReactJS S2: git-style red/green diff replaces <script type='module'> with type='text/babel', then collapses the 4-line React.createElement call into 1-line JSX"
      - "ReactJS S3: 'Accessing Props' across ~3 same-code slides, each adding one orange box — (props) param → console.log(props) → const {name}=props destructure"
      - "GenAI S4: a prompt built up Role → +Context → +Action → +Format → +Tone, prior lines greyed and the new block bold — progressive reveal applied to a PROMPT, not code"
    rules:
      - "NEVER show a complete code block on the first slide — build it up"
      - "Each slide adds 1-2 lines to the previous code, highlighted with blue box"
      - "Show Input → Code → Output for every code example"
      - "When showing errors, follow the sequence: write code → run → see error → explain → fix → run again"
      - "Use git-style formatting (red/green) when replacing lines of code"
      - "Two variants: (1) build-up — add lines incrementally; (2) annotation — show complete code, highlight one element per slide with callout"
      - "Token-level annotation sub-variant: for a syntax template with named slots, dissect ONE token per slide (highlight box + dashed arrow + caption) while the full template stays stable (e.g. C++ 'type array_name[array_size]')"
      - "Applies beyond source code — build up prompts, config, and node setups the same way (grey prior parts, bold the new)"

  metacognitive_development:
    description: "Help learners understand their own learning process"
    observed_in:
      - "Python S1: explicitly teaches 'how to learn a new programming language' — meta-skill"
      - "C++ S1: 'Three key areas to focus: Abstractions, Problem-Solving, Syntax' — framework for learning ANY language"
      - "Python S3: teaches how to USE the coding platform (timer, save, reset, AI tutor) — learning to learn"
      - "C++ S1: 'Learning time: ~300 hours for first language, ~10 hours for second' — setting expectations"
      - "CSS Part 1: opens by recapping a dedicated 'Leveraging Gen AI for accelerated learning' session (learning/clarifying a concept, testing knowledge, understanding code; tools: Perplexity, NotebookLM) — AI-assisted learning taught as an explicit meta-skill inside the frontend track"
    rules:
      - "Include sessions that explicitly teach 'how to learn' this subject"
      - "Provide frameworks for self-directed learning (three key areas, learning roadmaps)"
      - "Set realistic time expectations ('it takes ~30 days for the first language, ~2 hours for the next')"
      - "Teach tool usage explicitly (IDE, debugger, AI tutor, practice platform)"

  motivation_through_relevance:
    description: "Keep learners motivated by showing WHY this matters"
    observed_in:
      - "C++ S1: company logos, job market stats, competitive programming stats"
      - "DSA S1: search engines, social media, healthcare, finance as real applications"
      - "ReactJS: download trends chart, top companies, career advantages"
      - "C++ S1: 'F-35 fighter jet relies on C++ for avionics' — impressive facts"
      - "CSS Part 1: 'Google Chrome is a Must' justified with ~89.1% India browser market share, source (gs.statcounter) cited on-slide — even tooling choices get a sourced statistic"
    rules:
      - "First 10% of any new topic: WHY should I care? (industry relevance, career impact)"
      - "Show named companies, real products, job statistics"
      - "Use facts that create 'wow' moments ('NASA uses C++ for flight software')"
      - "Address the 'will I actually use this?' question proactively"

  visual_before_textual:
    description: "Use diagrams, flowcharts, and memory layouts before showing code syntax"
    observed_in:
      - "C++ Loops: For loop flowchart (Initialization → Condition → Statements → Increment/Decrement → End) shown BEFORE syntax"
      - "C++ Loops: Array memory diagram with contiguous addresses (100, 104, 108, 112, 116) and index labels before array syntax"
      - "C++ Operators: Type conversion hierarchy diagram (int → long long, int → float, int → double) before code examples"
      - "C++ Operators: Binary representation (16-bit short) diagram to explain data loss in short → char conversion"
      - "DSA S2: Big O growth-curve graph (Time vs Input size, three curves labeled Slowest/Slow/Fastest) before naming asymptotic classes"
      - "DSA S3: memory-cell boxes a|b|c with 'Number of memory spaces = 3' before stating O(1)"
      - "Python S5: string 'Ravi' shown with index labels 0 1 2 3 and username[0]→'R' BEFORE the indexing code"
    rules:
      - "When a concept has a visual model (flowcharts, memory layouts, type hierarchies), show the diagram FIRST"
      - "Include actual values in diagrams (memory addresses, binary digits, iteration values) — not just abstract shapes"
      - "Use iteration trace tables (Iteration | Value | Condition | Action | Updated Value) for loop explanations"
      - "Show data type size tables (Data Type | Bits | Bytes) when teaching type conversion"

  deliberate_error_exposure:
    description: "Intentionally show incorrect behavior to teach correct usage"
    observed_in:
      - "C++ Operators: Switch statement shown WITHOUT break — output is 'A B' instead of just 'A' — then correct version with break"
      - "C++ Operators: short 300 → char produces ',' (ASCII 44) — shows data loss with binary diagram, then explains why"
      - "C++ Functions: Pass by value shown first, then pass by reference — contrasting outputs (Main: a=2 vs Main: a=4) to highlight the difference"
      - "Python S5: '\"*\" + 10' shown producing a real TypeError traceback (with a frustrated-character illustration), then fixed with str(10)"
      - "Python S5: message[2]='e' shown producing 'str object does not support item assignment' to teach immutability"
      - "ReactJS S3: component renamed Welcome→welcome to show React treats a lowercase name as a raw HTML tag (breaks), then restates the capitalization rule"
    rules:
      - "When a construct has a common pitfall, show the pitfall BEFORE the correct usage"
      - "Compare outputs side-by-side: 'what you expected' vs 'what actually happened'"
      - "Use the error to motivate WHY the correct approach exists"

  predict_the_output_challenge:
    description: "Freeze a code result behind a 'What will be the output?' prompt — often pairing a KNOWN case (answer shown) with a TWIST case (answer withheld) — then reveal on the next slide"
    observed_in:
      - "Python S5: '1+2 → 3' shown, but adjacent '\"1\"+\"2\"' replaced with a dashed-arrow 'What will be the output?' box; answer (12) revealed next slide"
      - "Python S5: '\"*\" + 10' output withheld, next slide reveals it is a TypeError"
      - "Python S5: 'Can we modify a string like this?' posed before revealing message[2]='e' errors"
    rules:
      - "Pair a working case with a surprising/breaking case on one slide; show the known answer, hide the surprising one"
      - "Use a dashed connector into a bordered prompt box to mark 'you predict, we reveal'"
      - "Reveal the withheld answer only on the NEXT slide — force a prediction first"
      - "Prefer this where the intuitive guess is WRONG, so the reveal corrects a misconception"

  incremental_visual_styling_loop:
    description: "Teach visual/markup domains by applying ONE property/element at a time and immediately rendering the change — the payoff is a SEEN visual delta, not just a new code line (visual analogue of progressive_code_reveal)"
    observed_in:
      - "HTML/CSS S1: a Tourism page built element-by-element — h1 appears → p appended → button appended, each on its own slide"
      - "HTML/CSS S2: styling arc color:blue (heading) → color:grey (paragraph) → background-color:lightblue (.card), each an apply→render step"
      - "CSS Part 1: one structural step (wrap in div, render unchanged) then one styling step (class='h-center', render centered) — each rendered before the next"
    rules:
      - "Change exactly one property/element per step and render the result before adding the next"
      - "Keep the same running artifact (one page/card) across the session so every change is a visible diff"
      - "Sequence content before chrome (text styling before container/background)"
      - "Separate structural steps from styling steps — never bundle a wrapper change and a style change into one reveal"

  contrastive_prompt_quality_demo:
    description: "Teach prompt quality by showing a weak prompt and its poor output, then an improved prompt and its better output — the prompt is the 'code' and a vague prompt is the 'error' (prompt-domain analogue of deliberate_error_exposure)"
    observed_in:
      - "GenAI S4: 'Write a resume.' → 'Can you improvise the prompt?' → detailed prompt with sections/tips"
      - "GenAI S4: bare 'What is generative AI?' vs the same targeted at a 'first-year B.Tech student with examples in apps like ChatGPT'"
      - "GenAI S4: 'How to prepare for exams?' vs a context-loaded version (exams in two weeks, revision + breaks + hard subjects)"
    rules:
      - "Present the naive short prompt first; let its weakness be felt before improving it"
      - "Improve by adding ONE specific missing dimension (role, context, constraints, format) so the lesson is legible"
      - "Show both prompts' resulting outputs so the causal link (better prompt → better output) is explicit"

  capability_menu_with_selection_judgment:
    description: "For fast-moving tool/model landscapes, teach a MENU of options plus the judgment for when to use which — selection skill over memorization"
    observed_in:
      - "GenAI S2: six model categories, each definition → strengths → named top models → example task, closing 'choose the best LLM depending on your needs'"
      - "GenAI S4: Zero/One/Few-shot each taught, then unified in a 'when it is best' table"
      - "GenAI S2/S3: repeated 'try Claude, Gemini, and Llama' + daily-limit notes — tool substitution taught as a skill"
    rules:
      - "Present options as a labeled menu; give each a one-line 'best when…' criterion"
      - "End with an explicit selection heuristic ('choose depending on your needs/task')"
      - "Name real current exemplars but frame them as interchangeable/expiring — encourage trying multiple"

# ─── SESSION STRUCTURE PATTERNS ─────────────────────────────────────────────────

session_patterns:

  concept_explainer_flow:
    description: "Standard flow for explaining a new concept"
    pattern:
      - "WELCOME"
      - "Recap (prior session key points)"
      - "Agenda (what we'll cover today)"
      - "Motivation (why this matters — industry context, real-world applications)"
      - "Analogy (real-world analogy before the concept)"
      - "Bridge (connect to what they already know — comparison tables)"
      - "Core concept (definition + explanation, progressive reveal)"
      - "Code examples (progressive code reveal — build up step by step)"
      - "Practice (worked examples, then independent practice)"
      - "Key Takeaways (Part 1/N, mirrors agenda)"
      - "Next Session (preview what comes next)"
      - "ALL THE BEST"

  coding_practice_flow:
    description: "Standard flow for a coding practice walkthrough session"
    pattern:
      - "WELCOME"
      - "Recap"
      - "Agenda"
      - "Platform introduction (if first time)"
      - "Question walkthrough (description → approach → code → test → debug → submit)"
      - "Feature exploration (AI tutor, save, reset, settings)"
      - "Key Takeaways"
      - "Next Session"

  project_building_flow:
    description: "Standard flow for a project building session"
    pattern:
      - "WELCOME"
      - "Topics overview (what we'll build)"
      - "Initial setup (IDE, repo, starter code)"
      - "Architecture overview (MERN stack diagram, component tree)"
      - "Incremental building (component by component, feature by feature)"
      - "Testing each increment"
      - "Key Takeaways"

  framework_intro_flow:
    description: "Session 1 of a project-building framework/library track (e.g. ReactJS)"
    pattern:
      - "WELCOME"
      - "Session title"
      - "Stack context (name the stack, e.g. MERN; architecture flow diagram; highlight the piece being taught)"
      - "Topics to be Covered (whole-course checklist — macro scope)"
      - "Agenda for Today (single-session chevron — micro scope)"
      - "Motivation (what it is → why: perf/less-code/reusable → top companies → download trends chart)"
      - "Session Initial Setup (screenshots of the real IDE/workspace/terminal — followable click-path)"
      - "Vanilla baseline (build the target artifact the known way → run → show output)"
      - "Framework rebuild (same artifact the new way, side-by-side old/new with logo tags, matched output)"
      - "Progressive build of the working snippet (imports → module → create → root → render)"
      - "New-syntax bridge (JSX shown, 'compiles to' the API just learned)"
      - "Key Takeaways (green checks, mirror agenda)"
      - "Practice"
      - "Next Session preview"
      - "THANK YOU / ALL THE BEST"
    observed: "ReactJS 'Introduction to React JS' sample project deck (44 slides)"

  project_track_intro_flow:
    description: "Opener for a project-building track that motivates and previews capstones (e.g. GenAI)"
    pattern:
      - "WELCOME"
      - "'Your Learning Journey' title (aspirational subtitle: 'From X-curious to X-confident')"
      - "Motivation (the field is changing rapidly — visual escalation device)"
      - "Relevance (grid of familiar consumer products powered by the tech)"
      - "Stakes (cited disruption statistic + urgency/worried-character framing)"
      - "Transition ('Your Path to Excellence')"
      - "Concepts You Will Learn (outcome-phrased chevrons, not topic names)"
      - "Projects You Will Build (one data-flow pipeline diagram per capstone)"
      - "THANK YOU / ALL THE BEST"
    observed: "GenAI sample project deck (14 slides)"

  new_language_intro_flow:
    description: "Standard flow when introducing a new programming language"
    pattern:
      - "WELCOME"
      - "Analogy (driving a car)"
      - "Bridge (common aspects between languages)"
      - "Differences (what's actually new)"
      - "Why this language (industry context, companies, facts)"
      - "Language comparison (known vs new — side by side)"
      - "First program (Hello World — compare with known language)"
      - "Progressive syntax introduction (each feature compared with known language)"
      - "Practice questions (in both languages for comparison)"
      - "Key Takeaways"

  stl_container_flow:
    description: "Standard flow for teaching STL container sessions (C++-only or selective Python comparison)"
    pattern:
      - "WELCOME"
      - "Session title (C++ STL : Container Name)"
      - "Agenda (2-3 containers/topics with chevron flow)"
      - "For each container:"
      - "  Section break slide (just the container name)"
      - "  Introduction (definition with key terms bolded in dashed box)"
      - "  Bridge from known (arrays → vectors, or Python list → vector)"
      - "  Declaration and Initialization (C++ vs Python if applicable)"
      - "  Operations (progressive push/pop/insert/erase with Before/After visuals)"
      - "  Quiz Time!"
      - "  Practice Problem (problem statement → step-by-step walkthrough → code)"
      - "Key Takeaways (Part 1/N, green checkmarks)"
      - "THANK YOU"
      - "ALL THE BEST"
      - "Supplementary slides (advanced topics, real-world problems)"
    observed: "C++ STL Pair & Vector, C++ STL Queue & Priority Queue, C++ STL Sets, C++ STL Deque & Stack, C++ STL Maps — all follow this structure"

  bridge_course_flow:
    description: "Standard flow for bridging from a known language to a new one (mid-course sessions)"
    pattern:
      - "WELCOME"
      - "Session title (Language B | Topic)"
      - "Agenda (3-4 items with visual chevron flow)"
      - "Section header (Topic: Language A vs Language B with both logos)"
      - "Definition/Introduction (formal definition with key terms bolded)"
      - "Syntax comparison (Language A left, Language B right, dashed separator)"
      - "Code example with Input/Output boxes"
      - "Sub-concepts (progressive reveal or annotation)"
      - "Quiz Time! (after each major concept)"
      - "Comparison table (feature rows, Language A and Language B columns)"
      - "Key Takeaways (bullet points with green checkmarks)"
      - "THANK YOU"
      - "ALL THE BEST"
      - "Practice Problems (problem statement → side-by-side solutions in both languages)"
    observed: "C++ Functions, C++ Loops and Arrays, C++ Operators/Type Conversion/Conditionals — all follow this exact structure"

  stl_algorithm_flow:
    description: "Flow for teaching free-function STL algorithms (not containers) — organized by function family, each taught as a signature contract applied uniformly across array/vector with matched I/O"
    pattern:
      - "WELCOME → title (e.g. C++ Utility Functions) → Agenda (Sorting → Max/Min/Find → Permutations chevrons)"
      - "For each algorithm: 'About' slide (what it does + which <header>) → annotated signature (first/last iterators, 'includes start, excludes end')"
      - "Apply to array → apply to vector (same algorithm back-to-back, to establish generality)"
      - "Variants as incremental modifiers (default → greater<int>() → custom comparator → subarray/range → 2D)"
      - "Quiz Time! between families → Key Takeaways → THANK YOU / ALL THE BEST → supplementary coded problems"
    observed: "C++ S10 (Utility): sort → max_element/min_element/find → next_permutation/prev_permutation"

  complexity_analysis_flow:
    description: "Flow for teaching algorithm-efficiency analysis (time/space complexity)"
    pattern:
      - "WELCOME → title (Analyzing Algorithm Efficiency : Time/Space Complexity)"
      - "Agenda (Introduction → Complexity → Asymptotic Notation / Key Takeaways)"
      - "Motivation illustration + formal definition of the metric"
      - "Intuition builder (linear vs exponential resource tables; constant/linear/quadratic examples)"
      - "Method statement (step-counting formula; memory-cell counting)"
      - "Worked problems, escalating (single loop → conditional → nested loop) via algorithm_step_trace_annotation"
      - "Cross-algorithm complexity_growth_table with substitutions and verdicts"
      - "Abstraction layer (Big O/Ω/Θ, growth-curve graph, simplification rules)"
      - "Optimization refactor (Socratic 'can we reduce this?' → improved code)"
      - "Key Takeaways → THANK YOU / ALL THE BEST"
    observed: "DSA S2 (time complexity), DSA S3 (space complexity)"

  pseudocode_intro_flow:
    description: "Short flow for introducing language-agnostic pseudocode"
    pattern:
      - "WELCOME → definition (language-agnostic algorithm representation)"
      - "Problem statement → numbered pseudocode → C++ implementation → Python implementation"
      - "THANK YOU / ALL THE BEST"
    observed: "DSA S4 (Pseudo Code, 9p)"

  html_css_markup_flow:
    description: "Flow for HTML/CSS markup/styling sessions — build one visible artifact incrementally, code always paired with rendered output"
    pattern:
      - "WELCOME + session title"
      - "Recap (heavy in the CSS decks — a full re-derivation of prior syntax)"
      - "Agenda (chevron of sub-topics with callout labels)"
      - "Driving question + before→after rendered goal states of today's artifact (goal_state_preview)"
      - "Motivation (frontend importance / MNC-salary lever; tooling choices backed by sourced stats)"
      - "Tooling/environment (browser + Code Playground desktop & mobile preview)"
      - "Decompose the target artifact into named parts (real screenshot with labeled orange boxes: Image/Heading/Paragraph/Button)"
      - "Per element/property: section-break (mascot 'How to add X') → syntax-anatomy diagram (labeled braces; template before instance) → code slide with the new line/attribute highlighted, PAIRED with rendered output → (CSS) color swatch → isolated rendered 'after'"
      - "Quiz Time! → Key Takeaways (mirror agenda) → Practice (+ Feedback) → Next Session → THANK YOU / ALL THE BEST"
    observed: "HTML/CSS S1 (HTML intro), CSS Part 1 (syntax, div, class attribute), S2/S3 (CSS color & background)"

  tool_walkthrough_flow:
    description: "Flow for teaching third-party AI tools/platforms as followable 'how to use' recipes (breadth over one tool)"
    pattern:
      - "WELCOME + reflective hook ('think of a task where AI could help')"
      - "Agenda (chevron of tools/capabilities, re-shown between sections)"
      - "Per tool: Problem Statement (the pain it removes) → one-line 'what it does' on a logo section-break → 'How to Use' numbered step tracker (usually 3, completed steps ticked green) → per-step screens → Advantages → Similar Tools (2-3 alternatives)"
      - "Reflection prompt → Quiz Time!"
      - "Key Takeaways → Practice → Feedback → THANK YOU / ALL THE BEST"
      - "'Stay Updated' meta-slide (how to keep current)"
    observed: "GenAI S2 (capabilities tour), GenAI S3 (Gamma / Code2Tutorial / ChatGPT features)"

  prompt_engineering_concept_flow:
    description: "Flow for a prompt-engineering concept session"
    pattern:
      - "WELCOME → hook (a bad-response question) → contrastive weak-vs-improved prompt demo"
      - "Define prompt / prompt engineering → 'why it matters' grid → intern analogy"
      - "Framework taught one component per slide, each accumulating onto a running example prompt (CRAFT/RCAFT: Role → Context → Action → Format → Tone)"
      - "Frameworks menu (RCAFT/STAR/RISEN) → shot techniques (Zero/One/Few) with a 'when best' table"
      - "Templates with {{variables}} (separate data from instructions) → System/User/Assistant roles → iteration"
      - "Quiz → Key Takeaways → Practice → Next Session"
    observed: "GenAI S4 (Prompt Engineering Fundamentals)"

  no_code_workflow_build_flow:
    description: "Flow for building a multi-service no-code AI automation end-to-end (the 'code' is node config + prompts, not source — distinct from project_building_flow)"
    pattern:
      - "Recap of prior concepts → hook ('Can an LLM do this alone?')"
      - "Anchor pipeline diagram (re-shown throughout with the active stage/LLM badge highlighted)"
      - "Workflow concept + manual-vs-automated time contrast → applications"
      - "Building blocks (nodes/modules/connections) → list account/API pre-requisites up front"
      - "Per-step build: add node → configure → paste the exact prompt (one node per slide), master step-tracker re-shown between steps"
      - "Real-world friction notes → scheduling → testing (trigger → content-quality → end-to-end) + Common Issues"
      - "(optional) rebuild the same pipeline in a second platform → Quiz → Key Takeaways → Practice"
    observed: "GenAI S5 (Social Media Content Automation — built in n8n, then rebuilt in Make.com)"

# ─── CROSS-CUTTING PATTERNS ─────────────────────────────────────────────────────

cross_cutting:

  comparison_table_pattern:
    description: "Use comparison tables whenever contrasting two things"
    examples:
      - "Python S2: JavaScript vs Python (output function, semicolons, parentheses, quotes)"
      - "C++ S1: Compiler vs Interpreter table"
      - "C++ S1: float vs double (precision, memory, default type)"
    rules:
      - "When comparing language A vs B: use a structured table with named aspects"
      - "When comparing approaches: show pros/cons in visual format"
      - "Tables should have column headers and at most 5-6 rows per slide"

  error_teaching_pattern:
    description: "Deliberately show errors to teach debugging"
    examples:
      - "C++ S1: show type mismatch error, explain error message line by line"
      - "Python S3: Test Case - Fail → Difference between Outputs → Correcting Code → Test Case - Pass"
    rules:
      - "Show common errors DELIBERATELY — don't just show correct code"
      - "Walk through the error message (what does each line mean?)"
      - "Show the fix process: identify error → understand why → fix → verify"
      - "Frame errors positively ('errors are how you learn')"

  visual_data_structure_pattern:
    description: "Use visual representations for abstract data structures"
    examples:
      - "DSA S1: visual icons for Arrays, Linked Lists, Stacks, Queues, Trees, Graphs"
      - "ReactJS: component tree diagrams, HTML DOM tree, lifecycle phase diagrams"
      - "Coding Illustrations: 251 pages of branded visual assets"
      - "C++ STL Vector: Array blocks with indices (0, 1, 2...) and Before/After rows for every operation"
      - "C++ STL Queue: Horizontal cells with Front/Rear pointer labels, updated on every push/pop slide"
      - "C++ STL Priority Queue: Vertical stack with dashed border and Top pointer arrow — consistent across all 5 push slides"
      - "C++ STL Set: Mathematical curly brace notation { } with elements, green arrow showing state transitions"
    rules:
      - "Every data structure must have a visual representation"
      - "Use branded illustration style (vector, freepik-sourced)"
      - "Diagrams should build up incrementally (not show the full complex diagram at once)"
      - "Container state must be shown on EVERY operation slide — never drop the visual"
      - "Each container type has a consistent visual idiom: arrays use blocks+indices, queues use horizontal cells+pointers, stacks/PQs use vertical stacks+Top pointer, sets use curly braces"

  supplementary_content_pattern:
    description: "Optional/advanced content placed after the closing slides for self-paced reference"
    examples:
      - "C++ STL Pair & Vector: Safe Access .at() slides (pp 81-82) placed AFTER THANK YOU / ALL THE BEST"
      - "C++ STL Queue & Priority Queue: Emergency Room real-world problem with full class code (pp 63-68) AFTER closing"
      - "C++ STL Sets: Iteration slides and additional problem statements (pp 76-80) AFTER closing"
    rules:
      - "Core session ends at THANK YOU / ALL THE BEST — this is the natural stopping point for live delivery"
      - "Supplementary slides follow closing for: advanced topics, real-world application problems, additional API methods"
      - "Supplementary content should be self-contained (not dependent on live explanation)"
      - "Use for content that motivated learners can explore asynchronously"

  stack_context_map:
    description: "Before teaching a technology, place it inside its larger stack/architecture with a 'you are here' diagram"
    examples:
      - "ReactJS S1 (sample): MERN definition (MongoDB/Express/React/Node) + application-flow diagram (React=client ⇄ Node/Express=server ⇄ MongoDB=db), React highlighted in an orange box, BEFORE defining React"
    rules:
      - "For framework/library/tool domains, open with where the tech sits in the whole architecture, then zoom into the piece being taught"
      - "Pair a macro scope (whole-course/whole-stack) with the micro scope (today's session) on consecutive slides"

  api_signature_annotation:
    description: "Teach a function/API contract by annotating its signature with braces pointing to each argument"
    examples:
      - "ReactJS S1 (sample): React.createElement(type, props, children) with up/down braces labeling 'tag name / properties / child nodes', then green-checked expansions of each"
      - "GenAI/tool APIs: label each parameter with what it controls and give 2-3 concrete example values"
      - "CSS Part 1: ruleset TEMPLATE 'selector { property1: value1; }' (green Ruleset brace) → concrete '.h-center { text-align: center; }' with SELECTOR/PROPERTY/VALUE label boxes — each syntax role keeps ONE color across template, instance, and label (selector=red, property=orange, value=blue)"
      - "CSS Part 1: generic attribute template '<tag attribute=\"value\">Content</tag>' with labeled braces taught BEFORE the concrete '<h1 class=\"h-center\">Tourism</h1>' instance"
    rules:
      - "When introducing an API call, annotate the signature itself — don't just describe it in prose"
      - "Follow the annotated signature with concrete example values for each parameter"
      - "Teach the generic template first, then instantiate it — and keep one color per syntax role, reused across the template, the concrete instance, and the label boxes"

  project_as_pipeline:
    description: "Scope a project (esp. GenAI/integration projects) as a left-to-right pipeline of processing stages, not a feature list"
    examples:
      - "GenAI (sample): Social Media Automation = List articles → Summarize → Generate platform content → Asset handling → Auto-post (numbered stages)"
      - "GenAI (sample): AI News Summarizer = Fetch news → Summarize with Gemini → Deliver newsletter; the LLM is ONE stage among fetch/deliver stages"
      - "GenAI (sample): pipelines name real services as endpoints — Gemini, Telegram, Amazon, Google Docs, Google Calendar"
    rules:
      - "Present integration/AI projects as a data-flow pipeline of labeled stages with arrows, each stage an icon + short label"
      - "Show the LLM/model as one stage among fetch/transform/deliver stages — foreground orchestration, not model internals"
      - "Name the real external tools/services students will wire together (tool-orchestration literacy)"
      - "Phrase learning outcomes as capabilities ('build X without coding', 'save hours weekly'), not topic names"

  motivation_lever_varies_by_domain:
    description: "The emotional lever used to motivate differs by domain — match it"
    examples:
      - "C++/DSA: aspiration/impressiveness ('NASA uses C++ for flight software', competitive-programming stats)"
      - "GenAI (sample): adapt-or-fall-behind urgency ('22% of jobs disrupted by 2030', WEF 2025, worried-character framing)"
      - "ReactJS (sample): pragmatic career/industry proof (top companies grid, npm download-trend chart vs Angular/Vue)"
    rules:
      - "Choose the motivation lever by domain: aspiration for foundational CS, urgency for fast-moving fields (GenAI), industry-adoption proof for framework choices"
      - "Always pair any statistic with a credible named source shown on the slide"

  variant_based_teaching:
    description: "Teach related data structure variants sequentially using identical API to highlight behavioral differences"
    examples:
      - "C++ STL Sets: Set (unique+sorted) → Multiset (duplicate+sorted) → Unordered Set (unique+unordered) — same operations (insert, erase, find, size, empty, clear, swap) for each"
      - "C++ STL Priority Queue: Max-Heap → Min-Heap — same operations, different declaration syntax"
      - "C++ STL Maps: Map → Multimap → Unordered Map — same pattern (from prior analysis)"
    rules:
      - "When teaching variants of a data structure, use the SAME API operations in the SAME order for each variant"
      - "Highlight behavioral differences through contrast (sorted vs unsorted, unique vs duplicate) rather than through separate conceptual explanations"
      - "Each variant section gets its own section break slide and Quiz Time!"

  matched_output_code_slide:
    description: "Show each runnable example as a consistent two-box slide: a bordered code panel tagged with a language pill, only the lines-of-interest highlighted (boilerplate left quiet), and the result in a separate box tagged with an 'Output' pill — output often revealed on a second slide"
    examples:
      - "C++ S2: stoi/stod slides — orange box around the 3 relevant lines, green Output pill (123 / 3.14159); #include/main left un-highlighted"
      - "C++ S4: function examples use the same code-then-Output reveal"
      - "CSS Part 1: the pill idiom generalizes to markup — every panel tagged HTML or CSS; 'Combining HTML & CSS' shows an HTML-pill panel and a CSS-pill panel side by side; newly-added lines (div tags, class attribute) boxed orange while the rest stays quiet"
    rules:
      - "Tag each code panel with a language pill so multi-language slides are unambiguous; tag results with a distinct 'Output' pill"
      - "Highlight ONLY the lines that carry the concept; leave boilerplate visually quiet"
      - "Reveal output on a separate slide after the code so learners can predict it first"

  use_case_data_table_motivation:
    description: "Motivate a keyed/associative structure by walking a realistic dataset table and iteratively discovering WHY a naive design fails — reaching the correct design by elimination"
    examples:
      - "C++ S9 (Maps): 'store all citizens' → table (Name/Gender/Place) → 'names aren't unique, can't be key' → add Aadhaar column → adopt Aadhaar as key"
    rules:
      - "Motivate keyed structures with a concrete dataset table before the definition, not a one-line analogy"
      - "Introduce the correct design by proposing and refuting a naive one (active elimination)"
      - "Grow the table across slides so the fix is visibly motivated by the failure"

  iterator_result_caveat_box:
    description: "When an STL function returns an iterator (not a value), a repeated highlighted 'Important note' box warns it must be dereferenced with *"
    examples:
      - "C++ S10: identical 'result is an iterator, not the value; dereference with *' box for max_element, min_element, and find"
    rules:
      - "Flag return-type gotchas (iterator vs value/bool) with a consistent, repeated callout across every function that shares the gotcha"
      - "Pair the caveat with the corrected usage inline (*max_element(...))"

  real_world_problem_capstone_pattern:
    description: "Close a data-structure session (in the supplementary zone) with ONE named real-world scenario whose natural solution IS this container — delivered as problem → ops → traced example → full class code"
    examples:
      - "C++ S7 Priority Queue: 'Emergency Room' — patients ranked by severity, ops A/T/D, worked trace, then a full EmergencyRoom class using priority_queue<pair<int,string>>"
      - "C++ S6 Stack: 'SpecialStack' with O(1) getMin, two-stack (main + min) class code"
      - "C++ S6 Deque: online food-delivery order-management (AF/AB/RF/RB/D)"
    rules:
      - "End each data-structure session with exactly one named, domain-flavored problem whose natural solution is this container"
      - "Structure it as: problem statement → supported operations → worked I/O trace → full class implementation"
      - "Place it after THANK YOU/ALL THE BEST so live delivery can stop earlier but motivated learners get the applied payoff"

  algorithm_step_trace_annotation:
    description: "Teach time/space complexity by overlaying execution onto the source code — color-coded boxes tag each part (init/condition/updation/body) with dotted arrows to its runtime effect and per-iteration step count, accumulated into a closed-form expression"
    examples:
      - "DSA S2 Problem-1: for-loop with green box on condition, orange on i++, purple on cout body; 'Iteration 2 to N (3 steps each)' + 'loop break (2 steps)' summed to # Steps = 3N+2"
      - "DSA S2 Problem-3: nested loop reuses the 3N+2 inner cost → 3N²+4N+2"
      - "DSA S3: function annotated with memory cells a|b|c → 'memory spaces = 3'; array split into input O(n) vs auxiliary O(1)"
    rules:
      - "Overlay the analysis on the actual code: box each part, connect with a dotted arrow to its cost"
      - "Use a consistent color per role (condition=green, updation=orange, body=purple; failing condition=red), stable across slides"
      - "Accumulate per-iteration costs into an explicit closed form (3N+2, 3N²+4N+2), then reduce to Big O later"
      - "Reuse a previously derived cost as a building block for a more complex structure"

  complexity_growth_table:
    description: "Compare algorithms by tabulating step-count formulas against escalating input sizes, substituting concrete N values on-slide, so learners SEE divergence before Big O is introduced"
    examples:
      - "DSA S2: rows N=1,5,100,100000 for 3N+2 / 2 / 3N²+4N+2 with substitution shown; verdicts 'medium/less/maximum time'; then each column mapped to O(N)/O(1)/O(N²)"
    rules:
      - "Before naming Big O, build a formula-rows × increasing-N-columns table filled with computed values (show the substitution)"
      - "Escalate N dramatically (1 → 100000) so constants/lower-order terms visibly become negligible"
      - "Cap the table by mapping each column to its Big O class — the abstraction as a summary of data already seen"

  code_and_rendered_output_pairing:
    description: "Pair source code with its live browser-rendered result so cause (markup/style) and effect (visual) are seen together — the defining loop of markup/visual teaching"
    examples:
      - "HTML/CSS S2: 'Code' slide shows the <body> markup LEFT and the actual rendered card (heading, paragraph, 'Get Started' button) RIGHT"
      - "HTML/CSS S1: Code Playground desktop & mobile preview — HTML source pane left, rendered output pane right, 'Run Code' button"
      - "CSS Part 1 'Adding Div': div-wrapped HTML (new <div></div> tags boxed orange) paired with a deliberately UNCHANGED render; only after class='h-center' is added is the render re-shown centered — structure-only vs styling changes separated visually"
    rules:
      - "For markup/styling, always show the rendered output, not just code — source left, rendered result right"
      - "After applying a style, show the rendered 'after' state on its own so the change is unmistakable"
      - "Prefer the real in-product editor (split code/preview + Run) so slides mirror the tool students use"
      - "Show the render even when a structural-only edit leaves it UNCHANGED — proving structure and style are separate concerns"

  goal_state_preview:
    description: "Open the session with the target end-state as a driving question plus before→after views of the same artifact — the whole session then works toward one visible, promised goal"
    examples:
      - "CSS Part 1: 'How to Center the Heading, Paragraph, & Button Elements Horizontally?' with left-aligned vs centered Tourism-card renders joined by a green arrow — shown BEFORE any CSS is taught; the session ends by producing exactly that after-state via class='h-center'"
      - "GenAI S5 (related): manual process vs automated workflow time contrast shown before the build — the target state motivates the session"
    rules:
      - "Phrase the session goal as a question the learner cannot yet answer"
      - "Show the before and after states of the SAME artifact side by side (rendered/real, not described)"
      - "Anchor every intermediate concept as a step toward that one goal, and end by delivering the exact promised after-state"

  color_value_swatch_rendering:
    description: "When a CSS value is a color, render it as a literal swatch on the slide so the keyword maps to what the eye will see"
    examples:
      - "HTML/CSS S2: 'color: blue;' with 'Blue =' followed by a solid blue rectangle; 'background-color: lightblue;' with a light-blue swatch"
    rules:
      - "Represent every color value as an on-slide swatch next to the keyword"
      - "Place the swatch adjacent to the rule so value → appearance is a one-glance mapping"

  attribute_as_html_css_bridge:
    description: "Teach the HTML class attribute as the explicit connective tissue between an element and a CSS ruleset — decomposed into Attribute Name (class) and Attribute Value (selector), with the added attribute highlighted"
    examples:
      - "CSS Part 1 (the original teaching): HTML panel left / CSS panel right with language pills, then 'With the help of Attribute, we can combine HTML and CSS' → attribute anatomy → explicit rule slide: 'class name in HTML and Selector name in CSS must be the same, then only the styling will be applied correctly' (pointing-character emphasis)"
      - "HTML/CSS S2: 'Combining HTML & CSS' — 'Attribute Name - class' / 'Attribute Value - main-heading' ties the .main-heading ruleset to the <h1>"
      - "HTML/CSS S2: newly-added class='paragraph' / class='card' boxed in orange in otherwise-unchanged markup"
    rules:
      - "Name the wiring mechanism explicitly (class attribute) and split it into name vs value"
      - "Box/highlight the attribute added to the HTML so learners see exactly what changed"
      - "Reinforce that the selector name (.x) and the attribute value (x) are the same token"
      - "State the matching requirement as an explicit rule slide with emphasis — it is the #1 silent failure mode for beginners"

  tooling_onboarding_walkthrough:
    description: "Teach real project scaffolding by walking the actual terminal/IDE flow with labeled screenshots — command → interactive prompts → generated folder tree → config → install → run → live output — not abstract description"
    examples:
      - "ReactJS S4: 'npm create vite@8.0.2' → screenshot of Vite's interactive prompts → generated myapp tree (public/src boxed) → 'npm install' → 'npm run dev' → 'Checking the Output' dev-server URL popup"
    rules:
      - "Show each command in its own Terminal-labeled block using the real course-IDE prompt string"
      - "Screenshot the tool's actual output (scaffolder prompts, file tree, dev-server URL) — don't paraphrase"
      - "Flag environment-specific steps as skippable ('specific to our IDE; you may not need this locally')"
      - "Sequence strictly: scaffold → prompts → folder tree → config → install → run → verify"

  api_equivalence_summary_grid:
    description: "Close a 'build the same artifact N ways' arc with a side-by-side grid mapping each approach's key API calls, so learners see the through-line (reinforces bridge_from_known_to_unknown)"
    examples:
      - "ReactJS S2 'Summary': three logo-headed columns — vanilla JS (document.createElement/appendChild), React (React.createElement/createRoot().render), React+JSX (<h1>…</h1>/createRoot().render)"
    rules:
      - "After teaching the same result via progressive equivalent approaches, add one recap grid aligning the corresponding call in each column"
      - "Head each column with the approach's logo/icon for instant recognition"

  mock_tool_ui_prompt_card:
    description: "Make 'use the AI this way' ideas concrete with a stylized mock chat/prompt UI (input box, avatar, sample prompt, target-model logos) rather than plain body text"
    examples:
      - "GenAI S2: Trending Reels / Local Recommendations / Financial Updates each shown as a prompt card with input box + Gemini/ChatGPT/Claude logo trio"
      - "GenAI S4: role/context prompts rendered as avatar speech-bubble cards with the newly-added part bold"
    rules:
      - "Show the concrete example prompt inside a branded mock input box, not as plain text"
      - "Attach the relevant model logos so learners know which tools apply"
      - "Bold/foreground the part of the prompt that illustrates the current teaching point"

  real_world_friction_note:
    description: "Distinct pink/amber 'Note / Important' callouts that surface current external-tool friction (paywalls, rate limits, API errors, UI drift) — teaching operational resilience, not just the happy path"
    examples:
      - "GenAI S5: 'X Developer Portal moved to pay-for-use → posting to X not possible with new accounts'"
      - "GenAI S5: 'Common Issues' — 402 (post too long), auth failures, rate limiting; free-tier Gemini rate-limit → 'use an alternate API key'"
      - "GenAI S5: 'n8n changed the Active button to Publish' UI-drift note"
    rules:
      - "Flag known external failure modes and platform changes in a visually distinct callout"
      - "Give the concrete workaround (alternate API key, keep posts short, use a business account)"
      - "Acknowledge live tools drift ('this button may now be named X') — set expectation the UI won't match exactly"
```

---

## 4. Stack-specific pedagogy overlays

The universal file above applies everywhere. What follows is the **per-stack distillation** — what is distinctive about each stack's teaching, which flows dominate, and which levers/policies to apply. Use these when generating stack-scoped content.

### 4.1 C++ (bridge-course stack — learners already know Python)

- **Dominant flows:** `bridge_course_flow` (operators/loops/functions), `stl_container_flow` (all STL containers), `stl_algorithm_flow` (free functions), `new_language_intro_flow` (S1).
- **Comparison-language policy:** C++ vs Python side-by-side by default (dashed orange separator, language logo pills) — but **drop Python selectively** where no clean equivalent exists (do-while, switch, queue/PQ/sets/maps/utility algorithms). Never force a confusing comparison.
- **Distinctive patterns:** `matched_output_code_slide` (language pill + orange lines-of-interest + green Output pill, output on next slide), token-level syntax annotation (one token per slide), `variant_based_teaching` (Set→Multiset→Unordered Set with identical API order), `use_case_data_table_motivation` (Aadhaar table for Maps), `iterator_result_caveat_box`, `real_world_problem_capstone_pattern` (Emergency Room / SpecialStack / food-delivery deque — placed after ALL THE BEST).
- **Motivation lever:** aspiration/impressiveness (NASA/F-35 facts, competitive-programming stats).
- **Practice:** graduated problems (Easy→Medium→Hard) in supplementary zone, often solved in both languages.

### 4.2 Python (first-language stack — learners know JavaScript)

- **Dominant flows:** `concept_explainer_flow`, `coding_practice_flow` (platform walkthrough).
- **Comparison-language policy:** JavaScript-left vs Python-right for nearly every concept + JS→Py API mapping tables (String()→str, parseInt()→int…).
- **Distinctive patterns:** `predict_the_output_challenge` (known case shown, twist case withheld to next slide — used where intuition is WRONG: "1"+"2", "*"+10, string immutability), deliberate TypeError exposure with real tracebacks, annotated slicing syntax diagrams, 4-slide progressive slicing variations on one example string.
- **Motivation lever:** platform/tool mastery + metacognition (how to learn a language, ~30 days first language).
- **Session cadence:** 2 Quiz Time! breaks mid-session; Recap ↔ Key Takeaways bookend; Next Session preview.

### 4.3 DSA (analysis stack — language-agnostic reasoning)

- **Dominant flows:** `complexity_analysis_flow` (time/space), `pseudocode_intro_flow`, concept-explainer for structures (S1).
- **Distinctive patterns:** `algorithm_step_trace_annotation` (color-coded loop parts: condition=green, updation=orange, body=purple; closed-form step counts 3N+2 → 3N²+4N+2), `complexity_growth_table` (formulas × escalating N with on-slide substitution BEFORE naming Big O), Socratic optimization refactors ("can we reduce space?" before the improved code), reuse of previously derived costs as building blocks.
- **Visual idioms:** every structure has a consistent visual (arrays=blocks+indices, queues=horizontal cells+Front/Rear, stacks/PQs=vertical+Top, sets=curly braces); container state shown on EVERY operation slide.
- **Motivation lever:** real-world application breadth (search engines, social media, healthcare, finance).
- **Bridge policy:** pseudocode → C++ → Python (language-agnostic first, then both implementations).

### 4.4 HTML/CSS (markup/visual stack — output is SEEN, not printed)

- **Dominant flow:** `html_css_markup_flow`.
- **Distinctive patterns:** `goal_state_preview` (driving question + before→after rendered states at session start), `code_and_rendered_output_pairing` (source left, rendered result right; render shown even when a structural edit leaves it UNCHANGED — structure ≠ style), `incremental_visual_styling_loop` (one property per step, render each), `color_value_swatch_rendering`, `attribute_as_html_css_bridge` (class attribute anatomy + explicit "class name must equal selector name" rule slide), syntax-anatomy braces with one consistent color per syntax role across template/instance/label.
- **Running artifact:** ONE page (the Tourism card) built and styled across sessions — every change is a visible diff.
- **Motivation lever:** career/salary framing (frontend importance, MNC requirements) + sourced stats even for tooling (Chrome ~89.1% India share, gs.statcounter).
- **Track note:** the track interleaves an AI-assisted-learning meta-skill session (Perplexity/NotebookLM) — pedagogy expects learners to use GenAI to accelerate learning.

### 4.5 ReactJS (framework stack — learners know HTML/CSS/JS)

- **Dominant flows:** `framework_intro_flow` (S1/JSX), then concept-then-project sessions; `tooling_onboarding_walkthrough` for app scaffolding.
- **Distinctive patterns:** `stack_context_map` (MERN "you are here" diagram before defining React), matched-output proof (build Hello World vanilla → rebuild identical in React → JSX as "compiles to" sugar), `api_equivalence_summary_grid` (vanilla vs React vs JSX API columns), git-style red/green diffs when replacing lines, `api_signature_annotation` (createElement/props signatures), deliberate lowercase-component failure demo, real IDE/terminal screenshots with environment-specific steps flagged skippable.
- **Motivation lever:** pragmatic industry proof (top companies, npm download-trend charts vs Angular/Vue, "Evan You created Vite" credibility facts).
- **Gap:** no analyzed deck covers Lists/Keys, State, Events, or Routing — do not claim observed patterns there.

### 4.6 GenAI (applied/no-code stack — tool orchestration, fast-moving landscape)

- **Dominant flows:** `project_track_intro_flow` (track opener), `tool_walkthrough_flow` (capabilities/tools), `prompt_engineering_concept_flow`, `no_code_workflow_build_flow` (capstone builds in n8n/Make.com).
- **Distinctive patterns:** `project_as_pipeline` (LLM is ONE stage among fetch/transform/deliver; real services named: Gemini, Telegram, Amazon, Google Docs/Calendar), `contrastive_prompt_quality_demo` (weak prompt → poor output → improved prompt → better output; the prompt IS the code), `capability_menu_with_selection_judgment` (model/tool menus + "best when…" criteria; exemplars framed as interchangeable/expiring), `mock_tool_ui_prompt_card` (branded mock chat UI with model logos), `real_world_friction_note` (pink/amber callouts: paywalls, rate limits, 402 errors, UI drift — with concrete workarounds), progressive PROMPT reveal (Role→+Context→+Action→+Format→+Tone).
- **Motivation levers:** urgency ("22% of jobs disrupted by 2030", WEF cited on-slide) for the track; pragmatic time-saving ("30–45 min → <2 min") for workflows.
- **Assessment note:** per the GenAI packaging profile, expect project + coding evidence alongside conceptual checks; topic phases run Problem framing → Architecture and concepts → Guided build → Checkpoint and quiz.

---

## 5. Eval set — checkable criteria per principle, applied to stacks

Machine-usable rubric for judging generated session/slide content against the intelligence. Each item: a check question, pass criteria, and stack-specific pass examples drawn from observed evidence. Scoring suggestion: pass/fail per applicable item; report failures with the slide/section that violates.

```yaml
eval_set:
  version: 1
  scope_note: >
    Items marked applies_to: all are universal. Stack-conditional items apply only when
    the artifact's stack/delivery form matches. "Course context" = the packaging profile
    in force (quiz cadence, unit mix, phase labels).

  items:
    - id: E01
      key: incremental_learning_progression
      applies_to: all
      check: "Does every new concept build on something already established, with exactly ONE new concept per slide/section?"
      pass: "No slide introduces two new concepts; each session opens with a recap; complexity ramps simple → general → edge."
      stack_examples:
        cpp: "STL session introduces Pair before Vector before iterators."
        dsa: "Step counting taught on a single loop before nested loops reuse the derived 3N+2."
        htmlcss: "h1 added and rendered before p, before button."

    - id: E02
      key: analogy_before_abstraction
      applies_to: all
      check: "Does each abstract concept get a concrete, structurally-mapping analogy BEFORE its formal definition?"
      pass: "Analogy present, uses everyday objects, and maps structurally (not decorative)."
      stack_examples:
        cpp: "VIP queue for priority_queue (VIP = higher priority = served first)."
        genai: "LLM as a new intern who needs explicit instructions, before defining prompt engineering."
        htmlcss: "Boxes packed into a container onto a truck, before div syntax."

    - id: E03
      key: bridge_from_known_to_unknown
      applies_to: stacks_with_prior_language   # cpp (from python), python (from js), react (from js/html)
      check: "Is the known language/framework shown side-by-side, with SAME highlighted before DIFFERENT — and is the comparison DROPPED where it would confuse?"
      pass: "Side-by-side with separator + language tags where an equivalent exists; no forced comparison for constructs without equivalents (e.g. do-while, priority_queue)."
      stack_examples:
        cpp: "For/While shown C++ left / Python right; do-while shown C++-only."
        python: "JS String()/parseInt() mapped to str()/int() in a table."
        react: "Vanilla DOM Hello World rebuilt identically in React, then JSX as compile-target."

    - id: E04
      key: cognitive_load_management
      applies_to: all
      check: "Max 30-40 words per slide, one idea per slide, complex reveals split across slides?"
      pass: "No text-wall slides; multi-part syntax/operations revealed progressively (build-up or annotation variant)."
      stack_examples:
        cpp: "Array syntax dissected one token per slide."
        genai: "CRAFT taught one letter per slide accumulating onto one running prompt."

    - id: E05
      key: contextual_and_applied_learning + motivation levers
      applies_to: all
      check: "Within the first ~10% of a new topic, is there a WHY with named companies/products/stats — using the RIGHT lever for the domain — and is every statistic paired with a named source?"
      pass: "Named examples (not 'many companies'); lever matches domain (aspiration=CS foundations, urgency=GenAI, industry-adoption=frameworks, career/salary=frontend); sources cited on-slide."
      stack_examples:
        cpp: "'NASA uses C++ for flight software'."
        genai: "'22% of jobs face disruption by 2030' — WEF 2025 cited."
        htmlcss: "Chrome mandated with ~89.1% India share, gs.statcounter cited."

    - id: E06
      key: skill_mastery_through_deliberate_practice
      applies_to: all
      check: "Is >=40% of session time active practice, with graduated Easy→Medium→Hard problems and try-before-solution framing?"
      pass: "Practice present, graduated, mapped to objectives; worked solutions provided after attempt prompt."
      stack_examples:
        cpp: "Swap → Find Max → Sum of Digits → Calculator (increasing complexity)."
        genai: "Guided build checkpoints in the workflow session."

    - id: E07
      key: active_recall + quiz cadence (course context)
      applies_to: all
      check: "Are questions posed BEFORE answers, with Quiz Time! breaks after each major concept (matching the packaging profile's classroom_quiz_every_minutes, default 20)?"
      pass: "2-3 quiz breaks per session interleaved (not only terminal); Socratic prompts precede reveals."
      stack_examples:
        python: "'What will be the output?' box before revealing '12' for '1'+'2'."
        dsa: "'Is there anything we can do to reduce space?' before the optimized return(a+b)."

    - id: E08
      key: spaced_repetition / bookend
      applies_to: all
      check: "Mandatory Recap at start; Key Takeaways mirroring the Agenda at end; Next Session preview present?"
      pass: "All three present; takeaways split into parts if long; recap reinforces the PRIOR session's keys."

    - id: E09
      key: progressive_code_reveal
      applies_to: code_stacks   # cpp, python, react, dsa
      check: "Is code built up (or annotated) across slides — never a complete block on slide one — with Input → Code → Output shown?"
      pass: "Build-up adds 1-2 lines per slide OR annotation highlights one element per slide; output revealed after prediction opportunity; git-style red/green for replacements."
      stack_examples:
        react: "createElement built up: imports → module → create → root → render; JSX diff shown red/green."
        genai: "Applies to PROMPTS too: Role → +Context → +Action → +Format → +Tone."

    - id: E10
      key: deliberate_error_exposure
      applies_to: all
      check: "Is at least one common pitfall shown BEFORE the correct usage, with expected-vs-actual outputs compared and the fix walked through?"
      pass: "Pitfall → real error/output → explanation → fix → verify sequence present where the construct has a known trap."
      stack_examples:
        cpp: "switch without break outputs 'A B'; then corrected."
        python: "'*' + 10 TypeError traceback, then str(10) fix."
        react: "lowercase component name silently treated as HTML tag."
        genai: "Vague prompt → poor output is the error-analogue (contrastive_prompt_quality_demo)."

    - id: E11
      key: visual_before_textual / visual_data_structure_pattern
      applies_to: all
      check: "When a concept has a visual model, is the diagram shown FIRST with REAL values (addresses, indices, iteration values), and is container/artifact state re-shown on every operation slide?"
      pass: "Diagram precedes syntax; live values not abstract shapes; consistent per-structure visual idiom maintained."
      stack_examples:
        dsa: "Loop flowchart before for-syntax; memory cells a|b|c before O(1)."
        cpp: "Queue cells with Front/Rear pointers updated on every push/pop slide."

    - id: E12
      key: matched_output_code_slide
      applies_to: code_stacks
      check: "Is every code panel tagged with a language pill, only concept-bearing lines highlighted, and the result in a distinct Output-tagged box?"
      pass: "Pill + selective highlight + separate output; boilerplate visually quiet."

    - id: E13
      key: code_and_rendered_output_pairing + goal_state_preview
      applies_to: markup_stacks   # htmlcss, and any UI-rendering stack
      check: "Is the rendered result paired with the source for every change (even unchanged renders after structural edits), and does the session open with a driving question + before→after goal states?"
      pass: "Source left/render right; unchanged render shown for structure-only edits; session ends by delivering the promised after-state."

    - id: E14
      key: variant_based_teaching
      applies_to: stacks_with_variant_families   # cpp STL, any API-family teaching
      check: "Are related variants taught sequentially with the IDENTICAL operation set in the IDENTICAL order, differences shown by contrast?"
      pass: "Same API sequence per variant; each variant gets its own section break + quiz."

    - id: E15
      key: algorithm_step_trace_annotation + complexity_growth_table
      applies_to: dsa
      check: "Is complexity derived by overlaying costs on the actual code (consistent role colors) into a closed form, then compared in a concrete-N growth table BEFORE Big O is named?"
      pass: "Closed-form expression accumulated on-slide; table substitutes real N values; Big O introduced as a summary of seen data."

    - id: E16
      key: tool_walkthrough_flow + capability_menu_with_selection_judgment
      applies_to: genai_and_tool_stacks
      check: "Does each tool open with the pain it removes, use a numbered green-tick step tracker, close with Advantages + Similar Tools, and teach WHEN-to-use-which rather than one canonical tool?"
      pass: "Problem statement first; 3-step tracker re-shown; alternatives named; selection heuristic explicit."

    - id: E17
      key: real_world_friction_note
      applies_to: genai_and_tool_stacks
      check: "Are known external failure modes (paywalls, rate limits, API errors, UI drift) flagged in distinct callouts WITH workarounds?"
      pass: "At least the known frictions of the tools used are surfaced; workaround given; UI-drift expectation set."

    - id: E18
      key: real_world_problem_capstone_pattern + supplementary_content_pattern
      applies_to: data_structure_sessions
      check: "Does the session close (after THANK YOU/ALL THE BEST) with ONE named domain-flavored problem whose natural solution IS the taught structure, as problem → ops → trace → full class code?"
      pass: "Capstone present in supplementary zone; self-contained; motivates the container."

    - id: E19
      key: api_signature_annotation
      applies_to: all
      check: "Are new API/syntax contracts annotated on the signature itself (template before instance, one consistent color per syntax role) rather than described in prose?"
      pass: "Braces/boxes label each slot; generic template precedes concrete instantiation; colors stable across template/instance/labels."

    - id: E20
      key: packaging alignment (course context)
      applies_to: all
      check: "Does the artifact respect the resolved packaging profile — unit mix, topic phase labels (e.g. GenAI: Problem framing → Architecture → Guided build → Checkpoint), quiz cadence, assessment types?"
      pass: "Session structure maps onto the profile's phase labels; quiz breaks match cadence; practice/assessment types match the allowed set."
```

---

## 6. Implementation examples — composing the intelligence per stack

Three worked skeletons showing how a generation agent should compose flows + patterns for a specific stack/course context.

### 6.1 C++ — "STL Map" session (bridge-course learner, Intensive/NIAT packaging)

1. WELCOME → title "C++ STL : Maps" → Agenda chevron (Map → Multimap → Unordered Map) — `stl_container_flow`
2. Motivate with a citizens dataset table; refute Name-as-key, add Aadhaar column, adopt unique key — `use_case_data_table_motivation`
3. Per variant (identical API order: insert, find, erase, count, size, swap, iterate) — `variant_based_teaching`:
   section break → dashed-box definition (key terms bold) → declaration → operations with key:value brace-stack state on EVERY slide (`visual_data_structure_pattern`) → each example as language-pill code panel, orange lines-of-interest, green Output pill on the NEXT slide (`matched_output_code_slide`, `predict_the_output_challenge`) → Quiz Time!
4. NO Python comparison (no clean equivalent policy)
5. Iterator access: annotated signature `it->first / it->second` + repeated "result is an iterator, dereference with *" callout — `iterator_result_caveat_box`
6. Key Takeaways (green checks, mirror agenda) → THANK YOU / ALL THE BEST
7. Supplementary: "Word Frequency Counter" capstone — problem → ops → trace → full class code — `real_world_problem_capstone_pattern`
8. Packaging check: quiz breaks ≈ every 20 min; skill-assessment items mcq+coding (E20)

### 6.2 HTML/CSS — hypothetical "Flexbox basics" session (applying the intelligence to a NEW session)

1. WELCOME → Recap of CSS Part 2 (color/background) → Agenda chevron
2. Driving question: "How to place the Heading, Paragraph & Button in a row?" + before→after renders of the SAME Tourism card joined by an arrow — `goal_state_preview`
3. Syntax anatomy: `display: flex;` ruleset template with SELECTOR/PROPERTY/VALUE role colors (stable across template → instance → labels) — `api_signature_annotation`
4. One property per step, render after each: `display:flex` (render changes) → `flex-direction` → `justify-content` — `incremental_visual_styling_loop`; structural wrapper edits shown with UNCHANGED render first (structure ≠ style)
5. Every code panel HTML/CSS-pilled; new lines boxed orange; source left / rendered result right — `code_and_rendered_output_pairing`
6. Quiz Time! after the first property cluster; second after alignment properties (E07 cadence)
7. Key Takeaways mirror agenda → Practice → Next Session → THANK YOU / ALL THE BEST

### 6.3 GenAI — "New tool: <X> walkthrough" session (Academy/Intensive packaging, genai stack profile)

1. WELCOME → reflective hook ("think of a task where this would help") → Agenda (re-shown between sections)
2. Problem Statement slide (the pain, e.g. "creating X takes hours") — lever = time-saving with a concrete manual-vs-tool contrast — `motivation_lever_varies_by_domain`
3. Logo section-break + one-line "what it does" → "How to Use" 3-step tracker, completed steps ticked green, one step per slide with real screenshots — `tool_walkthrough_flow`
4. Example prompts inside branded mock input boxes with model logos, teaching-point part bolded — `mock_tool_ui_prompt_card`
5. Weak prompt → output vs improved prompt → output, changing ONE dimension — `contrastive_prompt_quality_demo`
6. Pink "Note" callouts for the tool's real frictions (free-tier limits, auth, UI drift) + workarounds — `real_world_friction_note`
7. Advantages → Similar Tools (2-3 alternatives) + explicit "choose by need" heuristic — `capability_menu_with_selection_judgment`
8. Quiz Time! → Key Takeaways → Practice (guided build checkpoint per genai packaging phases) → "Stay Updated" meta-slide

---

## 7. How this connects to the product context

- **Packaging drives cadence, pedagogy intelligence drives content.** E.g. NIAT B3×GenAI resolves to 120h ±5%, 3 modules, coding-heavy unit mix, topic phases "Problem framing → Architecture → Guided build → Checkpoint" — the GenAI session flows in §4.6 are exactly how those phases are realized on slides.
- **Pedagogy profiles** referenced by product manifests (e.g. NIAT GenAI `project_build_along`) are satisfied by the observed GenAI flows (`no_code_workflow_build_flow`, `project_as_pipeline`).
- **Audience calibration:** NIAT (post-12th, first formal exposure) leans harder on analogy_before_abstraction, goal_state_preview, and metacognitive scaffolding; Intensive/Academy (mature upskillers) can compress motivation and accelerate to practice — but the quiz cadence and bookend structure hold for both (they come from packaging + slide-prep guide, not audience).
- The companion standalone document **"Open ACP — Canonical Product Context (All Products)"** carries the full product/structure/packaging detail; the two documents together are the complete context pair for downstream agents.

---

## Provenance (for maintainers; all content above is inlined)

Derived from: `knowledge/analyses/pedagogy/universal_principles.yaml` (v4, inlined verbatim in §3), the 34-deck corpus under `knowledge/raw/brand/` (inventory in §2), per-domain analyst reports (2026-07-06 run), and `knowledge/manifests/packaging/{default,genai}.yaml` for course-context eval items.
