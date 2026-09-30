# This import must stay first. matplotlib.dates loads dateutil/six, which
# crashes with an AttributeError if PySide6 has already been imported.
import matplotlib.dates  # noqa: F401

import hashlib
import os
import shutil
import sys
import tempfile
from datetime import datetime

import requests

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from PySide6.QtCore import Qt, QSize, QThread, Signal, Slot
from PySide6.QtGui import QMovie
from PySide6.QtWidgets import (
    QApplication,
    QDoubleSpinBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from src.analysis import analyze_weekly_performance, weekly_chart_data
from src.api import VERIFY_SSL, find_exercise_by_name, suggest_exercises
from src.charts import draw_weekly_chart
from src.database import (
    create_database,
    get_history,
    get_personal_records,
    save_session,
)


# ==========================================
# PAGE INDEXES
# ==========================================
#
# Every page has ONE fixed slot in the QStackedWidget. Pages are never added
# while the program runs, they only change their content when opened.
#

HOME, WORKOUTS, EXERCISES, PROGRESS, RECORDS, GOALS, DETAIL, SESSION = range(8)

EXERCISE_COLUMNS = 3
EXERCISES_PER_BATCH = 12


# ==========================================
# BACKGROUND WORK
# ==========================================

_threads = set()


class Worker(QThread):
    """Run fn(*args) in a background thread, then call callback(result)
    on the main thread. result is None if fn raised an error."""

    done = Signal(object)

    def __init__(self, fn, args, callback):
        super().__init__()

        self.fn = fn
        self.args = args
        self.callback = callback

        # Both slots belong to this object, which lives in the main thread,
        # so Qt runs them there.
        self.done.connect(self._deliver)
        self.finished.connect(self._cleanup)

    def run(self):
        try:
            result = self.fn(*self.args)
        except Exception as error:
            print("Background task error:", error)
            result = None

        self.done.emit(result)

    @Slot(object)
    def _deliver(self, result):
        try:
            self.callback(result)
        except RuntimeError:
            # The widget that wanted the result was already deleted.
            pass

    @Slot()
    def _cleanup(self):
        _threads.discard(self)


def run_async(fn, *args, callback):
    worker = Worker(fn, args, callback)
    _threads.add(worker)  # keep a reference until the thread has finished
    worker.start()


# ==========================================
# GIF LOADING (shared by cards and detail page)
# ==========================================

_gif_dir = tempfile.mkdtemp(prefix="fitness_gifs_")
_gif_cache = {}


def download_gif(url):
    """Download a GIF once and return the local file path."""
    if url in _gif_cache:
        return _gif_cache[url]

    response = requests.get(url, timeout=10, verify=VERIFY_SSL)
    response.raise_for_status()

    name = hashlib.md5(url.encode()).hexdigest() + ".gif"
    path = os.path.join(_gif_dir, name)

    with open(path, "wb") as file:
        file.write(response.content)

    _gif_cache[url] = path

    return path


def show_gif(label, path, size):
    """Show a downloaded GIF in a label (or 'No image' if it is unusable)."""
    if not path:
        label.setText("No image")
        return

    movie = QMovie(path)

    if not movie.isValid():
        label.setText("No image")
        return

    movie.setScaledSize(QSize(size, size))
    label.setMovie(movie)
    label._movie = movie  # keep the movie alive
    movie.start()


def load_gif_into(label, url, size):
    if not url:
        label.setText("No image")
        return

    label.setText("Loading image...")

    run_async(
        download_gif,
        url,
        callback=lambda path: show_gif(label, path, size)
    )


# ==========================================
# SMALL HELPERS
# ==========================================

def title_label(text):
    label = QLabel(text)
    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet("font-size: 22px; font-weight: bold;")
    return label


def centered_label(text="", wrap=False):
    label = QLabel(text)
    label.setAlignment(Qt.AlignCenter)
    label.setWordWrap(wrap)
    return label


def clear_layout(layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()

        if widget:
            widget.deleteLater()


def format_sets(sets):
    return ", ".join(f"{reps} × {weight:g} kg" for reps, weight in sets)


# ==========================================
# EXERCISE CARD (Exercises page)
# ==========================================

class ExerciseCard(QFrame):
    clicked = Signal(dict)

    def __init__(self, exercise):
        super().__init__()

        self.exercise = exercise

        self.setFrameShape(QFrame.StyledPanel)
        self.setMinimumSize(220, 300)
        self.setMaximumWidth(280)
        self.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout()

        self.image_label = centered_label("Loading image...")
        self.image_label.setMinimumHeight(180)
        layout.addWidget(self.image_label)

        layout.addWidget(
            centered_label(exercise.get("name", "Unknown Exercise"), True)
        )

        target = exercise.get("targetMuscles", [])
        layout.addWidget(
            centered_label(f"Target: {', '.join(target)}", True)
        )

        equipment = exercise.get("equipments", [])
        layout.addWidget(
            centered_label(f"Equipment: {', '.join(equipment)}", True)
        )

        self.setLayout(layout)

        load_gif_into(self.image_label, exercise.get("gifUrl"), 180)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.exercise)

        super().mousePressEvent(event)


# ==========================================
# EXERCISE DETAIL PAGE (one page, reused)
# ==========================================

class ExerciseDetailPage(QWidget):
    back_requested = Signal()
    start_requested = Signal(dict)

    def __init__(self):
        super().__init__()

        self.back_index = EXERCISES
        self.exercise = {}
        self.token = 0  # detects results that arrive for an older exercise

        layout = QVBoxLayout()

        back_button = QPushButton("← Back")
        back_button.clicked.connect(self.back_requested.emit)
        layout.addWidget(back_button)

        self.image_label = centered_label("")
        self.image_label.setMinimumHeight(280)
        layout.addWidget(self.image_label)

        self.name_label = title_label("")
        self.name_label.setWordWrap(True)
        layout.addWidget(self.name_label)

        self.target_label = centered_label("", True)
        self.equipment_label = centered_label("", True)
        self.secondary_label = centered_label("", True)

        layout.addWidget(self.target_label)
        layout.addWidget(self.equipment_label)
        layout.addWidget(self.secondary_label)

        self.instructions_label = QLabel("")
        self.instructions_label.setWordWrap(True)
        self.instructions_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.instructions_label)
        layout.addWidget(scroll, 1)

        self.start_button = QPushButton("▶ Start Exercise")
        self.start_button.clicked.connect(
            lambda: self.start_requested.emit(self.exercise)
        )
        layout.addWidget(self.start_button)

        self.setLayout(layout)

    def show_exercise(self, exercise, back_index, allow_start):
        """Fill the page with an exercise.

        back_index: page the Back button returns to
        allow_start: False when opened from a workout that is already running
        """
        self.token += 1
        self.back_index = back_index
        self.exercise = exercise
        self.start_button.setVisible(allow_start)

        # Programs only know exercise names. Look up the full details.
        incomplete = (
            not exercise.get("gifUrl")
            and not exercise.get("instructions")
        )

        self._render(exercise, loading=incomplete)

        if incomplete:
            token = self.token

            run_async(
                find_exercise_by_name,
                exercise.get("name", ""),
                callback=lambda found: self._on_found(found, token)
            )

    def _render(self, exercise, loading=False):
        self.name_label.setText(exercise.get("name", "Unknown Exercise"))

        self.target_label.setText(
            "Target Muscles: " + ", ".join(exercise.get("targetMuscles", []))
        )
        self.equipment_label.setText(
            "Equipment: " + ", ".join(exercise.get("equipments", []))
        )
        self.secondary_label.setText(
            "Secondary Muscles: "
            + ", ".join(exercise.get("secondaryMuscles", []))
        )

        steps = exercise.get("instructions", [])

        if steps:
            self.instructions_label.setText(
                "Instructions\n\n" + "\n".join(steps)
            )
        elif loading:
            self.instructions_label.setText("Loading details...")
        else:
            self.instructions_label.setText("No instructions available.")

        url = exercise.get("gifUrl")

        if url:
            self.image_label.setText("Loading image...")
            token = self.token

            run_async(
                download_gif,
                url,
                callback=lambda path: self._on_image(path, token)
            )
        else:
            self.image_label.setText(
                "Loading image..." if loading else "No image"
            )

    def _on_found(self, found, token):
        if token != self.token:
            return  # the user already moved to another exercise

        if found:
            merged = dict(found)
            merged["name"] = self.exercise.get("name", found.get("name"))
            self.exercise = merged

        self._render(self.exercise)

    def _on_image(self, path, token):
        if token != self.token:
            return

        show_gif(self.image_label, path, 280)


