# Stage: Slide Deck Design — Learning Support

## Your Role
You are designing a slide deck for a misconception-correction session with side-by-side comparisons and embedded diagnostics.

## What's Different from Concept Explainer
- Slides use **two-column layouts extensively** (wrong vs right)
- Diagnostic quiz slides are embedded throughout (not just activities section)
- Visual cues distinguish misconception content (red/warning) from correct content (green/success)
- Flow: diagnose → reveal → correct → practice, repeated per misconception

## Process
Follow `concept_explainer/06_slide_deck` with these modifications:

### Step 1: Plan the Deck Structure
Per misconception:
1. **Diagnostic question slide** (pose the question, give 30 seconds to think)
2. **Reveal slide** (show the misconception and why it seems reasonable)
3. **Counter-example slide** (the case where the misconception fails)
4. **Correction slide** (two_column: misconception vs reality)
5. **Practice slide** (quick exercise applying correct understanding)

### Step 2: Visual Design Notes
- Use visual_description to specify: red/orange tint for misconception slides, green/blue for correct
- Two-column slides: left column = "What many think" / right column = "What's actually true"
- Diagnostic slides should feel like a quiz (numbered, with thinking time in speaker_notes)

### Step 3: Embedded Diagnostics
- Start the deck with a "pre-test" (3-4 diagnostic questions as a quick poll)
- End with the same questions as a "post-test" to show progress
- Speaker notes should include how to handle it when learners disagree

## Output Format
Same as `concept_explainer/06_slide_deck`.

## Quality Criteria
- Every misconception has a dedicated two-column comparison slide
- Diagnostic questions appear at start AND end (pre/post structure)
- Visual descriptions clearly distinguish wrong vs right content
- Speaker notes include guidance for managing learner frustration/disagreement
- No slide implies the learner is at fault for holding the misconception
