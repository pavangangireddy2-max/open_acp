# Stage: Slide Deck Design — Induction

## Your Role
You are designing an induction slide deck with visual timelines, resource links, and setup guidance.

## What's Different from Concept Explainer
- Deck emphasizes **visual timelines** and **resource directories**
- QR codes and links are prominent for easy access to tools
- Slides are less text-heavy, more visual and welcoming
- Setup slides mirror the walkthrough pattern (screenshot-heavy)

## Process
Follow `concept_explainer/06_slide_deck` with these modifications:

### Step 1: Plan the Deck Structure
1. **Welcome slides** (2-3): Title, team introductions, icebreaker prompt
2. **Program timeline** (1-2): Visual roadmap of the entire program
3. **Tools setup** (3-5): Per-tool setup with screenshots, QR codes to download pages
4. **Communication channels** (1-2): Where to find things, how to get help
5. **First assignment** (1-2): Preview and quick-start
6. **Activity slides**: Setup checklist, introductions, scavenger hunt

### Step 2: Visual Design Emphasis
- visual_description should specify:
  - Timeline graphics (Gantt-style or roadmap visual)
  - QR code placements for tool download URLs
  - Team/instructor photos (placeholder descriptions)
  - Resource directory layout (icon + label + link format)
- Use `full_image` layout for timeline and roadmap slides
- Use `two_column` for setup slides (instructions left, screenshot right)

### Step 3: Resource Slides
- Create "resource hub" slides with links organized by category
- Include QR codes for mobile access
- Speaker notes should mention that these slides will be shared as a reference

## Output Format
Same as `concept_explainer/06_slide_deck`.

## Quality Criteria
- Visual timeline of the program is included
- QR codes or prominent links for every tool/resource
- Welcome slides feel warm, not corporate
- Setup slides have verification checkpoints
- Total slide count is lower than concept_explainer (aim for 15-20 slides, not 25+)
