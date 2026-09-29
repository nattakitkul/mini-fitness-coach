import sys
from datetime import datetime
import tempfile
import requests


from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QMovie
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QMessageBox,
    QScrollArea,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from src.database import log_workout
from src.api import suggest_exercises

class GifLoader(QThread):

    finished = Signal(bytes)
    failed = Signal()

    def __init__(self, url):
        super().__init__()

        self.url = url

    def run(self):

        try:
            response = requests.get(
                self.url,
                timeout=10,
                verify=False
            )

            response.raise_for_status()

            self.finished.emit(
                response.content
            )

        except requests.RequestException:

            self.failed.emit()

class ExerciseCard(QFrame):
    clicked = Signal(dict)
    def __init__(self, exercise):
        super().__init__()

        self.exercise = exercise

        self.setFrameShape(QFrame.StyledPanel)
        self.setMinimumSize(240, 320)
        self.setMaximumWidth(280)

        layout = QVBoxLayout()

        # ==============================
        # Exercise GIF
        # ==============================

        self.image_label = QLabel("Loading...")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumHeight(180)

        layout.addWidget(self.image_label)

        # ==============================
        # Exercise Name
        # ==============================

        name = QLabel(
            exercise.get("name", "Unknown Exercise")
        )
        name.setAlignment(Qt.AlignCenter)
        name.setWordWrap(True)

        layout.addWidget(name)

        # ==============================
        # Target Muscle
        # ==============================

        target = exercise.get("targetMuscles", [])

        target_label = QLabel(
            f"Target: {', '.join(target)}"
        )
        target_label.setAlignment(Qt.AlignCenter)
        target_label.setWordWrap(True)

        layout.addWidget(target_label)

        # ==============================
        # Equipment
        # ==============================

        equipment = exercise.get("equipments", [])

        equipment_label = QLabel(
            f"Equipment: {', '.join(equipment)}"
        )
        equipment_label.setAlignment(Qt.AlignCenter)
        equipment_label.setWordWrap(True)

        layout.addWidget(equipment_label)

        self.setLayout(layout)

        # ==============================
        # Load GIF
        # ==============================

        self.load_gif()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.exercise)

        super().mousePressEvent(event)

    def load_gif(self):

        url = self.exercise.get("gifUrl")

        if not url:
            self.image_label.setText(
                "No image"
            )
            return

        self.image_label.setText(
            "Loading image..."
        )

        self.gif_loader = GifLoader(url)

        self.gif_loader.finished.connect(
            self.gif_loaded
        )

        self.gif_loader.failed.connect(
            self.gif_failed
        )

        self.gif_loader.start()

    def gif_loaded(self, data):

        temp_file = tempfile.NamedTemporaryFile(
            suffix=".gif",
            delete=False
        )

        temp_file.write(data)
        temp_file.close()

        self.gif_path = temp_file.name

        self.movie = QMovie(
            self.gif_path
        )

        if not self.movie.isValid():

            self.image_label.setText(
                "No image"
            )

            return

        self.image_label.setMovie(
            self.movie
        )

        self.movie.start()

    def gif_failed(self):

        self.image_label.setText(
            "No image"
        )

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Mini Fitness Coach"
        )

        self.resize(1200, 750)

        # ==============================
        # Main Layout
        # ==============================

        main_layout = QHBoxLayout()

        # ==============================
        # Sidebar
        # ==============================

        sidebar = QWidget()
        sidebar.setFixedWidth(220)

        sidebar_layout = QVBoxLayout()

        logo = QLabel(
            "🏋️\nMini Fitness Coach"
        )

        logo.setAlignment(
            Qt.AlignCenter
        )

        sidebar_layout.addWidget(logo)

        sidebar_layout.addSpacing(30)

        self.home_button = QPushButton(
            "🏠  Home"
        )

        self.workouts_button = QPushButton(
            "💪  Workouts"
        )

        self.exercises_button = QPushButton(
            "🏋️  Exercises"
        )

        self.progress_button = QPushButton(
            "📊  Progress"
        )

        self.records_button = QPushButton(
            "🏆  Records"
        )

        self.goals_button = QPushButton(
            "🎯  Goals"
        )

        sidebar_layout.addWidget(
            self.home_button
        )

        sidebar_layout.addWidget(
            self.workouts_button
        )

        sidebar_layout.addWidget(
            self.exercises_button
        )

        sidebar_layout.addWidget(
            self.progress_button
        )

        sidebar_layout.addWidget(
            self.records_button
        )

        sidebar_layout.addWidget(
            self.goals_button
        )

        sidebar_layout.addStretch()

        sidebar.setLayout(
            sidebar_layout
        )

        # ==============================
        # Pages
        # ==============================

        self.pages = QStackedWidget()

        self.pages.addWidget(
            self.create_home_page()
        )

        self.pages.addWidget(
            self.create_workouts_page()
        )

        self.pages.addWidget(
            self.create_exercises_page()
        )

        self.pages.addWidget(
            self.create_progress_page()
        )

        self.pages.addWidget(
            self.create_records_page()
        )

        self.pages.addWidget(
            self.create_goals_page()
        )

        # ==============================
        # Navigation
        # ==============================

        self.home_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(0)
        )

        self.workouts_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(1)
        )

        self.exercises_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(2)
        )

        self.progress_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(3)
        )

        self.records_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(4)
        )

        self.goals_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(5)
        )

        # ==============================
        # Combine
        # ==============================

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.pages)

        container = QWidget()

        container.setLayout(
            main_layout
        )

        self.setCentralWidget(
            container
        )

    # ==========================================
    # HOME
    # ==========================================

    def create_home_page(self):

        page = QWidget()

        layout = QVBoxLayout()

        title = QLabel(
            "Welcome to Mini Fitness Coach"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        subtitle = QLabel(
            "Your personal workout companion"
        )

        subtitle.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addStretch()

        page.setLayout(layout)

        return page

    # ==========================================
    # WORKOUTS
    # ==========================================

    def create_workouts_page(self):
        page = QWidget()

        layout = QVBoxLayout()

        title = QLabel(
                "💪 Workout Programs"
        )

        title.setAlignment(
                Qt.AlignCenter
        )

        layout.addWidget(title)

        subtitle = QLabel(
                "Choose a workout program"
        )

        subtitle.setAlignment(
                Qt.AlignCenter
        )

        layout.addWidget(subtitle)

        # ==============================
        # Workout Programs
        # ==============================

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

                card.setFrameShape(
                        QFrame.StyledPanel
                )

                card.setMinimumHeight(150)

                card_layout = QVBoxLayout()

                name = QLabel(
                        program["name"]
                )

                name.setAlignment(
                        Qt.AlignCenter
                )

                card_layout.addWidget(name)

                description = QLabel(
                        program["description"]
                )

                description.setAlignment(
                        Qt.AlignCenter
                )

                description.setWordWrap(True)

                card_layout.addWidget(
                        description
                )

                days = QLabel(
                        program["days"]
                )

                days.setAlignment(
                        Qt.AlignCenter
                )

                card_layout.addWidget(days)

                exercise_count = QLabel(
                        f'{len(program["exercises"])} Exercises'
                )

                exercise_count.setAlignment(
                        Qt.AlignCenter
                )

                card_layout.addWidget(
                        exercise_count
                )

                start_button = QPushButton(
                        "▶ Start Workout"
                )

                start_button.clicked.connect(
                lambda checked=False, p=program:
                self.start_workout(p)
                )

                card_layout.addWidget(
                        start_button
                )

                card.setLayout(
                        card_layout
                )

                layout.addWidget(
                        card
                )

        layout.addStretch()

        page.setLayout(
                layout
        )

        return page
    # ==========================================
    # EXERCISES
    # ==========================================

    def create_exercises_page(self):

        page = QWidget()

        main_layout = QVBoxLayout()

        title = QLabel(
            "🏋️ Exercise Library"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        main_layout.addWidget(title)

        # ==============================
        # Muscle Buttons
        # ==============================

        filter_layout = QHBoxLayout()

        muscles = [
            "chest",
            "back",
            "legs",
            "shoulders",
            "arms",
            "abs",
        ]

        for muscle in muscles:

            button = QPushButton(
                muscle.capitalize()
            )

            button.clicked.connect(
                lambda checked=False,
                m=muscle:
                self.load_exercises(m)
            )

            filter_layout.addWidget(
                button
            )

        main_layout.addLayout(
            filter_layout
        )

        # ==============================
        # Scroll Area
        # ==============================

        self.exercise_scroll = QScrollArea()

        self.exercise_scroll.setWidgetResizable(
            True
        )

        self.exercise_container = QWidget()

        self.exercise_layout = QHBoxLayout()

        self.exercise_container.setLayout(
            self.exercise_layout
        )

        self.exercise_scroll.setWidget(
            self.exercise_container
        )

        main_layout.addWidget(
            self.exercise_scroll
        )

        page.setLayout(
            main_layout
        )

        # Load Chest initially

        self.load_exercises(
            "chest"
        )

        return page

    # ==========================================
    # LOAD EXERCISES
    # ==========================================

    def load_exercises(self, muscle):

        # Clear old cards

        while self.exercise_layout.count():

            item = self.exercise_layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

        # Loading message

        loading = QLabel(
            "Loading exercises..."
        )

        loading.setAlignment(
            Qt.AlignCenter
        )

        self.exercise_layout.addWidget(
            loading
        )

        QApplication.processEvents()

        # Fetch API

        exercises = suggest_exercises(
            muscle
        )

        # Remove loading

        while self.exercise_layout.count():

            item = self.exercise_layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

        if not exercises:

            message = QLabel(
                "No exercises found."
            )

            message.setAlignment(
                Qt.AlignCenter
            )

            self.exercise_layout.addWidget(
                message
            )

            return

        # Add cards

        for exercise in exercises[:8]:

            card = ExerciseCard(
                exercise
            )

            card.clicked.connect(
                self.show_exercise_detail
            )

            self.exercise_layout.addWidget(
                card
            )

        self.exercise_layout.addStretch()

    # ==========================================
    # PROGRESS
    # ==========================================

    def show_exercise_detail(self, exercise):

        page = QWidget()

        layout = QVBoxLayout()

        image_label = QLabel("Loading image...")
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setMinimumHeight(250)

        layout.addWidget(image_label)

        # ==============================
        # Back Button
        # ==============================

        back_button = QPushButton(
            "← Back to Exercises"
        )

        back_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(2)
        )

        layout.addWidget(
            back_button
        )

        # ==============================
        # Exercise Name
        # ==============================

        name = QLabel(
            exercise.get(
                "name",
                "Unknown Exercise"
            )
        )

        name.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            name
        )

        # ==============================
        # Target
        # ==============================

        target = exercise.get(
            "targetMuscles",
            []
        )

        target_label = QLabel(
            f"Target Muscles: {', '.join(target)}"
        )

        target_label.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            target_label
        )

        # ==============================
        # Equipment
        # ==============================

        equipment = exercise.get(
            "equipments",
            []
        )

        equipment_label = QLabel(
            f"Equipment: {', '.join(equipment)}"
        )

        equipment_label.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            equipment_label
        )

        # ==============================
        # Secondary Muscles
        # ==============================

        secondary = exercise.get(
            "secondaryMuscles",
            []
        )

        secondary_label = QLabel(
            f"Secondary Muscles: {', '.join(secondary)}"
        )

        secondary_label.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            secondary_label
        )

        # ==============================
        # Instructions
        # ==============================

        instructions = exercise.get(
            "instructions",
            []
        )

        instruction_text = "\n".join(
            instructions
        )

        instruction_label = QLabel(
            "Instructions\n\n"
            + instruction_text
        )

        instruction_label.setWordWrap(
            True
        )

        layout.addWidget(
            instruction_label
        )

        # ==============================
        # Start Exercise
        # ==============================

        start_button = QPushButton(
            "▶ Start Exercise"
        )

        layout.addWidget(
            start_button
        )

        layout.addStretch()

        page.setLayout(
            layout
        )

        url = exercise.get("gifUrl")

        if url:
            loader = GifLoader(url)

            def gif_loaded(data):
                temp_file = tempfile.NamedTemporaryFile(
                    suffix=".gif",
                    delete=False
                )
                temp_file.write(data)
                temp_file.close()

                movie = QMovie(temp_file.name)

                if movie.isValid():
                    image_label.setMovie(movie)
                    movie.start()
                else:
                    image_label.setText("No image")

            def gif_failed():
                image_label.setText("No image")

            loader.finished.connect(gif_loaded)
            loader.failed.connect(gif_failed)

            page.gif_loader = loader
            loader.start()

        else:
            image_label.setText("No image")
        # Add detail page

        index = self.pages.addWidget(
            page
        )

        self.pages.setCurrentIndex(
            index
        )

    def start_workout(self, program):

        self.show_workout_session(program)

    def show_workout_session(self, program):

        page = QWidget()

        layout = QVBoxLayout()

        title = QLabel(
            program["name"]
        )

        title.setAlignment(
                Qt.AlignCenter
        )

        layout.addWidget(title)

        push_up_data = suggest_exercises("chest")
        

        back_data = suggest_exercises("back")


        lat_pulldown = None

        for item in back_data:

            if "machine front pulldown" in item.get("name", "").lower():

                lat_pulldown = item

                break
        
        push_up = None

        for item in push_up_data:

            if "push" in item.get("name", "").lower():
                
                push_up = item

                break

        if push_up:

            push_up["name"] = "Push Up"

            push_up_card = ExerciseCard(push_up)

            layout.addWidget(push_up_card)

            push_up_sets = QLabel(
            "3 Sets × 10 Reps"
            )

            push_up_sets.setAlignment(
            Qt.AlignCenter
            )

            layout.addWidget(
            push_up_sets
            )

            push_up_button = QPushButton(
                "▶ Start Push Up"
            )

            layout.addWidget(
                push_up_button
            )

            push_up_button.clicked.connect(
                lambda: self.show_exercise_detail(push_up)
            )
            
        if lat_pulldown:

            lat_pulldown["name"] = "Lat Pulldown"

            lat_card = ExerciseCard(lat_pulldown)

            layout.addWidget(lat_card)
        lat_sets = QLabel(
        "3 Sets × 10 Reps"
        )

        lat_sets.setAlignment(
        Qt.AlignCenter
        )

        layout.addWidget(
        lat_sets
        )

        page.setLayout(
                layout
        )

        index = self.pages.addWidget(
                page
        )

        self.pages.setCurrentIndex(
                index
        )
        lat_button = QPushButton(
            "▶ Start Lat Pulldown"
        )

        layout.addWidget(
            lat_button
        )

        lat_button.clicked.connect(
            lambda: self.show_exercise_detail(lat_pulldown)
        )
        
        finish_button = QPushButton(
            "✓ Finish Workout"
        )

        layout.addWidget(
            finish_button   
        )
        finish_button.clicked.connect(
            lambda: (
            log_workout(
                "Push Up",
                datetime.now().strftime("%Y-%m-%d"),
                3,
                10,
                0
            ),

            log_workout(
                "Lat Pulldown",
                datetime.now().strftime("%Y-%m-%d"),
                3,
                10,
                0
            ),



            QMessageBox.information(
                self,
                "Workout Completed",
                "Workout logged successfully!"
            )
        )
        )

    def create_progress_page(self):

        page = QWidget()

        layout = QVBoxLayout()

        title = QLabel(
            "📊 Progress"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        info = QLabel(
            "Your workout progress will appear here."
        )

        info.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(title)
        layout.addWidget(info)

        layout.addStretch()

        page.setLayout(layout)

        return page

    # ==========================================
    # RECORDS
    # ==========================================

    def create_records_page(self):

        page = QWidget()

        layout = QVBoxLayout()

        title = QLabel(
            "🏆 Personal Records"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        info = QLabel(
            "Your personal records will appear here."
        )

        info.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(title)
        layout.addWidget(info)

        layout.addStretch()

        page.setLayout(layout)

        return page

    # ==========================================
    # GOALS
    # ==========================================

    def create_goals_page(self):

        page = QWidget()

        layout = QVBoxLayout()

        title = QLabel(
            "🎯 Workout Goals"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        info = QLabel(
            "Your workout goals will appear here."
        )

        info.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(title)
        layout.addWidget(info)

        layout.addStretch()

        page.setLayout(layout)

        return page


def main():

    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()