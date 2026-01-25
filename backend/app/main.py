"""FastAPI application for JADE schema validation and record storage."""

from uuid import uuid4
from psycopg2.extras import Json
from fastapi import FastAPI, HTTPException

from .audit import log_action  # pylint: disable=relative-beyond-top-level
from .db import get_connection  # pylint: disable=relative-beyond-top-level
from .schema_loader import load_active_schema  # pylint: disable=relative-beyond-top-level
from .validators import validate_payload  # pylint: disable=relative-beyond-top-level

app = FastAPI()

# Load active schema ONCE at startup, with fallback
_validator = None

def get_validator():
    """Get the cached validator, loading lazily if needed."""
    global _validator
    if _validator is None:
        try:
            _validator = load_active_schema()
        except Exception as e:
            raise RuntimeError(f"Failed to load schema: {e}") from e
    return _validator


@app.post("/records")
def create_record(payload: dict):
    """Create and validate a new record against the active schema."""
    try:
        validate_payload(get_validator(), payload)
    except Exception as e:
        log_action(
            action="REJECTED_RECORD",
            performed_by="system",
            metadata={"error": str(e)}
        )
        raise HTTPException(status_code=400, detail=str(e)) from e

    record_id = str(uuid4())

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO records (id, schema_version, data, created_by)
        VALUES (%s, %s, %s, %s)
        """,
        (
            record_id,
            "v1.0",
            Json(payload),
            "manual_operator"
        )
    )

    conn.commit()
    cur.close()
    conn.close()

    log_action(
        action="CREATE_RECORD",
        performed_by="manual_operator",
        record_id=record_id
    )

    return {
        "record_id": record_id,
        "status": "stored"
    }
