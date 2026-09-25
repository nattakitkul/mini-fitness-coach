from datetime import datetime
from src.database import create_database, log_workout, get_workout_history
from src.api import suggest_exercises


def is_valid_date(date):
    """Check whether the date follows YYYY-MM-DD format."""
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False

    
def is_valid_menu_choice(choice):
    """Check whether the main menu choice is valid."""
    return choice in ["1", "2", "3", "4","5"]

def is_valid_exercise_choice(choice):
    """Check whether the exercise menu choice is valid."""
    return choice in ["1", "2", "3", "4", "5", "6", "7"]


def show_menu():
    print("\n================================")
    print("       MINI FITNESS COACH")
    print("================================")
    print("1. Exercise Suggestion")
    print("2. Workout Logger")
    print("3. Workout History")
    print("4. Weekly Performance")
    print("5. Exit")
    print("================================")


def exercise_menu():
    while True:
        print("\n==============================")
        print("      EXERCISE SUGGESTION")
        print("==============================")
        print("1. Chest")
        print("2. Back")
        print("3. Legs")
        print("4. Shoulders")
        print("5. Arms")
        print("6. Abs")
        print("7. Back to menu")

        choice = input("Select muscle group: ")

        if not is_valid_exercise_choice(choice):
            print("\nInvalid choice. Please select 1-7.")
            continue

        if choice == "7":
            break

        muscle_groups = {
            "1": "chest",
            "2": "back",
            "3": "legs",
            "4": "shoulders",
            "5": "arms",
            "6": "abs"
        }

        muscle = muscle_groups[choice]

        print(f"\nYou selected {muscle.title()}")
        print("Loading exercises...")

        exercises = suggest_exercises(muscle)

        if not exercises:
            print("No exercises found.")
            continue

        print("\nRecommended Exercises:")

        for exercise in exercises[:10]:
            name = exercise.get("name", "Unknown")
            equipment = exercise.get("equipments", [])

            print(f"\n- {name}")

            if equipment:
                print(f"  Equipment: {', '.join(equipment)}")


def workout_menu():
    print("\n==============================")
    print("      WORKOUT LOGGER")
    print("==============================")

    exercise = input("Enter exercise name: ")

    while True:
        date = input("Enter date (YYYY-MM-DD): ")

        if is_valid_date(date):
            break
        else:
            print("Invalid date. Please use YYYY-MM-DD.")

    sets = int(input("Enter number of sets: "))
    reps = int(input("Enter number of reps: "))
    weight = float(input("Enter weight used (kg): "))

    log_workout(
        exercise,
        date,
        sets,
        reps,
        weight
    )
    print("\nWorkout saved successfully!")


def workout_history():
    """Display all saved workout records."""
    print("\n==============================")
    print("       WORKOUT HISTORY")
    print("==============================")

    workouts = get_workout_history()

    if not workouts:
        print("No workout history found.")
        return

    for workout in workouts:
        exercise, date, sets, reps, weight = workout

        print("\nExercise:", exercise)
        print("Date:", date)
        print("Sets:", sets)
        print("Reps:", reps)
        print("Weight:", weight, "kg")


def weekly_performance():
    print("\n==============================")
    print("      WEEKLY PERFORMANCE")
    print("==============================")
    print("Workout count: -")
    print("Exercise frequency: -")
    print("Total sets: -")
    print("\nChart coming soon: -")


def main():
    create_database()


    while True:
        show_menu()

        choice = input("Select menu: ")

        if not is_valid_menu_choice(choice):
            print("\nInvalid choice. Please select 1-5.")
            continue

        if choice == "1":
            exercise_menu()

        elif choice == "2":
            workout_menu()

        elif choice == "3":
            workout_history()

        elif choice == "4":
            weekly_performance()

        elif choice == "5":
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid choice. Please select 1-4.")


if __name__ == "__main__":
    main()