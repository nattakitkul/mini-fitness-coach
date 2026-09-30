import os
import sqlite3
from contextlib import contextmanager
from datetime import date, timedelta


# Absolute path, so the database is the same no matter where the program is run from.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATABASE = os.path.join(DATA_DIR, "fitness.db")


@contextmanager
def db():
    """Open a connection, commit on success, roll back on error, always close."""
    os.makedirs(DATA_DIR, exist_ok=True)

    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _week_start():
    """First day of the 7-day window (today and the 6 days before), local time."""
    return (date.today() - timedelta(days=6)).isoformat()


# ==========================================
# SCHEMA
# ==========================================
#
# sessions: one row = one time the user went and worked out
# sets:     one row = one real set (reps + weight) done in that session
#

def create_database():
    """Create the tables if needed and import old data once."""
    with db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS sets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL
                    REFERENCES sessions(id) ON DELETE CASCADE,
                exercise_name TEXT NOT NULL,
                set_number INTEGER NOT NULL,
                reps INTEGER NOT NULL,
                weight REAL NOT NULL
            )
        """)

        _migrate_old_workouts(conn)


def _migrate_old_workouts(conn):
    """Move rows from the old one-row-per-exercise table into sessions/sets.

    Old rows have no session, so all rows from the same date become one session.
    The old table is renamed (not deleted) so nothing is lost.
    """
    old = conn.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type = 'table' AND name = 'workouts'"
    ).fetchone()

    if not old:
        return

    rows = conn.execute("""
        SELECT exercise_name, date, sets, repetitions, weight
        FROM workouts
        ORDER BY date, id
    """).fetchall()

    session_by_date = {}

    for exercise_name, day, sets, reps, weight in rows:
        if day not in session_by_date:
            cursor = conn.execute(
                "INSERT INTO sessions (name, date) VALUES (?, ?)",
                ("Imported workout", day)
            )
            session_by_date[day] = cursor.lastrowid

        for number in range(1, sets + 1):
            conn.execute("""
                INSERT INTO sets
                (session_id, exercise_name, set_number, reps, weight)
                VALUES (?, ?, ?, ?, ?)
            """, (session_by_date[day], exercise_name, number, reps, weight))

    conn.execute("ALTER TABLE workouts RENAME TO workouts_legacy")


# ==========================================
# WRITE
# ==========================================

def save_session(name, day, exercises):
    """Save one finished workout.

    exercises: list of (exercise_name, [(reps, weight), (reps, weight), ...])
    Returns the new session id, or None if there were no sets to save.
    """
    exercises = [
        (exercise_name, sets)
        for exercise_name, sets in exercises
        if sets
    ]

    if not exercises:
        return None

    with db() as conn:
        cursor = conn.execute(
            "INSERT INTO sessions (name, date) VALUES (?, ?)",
            (name, day)
        )

        session_id = cursor.lastrowid

        for exercise_name, sets in exercises:
            for number, (reps, weight) in enumerate(sets, start=1):
                conn.execute("""
                    INSERT INTO sets
                    (session_id, exercise_name, set_number, reps, weight)
                    VALUES (?, ?, ?, ?, ?)
                """, (session_id, exercise_name, number, reps, weight))

    return session_id


# ==========================================
# READ
# ==========================================

def get_history():
    """All sessions, newest first.

    Returns a list of dicts:
    {"id", "name", "date", "exercises": [{"name", "sets": [(reps, weight), ...]}]}
    """
    with db() as conn:
        rows = conn.execute("""
            SELECT s.id, s.name, s.date,
                   t.exercise_name, t.reps, t.weight
            FROM sessions s
            JOIN sets t ON t.session_id = s.id
            ORDER BY s.date DESC, s.id DESC, t.id ASC
        """).fetchall()

    sessions = []
    by_id = {}

    for session_id, name, day, exercise_name, reps, weight in rows:
        if session_id not in by_id:
            session = {
                "id": session_id,
                "name": name,
                "date": day,
                "exercises": [],
            }
            by_id[session_id] = session
            sessions.append(session)

        session = by_id[session_id]

        if (not session["exercises"]
                or session["exercises"][-1]["name"] != exercise_name):
            session["exercises"].append(
                {"name": exercise_name, "sets": []}
            )

        session["exercises"][-1]["sets"].append((reps, weight))

    return sessions


def get_personal_records():
    """Best weight and best reps ever done for each exercise.

    Returns a list of (exercise_name, best_weight, best_reps).
    """
    with db() as conn:
        return conn.execute("""
            SELECT exercise_name, MAX(weight), MAX(reps)
            FROM sets
            GROUP BY exercise_name
            ORDER BY exercise_name
        """).fetchall()


def get_weekly_performance():
    """Stats for the last 7 days (local time).

    Returns (workouts, different_exercises, total_sets), where
    workouts = number of sessions, not number of exercises.
    """
    with db() as conn:
        return conn.execute("""
            SELECT
                COUNT(DISTINCT s.id),
                COUNT(DISTINCT t.exercise_name),
                COUNT(t.id)
            FROM sessions s
            LEFT JOIN sets t ON t.session_id = s.id
            WHERE s.date >= ?
        """, (_week_start(),)).fetchone()


def get_weekly_sets():
    """Total sets for each day of the last 7 days (only days with data)."""
    with db() as conn:
        return conn.execute("""
            SELECT s.date, COUNT(t.id)
            FROM sessions s
            JOIN sets t ON t.session_id = s.id
            WHERE s.date >= ?
            GROUP BY s.date
            ORDER BY s.date
        """, (_week_start(),)).fetchall()


if __name__ == "__main__":
    create_database()
    print("Database created successfully.")