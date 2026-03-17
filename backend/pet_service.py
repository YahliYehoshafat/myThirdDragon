from pets_db import get_latest_pet_state
import pets_db
from typing import Dict, Any, List
from Pet import Pet


ACTION_MAP = {
    "sleep": Pet.sleep,
    "play": Pet.play,
    "eat": Pet.eat
}


def get_pet_properties(pet_id: int) -> Dict[str, Any]:
    """
    Retrieves the properties of a pet from the database using the provided pet ID

    :param pet_id: The unique ID of the pet.
    :param state: The latest state of the pet from the database, or None if it doesn't exist.
    :param actions: A list of all actions the pet has performed
    """
    state = pets_db.get_latest_pet_state(pet_id)
    actions = pets_db.get_all_pet_actions(pet_id)
    if state is None:
        return {
            "pet_id": pet_id,
            "energy": 50,
            "hunger": 50,
            "happiness": 50,
            "overall_score": 50,
            "points": 0,
            "actions": []
        }
    return {
        "pet_id": pet_id,
        "energy": state["energy"],
        "hunger": state["hunger"],
        "happiness": state["happiness"],
        "overall_score": state["overall_score"],
        "points": state["points"],
        "actions": actions  
    }


def get_user_pets(user_id: int) -> List[Dict[str, Any]]:
    """
    Returns all pets belonging to a specific user from the database.

    :param pet_id: The unique ID of the pet.
    """
    return pets_db.get_user_pets(user_id)


def perform_action(pet_id: int, action: str) -> Dict[str, Any]:
    """
    Performs a specified action on a pet and updates its state in the database.

    :param pet_id: The unique ID of the pet.
    :param action: The action to perform; must be one of the keys in ACTION_MAP 
    :param state: Current properties of the pet retrieved from the database.
    :param energy: The pet's energy level, updated according to the action.
    :param hunger: The pet's hunger level, updated according to the action. 
    :param happiness: The pet's happiness level, updated according to the action.
    :param points: The pet's points, updated according to the action.
    :param overall_score: The average score of energy, hunger, and happiness after performing the action.
    """
    state = get_pet_properties(pet_id)
    energy = state["energy"]
    hunger = state["hunger"]
    happiness = state["happiness"]
    points = state["points"]
    if action not in ACTION_MAP:
        raise ValueError("Invalid action")
    energy, hunger, happiness, points = ACTION_MAP[action](
        energy, hunger, happiness, points
    )
    overall_score = (energy + hunger + happiness) / 3
    pets_db.insert_to_db(
        pet_id,
        action,
        energy,
        hunger,
        happiness,
        overall_score,
        points
    )
    return {
        "pet_id": pet_id,
        "energy": energy,
        "hunger": hunger,
        "happiness": happiness,
        "overall_score": overall_score,
        "points": points
    }


def create_pet(name: str, pet_type: str, user_id: int) -> Dict[str, Any]:
    """
    Creates a new pet for a given user and stores it in the database.
    
    :param name: The name of the pet to create. Cannot be empty.
    :param pet_type: The type/species of the pet (e.g., "squirrel", "koala", "goat").
    :param user_id: The ID of the user who owns this pet.
    :return: A dictionary containing the pet's ID, name, and type.
    """
    if not name or not name.strip():
        raise ValueError("Pet name is required")
    pet_type = pet_type.lower()
    if pet_type not in ["squirrel", "koala", "goat"]:
        raise ValueError("Invalid pet type")
    pet_id = pets_db.add_new_pet(name.strip(), pet_type, user_id)
    return {
        "pet_id": pet_id,
        "name": name,
        "type": pet_type
    }


