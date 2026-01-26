from fastapi import HTTPException
from .db import get_connection


def get_record_by_id(record_id: str):
    """Fetch a record's JSON data by record ID (read-only)."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT data
        FROM records
        WHERE id = %s AND is_deleted = false
        """,
        (record_id,)
    )

    row = cur.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Record not found")

    return row[0]
