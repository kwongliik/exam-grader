import os
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.environ.get("DATABASE_URL")


def get_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set. Add it to your .env file.")
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


def init_db():
    """Creates the results table if it doesn't exist yet.
    Safe to call every time the app starts."""
    conn = get_connection()
    with conn, conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS results (
                id SERIAL PRIMARY KEY,
                student_id TEXT NOT NULL,
                question_id TEXT NOT NULL,
                score NUMERIC NOT NULL,
                max_score NUMERIC NOT NULL,
                extracted_answer TEXT,
                feedback TEXT,
                created_at TIMESTAMPTZ DEFAULT NOW()
            );
            """
        )
    conn.close()


def save_result(student_id, question_id, score, max_score, extracted_answer, feedback):
    conn = get_connection()
    with conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO results (student_id, question_id, score, max_score, extracted_answer, feedback)
            VALUES (%s, %s, %s, %s, %s, %s);
            """,
            (student_id, question_id, score, max_score, extracted_answer, feedback),
        )
    conn.close()
