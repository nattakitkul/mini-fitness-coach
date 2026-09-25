import sqlite3
from src import database


def test_create_database(tmp_path, monkeypatch):
    test_db = tmp_path / "test.db"

    monkeypatch.setattr(database, "DATABASE", str(test_db))

    database.create_database()

    assert test_db.exists()


def test_log_workout(tmp_path, monkeypatch):
    test_db = tmp_path / "test.db"

    monkeypatch.setattr(database, "DATABASE", str(test_db))

    database.create_database()

    database.log_workout(
        "Bench Press",
        "2026-09-22",
        4,
        10,
        20
    )

    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM workouts")
    row = cursor.fetchone()

    conn.close()

    assert row[1] == "Bench Press"
    assert row[2] == "2026-09-22"
    assert row[3] == 4
    assert row[4] == 10
    assert row[5] == 20


def test_get_workout_history(tmp_path, monkeypatch):
    test_db = tmp_path / "test.db"

    monkeypatch.setattr(database, "DATABASE", str(test_db))

    database.create_database()

    database.log_workout(
        "Bench Press",
        "2026-09-22",
        4,
        10,
        20
    )

    database.log_workout(
        "Squat",
        "2026-09-23",
        3,
        12,
        30
    )

    workouts = database.get_workout_history()

    assert len(workouts) == 2
    assert workouts[0] == ("Bench Press", "2026-09-22", 4, 10, 20)
    assert workouts[1] == ("Squat", "2026-09-23", 3, 12, 30)