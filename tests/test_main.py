from src.main import (
    show_menu,
    exercise_menu,
    workout_menu,
    workout_history,
    weekly_performance,
    main,
    is_valid_menu_choice,
    is_valid_exercise_choice,
    is_valid_date
)


def test_show_menu():
    show_menu()


def test_exercise_menu_back(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "7")

    exercise_menu()


def test_workout_menu(monkeypatch):
    inputs = iter([
        "Bench Press",
        "2026-09-22",
        "4",
        "10",
        "20"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    workout_menu()


def test_weekly_performance():
    weekly_performance()

def test_invalid_main_menu_choice(monkeypatch, capsys):
    inputs = iter(["99", "5"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    main()

    captured = capsys.readouterr()

    assert "Invalid choice. Please select 1-5." in captured.out
    assert "Goodbye!" in captured.out


def test_is_valid_menu_choice():
    assert is_valid_menu_choice("1") is True
    assert is_valid_menu_choice("2") is True
    assert is_valid_menu_choice("3") is True
    assert is_valid_menu_choice("4") is True
    assert is_valid_menu_choice("5") is True

    assert is_valid_menu_choice("6") is False
    assert is_valid_menu_choice("99") is False
    assert is_valid_menu_choice("abc") is False

def test_is_valid_exercise_choice():
    assert is_valid_exercise_choice("1") is True
    assert is_valid_exercise_choice("2") is True
    assert is_valid_exercise_choice("3") is True
    assert is_valid_exercise_choice("4") is True
    assert is_valid_exercise_choice("5") is True
    assert is_valid_exercise_choice("6") is True
    assert is_valid_exercise_choice("7") is True

    assert is_valid_exercise_choice("8") is False
    assert is_valid_exercise_choice("99") is False
    assert is_valid_exercise_choice("abc") is False

def test_invalid_exercise_choice(monkeypatch, capsys):
    inputs = iter(["99", "7"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    exercise_menu()

    captured = capsys.readouterr()

    assert "Invalid choice. Please select 1-7." in captured.out

def test_is_valid_date():
    #correct date format
    assert is_valid_date("2026-09-22") is True
    assert is_valid_date("2026-01-01") is True

    # wrong date format
    assert is_valid_date("2026-13-50") is False
    assert is_valid_date("abc") is False
    assert is_valid_date("22-09-2026") is False


def test_workout_history(monkeypatch):
    workout_history()