# ==========================================
# WORKOUT SESSION PAGE (one page, reused)
# ==========================================

class ExerciseBlock(QFrame):
    """One exercise in a running workout, with editable sets."""

    details_requested = Signal(dict)

    def __init__(self, exercise):
        super().__init__()

        self.exercise = exercise
        self.rows = []

        self.setFrameShape(QFrame.StyledPanel)

        layout = QVBoxLayout()

        header = QHBoxLayout()

        name = QLabel(exercise.get("name", "Unknown Exercise"))
        name.setStyleSheet("font-size: 16px; font-weight: bold;")
        name.setWordWrap(True)
        header.addWidget(name, 1)

        details_button = QPushButton("ℹ Details")
        details_button.clicked.connect(
            lambda: self.details_requested.emit(self.exercise)
        )
        header.addWidget(details_button)

        layout.addLayout(header)

        self.sets_layout = QVBoxLayout()
        layout.addLayout(self.sets_layout)

        buttons = QHBoxLayout()

        add_button = QPushButton("+ Add set")
        add_button.clicked.connect(self.add_set)
        buttons.addWidget(add_button)

        remove_button = QPushButton("− Remove set")
        remove_button.clicked.connect(self.remove_set)
        buttons.addWidget(remove_button)

        layout.addLayout(buttons)

        self.setLayout(layout)

        for _ in range(3):
            self.add_set()

    def add_set(self):
        # New sets start with the values of the previous set.
        if self.rows:
            _, last_reps, last_weight = self.rows[-1]
            reps_value = last_reps.value()
            weight_value = last_weight.value()
        else:
            reps_value = 10
            weight_value = 0.0

        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)

        row_layout.addWidget(QLabel(f"Set {len(self.rows) + 1}"))

        reps = QSpinBox()
        reps.setRange(1, 200)
        reps.setSuffix(" reps")
        reps.setValue(reps_value)
        row_layout.addWidget(reps)

        weight = QDoubleSpinBox()
        weight.setRange(0, 1000)
        weight.setDecimals(1)
        weight.setSingleStep(2.5)
        weight.setSuffix(" kg")
        weight.setValue(weight_value)
        row_layout.addWidget(weight)

        self.rows.append((row, reps, weight))
        self.sets_layout.addWidget(row)

    def remove_set(self):
        if len(self.rows) <= 1:
            return

        row, _, _ = self.rows.pop()
        self.sets_layout.removeWidget(row)
        row.deleteLater()

    def exercise_name(self):
        return self.exercise.get("name", "Unknown Exercise")

    def get_sets(self):
        return [(reps.value(), weight.value()) for _, reps, weight in self.rows]


