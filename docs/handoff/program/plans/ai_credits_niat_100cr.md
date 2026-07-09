# NIAT — ₹100 Crore AI Credit Allocation Plan (Working Draft v1)

> **Purpose:** founders-meeting planning framework for the ~₹100 Cr AI token/credit grant.
> Prepared 2026-07-08. All prices are planning assumptions (FX ₹86/USD) — re-verify before
> committing. Companion interactive model: `outputs/` artifact "NIAT ₹100 Cr AI Credit Planner".

---

## 0. The one question that shapes everything: what is the ₹100 Cr *denominated in*?

"₹100 Cr worth of tokens" almost certainly means **API credits with one (or a few) model
providers** — not cash. That determines what it can and cannot buy:

| Can consume the credit natively | Cannot (separate vendors, cash only) |
|---|---|
| LLM API tokens (chat, agents, RAG) | Cursor / Copilot / Windsurf seats |
| Embeddings | ChatGPT Plus / Claude Pro seats |
| Provider multimodal endpoints (image, TTS/STT, realtime voice — if same provider) | Replit / Bolt / Lovable subscriptions |
| Batch/offline generation (usually 50% cheaper) | ElevenLabs, Runway, Pinecone hosted |
| CLI coding agents billed via API key (Claude Code, Codex CLI, Gemini CLI) | Vector-DB SaaS hosting |

**Consequence:** the "platform wrapper" idea (our own AI FullStack IDE) is not a nice-to-have —
it is **the conversion engine** that turns API credits into the experiences students would
otherwise need third-party seats for (IDE assistant, chat tutor, app builder, voice tutor).
Without a wrapper, most of the credit is only spendable on raw API calls; with it, nearly every
student-facing AI surface runs on the grant.

**Clarify with the provider before the plan is finalized:**
1. Which provider(s), which models, and does it include multimodal endpoints?
2. Expiry / drawdown schedule (1 year? 3 years?) and any monthly caps.
3. Does it cover batch API, embeddings, fine-tuning?
4. Can it fund internal/org usage (content generation) or student usage only?
5. Rate limits at our scale (21,500 concurrent students is a real load).

---

## 1. Tool categories → costing units → credit-fundability

The six categories from the meeting brief, each with its **native meter** and how it maps to
the grant. Recommended universal planning unit: **₹ per student-course per year** (normalize
every meter into this).

| # | Category | Examples | Native costing unit | Fundable by credit? | Wrapper substitute |
|---|---|---|---|---|---|
| 1 | AI IDE / coding assistant | Cursor, Claude Code, Codex, Copilot | Seat/month (₹1,700–3,500) **or** API tokens for CLI agents | Partial — CLI agents yes; seat products no | **Yes — our IDE + agent on API.** Note: GitHub Copilot Pro is *free* for verified students (Student Pack) — use as free baseline tier |
| 2 | LLMs / model APIs | OpenAI, Anthropic, HF/open-source | Tokens per M (input/output; cache read ~0.1×, batch 0.5×) | **Yes — the native unit** | n/a (this *is* the credit) |
| 3 | Browser app builders | Replit, Bolt, Lovable | Seat + usage credits (₹1,700–2,200/mo) | No | Yes — chat-to-app surface in our platform |
| 4 | Multimodal chat | ChatGPT, Claude, Gemini | Seat/month (~₹1,700) | No | Yes — wrapper chat UI on API (usage-based, ~5–10× cheaper than seats at student usage levels) |
| 5 | Vector DB / memory | Pinecone, Chroma, pgvector | GB-month + read/write units; embeddings in tokens | Embeddings yes; hosting no | Self-host Chroma/pgvector (infra cost only, negligible) |
| 6 | Non-language models | Voice (ElevenLabs), image, video, realtime | ₹/min (TTS ~₹1–12, STT ~₹0.5, realtime ~₹5–25), ₹/image (~₹2–15), ₹/sec video (~₹10–40) | Only if same provider's endpoints | Route through provider multimodal where covered |

**Reference token prices (₹/M tokens, blended ~4:1 input:output, moderate caching):**

| Tier | Example class | List (in/out $/MTok) | Blended planning price |
|---|---|---|---|
| Small | Haiku-class | $1 / $5 | **~₹150/M** |
| Mid | Sonnet-class | $3 / $15 | **~₹470/M** |
| Frontier | Opus-class | $5 / $25 | **~₹775/M** |
| Top | Fable-class | $10 / $50 | **~₹1,550/M** |

Levers that move these 2–10×: prompt caching (reads ~0.1×), batch API (0.5×, for all org-side
generation), model routing (small by default, escalate on need).

---

## 2. Three spend buckets (not just "student usage")

