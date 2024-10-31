# Backend code for the Bakery Shift Scheduler web app using Flask

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bakery_scheduler.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
ma = Marshmallow(app)


# Define Roles table
class Role(db.Model):
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), unique=True, nullable=False)


# Define Users table
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.role_id"))
    role = db.relationship("Role", backref=db.backref("users", lazy=True))
    date_joined = db.Column(db.DateTime, default=db.func.current_timestamp())


# Define Shifts table
class Shift(db.Model):
    shift_id = db.Column(db.Integer, primary_key=True)
    shift_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    num_trainee_needed = db.Column(db.Integer, default=0)
    num_trained_needed = db.Column(db.Integer, default=0)
    num_trainer_needed = db.Column(db.Integer, default=0)


# Define ShiftAssignments table
class ShiftAssignment(db.Model):
    assignment_id = db.Column(db.Integer, primary_key=True)
    shift_id = db.Column(db.Integer, db.ForeignKey("shift.shift_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    role_id = db.Column(db.Integer, db.ForeignKey("role.role_id"))
    shift = db.relationship("Shift", backref=db.backref("assignments", lazy=True))
    user = db.relationship("User", backref=db.backref("assignments", lazy=True))
    role = db.relationship("Role")


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

    assignment_id = ma.auto_field()
    # TODO work out why we need these ids for the jsonify to work correctly in the front end
    shift_id = ma.auto_field()
    user_id = ma.auto_field()
    role_id = ma.auto_field()


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
    all_users = User.query.all()
    return users_schema.jsonify(all_users)


# Create a new shift
@app.route("/shifts", methods=["POST"])
def add_shift():
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
    all_shifts = Shift.query.all()
    return shifts_schema.jsonify(all_shifts)


# Assign user to a shift
@app.route("/shift_assignments", methods=["POST"])
def assign_shift():
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
    all_assignments = ShiftAssignment.query.all()
    return shift_assignments_schema.jsonify(all_assignments)


if __name__ == "__main__":
    if not os.path.exists("bakery_scheduler.db"):
        with app.app_context():
            db.create_all()
            print("Database created successfully!")
    app.run(debug=True)
