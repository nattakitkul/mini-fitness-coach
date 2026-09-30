import requests
import urllib3


BASE_URL = "https://oss.exercisedb.dev/api/v1/exercises"
API_URL = BASE_URL + "/bodyparts"
SEARCH_URL = BASE_URL + "/search"

# The original program disabled SSL verification. Kept as one switch here so it
# is easy to turn on (True) if your network allows it.
VERIFY_SSL = False

if not VERIFY_SSL:
    urllib3.disable_warnings(
        urllib3.exceptions.InsecureRequestWarning
    )


MUSCLE_MAP = {
    "chest": ["chest"],
    "back": ["back"],
    "legs": ["upper legs", "lower legs"],
    "shoulders": ["shoulders"],
    "arms": ["upper arms", "lower arms"],
    "abs": ["waist"],
}


def _get_json(url, params):
    """GET a URL and return parsed JSON, or None on any error."""
    try:
        response = requests.get(
            url,
            params=params,
            timeout=10,
            verify=VERIFY_SSL
        )

        if response.status_code == 429:
            print("API rate limit reached. Please try again later.")
            return None

        response.raise_for_status()

        return response.json()

    except requests.RequestException as error:
        print("API Error:", error)
        return None

    except ValueError as error:
        print("JSON Error:", error)
        return None


def fetch_exercises(body_parts, limit=12):
    """Fetch exercises for the given body parts from ExerciseDB."""
    return _get_json(
        API_URL,
        {
            "bodyParts": ",".join(body_parts),
            "limit": limit,
        }
    )


def suggest_exercises(muscle):
    """Suggest exercises for a muscle group.

    Each body part is requested separately and the results are interleaved,
    so a group like "legs" shows both upper and lower leg exercises instead of
    only whichever part the API happens to list first.
    """
    target_parts = MUSCLE_MAP.get(muscle.lower(), [])

    if not target_parts:
        return []

    per_part = []

    for part in target_parts:
        data = fetch_exercises([part])

        if data:
            per_part.append(data.get("data", []))

    results = []
    seen = set()

    for index in range(max((len(items) for items in per_part), default=0)):
        for items in per_part:
            if index < len(items):
                exercise = items[index]
                key = exercise.get("exerciseId") or exercise.get("name")

                if key not in seen:
                    seen.add(key)
                    results.append(exercise)

    return results


def find_exercise_by_name(name):
    """Look up one exercise by name. Returns the exercise dict or None.

    Used for workout programs, which only store exercise names.
    """
    data = _get_json(
        SEARCH_URL,
        {
            "q": name,
            "limit": 1,
        }
    )

    if not data:
        return None

    items = data.get("data", [])

    return items[0] if items else None


if __name__ == "__main__":
    exercises = suggest_exercises("legs")

    if exercises:
        print("API connection successful!")
        print("Exercises found:", len(exercises))

        for exercise in exercises[:5]:
            print("-", exercise.get("name"))
    else:
        print("No exercises found.")