def signup_user(username: str, email: str, password: str) -> Dict[str, Any]:
    """
    Signs up a new user by adding them to the database and retrieving their information.
    
    :param username: The username of the new user. Cannot be empty.
    :param email: The email of the new user. Must be unique and cannot be empty.
    :param password: The password for the new user. Cannot be empty.
    :return: A dictionary containing the user's ID, username, and email.
    """
    if not username or not username.strip():
        raise ValueError("Username is required")
    if not email or not email.strip():
        raise ValueError("Email is required")
    if not password or not password.strip():
        raise ValueError("Password is required")
    username = username.strip()
    email = email.strip()
    password = password.strip()
    if pets_db.check_if_email_exists(email):
        raise ValueError("Email already exists")
    pets_db.add_new_user(username, email, password)
    user = pets_db.get_user_by_email_and_password(email, password)
    if not user:
        raise ValueError("Failed to create user")
    return {
        "user_id": user["user_id"],
        "username": user["username"],
        "email": user["email"]
    }


def login_user(email: str, password: str) -> Dict[str, Any]:
    """
    Logs in a user by verifying their email and password against the database.
    
    :param email: The email of the user attempting to log in. Cannot be empty.
    :param password: The password of the user attempting to log in. Cannot be empty.
    :return: A dictionary containing the user's ID, username, and email if login is successful.
    :raises ValueError: If email or password is missing, or if the credentials are incorrect.
    """
    if not email or not email.strip():
        raise ValueError("Email is required")
    if not password or not password.strip():
        raise ValueError("Password is required")
    user_info = pets_db.get_user_by_email_and_password(
        email.strip(),
        password
    )
    if not user_info:
        raise ValueError("Incorrect email or password")
    return {
        "user_id": user_info["user_id"],
        "username": user_info["username"],
        "email": user_info["email"]
    }


def get_metrics(pet_id: int) -> Dict[str, Any]:
    """
    Retrieves various metrics and statistics for a given pet from the database.
    
    :param pet_id: The unique ID of the pet for which metrics are being retrieved.
    :return: A dictionary containing metrics and statistics of the pet, including:
        - overall_score_under: Number of states where overall score was under 70.
        - most_happiness_hour: Hour of the day when the pet was happiest on average.
        - most_popular_action: The action performed most frequently by the pet.
        - points_state: List of points accumulated over time.
        - happiness_state: List of happiness values over time.
        - energy_state: List of energy values over the last 24 hours.
        - last_24_hour: Timestamps corresponding to the last 24 hours for energy tracking.
        - actions_performed: Number of actions performed each day.
        - average_time_between_actions: Average time between consecutive actions (in minutes).
        - dates_range: List of distinct dates where actions were performed.
        - get_timestamp: List of timestamps of all actions.
        - happiness_avg: Average happiness over all recorded states.
    :raises Exception: If an error occurs while fetching metrics from the database.
    """
    try:
        overall_score_under = pets_db.overall_score_under(pet_id) or 0
        most_happiness_hour = pets_db.most_happiness_hour(pet_id) or "No data"
        most_popular_action = pets_db.most_popular_action(pet_id) or "No data"
        points_state = pets_db.points_state(pet_id) or [0]
        happiness_state = pets_db.happiness_state(pet_id) or [50]  
        actions_performed = pets_db.actions_performed_by_day(pet_id) or []
        average_time_between_actions = pets_db.average_time_between_actions(pet_id) or 0
        dates_range = pets_db.dates_range(pet_id) or []
        get_timestamp = pets_db.get_timestamp(pet_id) or []
        energy = pets_db.energy_state(pet_id) or ([], [50]*24) 
        happiness_avg = sum(happiness_state)/len(happiness_state) if happiness_state else 0
        return {
            "overall_score_under": overall_score_under,
            "most_happiness_hour": most_happiness_hour,
            "most_popular_action": most_popular_action,
            "points_state": points_state,
            "happiness_state": happiness_state,
            "energy_state": energy[1],
            "last_24_hour": energy[0],
            "actions_performed": actions_performed,
            "average_time_between_actions": average_time_between_actions,
            "dates_range": dates_range,
            "get_timestamp": get_timestamp,
            "happiness_avg": happiness_avg
        }
    except Exception as e:
        print("ERROR IN get_metrics:", e)
        raise