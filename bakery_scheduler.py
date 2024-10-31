# Backend code for the Bakery Shift Scheduler web app using Flask

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from db_setup_script import setup_database, Role, User, Shift, ShiftAssignment
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bakery_scheduler.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
bcrypt = Bcrypt(app)
ma = Marshmallow(app)


# Marshmallow Schemas for serialization
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True


class ShiftSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Shift
        include_relationships = True
        load_instance = True


class ShiftAssignmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ShiftAssignment
        include_relationships = True
        load_instance = True


# Initialize Schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
shift_schema = ShiftSchema()
shifts_schema = ShiftSchema(many=True)
shift_assignment_schema = ShiftAssignmentSchema()
shift_assignments_schema = ShiftAssignmentSchema(many=True)

# API Endpoints


# Create a new user
@app.route("/users", methods=["POST"])
def add_user():
    with app.app_context():
        username = request.json["username"]
        email = request.json["email"]
        password = request.json["password"]
        role_id = request.json["role_id"]

        # Hash the password
        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = User(
            username=username, email=email, password_hash=password_hash, role_id=role_id
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            return user_schema.jsonify(new_user), 201
        except Exception as e:
            return jsonify({"message": str(e)}), 400


# Get all users
@app.route("/users", methods=["GET"])
def get_users():
    with app.app_context():
        all_users = User.query.all()
        return users_schema.jsonify(all_users)


# Create a new shift
@app.route("/shifts", methods=["POST"])
def add_shift():
    with app.app_context():
        shift_date_str = request.json["shift_date"]
        start_time_str = request.json["start_time"]
        end_time_str = request.json["end_time"]
        num_trainee_needed = request.json.get("num_trainee_needed", 0)
        num_trained_needed = request.json.get("num_trained_needed", 0)
        num_trainer_needed = request.json.get("num_trainer_needed", 0)

        # Convert date and time strings to Python datetime objects
        try:
            shift_date = datetime.strptime(shift_date_str, "%Y-%m-%d").date()
            start_time = datetime.strptime(start_time_str, "%H:%M:%S").time()
            end_time = datetime.strptime(end_time_str, "%H:%M:%S").time()
        except ValueError as e:
            return (
                jsonify(
                    {
                        "message": "Invalid date or time format. Use YYYY-MM-DD for dates and HH:MM:SS for times."
                    }
                ),
                400,
            )

        new_shift = Shift(
            shift_date=shift_date,
            start_time=start_time,
            end_time=end_time,
            num_trainee_needed=num_trainee_needed,
            num_trained_needed=num_trained_needed,
            num_trainer_needed=num_trainer_needed,
        )

        try:
            db.session.add(new_shift)
            db.session.commit()
            return shift_schema.jsonify(new_shift), 201
        except Exception as e:
            return jsonify({"message": str(e)}), 400


# Get all shifts
@app.route("/shifts", methods=["GET"])
def get_shifts():
    with app.app_context():
        all_shifts = Shift.query.all()
        return shifts_schema.jsonify(all_shifts)


# Assign user to a shift
@app.route("/shift_assignments", methods=["POST"])
def assign_shift():
    with app.app_context():
        shift_id = request.json["shift_id"]
        user_id = request.json["user_id"]
        role_id = request.json["role_id"]

        new_assignment = ShiftAssignment(
            shift_id=shift_id, user_id=user_id, role_id=role_id
        )
        try:
            db.session.add(new_assignment)
            db.session.commit()
            return shift_assignment_schema.jsonify(new_assignment), 201
        except Exception as e:
            return jsonify({"message": str(e)}), 400


# Get all shift assignments
@app.route("/shift_assignments", methods=["GET"])
def get_shift_assignments():
    with app.app_context():
        all_assignments = ShiftAssignment.query.all()
        return shift_assignments_schema.jsonify(all_assignments)


if __name__ == "__main__":
    setup_database(app)
    app.run(debug=True)
