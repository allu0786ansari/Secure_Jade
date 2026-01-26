ALLOWED_QUERY_TYPES = [
    "FIELD_LOOKUP",        # e.g. proposer name, security status
    "SECTION_LOOKUP",      # e.g. security details
    "EXISTENCE_CHECK"      # e.g. does CCTV exist?
]

DISALLOWED_QUERY_TYPES = [
    "WHY",
    "HOW",
    "COMPARISON",
    "AGGREGATION",
    "PREDICTION",
    "INFERENCE"
]
