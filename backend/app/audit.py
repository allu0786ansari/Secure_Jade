"""Audit logging for record operations."""

import json

from .db import get_connection  # pylint: disable=relative-beyond-top-level


def log_action(action, performed_by, record_id=None, metadata=None):
    """Log an action to the audit_logs table."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO audit_logs (record_id, action, performed_by, metadata)
        VALUES (%s, %s, %s, %s)
    """, (
        record_id,
        action,
        performed_by,
        json.dumps(metadata) if metadata else None
    ))

    conn.commit()
    conn.close()
