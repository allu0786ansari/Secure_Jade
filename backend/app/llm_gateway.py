"""
FastAPI application for JADE schema validation, record storage,
controlled querying, and safe chat interface.
"""

from uuid import uuid4
from psycopg2.extras import Json
from fastapi import FastAPI, HTTPException

from .query_controller import get_record_by_id
from .field_resolver import resolve_field
from .audit import log_action
from .db import get_connection
from .schema_loader import load_active_schema
from .validators import validate_payload

app = FastAPI()


# -------------------------------------------------
# 🔒 Query rejection rules (GLOBAL)
# -------------------------------------------------
def is_disallowed_query(field: str) -> bool:
    """Reject queries that imply inference, reasoning, or comparison."""
    disallowed_keywords = [
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
    return any(keyword in field.lower() for keyword in disallowed_keywords)


# -------------------------------------------------
# 📦 Schema Validator Cache
# -------------------------------------------------
class ValidatorCache:
    """Cache for the active schema validator and version."""
    _validator = None
    _version = None

    @classmethod
    def load(cls):
        validator, version = load_active_schema()
        cls._validator = validator
        cls._version = version

    @classmethod
    def get_validator(cls):
        if cls._validator is None:
            cls.load()
        return cls._validator

    @classmethod
    def get_version(cls):
        if cls._version is None:
            cls.load()
        return cls._version


# -------------------------------------------------
# 📄 Record APIs
# -------------------------------------------------
@app.get("/records/{record_id}")
def read_record(record_id: str):
    data = get_record_by_id(record_id)

    log_action(
        action="READ_RECORD",
        performed_by="internal_user",
        record_id=record_id
    )

    return {
        "record_id": record_id,
        "data": data
    }


@app.post("/records")
def create_record(payload: dict):
    """Create and validate a new record against the active schema."""
    try:
        validate_payload(ValidatorCache.get_validator(), payload)
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
            ValidatorCache.get_version(),
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


# -------------------------------------------------
# 🔎 Deterministic Query API (SOURCE OF TRUTH)
# -------------------------------------------------
@app.post("/query")
def query_record(payload: dict):
    record_id = payload.get("record_id")
    field = payload.get("field")

    if not record_id or not field:
        raise HTTPException(status_code=400, detail="record_id and field required")

    # 🔒 Reject inference BEFORE data access
    if is_disallowed_query(field):
        log_action(
            action="REJECTED_QUERY",
            performed_by="internal_user",
            record_id=record_id,
            metadata={"field": field, "reason": "disallowed_query"}
        )
        raise HTTPException(status_code=400, detail="Query type not supported")

    data = get_record_by_id(record_id)
    answer = resolve_field(data, field)

    log_action(
        action="QUERY_RECORD",
        performed_by="internal_user",
        record_id=record_id,
        metadata={"field": field}
    )

    return {
        "record_id": record_id,
        "field": field,
        "answer": answer
    }


# -------------------------------------------------
# 💬 Chat API (LLM / UI Layer ONLY)
# -------------------------------------------------
@app.post("/chat")
def chat(payload: dict):
    """
    Chat endpoint acts as a UI adapter.
    It does NOT infer, explain, or reason.
    """

    record_id = payload.get("record_id")
    question = payload.get("question")

    if not record_id or not question:
        raise HTTPException(
            status_code=400,
            detail="record_id and question are required"
        )

    # 🔒 Fixed question → field mapping
    QUESTION_FIELD_MAP = {
        "is cctv installed": "security.cctv.installed",
        "does the premises have cctv": "security.cctv.installed",
        "are security guards present": "security.guards.present",
        "has there been any claims": "claims_history.has_claims"
    }

    normalized = question.lower().strip()

    if normalized not in QUESTION_FIELD_MAP:
        return {
            "answer": "Query type not supported."
        }

    field = QUESTION_FIELD_MAP[normalized]

    # Reuse the SAME logic as /query
    if is_disallowed_query(field):
        return {
            "answer": "Query type not supported."
        }

    data = get_record_by_id(record_id)
    answer = resolve_field(data, field)

    log_action(
        action="CHAT_QUERY",
        performed_by="internal_user",
        record_id=record_id,
        metadata={"question": question, "field": field}
    )

    return {
        "record_id": record_id,
        "question": question,
        "answer": answer
    }
