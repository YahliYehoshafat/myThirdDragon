from flask import Flask, request, jsonify
from flask.wrappers import Response
from user_details import UserDetails
from flask_cors import CORS
import pet_service
from typing import Tuple


app = Flask(__name__)
CORS(app)


@app.errorhandler(ValueError)
def handle_value_error(e) -> Tuple[Response, int]:
    """
    Handles ValueError exceptions raised in the Flask app.

    :param e: The ValueError exception instance.
    """
    return jsonify({
        "success": False,
        "message": str(e)
    }), 400


@app.errorhandler(Exception)
def handle_general_error(e) -> Tuple[Response, int]:
    """
    Handles all uncaught exceptions in the Flask app.

    :param e: The Exception instance that was raised.
    """
    print("Server error:", e)
    return jsonify({
        "success": False,
        "message": "Internal server error"
    }), 500


@app.route('/pet_info')
def pet_info() -> Response:
    """
    Retrieves a list of pets for the current user.
    """
    pets_list = pet_service.get_user_pets(UserDetails.user_id)
    return jsonify(pets_list)


@app.route('/pet_properties/<int:pet_id>')
def pet_properties(pet_id: int) -> Response:
    """
    Retrieves the properties of a specific pet by its ID.

    :param pet_id: The unique identifier of the pet whose properties are being requested.
    """
    result = pet_service.get_pet_properties(pet_id)
    return jsonify(result)


@app.route('/performing_an_action', methods=['POST'])
def performing_an_action() -> Response:
    """
    Performs a specified action on a pet and returns the updated pet properties.

    :param pet_id: the unique ID of the pet.
    :param action: the action to perform
    """
    data = request.get_json()
    result = pet_service.perform_action(
        pet_id=data["pet_id"],
        action=data["action"]
    )
    return jsonify(result)


@app.route('/create_a_new_pet', methods=['POST'])
def create_a_new_pet() -> Response:
    """
    Creates a new pet for the current user and stores it in the database.

    :param name: The name of the new pet.
    :param pet_type: The pet type
    :param user_id: the unique ID of the user.
    """
    data = request.get_json()
    pet = pet_service.create_pet(
        name=data.get("name"),
        pet_type=data.get("type"),
        user_id=UserDetails.user_id
    )
    return jsonify({
        "success": True,
        "pet": pet
    }), 201


@app.route('/signup', methods=['POST'])
def signup_user() -> Response:
    """
    Registers a new user and stores their details.

    :param username: The desired username of the new user.
    :param email: The email address of the new user.
    :param password: The password for the new user account.
    """
    data = request.get_json()
    user = pet_service.signup_user(
        username=data.get("username"),
        email=data.get("email"),
        password=data.get("password")
    )
    UserDetails.user_id = user["user_id"]
    UserDetails.username = user["username"]
    UserDetails.user_email = user["email"]
    return jsonify({
        "success": True,
        "user": user
    }), 201


@app.route('/login', methods=['POST'])
def login_user() -> Response:
    """
    Authenticates an existing user using their email and password.

    :param email: The email address of the user.
    :param password: The password for the user account.
    """
    data = request.get_json()
    user = pet_service.login_user(
        email=data.get("email"),
        password=data.get("password")
    )
    UserDetails.user_id = user["user_id"]
    UserDetails.username = user["username"]
    UserDetails.user_email = user["email"]
    return jsonify({
        "success": True,
        "user": user
    }), 200


@app.route('/metrics/<int:pet_id>')
def metrics(pet_id: int) -> Response:
    """
    Retrieves metrics for a specific pet by its unique ID.

    :param pet_id: The unique ID of the pet.
    """
    metrics_data = pet_service.get_metrics(pet_id)
    return jsonify(metrics_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
