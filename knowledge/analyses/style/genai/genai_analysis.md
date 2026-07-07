# GenAI Sample Project Analysis
# Source: sample_genai_project.pdf (14 slides) — the only intact GenAI deck
# Analyzed: 2026-07-06
# NOTE: genai_s2..s5 in knowledge/raw/brand/ are CORRUPT/truncated (fail to parse,
#       fonts missing, ~2 slides survive each) and could not be analyzed.
#       This analysis is based solely on the intact sample project deck.

## PPTs Analyzed

### 1. GenAI Sample Project — "Your Learning Journey: From AI-curious to AI-confident" (14 slides)
- **Topics**: Course positioning/motivation for a GenAI project track — world is changing, AI in everyday life, career impact/disruption, concepts to be learned, and a preview of 4 capstone projects (Social Media Content Automation, AI News Summarizer, Learning Path Generator, AI Shopping Assistant on Telegram).
- **Structure**: WELCOME → "Your Learning Journey" title → Motivation (world changing, AI everyday) → Career stakes (impact + disruption stat) → "Your Path to Excellence" → "Concepts You Will Learn" (5 chevrons) → "Projects You Will Build" (4 project flow diagrams) → THANK YOU → ALL THE BEST.
- **This is a course-intro/motivation deck**, not a concept-teaching session — so its value is in how a *project-building GenAI track is framed and scoped*, not in concept pedagogy.
- **Notable devices**:
  - **Edit-mark emphasis** (slide 3): "World is changing ~~Fast~~ → Rapidly" — the struck-through word is a deliberate visual rhetorical device to signal escalation.
  - **Familiar-product grid for AI motivation** (slide 4, "AI in Everyday Life"): Google Maps, Netflix, PhonePe, Gemini, Google Translate, Google Photos — concrete consumer apps, not abstract "AI is everywhere."
  - **Cited statistic with source** (slide 6): "22% of all Jobs Face Disruption by 2030 (World Economic Forum 2025)" in a dashed callout box + a worried-character illustration with a speech bubble ("Workers without new AI skills face high job loss risk"). Fear/urgency framing paired with a credible citation.
  - **Outcome-first concept list** (slide 8, "Concepts You Will Learn"): each item is a *capability/outcome* ("Master AI tools that save hours of work weekly", "Build complete AI workflows visually", "Build functional apps without coding", "Understand agent architectures and advanced concepts like MCP") rather than a topic name.
  - **Numbered pipeline diagrams for each project** — every project is shown as a *data-flow pipeline of stages*, not a feature list (see patterns below).

## New Pedagogy Patterns Discovered

### 1. Project-as-Pipeline framing (GenAI-specific)
Every capstone GenAI project is introduced as a **left-to-right pipeline of processing stages**, each a labeled node with an icon and an arrow to the next:
- **Social Media Automation**: Listing articles ① → Summarization ② → Generate Platform-Specific Content ③ → Asset Handling ④ → Auto-Post to Social Media ⑤ (numbered hexagons).
- **AI News Summarizer**: Fetches AI news + Collects tech updates → Summarize with Gemini AI → Deliver newsletter to email.
- **Learning Path Generator**: Takes learning goal → Researches resources → Creates day-wise path → Generates Google Doc → Schedules calendar events.
- **AI Shopping Assistant**: Text/voice product search → Real-time Amazon scraping → AI styling recommendations → Instant Telegram responses.

This is distinct from the C++/DSA "one concept per slide" model: GenAI projects are taught as **orchestrated workflows where the LLM is one stage among several (fetch → LLM → deliver)**. The pedagogy foregrounds *integration and data flow* over language syntax.

### 2. Named real tools as first-class curriculum (not just motivation)
The pipelines name concrete external services as the components students wire together: **Gemini AI** (the LLM stage), **Telegram** (delivery), **Amazon** (live scraping), **Google Docs / Google Calendar** (output targets), email/newsletter delivery. GenAI pedagogy here is **tool-orchestration literacy** — teaching students to compose real SaaS/APIs around an LLM — rather than teaching the model internals.

### 3. "AI workflows visually / apps without coding" — low-code framing
Two of the five stated learning outcomes ("Build complete AI workflows visually", "Build functional apps without coding") signal the track teaches GenAI through **visual/low-code workflow builders**, not from-scratch programming. This is a materially different delivery mode than the code-syntax progressions in C++/Python, and should not inherit "progressive code reveal" rules by default.

### 4. Advanced-concept name-drop as aspiration anchor (MCP, agent architectures)
The intro explicitly promises "agent architectures and advanced concepts like MCP" — naming a cutting-edge concept up front to set an aspirational ceiling, even though the concept is only delivered later. Motivation-by-frontier-terminology.

### 5. Urgency/stakes framing specific to GenAI's career narrative
Unlike C++ ("NASA uses C++" — pride/impressiveness), GenAI motivation leans on **disruption anxiety + credible stat** ("22% of jobs disrupted by 2030, WEF 2025") to create urgency. The emotional lever differs by domain: C++/DSA use *aspiration*, GenAI uses *adapt-or-fall-behind*.

## Session Structure Patterns

### genai_project_intro_flow (course/track opener)
```
WELCOME
"Your Learning Journey" (aspirational subtitle: "From X-curious to X-confident")
Motivation: the world/field is changing rapidly (visual escalation device)
Relevance: familiar consumer products powered by the tech (grid of logos)
Stakes: cited disruption statistic + worried-character urgency framing
"Your Path to Excellence" (transition)
"Concepts You Will Learn" (outcome-phrased chevrons, not topic names)
"Projects You Will Build" (one pipeline diagram per capstone project)
THANK YOU
ALL THE BEST
```

### project_pipeline_pattern (how each GenAI project is scoped)
```
Project title ("Projects You Will Build" eyebrow + project name)
Horizontal/numbered pipeline of stages, each = icon + short label
Arrows showing data flow between stages
LLM (e.g. Gemini) appears as ONE stage; other stages are fetch/scrape/deliver
Real named services as the endpoints (Telegram, Amazon, Google Docs, email)
```
