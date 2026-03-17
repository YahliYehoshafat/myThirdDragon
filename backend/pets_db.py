import pymysql
from datetime import datetime
from pymysql.connections import Connection
from typing import List, Tuple, Any, Dict


def get_connection() -> Connection:
    """
    Establishes a connection to the MySQL database.
    """
    return pymysql.connect(
        host="192.168.1.106",  
        port=3306,                   
        user="root",
        password="Shtuzon@1",
        database="petsdb",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
        ssl_disabled=True
    )
 

def insert_to_db(pet_id: int, action_type: str,energy: int, hunger: int, happiness: int, overall_score: float,
                 points: int) -> None:
    """
    Inserts a new record into the `pet_states` table for a specific pet.

    :param pet_id: The unique ID of the pet.
    :param action_type: The type of action the pet performed.
    :param energy: The pet's energy level at the time of the action.
    :param hunger: The pet's hunger level at the time of the action.
    :param happiness: The pet's happiness level at the time of the action.
    :param overall_score: The overall score for the pet at the time of the action.
    :param points: Points awarded or associated with the action.
    """
    connection = get_connection()
    cursor = connection.cursor()
    sql = """
    INSERT INTO pet_states (pet_id, action_type, energy, hunger, happiness, points, overall_score, timestamp)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (
        pet_id, action_type, energy,
        hunger, happiness, points,
        overall_score, datetime.now()
    ))
    connection.commit()
    cursor.close()
    connection.close()


def get_latest_pet_state(pet_id: int) -> Dict[str, Any]:
    """
    Retrieves the latest state record for a specific pet.

    :param pet_id: The unique ID of the pet.
    """
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM pet_states WHERE pet_id = %s ORDER BY timestamp DESC LIMIT 1"
    cursor.execute(sql, (pet_id,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result


def add_new_pet(pet_name: str, pet_type: str, user_id: int) -> int:
    """
    Adds a new pet to the `pets` table in the database.

    :param pet_name: The name of the new pet.
    :param pet_type: The type or species of the pet.
    :param user_id: The unique ID of the user who owns the pet.
    """
    connection = get_connection()
    cursor = connection.cursor()
    sql = "INSERT INTO pets (pet_name, user_id, pet_type) VALUES (%s, %s, %s)"
    cursor.execute(sql, (pet_name, user_id, pet_type))
    connection.commit()
    pet_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return pet_id


def get_user_pets(user_id: int) -> List[Dict[str, Any]]:
    """
    Retrieves all pets associated with a specific user.

    :param user_id: The unique ID of the user.
    """
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM pets WHERE user_id = %s"
    cursor.execute(sql, (user_id,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


def points_state(pet_id: int) -> List[int]:
    """
    Retrieves all points recorded for a specific pet from the `pet_states` table.

    :param pet_id: The unique ID of the pet.
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT points FROM pet_states WHERE pet_id=%s", (pet_id,))
    result = [row["points"] for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return result


def happiness_state(pet_id: int) -> List[int]:
    """
    Retrieves all happiness values recorded for a specific pet.

    :param pet_id: The unique ID of the pet.
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT happiness FROM pet_states WHERE pet_id=%s", (pet_id,))
    result = [row["happiness"] for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return result


def get_timestamp(pet_id: int) -> List[Any]:
    """
    Retrieves all timestamps of actions performed by a specific pet.

    :param pet_id: The unique ID of the pet.
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT timestamp FROM pet_states WHERE pet_id=%s", (pet_id,))
    result = [row["timestamp"] for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return result


def most_happiness_hour(pet_id: int) -> Any:
    """
    Retrieves the hour when the pet had the highest average happiness.

    :param pet_id: The unique ID of the pet.
    """
    connection = get_connection()
    cursor = connection.cursor()
    sql = """
    SELECT DATE_FORMAT(timestamp, '%%Y-%%m-%%d %%H:00:00') AS hour,
           AVG(happiness) AS avg_happiness
    FROM pet_states
    WHERE pet_id = %s
    GROUP BY DATE_FORMAT(timestamp, '%%Y-%%m-%%d %%H:00:00')
    ORDER BY avg_happiness DESC
    LIMIT 1
    """
    cursor.execute(sql, (pet_id,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result["hour"] if result else None


def most_popular_action(pet_id: int) -> str:
    """
    Retrieves the most frequently performed action by a specific pet.

    :param pet_id: The unique ID of the pet.
    """
    connection = get_connection()
    cursor = connection.cursor()
    sql = """
    SELECT action_type, COUNT(*) AS action_count FROM pet_states WHERE pet_id = %s
    GROUP BY action_type ORDER BY action_count DESC LIMIT 1
    """
    cursor.execute(sql, (pet_id,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result["action_type"] if result else None


def overall_score_under(pet_id: int) -> int:
    """
    Counts how many times the pet's overall score was below 70.

    :param pet_id: The unique ID of the pet.
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT COUNT(*) AS count FROM pet_states WHERE overall_score < 70 AND pet_id=%s""", (pet_id,))
    result = cursor.fetchone()["count"]
    cursor.close()
    connection.close()
    return result


def average_time_between_actions(pet_id: int) -> float:
    """
    Calculates the average time in minutes between the first and last recorded actions for a pet.

    :param pet_id: The unique ID of the pet.
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT TIMESTAMPDIFF(MINUTE, MIN(timestamp), MAX(timestamp)) / COUNT(*) AS avg_time
        FROM pet_states
        WHERE pet_id = %s
    """, (pet_id,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result["avg_time"] if result and result["avg_time"] else 0


def get_all_pet_actions(pet_id: int) -> List[str]:
    """
    Retrieves all actions performed by a pet, ordered from newest to oldest.

    :param pet_id: The unique ID of the pet.
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT action_type
        FROM pet_states
        WHERE pet_id = %s
        ORDER BY timestamp DESC
    """, (pet_id,))
    results = [row["action_type"] for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return results


def dates_range(pet_id: int) -> List[str]:
    """
    Returns all the distinct dates where actions were performed for the given pet, ordered chronologically.

    :param pet_id: The unique ID of the pet.
    """
    connection = get_connection()
    cursor = connection.cursor()
    sql = """
    SELECT DISTINCT DATE(timestamp) AS dates
    FROM pet_states
    WHERE pet_id = %s
    ORDER BY dates;
    """
    cursor.execute(sql, (pet_id,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return [row["dates"] for row in results]


def actions_performed_by_day(pet_id: int) -> List[int]:
    """
    Counts the number of actions performed by the pet on each day.

    :param pet_id: The unique ID of the pet.
    """
    connection = get_connection()
    cursor = connection.cursor()
    sql = """
        SELECT DATE(timestamp) AS day, COUNT(*) AS cnt
        FROM pet_states WHERE pet_id = %s GROUP BY day ORDER BY day
    """
    cursor.execute(sql, (pet_id,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return [row["cnt"] for row in results]


def add_new_user(username: str, user_email: str, user_password: str) -> None:
    """
    Adds a new user to the `users` table.

    :param username: The username of the new user.
    :param user_email: The email address of the new user.
    :param user_password: The password for the new user.
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
        (username, user_email, user_password)
    )
    connection.commit()
    cursor.close()
    connection.close()


def check_if_user_exists(user_email: str, user_password: str) -> bool:
    """
    Checks if a user exists in the database with the given email and password.

    :param user_email: The user's email.
    :param user_password: The user's password.
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT 1 FROM users
        WHERE email=%s AND password=%s
        LIMIT 1
    """, (user_email, user_password))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result is not None


def check_if_email_exists(user_email: str) -> bool:
    """
    Checks if an email already exists in the database.

    :param user_email: The email to check.
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT 1 FROM users WHERE email=%s LIMIT 1",
        (user_email,)
    )
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result is not None


def get_user_by_email_and_password(user_email: str, user_password: str) -> Any:
    """
    Retrieves user details for a given email and password.

    :param user_email: The user's email.
    :param user_password: The user's password.
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT user_id, username, email
        FROM users
        WHERE email=%s AND password=%s
    """, (user_email, user_password))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result


def energy_state(pet_id: int) -> Tuple[List[str], List[float]]:
    """
    Retrieves average energy values for a pet for the past 24 hours in hourly intervals.

    :param pet_id: The unique ID of the pet.
    """
    connection = get_connection()
    cursor = connection.cursor()
    sql = """
    WITH RECURSIVE hours AS (SELECT NOW() - INTERVAL 23 HOUR AS hour_start UNION ALL
        SELECT hour_start + INTERVAL 1 HOUR FROM hours WHERE hour_start + INTERVAL 1 HOUR <= NOW())
    SELECT DATE_FORMAT(h.hour_start, '%%Y-%%m-%%d %%H:00:00') AS hour_label, AVG(t.energy) AS avg_energy
    FROM hours h LEFT JOIN pet_states t ON t.pet_id = %s AND t.timestamp >= h.hour_start
        AND t.timestamp < h.hour_start + INTERVAL 1 HOUR 
    GROUP BY h.hour_start ORDER BY h.hour_start
    """
    cursor.execute(sql, (pet_id,))
    results = cursor.fetchall()
    last_val = 0
    avg_energy = []
    for row in results:
        if row["avg_energy"] is None:
            avg_energy.append(last_val)
        else:
            avg_energy.append(row["avg_energy"])
            last_val = row["avg_energy"]
    cursor.close()
    connection.close()
    return ([row["hour_label"] for row in results], avg_energy)