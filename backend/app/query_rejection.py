DISALLOWED_KEYWORDS = [
    "why",
    "how",
    "compare",
    "risk",
    "should",
    "suggest",
    "recommend",
    "predict",
    "analyze",
    "analysis",
    "better",
    "worse"
]


def is_disallowed_query(field: str) -> bool:
    """
    Reject queries that imply inference, reasoning, or comparison.
    """
    lowered = field.lower()
    return any(keyword in lowered for keyword in DISALLOWED_KEYWORDS)