class SessionPage(QWidget):
    finished = Signal()
    cancelled = Signal()
    details_requested = Signal(dict)

    def __init__(self):
        super().__init__()

        self.back_index = WORKOUTS
        self.session_name = "Workout"
        self.blocks = []

        layout = QVBoxLayout()

        header = QHBoxLayout()

        cancel_button = QPushButton("← Cancel workout")
        cancel_button.clicked.connect(self.cancelled.emit)
        header.addWidget(cancel_button)

        self.title = title_label("Workout Session")
        header.addWidget(self.title, 1)

        layout.addLayout(header)

        self.blocks_layout = QVBoxLayout()
        self.blocks_layout.addStretch()

        container = QWidget()
        container.setLayout(self.blocks_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(container)
        layout.addWidget(scroll, 1)

        finish_button = QPushButton("✓ Finish Workout")
        finish_button.clicked.connect(self.finish)
        layout.addWidget(finish_button)

        self.setLayout(layout)

    def start(self, name, exercises, back_index):
        """Begin a fresh workout. exercises = names or exercise dicts."""
        self.back_index = back_index
        self.session_name = name
        self.title.setText(name)

        # Remove old blocks (keep the stretch at the end).
        while self.blocks_layout.count() > 1:
            item = self.blocks_layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        self.blocks = []

        for exercise in exercises:
            if not isinstance(exercise, dict):
                exercise = {"name": exercise}

            block = ExerciseBlock(exercise)
            block.details_requested.connect(self.details_requested.emit)

            self.blocks.append(block)
            self.blocks_layout.insertWidget(
                self.blocks_layout.count() - 1,
                block
            )

    def finish(self):
        exercises = [
            (block.exercise_name(), block.get_sets())
            for block in self.blocks
        ]

        today = datetime.now().strftime("%Y-%m-%d")

        session_id = save_session(self.session_name, today, exercises)

        if session_id is None:
            QMessageBox.warning(
                self,
                "Nothing to save",
                "This workout has no sets."
            )
            return

        total_sets = sum(len(sets) for _, sets in exercises)

        QMessageBox.information(
            self,
            "Workout Completed",
            f"Saved {len(exercises)} exercise(s), {total_sets} set(s)."
        )

        self.finished.emit()


# ==========================================
# PROGRESS PAGE
# ==========================================

class ProgressPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(title_label("Weekly Progress"))

        self.workouts_label = centered_label()
        self.exercises_label = centered_label()
        self.sets_label = centered_label()

        layout.addWidget(self.workouts_label)
        layout.addWidget(self.exercises_label)
        layout.addWidget(self.sets_label)
        layout.addSpacing(10)

        # Weekly chart (matplotlib embedded in the window)
        self.figure = Figure(figsize=(7, 4))
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setMinimumHeight(300)

        layout.addWidget(self.canvas, 1)

        self.setLayout(layout)

        self.refresh()

    def refresh(self):
        stats = analyze_weekly_performance()

        self.workouts_label.setText(
            f"Workouts (last 7 days): {stats['workouts']}"
        )
        self.exercises_label.setText(
            f"Different exercises: {stats['exercises']}"
        )
        self.sets_label.setText(f"Total sets: {stats['sets']}")

        labels, values = weekly_chart_data()

        draw_weekly_chart(self.axes, labels, values)
        self.figure.tight_layout()
        self.canvas.draw_idle()


# ==========================================
# RECORDS PAGE
# ==========================================

class RecordsPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(title_label("🏆 Records"))

        self.content_layout = QVBoxLayout()

        container = QWidget()
        container.setLayout(self.content_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(container)

        layout.addWidget(scroll)

        self.setLayout(layout)

        self.refresh()

    def refresh(self):
        clear_layout(self.content_layout)

        records = get_personal_records()
        history = get_history()

        if not history:
            self.content_layout.addWidget(
                centered_label("No workout records yet.")
            )
            self.content_layout.addStretch()
            return

        # Personal bests
        heading = QLabel("Personal bests")
        heading.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.content_layout.addWidget(heading)

        for name, best_weight, best_reps in records:
            self.content_layout.addWidget(
                QLabel(f"{name}: {best_weight:g} kg | best {best_reps} reps")
            )

        # History, newest first
        heading = QLabel("History")
        heading.setStyleSheet(
            "font-size: 16px; font-weight: bold; margin-top: 16px;"
        )
        self.content_layout.addWidget(heading)

        for session in history:
            card = QFrame()
            card.setFrameShape(QFrame.StyledPanel)

            card_layout = QVBoxLayout()

            header = QLabel(f"{session['date']} — {session['name']}")
            header.setStyleSheet("font-weight: bold;")
            card_layout.addWidget(header)

            for exercise in session["exercises"]:
                line = QLabel(
                    f"{exercise['name']}: {format_sets(exercise['sets'])}"
                )
                line.setWordWrap(True)
                card_layout.addWidget(line)

            card.setLayout(card_layout)
            self.content_layout.addWidget(card)

        self.content_layout.addStretch()


# ==========================================
# MAIN WINDOW
# ==========================================

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mini Fitness Coach")
        self.resize(1200, 750)

        # State of the Exercises page
        self.exercise_request = 0
        self.exercise_results = []
        self.exercise_shown = 0

        main_layout = QHBoxLayout()

        # ------------------------------
        # Sidebar
        # ------------------------------

        sidebar = QWidget()
        sidebar.setFixedWidth(220)

        sidebar_layout = QVBoxLayout()

        sidebar_layout.addWidget(centered_label("🏋️\nMini Fitness Coach"))
        sidebar_layout.addSpacing(30)

        nav = [
            ("🏠  Home", HOME),
            ("💪  Workouts", WORKOUTS),
            ("🏋️  Exercises", EXERCISES),
            ("📊  Progress", PROGRESS),
            ("🏆  Records", RECORDS),
            ("🎯  Goals", GOALS),
        ]

        for text, index in nav:
            button = QPushButton(text)
            button.clicked.connect(
                lambda checked=False, i=index: self.go(i)
            )
            sidebar_layout.addWidget(button)

        sidebar_layout.addStretch()
        sidebar.setLayout(sidebar_layout)

        # ------------------------------
        # Pages (added in the order of the index constants)
        # ------------------------------

        self.progress_page = ProgressPage()
        self.records_page = RecordsPage()

        self.detail_page = ExerciseDetailPage()
        self.detail_page.back_requested.connect(
            lambda: self.go(self.detail_page.back_index)
        )
        self.detail_page.start_requested.connect(self.start_from_detail)

        self.session_page = SessionPage()
        self.session_page.details_requested.connect(
            lambda exercise: self.open_detail(exercise, SESSION)
        )
        self.session_page.finished.connect(lambda: self.go(PROGRESS))
        self.session_page.cancelled.connect(
            lambda: self.go(self.session_page.back_index)
        )

        self.pages = QStackedWidget()

        for page in [
            self.create_home_page(),        # HOME
            self.create_workouts_page(),    # WORKOUTS
            self.create_exercises_page(),   # EXERCISES
            self.progress_page,             # PROGRESS
            self.records_page,              # RECORDS
            self.create_goals_page(),       # GOALS
            self.detail_page,               # DETAIL
            self.session_page,              # SESSION
        ]:
            self.pages.addWidget(page)

        # Progress and Records re-read the database every time they are opened.
        self.pages.currentChanged.connect(self.on_page_changed)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.pages, 1)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    # ------------------------------
    # Navigation
    # ------------------------------

    def go(self, index):
        self.pages.setCurrentIndex(index)

    def on_page_changed(self, index):
        if index == PROGRESS:
            self.progress_page.refresh()
        elif index == RECORDS:
            self.records_page.refresh()

    def open_detail(self, exercise, origin):
        """Open the detail page. Back returns to `origin`."""
        self.detail_page.show_exercise(
            exercise,
            origin,
            allow_start=(origin != SESSION)
        )
        self.go(DETAIL)

    def start_session(self, name, exercises, back_index):
        self.session_page.start(name, exercises, back_index)
        self.go(SESSION)

    def start_from_detail(self, exercise):
        self.start_session(
            exercise.get("name", "Workout"),
            [exercise],
            self.detail_page.back_index
        )

    # ------------------------------
    # HOME
    # ------------------------------

    def create_home_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(title_label("Welcome to Mini Fitness Coach"))
        layout.addWidget(centered_label("Your personal workout companion"))
        layout.addStretch()

        page.setLayout(layout)
        return page

    # ------------------------------
    # WORKOUTS
    # ------------------------------

    def create_workouts_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(title_label("💪 Workout Programs"))
        layout.addWidget(centered_label("Choose a workout program"))

        programs = [
            {
                "name": "Beginner Full Body",
                "description": "A simple full-body workout for beginners.",
                "days": "3 Days / Week",
                "exercises": [
                    "Push Up",
                    "Bodyweight Squat",
                    "Lat Pulldown",
                    "Dumbbell Shoulder Press",
                ],
            },
            {
                "name": "Chest & Triceps",
                "description": "Focus on chest and triceps.",
                "days": "2 Days / Week",
                "exercises": [
                    "Bench Press",
                    "Cable Crossover",
                    "Chest Fly",
                    "Triceps Pushdown",
                ],
            },
            {
                "name": "Leg Day",
                "description": "Lower-body focused workout.",
                "days": "2 Days / Week",
                "exercises": [
                    "Barbell Squat",
                    "Leg Press",
                    "Leg Extension",
                    "Leg Curl",
                    "Calf Raise",
                ],
            },
        ]

        for program in programs:
            card = QFrame()
            card.setFrameShape(QFrame.StyledPanel)
            card.setMinimumHeight(150)

            card_layout = QVBoxLayout()

            name = centered_label(program["name"])
            name.setStyleSheet("font-size: 16px; font-weight: bold;")
            card_layout.addWidget(name)

            card_layout.addWidget(centered_label(program["description"], True))
            card_layout.addWidget(centered_label(program["days"]))
            card_layout.addWidget(
                centered_label(f"{len(program['exercises'])} Exercises")
            )

            start_button = QPushButton("▶ Start Workout")
            start_button.clicked.connect(
                lambda checked=False, p=program: self.start_session(
                    p["name"], p["exercises"], WORKOUTS
                )
            )
            card_layout.addWidget(start_button)

            card.setLayout(card_layout)
            layout.addWidget(card)

        layout.addStretch()

        page.setLayout(layout)
        return page

    # ------------------------------
    # EXERCISES
    # ------------------------------

    def create_exercises_page(self):
        page = QWidget()
        main_layout = QVBoxLayout()

        main_layout.addWidget(title_label("🏋️ Exercise Library"))

        filter_layout = QHBoxLayout()

        for muscle in ["chest", "back", "legs", "shoulders", "arms", "abs"]:
            button = QPushButton(muscle.capitalize())
            button.clicked.connect(
                lambda checked=False, m=muscle: self.load_exercises(m)
            )
            filter_layout.addWidget(button)

        main_layout.addLayout(filter_layout)

        self.exercise_status = centered_label("")
        main_layout.addWidget(self.exercise_status)

        self.exercise_grid = QGridLayout()
        self.exercise_grid.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        container = QWidget()
        container.setLayout(self.exercise_grid)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(container)
        main_layout.addWidget(scroll, 1)

        self.more_button = QPushButton("Show more")
        self.more_button.clicked.connect(self.show_more_exercises)
        self.more_button.hide()
        main_layout.addWidget(self.more_button)

        page.setLayout(main_layout)

        self.load_exercises("chest")

        return page

    def load_exercises(self, muscle):
        # Each request gets a number. If the user clicks another muscle before
        # the first one arrives, the old answer is ignored.
        self.exercise_request += 1
        request = self.exercise_request

        clear_layout(self.exercise_grid)
        self.exercise_results = []
        self.exercise_shown = 0
        self.more_button.hide()
        self.exercise_status.setText("Loading exercises...")

        run_async(
            suggest_exercises,
            muscle,
            callback=lambda result: self.on_exercises_loaded(result, request)
        )

    def on_exercises_loaded(self, exercises, request):
        if request != self.exercise_request:
            return

        if not exercises:
            self.exercise_status.setText("No exercises found.")
            return

        self.exercise_status.setText("")
        self.exercise_results = exercises
        self.show_more_exercises()

    def show_more_exercises(self):
        start = self.exercise_shown
        batch = self.exercise_results[start:start + EXERCISES_PER_BATCH]

        for exercise in batch:
            card = ExerciseCard(exercise)
            card.clicked.connect(
                lambda ex: self.open_detail(ex, EXERCISES)
            )

            row, column = divmod(self.exercise_shown, EXERCISE_COLUMNS)
            self.exercise_grid.addWidget(card, row, column)

            self.exercise_shown += 1

        self.more_button.setVisible(
            self.exercise_shown < len(self.exercise_results)
        )

    # ------------------------------
    # GOALS
    # ------------------------------

    def create_goals_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(title_label("🎯 Workout Goals"))
        layout.addWidget(centered_label("Your workout goals will appear here."))
        layout.addStretch()

        page.setLayout(layout)
        return page


def cleanup():
    """Wait for background threads and delete the temporary GIF files."""
    for worker in list(_threads):
        worker.wait(3000)

    shutil.rmtree(_gif_dir, ignore_errors=True)


def main():
    create_database()

    app = QApplication(sys.argv)
    app.aboutToQuit.connect(cleanup)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()