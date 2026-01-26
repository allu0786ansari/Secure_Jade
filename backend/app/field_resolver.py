def resolve_field(data: dict, field_path: str):
    """
    Safely resolve a dotted field path from record JSON.

    Examples:
    - proposer.name
    - security.cctv.installed
    - claims_history.has_claims
    """

    parts = field_path.split(".")
    current = data

    for part in parts:
        if not isinstance(current, dict):
            return "Information not available"

        if part not in current:
            return "Information not available"

        current = current[part]

    # Masking & null rules
    if current is None:
        return "Information not available"

    if current == "MASKED":
        return "Information not available"

    if isinstance(current, list) and len(current) == 0:
        return "Information not available"

    return current
