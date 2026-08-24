import sqlite3
import os
from datetime import datetime, date

DB_PATH = os.path.join(os.path.dirname(__file__), "physicsbowl.db")

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            VALUES (?, ?, ?, ?)
        """, (question_id, selected_option, is_correct, time_spent_seconds))
        conn.commit()

def get_question_status(question_id: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT is_correct FROM submissions
            WHERE question_id = ?
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
            SELECT question_id, MAX(is_correct) as has_solved, COUNT(id) as attempts
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
        cursor.execute("SELECT question_id FROM bookmarks WHERE question_id = ?", (question_id,))
        exists = cursor.fetchone()
        if exists:
            cursor.execute("DELETE FROM bookmarks WHERE question_id = ?", (question_id,))
            conn.commit()
            return False
        else:
            cursor.execute("INSERT INTO bookmarks (question_id) VALUES (?)", (question_id,))
            conn.commit()
            return True

def is_bookmarked(question_id: str) -> bool:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT question_id FROM bookmarks WHERE question_id = ?", (question_id,))
        return cursor.fetchone() is not None

def save_note(question_id: str, content: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO question_notes (question_id, note_content, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(question_id) DO UPDATE SET
                note_content = excluded.note_content,
                updated_at = CURRENT_TIMESTAMP
        """, (question_id, content))
        conn.commit()

def get_note(question_id: str) -> str:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT note_content FROM question_notes WHERE question_id = ?", (question_id,))
        row = cursor.fetchone()
        return row["note_content"] if row else ""

def save_contest_result(session_id: str, title: str, division: int, score: int, total: int, time_taken: int, answers_json: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO contest_sessions (id, title, division, score, total_questions, time_taken_seconds, answers_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (session_id, title, division, score, total, time_taken, answers_json))
        conn.commit()

def get_contest_result(session_id: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contest_sessions WHERE id = ?", (session_id,))
        return cursor.fetchone()

def get_recent_contests():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contest_sessions ORDER BY created_at DESC LIMIT 10")
        return cursor.fetchall()

def get_submission_history_daily():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT date(created_at) as sub_date, COUNT(id) as count, SUM(is_correct) as correct_count
            FROM submissions
            GROUP BY date(created_at)
            ORDER BY sub_date DESC
            LIMIT 365
        """)
        return cursor.fetchall()
