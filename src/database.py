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



if __name__ == "__main__":
    create_database()
    print("Database created successfully.")