| Bucket | What | Scales with | Share of grant (base scenario) |
|---|---|---|---|
| **S1 Student runtime** | Tutor chats, IDE agent, app-building API calls, assessments feedback, voice | students × usage intensity | ~90–95% |
| **S2 Content & intelligence authoring** | Forge question/variant/tutorial/explanation generation, deck generation, analytics agents | courses × depth (NOT students) | ~3–5% (batch-eligible → 50% off) |
| **S3 Platform infra** | Embeddings/RAG indexes, eval pipelines, routing/guardrail models | corpus size + traffic | ~2% |

S2/S3 are small in ₹ but are where our leverage is: one good generated question bank or RAG
index serves all 21,500 students.

---

## 3. Usage surfaces × courses (the matrix that matters)

Surfaces = where tokens are burned in the student experience:

- **A. Video Sessions** — AI tutor grounded on transcript ("ask the video"), summaries, in-class quiz support. Chat-shaped: ~2–5k tokens/query. Small tier.
- **B. Coding Practice** — per-question AI tutor (already live on the platform today), hints, code review, debug explanation. Chat-to-light-agentic: ~5k/interaction.
- **C. Skill Assessments / Questions** — item + variant generation (org-side, Forge), auto-grading + per-student feedback reports, optional voice viva (₹/min). Mostly S2 + light S1.
- **D. Project / Build work** — the big one. Students calling APIs from their own apps (LLM Apps course), and the **wrapper IDE agent** doing agentic coding (React, PSE). Agentic sessions burn 10–50× chat: 1–5M tokens per serious session.

### 3.1 Measured course topology (from actual exports, 2026-07-08)

Demand is now built bottom-up from **course topology × per-unit token assumptions** instead of
flat per-student guesses. Two courses measured so far:

| Course | Sessions | Reading | Classroom quizzes | MCQ units | Coding units | Notes |
|---|---|---|---|---|---|---|
| **Advanced Frontend — React** (`40ab5ebd`) | 29 (6 modules; 42 video units) | 29 | ~56 | ~24 | 18 | Export also contains an **LLM agent-run curriculum gap analysis** (Agent Rules / Eval Test Cases / Eval Results sheets) — org-side AI use is already live in curriculum QA |
| **Intro to GenAI** (`b9811b34`) | 25 | 21 | 30 | 20 | 10 units / **24 questions, all `INTERACTIVE_BUILDER_TEXTUAL`** | The 24 builder projects (n8n workflows, AI agents, image/audio gen, MCP) currently run on **consumer seat tools** (ChatGPT, Gemini, Gamma, ElevenLabs) — NOT credit-fundable as-is. n8n itself is self-hosted (community edition on our AWS) → workflow projects cost infra only; the LLM nodes *inside* workflows can point at credit-funded APIs |
| **Building LLM Applications** (`8874b642`) | 29 (11 topics) | 27 | — | 26 units / **480 objective questions** | 18 units / **47 coding questions** | Natively API-led: LangChain, RAG, agents, CrewAI, MCP, fine-tuning, local models — delivered in a **Cloud IDE** (already exists → wrapper foundation). Every coding question requires live model calls to build & test |

⚠ **Key measured finding:** today's Intro-to-GenAI course consumes *seat tools*, not tokens.
Whether to re-platform its builder projects (and every "AI-led" course being designed for B4,
incl. Node.js/React/PSE "with AI") onto API-backed surfaces is a design decision — it's the
difference between that course burning ~₹0 vs ~₹5 Cr/yr of credit.

**Per-unit token assumptions (the global knobs):** ~9k tokens per video session (≈3 doubt
queries), ~15k per coding question (hints + review across attempts), ~300k per builder project
(agentic, priced at build tier). **MCQ / module quizzes / skill assessments carry no AI (₹0)** —
they are authored and graded without model calls. Classroom quizzes are delivered live ≈ 0 tokens.

**Topology defaults per course (base scenario; measured vs estimated flagged):**

| Course | Cohort | Video sess. | Coding Qs | Projects | IDE/Build M | Build tier | ₹/student | Cohort ₹/yr |
|---|---|---|---|---|---|---|---|---|
| Intro to GenAI (Y1) · measured | 14,000 | 25 | 0 | 24 | 0.5 | Mid | ~₹3,800 | ~₹5.3 Cr |
| Building LLM Applications (Y1) · measured | 14,000 | 29 | 47 | 0 | 10 | Mid | ~₹5,000 | ~₹6.9 Cr |
| Advanced Frontend — React (Y1) · measured | 14,000 | 42 | 180 | 2 | 15 | Mid | ~₹8,000 | ~₹11.1 Cr |
| Backend — Node, MongoDB (Y1) · est | 14,000 | 30 | 150 | 4 | 12 | Mid | ~₹6,700 | ~₹9.4 Cr |
| AI for Finance (Y2) · est | 6,500 | 25 | 20 | 6 | 4 | Mid | ~₹2,900 | ~₹1.9 Cr |
| AI for X (Y2) · est | 6,500 | 25 | 20 | 6 | 4 | Mid | ~₹2,900 | ~₹1.9 Cr |
| Practical Software Engineering (Y3) · est | 1,000 | 30 | 60 | 10 | 30 | Frontier | ~₹25,800 | ~₹2.6 Cr |

