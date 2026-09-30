"""Weekly statistics and CSV export.

Pure functions plus thin wrappers around the database.
"""

import csv
from datetime import date, timedelta

from src.database import get_history, get_weekly_performance, get_weekly_sets


CSV_HEADER = ["date", "workout", "exercise", "set", "reps", "weight_kg"]


def last_7_days(today=None):
    """The 7 days ending today (oldest first), in local time."""
    today = today or date.today()

    return [today - timedelta(days=offset) for offset in range(6, -1, -1)]


def fill_missing_days(rows, days):
    """Turn [(date_text, sets), ...] into one (date, sets) pair for every day.

    Days without any workout get 0, so the chart always shows all 7 days.
    """
    sets_by_day = dict(rows)

    return [(day, sets_by_day.get(day.isoformat(), 0)) for day in days]


def analyze_weekly_performance():
    """Workout statistics for the last 7 days.

    workouts  = number of times the user worked out (sessions)
    exercises = number of different exercises
    sets      = total number of sets
    """
    workouts, exercises, sets = get_weekly_performance()

    return {
        "workouts": workouts,
        "exercises": exercises,
        "sets": sets,
    }


def weekly_chart_data(today=None):
    """Labels and values for the weekly bar chart, e.g. (["Mon 28", ...], [4, 0, ...])."""
    days = last_7_days(today)
    filled = fill_missing_days(get_weekly_sets(), days)

    labels = [day.strftime("%a %d") for day, _ in filled]
    values = [sets for _, sets in filled]

    return labels, values


def history_to_rows(sessions):
    """Flatten sessions (as returned by get_history) into CSV rows.

    One row per set: [date, workout, exercise, set number, reps, weight].
    """
    rows = []

    for session in sessions:
        for exercise in session["exercises"]:
            for number, (reps, weight) in enumerate(exercise["sets"], start=1):
                rows.append([
                    session["date"],
                    session["name"],
                    exercise["name"],
                    number,
                    reps,
                    weight,
                ])

    return rows


def export_history_csv(path, sessions=None):
    """Write the workout history to a CSV file, oldest workout first.

    Returns the number of sets written. Raises OSError if the file cannot be
    written (for example when it is open in Excel).
    """
    if sessions is None:
        sessions = get_history()

    # get_history returns the newest workout first; a spreadsheet reads better
    # in chronological order.
    rows = history_to_rows(list(reversed(sessions)))

    # utf-8-sig adds a BOM so Excel shows non-English text correctly.
    with open(path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(CSV_HEADER)
        writer.writerows(rows)

    return len(rows)