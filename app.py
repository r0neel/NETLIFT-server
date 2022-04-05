import json
from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity
from flask_cors import CORS
import hashlib
import datetime
from models.User import User
# from models.Exercise import Exercise
# exercise = Exercise()

app = Flask(__name__)
CORS(app)

jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'Your_Secret_Key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)


@app.route('/')
def home():
    return 'Hello, World!'


@app.route('/register', methods=['POST'])
def register():
    new_user = request.get_json()
    new_user['password_digest'] = hashlib.sha224(
        new_user['password'].encode("utf-8")).hexdigest()
    user = User.find_by_name(new_user["username"])
    if not user:
        user = User.create_user(new_user)
        return (user), 201
    else:
        return jsonify({'msg': 'Username already exists'}), 409


@app.route('/login', methods=['POST'])
def login():
    login_details = request.get_json()
    user = User.find_by_name(login_details['username'])
    if user:
        encrypted_password = hashlib.sha224(
            login_details['password'].encode("utf-8")).hexdigest()
        if encrypted_password == user['password_digest']:
            access_token = create_access_token(identity=user['username'])
            return jsonify(access_token=access_token), 200
    return jsonify({'msg': 'The username or password is incorrect'}), 401


@app.route('/user', methods=['GET', 'POST'])
@jwt_required()
def profile():
    if request.method == "GET":
        current_user = get_jwt_identity()
        user_profile = User.find_by_name(current_user)
        return jsonify(user_profile), 200
    elif request.method == "POST":
        pass


@app.route('/program', methods=["GET", "POST"])
@jwt_required()
def create_program():
    current_user = get_jwt_identity()
    user_profile = User.find_by_name(current_user)
    if request.method == "GET":
        user_program = user_profile["_programs"]
        return jsonify(user_program), 200
    elif request.method == "POST":
        new_program = request.get_json()
        program = User.add_program(current_user, new_program)
        return jsonify(program), 201


@app.route('/workout', methods=["GET", "POST"])
@jwt_required()
def workout():
    current_user = get_jwt_identity()
    user_profile = User.find_by_name(current_user)
    if request.method == "GET":
        user_workout = user_profile["_workouts"]
        return jsonify(user_workout), 200
    elif request.method == "POST":
        new_workout = request.get_json()
        workout = User.add_workout(current_user, new_workout)
        return jsonify(workout), 201


@app.route('/program/<int:program_id>', methods=["GET", "PATCH"])
@jwt_required()
def update_program(program_id):
    current_user = get_jwt_identity()
    user_profile = User.find_by_name(current_user)
    if request.method == "GET":
        user_program = user_profile["_programs"]
        for i in user_program:
            if i['id'] == program_id:
                return jsonify(i), 200

        return "Program not found", 404
    elif request.method == "PATCH":
        changed_program = request.get_json()
        program = User.add_program(current_user, changed_program)
        return jsonify(program), 201
#     return response.raw_result, 200


@app.route('/lifts', methods=["GET", "POST"])
@jwt_required()
def create_lifts():
    current_user = get_jwt_identity()
    user_profile = User.find_by_name(current_user)
    if request.method == "GET":
        user_lift = user_profile["_lifts"]
        return jsonify(user_lift), 200
    elif request.method == "POST":
        new_lift = request.get_json()
        lift = User.add_lift(current_user, new_lift)
        # print(lift)
        return jsonify(lift), 201


@app.route('/weights', methods=["GET", "POST"])
@jwt_required()
def create_weights():
    current_user = get_jwt_identity()
    user_profile = User.find_by_name(current_user)
    if request.method == "GET":
        user_weight = user_profile["_weights"]
        return jsonify(user_weight), 200
    elif request.method == "POST":
        new_weight = request.get_json()
        weight = User.add_weight(current_user, new_weight)
        # print(lift)
        return jsonify(weight), 201

# return all programs

# @app.route('/program', methods=['GET'])
# def profile():
#     user_profile = User.getAll()
#     return jsonify({'profile': user_profile}), 200


# edit workouts
# edit lifts


if __name__ == "__main__":
    app.run(debug=True)
