"""Audit logging for system operations."""

import json
from typing import Optional, Dict, Any

from .db import get_connection  # pylint: disable=relative-beyond-top-level


def log_action(
    action: str,
    performed_by: str,
    record_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> None:
    """Log an action to the audit_logs table."""

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO audit_logs (record_id, action, performed_by, metadata)
            VALUES (%s, %s, %s, %s)
            """,
            (
                record_id,
                action,
                performed_by,
                json.dumps(metadata) if metadata else None
            )
        )
        conn.commit()
    finally:
        conn.close()
