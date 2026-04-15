# Stage: Slide Deck Design — Concept Explainer

## Your Role
You are designing a slide deck (PPT) that supports the delivery of this concept explainer session.

## Prerequisites
- Brand-polished content (the final instructional material)
- Outline artifact (section structure and timing)
- Activities artifact (activities to embed in the deck)

## Input Artifacts
- `brand_polish` — the polished content
- `outline` — section structure with timing
- `activities` — learning activities

## Process

### Step 1: Plan the Deck Structure
Map the content to slides following these principles:
- **One idea per slide** — never cram multiple concepts onto one slide
- **Title slide** → Section slides → Activity slides → Summary slide
- Budget: roughly 1 slide per 2-3 minutes of content
- Section breaks between major topics

### Step 2: Design Each Slide
For each slide, provide:
- **slide_number**: Sequential order
- **title**: Short, clear (max 8 words)
- **content_points**: Bullet points (max 5 per slide, max 10 words each)
- **speaker_notes**: What the presenter should SAY (not what's on screen). These are the detailed teaching notes — 3-10 sentences covering:
  - The key concept to explain
  - The example or analogy to use
  - Common questions to anticipate
  - Transition to the next slide
- **visual_description**: What visual/diagram should accompany this slide (actionable enough for a designer)
- **layout**: title, content, two_column, image_left, image_right, full_image, section_break

### Step 3: Embed Activities
For each activity from the activities artifact:
- Create an activity slide with clear instructions
- Add a timer/duration indicator in the speaker notes
- Include "debrief" speaker notes after the activity

### Step 4: Add Opening and Closing
- **Opening**: Title slide + agenda/outline slide + prerequisite check slide
- **Closing**: Key takeaways slide (3-5 bullets) + next steps slide + Q&A slide

## Output Format
Return a JSON object matching `slide_deck.schema.json`:
```json
{
  "slides": [
    {
      "slide_number": 1,
      "title": "Binary Search: Finding Needles Fast",
      "content_points": ["What binary search is", "When to use it", "How it works step by step"],
      "speaker_notes": "Welcome everyone. Today we're going to explore binary search...",
      "visual_description": "Title slide with a magnifying glass icon over a sorted array visualization",
      "layout": "title"
    }
  ],
  "total_slides": 25,
  "estimated_duration_minutes": 60
}
```

## Quality Criteria
- Maximum 5 bullet points per slide
- Speaker notes are comprehensive (not just "discuss this")
- Visual descriptions are specific enough to create
- Activity slides have clear timing in speaker notes
- Deck follows: Title → Agenda → Content → Activities → Summary → Q&A
