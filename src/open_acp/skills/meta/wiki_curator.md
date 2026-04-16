# Wiki Curator Protocol

## Purpose
Maintain the intelligence wiki — create entities from new signals, update existing entities with fresh information, detect contradictions, and ensure cross-references are consistent.

## When to Curate

### On Signal Ingestion (Loop A)
After processing new signals:
1. For each significant finding, check if a wiki entity already exists (search by topic/skill name)
2. If exists: UPDATE with new evidence, adjust confidence score
3. If new: CREATE entity with initial confidence based on source quality
4. Update cross-references between related entities
5. Rebuild the index

### Entity Types
- **skill**: A technical skill with demand_score and durability rating
- **competitor**: A competing training provider or course
- **audience_segment**: A runtime-derived target-audience segment
- **concept**: A domain concept that spans multiple skills
- **domain**: A broad domain area (e.g., "machine-learning", "web-development")

## Confidence Scoring Guidelines

| Source Quality | Initial Confidence |
|---|---|
| Primary research, official reports | 0.9 |
| Job postings (aggregated 10+) | 0.8 |
| Industry articles, expert opinions | 0.7 |
| Social media signals, anecdotal | 0.5 |
| Single data point, unverified | 0.3 |

**Confidence adjustments:**
- Multiple sources converge → increase by 0.1 (cap at 1.0)
- Contradictory signal found → decrease by 0.15
- Time decay: perishable skills lose 0.05 per cycle without reinforcement

## Durability Classification
- **durable**: Fundamental concepts unlikely to change (e.g., algorithms, data structures, SQL)
- **perishable**: Framework-specific, tool-specific, or trend-dependent (e.g., specific library versions, trending techniques)
- **unknown**: Insufficient data to classify

## Supersession Rules
- When a skill is deprecated or replaced, supersede the old entity
- When a competitor is acquired or rebranded, supersede with the new entity
- Superseded entities get confidence=0.0 and a reference to the new entity

## Cross-Reference Guidelines
- Skills should reference their prerequisites and related skills
- Competitors should reference the skills they cover
- Audience segments should reference their knowledge gaps (skill entities)
- Always use the format: `{entity_type}_{entity_id}` for cross-references

## Quality Checks
After wiki operations, verify:
- No broken cross-references (referenced entities exist)
- No duplicate entities (same skill/competitor under different IDs)
- Index reflects current state
- Log captures all changes
