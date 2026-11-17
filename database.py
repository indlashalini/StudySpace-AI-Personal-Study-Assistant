
import sqlite3

DATABASE_NAME = "study_assistant.db"


# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# --------------------------------------------------
# CREATE DATABASE TABLES
# --------------------------------------------------

def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Study tasks
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            task TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            priority TEXT NOT NULL,
            deadline TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)

    # Subjects
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE COLLATE NOCASE,
            description TEXT DEFAULT ''
        )
    """)

    # Syllabus topics
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS syllabus_topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER NOT NULL,
            topic_name TEXT NOT NULL,
            teacher_taught INTEGER DEFAULT 0,
            learned INTEGER DEFAULT 0,
            needs_revision INTEGER DEFAULT 0,
            FOREIGN KEY (subject_id)
                REFERENCES subjects(id)
                ON DELETE CASCADE,
            UNIQUE(subject_id, topic_name)
        )
    """)

    # Daily study sessions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            topic TEXT NOT NULL,
            duration INTEGER NOT NULL,
            study_date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# --------------------------------------------------
# TASK FUNCTIONS: CREATE, READ, UPDATE, DELETE
# --------------------------------------------------

def add_task(subject, task, difficulty, priority, deadline):
    conn = get_connection()

    conn.execute("""
        INSERT INTO tasks
        (subject, task, difficulty, priority, deadline)
        VALUES (?, ?, ?, ?, ?)
    """, (subject, task, difficulty, priority, deadline))

    conn.commit()
    conn.close()


def get_tasks():
    conn = get_connection()

    rows = conn.execute("""
        SELECT * FROM tasks
        ORDER BY deadline ASC, id DESC
    """).fetchall()

    conn.close()
    return [dict(row) for row in rows]


def update_task(task_id, subject, task, difficulty, priority, deadline):
    conn = get_connection()

    conn.execute("""
        UPDATE tasks
        SET subject = ?,
            task = ?,
            difficulty = ?,
            priority = ?,
            deadline = ?
        WHERE id = ?
    """, (subject, task, difficulty, priority, deadline, task_id))

    conn.commit()
    conn.close()


def update_task_status(task_id, completed):
    conn = get_connection()

    conn.execute("""
        UPDATE tasks
        SET completed = ?
        WHERE id = ?
    """, (int(completed), task_id))

    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = get_connection()

    conn.execute("""
        DELETE FROM tasks
        WHERE id = ?
    """, (task_id,))

    conn.commit()
    conn.close()


# --------------------------------------------------
# SUBJECT FUNCTIONS: CREATE, READ, UPDATE, DELETE
# --------------------------------------------------

def add_subject(name, description=""):
    conn = get_connection()

    try:
        conn.execute("""
            INSERT INTO subjects (name, description)
            VALUES (?, ?)
        """, (name.strip(), description.strip()))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def get_subjects():
    conn = get_connection()

    rows = conn.execute("""
        SELECT * FROM subjects
        ORDER BY name ASC
    """).fetchall()

    conn.close()
    return [dict(row) for row in rows]


def update_subject(subject_id, name, description):
    conn = get_connection()

    try:
        conn.execute("""
            UPDATE subjects
            SET name = ?, description = ?
            WHERE id = ?
        """, (name.strip(), description.strip(), subject_id))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def delete_subject(subject_id):
    conn = get_connection()

    conn.execute("""
        DELETE FROM subjects
        WHERE id = ?
    """, (subject_id,))

    conn.commit()
    conn.close()


# --------------------------------------------------
# SYLLABUS TOPIC FUNCTIONS
# --------------------------------------------------

def add_topic(subject_id, topic_name):
    conn = get_connection()

    try:
        conn.execute("""
            INSERT INTO syllabus_topics
            (subject_id, topic_name)
            VALUES (?, ?)
        """, (subject_id, topic_name.strip()))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def get_topics(subject_id):
    conn = get_connection()

    rows = conn.execute("""
        SELECT * FROM syllabus_topics
        WHERE subject_id = ?
        ORDER BY id ASC
    """, (subject_id,)).fetchall()

    conn.close()
    return [dict(row) for row in rows]


def update_topic(topic_id, topic_name):
    conn = get_connection()

    try:
        conn.execute("""
            UPDATE syllabus_topics
            SET topic_name = ?
            WHERE id = ?
        """, (topic_name.strip(), topic_id))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def update_topic_status(topic_id, field, value):
    allowed_fields = [
        "teacher_taught",
        "learned",
        "needs_revision"
    ]

    if field not in allowed_fields:
        raise ValueError("Invalid topic status field")

    conn = get_connection()

    conn.execute(
        f"UPDATE syllabus_topics SET {field} = ? WHERE id = ?",
        (int(value), topic_id)
    )

    conn.commit()
    conn.close()


def delete_topic(topic_id):
    conn = get_connection()

    conn.execute("""
        DELETE FROM syllabus_topics
        WHERE id = ?
    """, (topic_id,))

    conn.commit()
    conn.close()


# --------------------------------------------------
# DAILY STUDY SESSION FUNCTIONS
# --------------------------------------------------

def add_study_session(subject, topic, duration, study_date):
    conn = get_connection()

    conn.execute("""
        INSERT INTO study_sessions
        (subject, topic, duration, study_date)
        VALUES (?, ?, ?, ?)
    """, (subject, topic.strip(), int(duration), study_date))

    conn.commit()
    conn.close()


def get_study_sessions():
    conn = get_connection()

    rows = conn.execute("""
        SELECT * FROM study_sessions
        ORDER BY study_date DESC, id DESC
    """).fetchall()

    conn.close()
    return [dict(row) for row in rows]


def delete_study_session(session_id):
    conn = get_connection()

    conn.execute("""
        DELETE FROM study_sessions
        WHERE id = ?
    """, (session_id,))

    conn.commit()
    conn.close()


# --------------------------------------------------
# INITIALIZE DATABASE
# --------------------------------------------------

create_database()
