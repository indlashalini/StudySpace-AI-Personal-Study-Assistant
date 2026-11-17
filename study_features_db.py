import sqlite3
import json
from datetime import date

DB_NAME = "study_assistant.db"


def _connect():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_features():
    """Create additional tables without changing existing project tables."""
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS quiz_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                score INTEGER NOT NULL,
                total INTEGER NOT NULL,
                attempted_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS flashcards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS exams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                subject TEXT NOT NULL,
                exam_date TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL UNIQUE,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                unlocked_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)


def save_quiz_result(topic, score, total):
    with _connect() as conn:
        conn.execute(
            "INSERT INTO quiz_results(topic, score, total) VALUES (?, ?, ?)",
            (topic, int(score), int(total))
        )


def get_quiz_stats():
    with _connect() as conn:
        row = conn.execute("""
            SELECT COUNT(*) AS attempts,
                   COALESCE(ROUND(AVG(100.0 * score / NULLIF(total, 0))), 0) AS average
            FROM quiz_results
        """).fetchone()
    return {"attempts": row["attempts"], "average": int(row["average"])}


def save_flashcards(topic, cards):
    with _connect() as conn:
        for card in cards:
            conn.execute(
                "INSERT INTO flashcards(topic, question, answer) VALUES (?, ?, ?)",
                (topic, card["question"].strip(), card["answer"].strip())
            )


def get_flashcard_topics():
    with _connect() as conn:
        rows = conn.execute(
            "SELECT DISTINCT topic FROM flashcards ORDER BY topic"
        ).fetchall()
    return [row["topic"] for row in rows]


def get_flashcards(topic):
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM flashcards WHERE topic = ? ORDER BY id",
            (topic,)
        ).fetchall()
    return [dict(row) for row in rows]


def add_exam(name, subject, exam_date):
    with _connect() as conn:
        conn.execute(
            "INSERT INTO exams(name, subject, exam_date) VALUES (?, ?, ?)",
            (name, subject, exam_date)
        )


def get_exams():
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM exams ORDER BY exam_date ASC"
        ).fetchall()
    return [dict(row) for row in rows]


def delete_exam(exam_id):
    with _connect() as conn:
        conn.execute("DELETE FROM exams WHERE id = ?", (exam_id,))


def unlock_achievement(code, title, description):
    with _connect() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO achievements(code, title, description) VALUES (?, ?, ?)",
            (code, title, description)
        )


def get_achievements():
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM achievements ORDER BY unlocked_at DESC"
        ).fetchall()
    return [dict(row) for row in rows]
