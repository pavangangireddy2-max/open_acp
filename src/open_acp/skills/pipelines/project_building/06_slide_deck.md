# Stage: Slide Deck Design — Project Building

## Your Role
You are designing a slide deck for a project building session with architecture diagrams and milestone checkpoints.

## What's Different from Concept Explainer
- Deck includes **architecture diagram slides** showing the system being built
- Milestone checkpoint slides show progress (what's done, what's next)
- Code demo slides are designed for live coding, not static display
- Fewer lecture slides, more "build along" guidance slides

## Process
Follow `concept_explainer/06_slide_deck` with these modifications:

### Step 1: Plan the Deck Structure
1. **Title + Project overview** (2-3 slides: what we're building, final demo preview)
2. **Architecture slide** (component diagram, always visible/referenced)
3. **Per milestone**: Goal slide → Build guide slides → Demo/verify slide → Checkpoint slide
4. **Integration + Final demo** (2-3 slides)
5. **Retrospective** (what we built, what we learned, next steps)

### Step 2: Architecture Diagram Slides
- Show the full architecture on one slide, with the CURRENT milestone highlighted
- Reuse this slide (with updated highlighting) at each milestone boundary
- Visual_description must be specific: boxes, arrows, labels, highlighted component

### Step 3: Code Demo Slides
- Show file structure on one slide before coding begins
- Code slides show snippets (max 12 lines), not full files
- "Expected output" slides show terminal/browser screenshots descriptions
- Include troubleshooting notes in speaker_notes for common setup issues

## Output Format
Same as `concept_explainer/06_slide_deck`.

## Quality Criteria
- Architecture diagram appears at least 3 times (start, mid, end) with progression
- Every milestone has a checkpoint slide showing cumulative progress
- Code slides have max 12 lines with clear file path labels
- Speaker notes include troubleshooting guidance for live coding
- Final slide shows the complete working project
