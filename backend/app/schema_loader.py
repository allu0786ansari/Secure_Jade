"""
Load and cache the active JSON Schema from the database.

This module enforces schema authority by ensuring that:
- Only one schema is active at a time
- Validation is always performed against the DB-backed schema
- Schema version is returned alongside the validator
"""

import json
from typing import Tuple

from jsonschema import Draft202012Validator

from .db import get_connection  # pylint: disable=relative-beyond-top-level


def load_active_schema() -> Tuple[Draft202012Validator, str]:
    """
    Load the currently active JSON schema from the database.

    Returns:
        (validator, version):
            validator (Draft202012Validator): Compiled JSON Schema validator
            version (str): Active schema version identifier

    Raises:
        LookupError: If no active schema is found
        ValueError: If schema JSON is invalid
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT schema_json, version
                FROM schema_versions
                WHERE is_active = true
                LIMIT 1;
                """
            )
            row = cur.fetchone()
    finally:
        conn.close()

    if not row:
        raise LookupError("No active schema found in schema_versions table")

    schema_json, version = row

    # If schema is stored as text, parse it
    if isinstance(schema_json, str):
        try:
            schema_json = json.loads(schema_json)
        except json.JSONDecodeError as exc:
            raise ValueError("Stored schema_json is not valid JSON") from exc

    # Compile validator (fails fast if schema itself is invalid)
    validator = Draft202012Validator(schema_json)

    return validator, version
