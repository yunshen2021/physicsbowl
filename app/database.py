import os
import psycopg2
import psycopg2.extras

DATABASE_URL = os.environ.get("POSTGRES_URL") or os.environ.get("DATABASE_URL")

_connection = None

def get_db():
    global _connection
    if _connection is None or _connection.closed:
        _connection = psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)
    return _connection

def _stringify_created_at(rows):
    for r in rows:
        if r.get("created_at") is not None:
            r["created_at"] = r["created_at"].strftime("%Y-%m-%d %H:%M:%S")
    return rows

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                id SERIAL PRIMARY KEY,
                question_id TEXT NOT NULL,
                selected_option TEXT NOT NULL,
                is_correct BOOLEAN NOT NULL,
                time_spent_seconds INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookmarks (
                question_id TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contest_sessions (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                division INTEGER NOT NULL,
                score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                time_taken_seconds INTEGER NOT NULL,
                answers_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS question_notes (
                question_id TEXT PRIMARY KEY,
                note_content TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()

def record_submission(question_id: str, selected_option: str, is_correct: bool, time_spent_seconds: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO submissions (question_id, selected_option, is_correct, time_spent_seconds)
            VALUES (%s, %s, %s, %s)
        """, (question_id, selected_option, is_correct, time_spent_seconds))
        conn.commit()

def get_question_status(question_id: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT is_correct FROM submissions
            WHERE question_id = %s
            ORDER BY created_at DESC
        """, (question_id,))
        rows = cursor.fetchall()
        if not rows:
            return "unsolved"
        if any(r["is_correct"] for r in rows):
            return "solved"
        return "attempted"

def get_all_question_statuses():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT question_id, MAX(is_correct::int) as has_solved, COUNT(id) as attempts
            FROM submissions
            GROUP BY question_id
        """)
        rows = cursor.fetchall()
        statuses = {}
        for r in rows:
            if r["has_solved"]:
                statuses[r["question_id"]] = "solved"
            else:
                statuses[r["question_id"]] = "attempted"
        return statuses

def toggle_bookmark(question_id: str) -> bool:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT question_id FROM bookmarks WHERE question_id = %s", (question_id,))
        exists = cursor.fetchone()
        if exists:
            cursor.execute("DELETE FROM bookmarks WHERE question_id = %s", (question_id,))
            conn.commit()
            return False
        else:
            cursor.execute("INSERT INTO bookmarks (question_id) VALUES (%s)", (question_id,))
            conn.commit()
            return True

def is_bookmarked(question_id: str) -> bool:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT question_id FROM bookmarks WHERE question_id = %s", (question_id,))
        return cursor.fetchone() is not None

def save_note(question_id: str, content: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO question_notes (question_id, note_content, updated_at)
            VALUES (%s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (question_id) DO UPDATE SET
                note_content = EXCLUDED.note_content,
                updated_at = CURRENT_TIMESTAMP
        """, (question_id, content))
        conn.commit()

def get_note(question_id: str) -> str:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT note_content FROM question_notes WHERE question_id = %s", (question_id,))
        row = cursor.fetchone()
        return row["note_content"] if row else ""

def save_contest_result(session_id: str, title: str, division: int, score: int, total: int, time_taken: int, answers_json: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO contest_sessions (id, title, division, score, total_questions, time_taken_seconds, answers_json)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
                title = EXCLUDED.title,
                division = EXCLUDED.division,
                score = EXCLUDED.score,
                total_questions = EXCLUDED.total_questions,
                time_taken_seconds = EXCLUDED.time_taken_seconds,
                answers_json = EXCLUDED.answers_json
        """, (session_id, title, division, score, total, time_taken, answers_json))
        conn.commit()

def get_contest_result(session_id: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contest_sessions WHERE id = %s", (session_id,))
        row = cursor.fetchone()
        if row:
            _stringify_created_at([row])
        return row

def get_recent_contests():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contest_sessions ORDER BY created_at DESC LIMIT 10")
        return _stringify_created_at(cursor.fetchall())

def get_recent_submissions(limit: int = 5):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, question_id, selected_option, is_correct, time_spent_seconds, created_at
            FROM submissions
            ORDER BY created_at DESC
            LIMIT %s
        """, (limit,))
        return _stringify_created_at(cursor.fetchall())

def get_submission_history_daily():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT created_at::date as sub_date, COUNT(id) as count, SUM(is_correct::int) as correct_count
            FROM submissions
            GROUP BY sub_date
            ORDER BY sub_date DESC
            LIMIT 365
        """)
        rows = cursor.fetchall()
        for r in rows:
            r["sub_date"] = str(r["sub_date"])
        return rows
