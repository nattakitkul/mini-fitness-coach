import requests
import urllib3


API_URL = "https://oss.exercisedb.dev/api/v1/exercises/bodyparts"

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)


def fetch_exercises(body_parts):
    """Fetch exercises by body parts from ExerciseDB API."""
    try:
        params = {
            "bodyParts": ",".join(body_parts),
            "limit": 25
        }

        response = requests.get(
            API_URL,
            params=params,
            timeout=10,
            verify=False
        )

        if response.status_code == 429:
            print("API rate limit reached. Please try again later.")
            return None

        response.raise_for_status()

        data = response.json()

        return data

    except requests.RequestException as error:
        print("API Error:", error)
        return None

    except ValueError as error:
        print("JSON Error:", error)
        return None


def suggest_exercises(muscle):
    """Suggest exercises based on muscle group."""

    muscle_map = {
        "chest": ["chest"],
        "back": ["back"],
        "legs": ["upper legs", "lower legs"],
        "shoulders": ["shoulders"],
        "arms": ["upper arms", "lower arms"],
        "abs": ["waist"]
    }

    target_parts = muscle_map.get(muscle.lower(), [])

    if not target_parts:
        return []

    data = fetch_exercises(target_parts)

    if not data:
        return []

    return data.get("data", [])


if __name__ == "__main__":
    exercises = suggest_exercises("legs")

    if exercises:
        print("API connection successful!")
        print("Exercises found:", len(exercises))

        for exercise in exercises[:5]:
            print("-", exercise.get("name"))
    else:
        print("No exercises found.")