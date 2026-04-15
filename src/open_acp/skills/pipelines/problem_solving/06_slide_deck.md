# Stage: Slide Deck Design — Problem Solving

## Your Role
You are designing a slide deck for a problem-solving session, optimized for live coding and step-by-step walkthroughs.

## What's Different from Concept Explainer
- Slides follow a **problem → think → solve → compare** rhythm
- Code-heavy slides need special formatting (large font, minimal bullets)
- Live coding segments need "pause point" slides
- Comparison slides use two-column layouts for approach comparisons

## Process
Follow `concept_explainer/06_slide_deck` with these modifications:

### Step 1: Plan the Deck Structure
Use this rhythm for each problem:
1. **Problem slide**: Statement + constraints + example I/O (one slide)
2. **Think slide**: "What approach would you use?" (pause for discussion, 1-2 min)
3. **Approach slide(s)**: Solution strategy explained visually
4. **Code slide(s)**: Solution code with highlighted key lines
5. **Comparison slide**: Complexity table comparing approaches (two_column layout)
6. **Activity slide**: Practice problem with timer

### Step 2: Code Slide Design
- Maximum 15 lines of code per slide
- Use syntax highlighting language tags in speaker notes
- Highlight the key insight line (bold or color callout in visual_description)
- Speaker notes should walk through the code line-by-line

### Step 3: Live Coding Considerations
- Add "LIVE CODING" indicator slides before live coding segments
- Speaker notes include: setup instructions, expected output, common errors to demonstrate
- Include a "checkpoint" slide after live coding showing the final state

## Output Format
Same as `concept_explainer/06_slide_deck`.

## Quality Criteria
- Problem statement and solution are NEVER on the same slide
- Code slides have max 15 lines, large font guidance in visual_description
- Every problem has a think/pause slide before the solution
- Comparison slides use two_column layout
- Live coding segments have setup and checkpoint slides
