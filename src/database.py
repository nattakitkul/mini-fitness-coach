import sqlite3


DATABASE = "data/fitness.db"


def create_database():
    """Create the workouts table if it does not exist."""
    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exercise_name TEXT NOT NULL,
            date TEXT NOT NULL,
            sets INTEGER NOT NULL,
            repetitions INTEGER NOT NULL,
            weight REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()



def log_workout(exercise_name, date, sets, repetitions, weight):
    """Save a workout record to the database."""
    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO workouts
        (exercise_name, date, sets, repetitions, weight)
        VALUES (?, ?, ?, ?, ?)
    """, (exercise_name, date, sets, repetitions, weight))

    conn.commit()
    conn.close()


def get_workout_history():
    """Get all workout records from the database."""
    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT exercise_name, date, sets, repetitions, weight
        FROM workouts
        ORDER BY date
    """)

    workouts = cursor.fetchall()

    conn.close()

    return workouts

def get_weekly_performance():
    """Get workout statistics for the last 7 days."""
    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) AS workout_count,
            COUNT(DISTINCT exercise_name) AS exercise_frequency,
            COALESCE(SUM(sets), 0) AS total_sets
        FROM workouts
        WHERE date >= date('now', '-6 days')
    """)

    result = cursor.fetchone()

    conn.close()

    return result

def get_weekly_sets():
    """Get total sets for each of the last 7 days."""
    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT date, SUM(sets)
        FROM workouts
        WHERE date >= date('now', '-6 days')
        GROUP BY date
        ORDER BY date
    """)

    result = cursor.fetchall()

    conn.close()

    return result

if __name__ == "__main__":
    create_database()
    print("Database created successfully.")