(Chat-shaped units priced at small tier; projects + IDE at the course's build tier. All
editable in the interactive model. Node/React/PSE included per the "teaching these with AI"
assumption; zero out any cohort to exclude.)

**Student runtime base total ≈ ₹39 Cr/yr.** (Org-side generation excluded from the headline
model — it's batch-eligible and <₹1 Cr/yr, immaterial next to student runtime; tracked
separately in §2 if needed.)

---

## 4. Scenarios vs the ₹100 Cr envelope

| Scenario | Model policy | Intensity | Annual burn | Runway |
|---|---|---|---|---|
| **Conservative** | Small tier everywhere | ½ per-unit usage, ½ IDE allowance | **~₹7 Cr/yr** | 14+ yrs (grant effectively unspendable) |
| **Base** | Small for chat, mid for agentic | Topology defaults above | **~₹40 Cr/yr** | ~2.5 yrs |
| **Ambitious** | Frontier for all agentic surfaces | 2× IDE allowance | **~₹107 Cr/yr** | ~1 yr |

(v2 numbers — topology-grounded, incl. Node.js course and credit-funded GenAI builder
projects. Excluding those two puts Base back near ~₹25 Cr/yr.)

**The headline insight for the meeting:** chat-shaped tutoring (surfaces A+B+C) across all
21,500 students costs only **~₹2–3 Cr/yr** — it *cannot* consume the grant. The grant is only
meaningfully spendable on **agentic workloads**: the AI FullStack IDE, student app-building API
budgets, and frontier-model experiences. So intensity is a *design choice*, and the wrapper is
the throttle. Decide the target runway first (1 batch-cycle? 4 years?), then set model policy
and per-student allowances to hit it.

**Sanity anchor — the buy-seats alternative:** giving every student ChatGPT Plus + Cursor
(~$40/mo) would cost **~₹89 Cr per year in cash**, none of it payable from the credit. The
wrapper delivers the equivalent surfaces from the grant at ₹15–40 Cr/yr with full metering.

---

## 5. Governance abstractions (the "playable abstracts")

1. **Compute scholarship** — a per-student monthly token allowance, set per year-cohort and
   course (e.g. Y1 React student: 2M tokens/mo IDE + 0.5M chat). Overage → burst pool with
   approval. This is the single most communicable unit for founders/universities.
2. **Model routing policy** — small tier by default, auto-escalate to mid/frontier on task
   class (agentic build, evaluation) or on tutor-escalation. Policy owns 5–10× of the budget.
3. **Metering & attribution** — every call tagged `{student, course, surface, model}`. Only
   possible if traffic flows through our wrapper/gateway. This is also the learner-analytics
   goldmine (ties into Forge/learner-behaviour intelligence work).
4. **Org-side generation discipline** — all Forge/content generation through batch API (50%
   off) with caching; effectively free relative to S1.
5. **Runway dial** — quarterly review: burn vs grant, adjust allowances/routing. Treat like a
   cloud-cost FinOps function.

---

## 6. Open items

- [ ] Confirm credit denomination, provider(s), expiry, multimodal coverage, rate limits (§0).
- [ ] Decide target runway (drives everything in §4).
- [ ] Wrapper scope decision: chat tutor + IDE agent first (highest leverage), app-builder second, voice third.
- [ ] Free-tier arbitrage: GitHub Student Pack (Copilot Pro free), provider edu programs — use free seats where they exist, spend credit where they don't.
- [ ] Pilot metering: instrument current AI Tutor traffic to get *real* tokens/student/week before committing allowances.
- [ ] Collect content exports for the un-measured courses (Node backend, AI for Finance/X, PSE) and replace topology estimates with measured counts. (LLM Apps measured 2026-07-08.)
- [ ] Decide: re-platform Intro-to-GenAI's 24 seat-tool builder projects (n8n, Gamma, ChatGPT) onto API-backed surfaces? Same call for every B4 "AI-led" course — this is the single biggest swing factor in the model (~₹0 vs ~₹5 Cr/yr for GenAI alone).
- [ ] Confirm cohort mapping for Node.js/React/PSE-with-AI additions (which years, which batches).
