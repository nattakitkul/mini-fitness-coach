
# Changelog — Mini Fitness Coach

All notable changes to the Mini Fitness Coach project are documented in this file.

This changelog records the development of Mini Fitness Coach across three sprints, from the initial command-line application to the final desktop application.

The project uses version numbers to represent major development milestones.

---

## [1.0.0] — Final Project Release

**Release type:** Stable release
**Development stage:** Final Project
**Status:** Complete

### Overview

This release consolidates the features developed during Sprint 1, Sprint 2, and Sprint 3 into the final Mini Fitness Coach application.

The project combines exercise information retrieval, workout management, persistent data storage, performance analysis, data visualization, automated testing, and a desktop graphical interface.

### Added

* Completed the PySide6 desktop application.
* Added the Exercise Library interface for browsing exercises.
* Added exercise detail views.
* Displayed exercise names, target muscles, equipment, secondary muscles, and instructions where available.
* Added exercise GIF demonstrations where supported by the exercise data.
* Added Workout Programs for organizing exercise sessions.
* Added the Workout Session interface.
* Displayed prescribed sets and repetitions.
* Added actions for starting individual exercises.
* Added a Finish Workout button.
* Connected workout completion to the SQLite database.
* Added a confirmation dialog after recording a workout.
* Integrated the graphical interface with the existing workout logging functionality.
* Retained the command-line application and supporting modules.

### Data Management

* Used SQLite to persist workout records.
* Stored exercise names, workout dates, sets, repetitions, and weight values.
* Supported retrieval of workout history.
* Retained weekly performance calculations from the database module.

### Testing

* Executed the automated test suite using pytest.
* Recorded a successful test run with 13 passed tests and 14 warnings.
* Manually verified workout logging by retrieving saved records from the database.

### Outcome

The project progressed from a command-line fitness tool into a desktop application with exercise browsing, workout sessions, database-backed logging, and supporting performance functionality.

---

## [0.3.0] — Sprint 3: Desktop GUI

**Release type:** Feature release
**Development stage:** Sprint 3
**Status:** Complete

### Overview

Sprint 3 focused on improving user interaction by introducing a desktop graphical user interface. The goal was to make the existing fitness functionality accessible through visual components instead of relying exclusively on command-line interaction.

### Added

* Introduced PySide6 as the desktop GUI framework.
* Developed the main application window.
* Added an Exercise Library interface.
* Added exercise cards to display exercise information.
* Added exercise detail navigation.
* Added exercise GIF display support.
* Added Workout Programs.
* Added Workout Session functionality.
* Added labels for sets and repetitions.
* Added Start Exercise buttons.
* Added a Finish Workout button.
* Added a workout completion confirmation dialog.

### Database Integration

* Imported the workout logging function into the desktop application.
* Connected the Finish Workout button to the database logging function.
* Used the current date when recording workout entries.
* Saved exercise names and workout details into SQLite.
* Verified that multiple exercises could be recorded during a workout completion action.

### User Interface Improvements

* Organized exercise information using cards and labels.
* Added buttons for navigating between workout-related actions.
* Provided a confirmation message after successful workout logging.
* Connected the GUI to the existing application modules instead of duplicating database operations.

### Testing and Verification

* Launched the application through the Python module entry point.
* Verified that the Finish Workout action displayed a confirmation message.
* Retrieved recent workout records from SQLite to confirm persistence.
* Ran the automated test suite after installing the missing Matplotlib dependency.

### Outcome

Sprint 3 delivered the desktop interface and connected the workout completion workflow to persistent storage, bringing the application closer to its final form.

---

## [0.2.0] — Sprint 2: API, Database, and Performance Tracking

**Release type:** Feature release
**Development stage:** Sprint 2
**Status:** Complete

### Overview

Sprint 2 expanded the core application by introducing external exercise data, persistent storage, workout history, performance calculations, and charting functionality.

### Added — Exercise API

* Integrated an external Exercise API through HTTP requests.
* Used the Requests library for API communication.
* Processed exercise information returned by the API.
* Supported retrieval of exercise details for the application's exercise-related features.
* Worked with structured exercise data such as names, target muscles, equipment, and instructions when available.

### Added — SQLite Database

* Created a database module in `src/database.py`.
* Implemented database initialization.
* Created the `workouts` table when it did not already exist.
* Defined fields for workout ID, exercise name, date, sets, repetitions, and weight.
* Used parameterized SQL statements when inserting workout records.
* Implemented workout logging.
* Implemented workout history retrieval.
* Ordered workout history by date.

### Added — Weekly Performance

* Implemented weekly performance statistics.
* Counted workout records during the last seven calendar days.
* Counted distinct exercise names.
* Calculated the total number of sets.
* Added a function to retrieve daily set totals.
* Grouped workout records by date for weekly analysis.

### Added — Data Visualization

* Used Matplotlib to support performance chart functionality.
* Added chart-related functionality to the application.
* Connected workout statistics to the reporting workflow where implemented.

### Added — Automated Testing

* Introduced pytest-based automated tests.
* Added database creation tests.
* Added workout logging tests.
* Added workout history tests.
* Added tests for functions in the main application module.

### Testing and Verification

* Verified database creation using a temporary test database.
* Verified that workout records were inserted with the expected values.
* Verified that workout history returned records in date order.
* Ran the automated test suite after installing Matplotlib.

### Outcome

Sprint 2 established the application's data foundation. Exercise information could be retrieved through an external API, workout records could be stored in SQLite, and historical data could support weekly performance analysis.

---

## [0.1.0] — Sprint 1: CLI Foundation and Input Validation

**Release type:** Initial development release
**Development stage:** Sprint 1
**Status:** Complete

### Overview

Sprint 1 established the initial structure of Mini Fitness Coach. The focus was on creating the basic Python application, defining how users interact with the system, and validating user input.

### Added — Command-Line Interface

* Created the initial command-line application.
* Added a basic interaction flow for users.
* Accepted user input through the terminal.
* Established the foundation for the exercise suggestion workflow.

### Added — Input Validation

* Added validation for user-provided input.
* Established checks intended to prevent invalid input from disrupting the application flow.
* Organized the initial program logic to separate input handling from other operations where appropriate.

### Added — Initial Application Structure

* Established the initial Python project structure.
* Created the foundation for the main application module.
* Prepared the application for later API integration and database development.

### Outcome

Sprint 1 delivered the initial command-line foundation. This provided the starting point for adding external exercise data, workout logging, performance tracking, and a graphical interface in subsequent sprints.

---

## Version Summary

| Version   | Development Stage | Main Focus                                                      |
| --------- | ----------------- | --------------------------------------------------------------- |
| `0.1.0` | Sprint 1          | CLI, input validation, and core application structure           |
| `0.2.0` | Sprint 2          | Exercise API, SQLite, workout history, and performance analysis |
| `0.3.0` | Sprint 3          | PySide6 GUI, workout sessions, and database integration         |
| `1.0.0` | Final Release     | Consolidated application and final verification                 |

---

## Project Status

**Project:** Mini Fitness Coach
**Development Process:** Three Sprints
**Final Status:** Complete

**Repository:** https://github.com/nattakitkul/mini-fitness-coach

### Notes

* Version numbers represent development milestones organized retrospectively from the three-sprint project.
* The changelog describes the implemented features and recorded verification results available during development.
* The version numbers do not imply that corresponding Git tags have already been created.
* Features described as available where supported depend on the exercise data returned by the external API.
