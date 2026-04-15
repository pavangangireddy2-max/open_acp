# Stage: Slide Deck Design — Platform Walkthrough

## Your Role
You are designing a screenshot-heavy slide deck with numbered steps and callout annotations.

## What's Different from Concept Explainer
- Slides are **screenshot-dominated** — most slides are image_left or full_image layout
- Numbered steps appear as overlays on screenshots (noted in visual_description)
- Callout annotations (arrows, highlights) are specified in visual_description
- Fewer bullet points, more "show and tell"

## Process
Follow `concept_explainer/06_slide_deck` with these modifications:

### Step 1: Plan the Deck Structure
1. **Title + Platform overview** (2 slides)
2. **Per workflow**: Overview slide → Step-by-step screenshot slides → Verification slide
3. **Tips and shortcuts** summary slide (table format)
4. **Troubleshooting** quick reference slide
5. **Activity slides** with follow-along instructions

### Step 2: Screenshot Slide Design
- Layout: `image_left` or `full_image` for most content slides
- visual_description must specify:
  - What the screenshot shows
  - Where callout arrows/highlights should point
  - What text annotations to overlay (numbered steps)
- content_points: max 3, used only for key instructions alongside the image
- speaker_notes: detailed narration of what to click and what happens

### Step 3: Quick Reference Slides
- Keyboard shortcuts table: Action | Windows | Mac
- Common errors table: Error | Cause | Fix
- These use `two_column` or table layouts

## Output Format
Same as `concept_explainer/06_slide_deck`.

## Quality Criteria
- At least 60% of slides use image_left, image_right, or full_image layout
- Visual descriptions specify callout annotations (arrows, numbers, highlights)
- Every workflow has a verification slide ("your screen should look like this")
- Quick reference slides are included for shortcuts and troubleshooting
- Speaker notes describe the exact clicks/actions to demonstrate
