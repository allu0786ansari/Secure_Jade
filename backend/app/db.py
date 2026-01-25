"""Database connection utilities."""

import psycopg2


def get_connection():
    """Create and return a new PostgreSQL connection."""
    return psycopg2.connect(
        dbname="jade_ground_truth",
        user="jade_user",
        password="jaassuregroup4",
        host="localhost",
        port=5432
    )
