from datetime import datetime




def is_valid_date(date):
    """Check whether the date follows YYYY-MM-DD format."""
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False

    
def is_valid_menu_choice(choice):
    """Check whether the main menu choice is valid."""
    return choice in ["1", "2", "3", "4"]

def is_valid_exercise_choice(choice):
    """Check whether the exercise menu choice is valid."""
    return choice in ["1", "2", "3", "4", "5", "6", "7"]


def show_menu():
    print("\n================================")
    print("       MINI FITNESS COACH")
    print("================================")
    print("1. Exercise Suggestion")
    print("2. Workout Logger")
    print("3. Weekly Performance")
    print("4. Exit")
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

        if choice == "1":
            print("\nYou selected Chest")

        elif choice == "2":
            print("\nYou selected Back")

        elif choice == "3":
            print("\nYou selected Legs")

        elif choice == "4":
            print("\nYou selected Shoulders")

        elif choice == "5":
            print("\nYou selected Arms")

        elif choice == "6":
            print("\nYou selected Abs")

        elif choice == "7":
            break

        else:
            print("\nInvalid choice. Please select 1-7.")


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
    sets = input("Enter number of sets: ")
    reps = input("Enter number of reps: ")
    weight = input("Enter weight used (kg): ")

    print("\nWorkout  information")
    print("Exercise: ",exercise)
    print("Date: ",date)
    print("Sets: ",sets)
    print("Reps: ",reps)
    print("Weight: ",weight)


def weekly_performance():
    print("\n==============================")
    print("      WEEKLY PERFORMANCE")
    print("==============================")
    print("Workout count: -")
    print("Exercise frequency: -")
    print("Total sets: -")
    print("\nChart coming soon: -")


def main():
    while True:
        show_menu()

        choice = input("Select menu: ")

        if not is_valid_menu_choice(choice):
            print("\nInvalid choice. Please select 1-4.")
            continue

        if choice == "1":
            exercise_menu()

        elif choice == "2":
            workout_menu()

        elif choice == "3":
            weekly_performance()

        elif choice == "4":
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid choice. Please select 1-4.")


if __name__ == "__main__":
    main()