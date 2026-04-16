"""Constants — model tiers, thresholds, paths."""

# Model tiers
ANTHROPIC_STRONG_MODEL = "claude-opus-4-6"
ANTHROPIC_CHEAP_MODEL = "claude-haiku-4-5-20251001"

# Backward-compatible aliases for older call sites.
STRONG_MODEL = ANTHROPIC_STRONG_MODEL
CHEAP_MODEL = ANTHROPIC_CHEAP_MODEL

# Evaluation
CONTENT_PASS_THRESHOLD = 3.5
MAX_COMPILER_ITERATIONS = 5
MAX_REVIEW_ROUNDS = 2

# Backprop
MAX_BACKPROP_CYCLES = 3
DRIFT_THRESHOLD = 0.3

# API
API_MAX_RETRIES = 3
API_RETRY_BACKOFF = 2.0

# Gates
GATE_G3_SAMPLE_RATE = 1.0  # Review 100% initially, relax to 0.3 at maturity

# Wiki
WIKI_CONFIDENCE_DECAY_RATE = 0.05  # Per cycle for perishable facts
WIKI_STALE_THRESHOLD_DAYS = 30
