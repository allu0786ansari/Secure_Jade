"""Load and cache active JSON schema from database."""

import json

from jsonschema import Draft202012Validator

from .db import get_connection  # pylint: disable=relative-beyond-top-level

def load_active_schema():
    """Load the currently active JSON schema from the database."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT schema_json
                FROM schema_versions
                WHERE is_active = true
                LIMIT 1;
            """)

            row = cur.fetchone()
        finally:
            cur.close()
    finally:
        conn.close()

    if not row:
        raise LookupError("No active schema found")

    schema_json = row[0]
    if isinstance(schema_json, str):
        schema_json = json.loads(schema_json)

    return Draft202012Validator(schema_json)
