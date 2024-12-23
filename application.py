# Backend code for the Bakery Shift Scheduler web app using Flask
from flask import Flask, request, jsonify, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import jwt
from datetime import timedelta
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os
from datetime import datetime
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import text
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_socketio import emit
import logging

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


# Secret key for JWT
token_secret_key = os.getenv("TOKEN_SECRET_KEY", "supersecretkey")

# Initialize Flask app
application = Flask(__name__)
CORS(application)

db_config = {
    "host": os.getenv("RDS_HOSTNAME"),  # The hostname of the DB instance
    "port": os.getenv(
        "RDS_PORT"
    ),  # The port for the DB instance, default 5432 for PostgreSQL
    "name": os.getenv("RDS_DB_NAME"),  # The database name, typically 'ebdb' for AWS RDS
    "user": os.getenv("RDS_USERNAME"),  # The username configured for the DB
    "password": os.getenv("RDS_PASSWORD"),  # The password for the DB
}

# Construct the DATABASE_URL for SQLAlchemy
DATABASE_URL = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['name']}"

# Set it in your app's configuration
application.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

logger.debug(f"Database URL from environment: {DATABASE_URL}")

application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
application.config["SQLALCHEMY_ECHO"] = True

# Initialize extensions

try:
    db = SQLAlchemy(application)
    logger.info("Database connection initialized successfully.")
except Exception as e:
    logger.error(f"Error initializing database connection: {e}")


application.logger.info("Setting up database checks before first request")
with application.app_context():
    try:
        # Use a raw SQL query to check if the 'role' table exists and has data
        query = text("SELECT COUNT(*) FROM role;")
        result = db.session.execute(query)
        count = result.scalar()

        if count > 0:
            application.logger.info("Database is connected and contains roles.")
        else:
            application.logger.warning("Database is connected but no roles found.")
    except Exception as e:
        application.logger.error(f"Failed to query the database: {str(e)}")


bcrypt = Bcrypt(application)
ma = Marshmallow(application)
socketio = SocketIO(application, cors_allowed_origins="*")


@socketio.on("connect")
def on_connect():
    logging.info("Client connected")
    emit("response", {"message": "Connected to server"})


@socketio.on("disconnect")
def on_disconnect():
    logging.info("Client disconnected")


@socketio.on("error")
def on_error(e):
    logging.error(f"Socket error: {e}")


@socketio.on_error_default
def default_error_handler(e):
    logging.error(f"Default error handler: {e}")


migrate = Migrate(application, db)


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
    status = db.Column(db.String(50), nullable=False, default="Available")
    shift = db.relationship("Shift", backref=db.backref("assignments", lazy=True))
    user = db.relationship("User", backref=db.backref("assignments", lazy=True))
    role = db.relationship("Role")


# Marshmallow Schemas for serialization


class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        include_fk = True
        load_instance = True


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True

    role = ma.Nested(RoleSchema, only=("role_id", "role_name"))


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
    shift_id = ma.auto_field()
    user_id = ma.auto_field()
    role_id = ma.auto_field()
    status = ma.auto_field()

    # Include role details
    role = ma.Nested(RoleSchema, only=("role_id", "role_name"))
    # Include user details
    user = ma.Nested(UserSchema, only=("user_id", "username"))


# Initialize Schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
shift_schema = ShiftSchema()
shifts_schema = ShiftSchema(many=True)
shift_assignment_schema = ShiftAssignmentSchema()
shift_assignments_schema = ShiftAssignmentSchema(many=True)


# Utility function to verify token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("x-access-token")
        if not token:
            return jsonify({"message": "Token is missing!"}), 403
        try:
            data = jwt.decode(token, token_secret_key, algorithms=["HS256"])
            current_user = (
                User.query.options(joinedload(User.role))
                .filter_by(user_id=data["user_id"])
                .first()
            )
        except:
            return jsonify({"message": "Token is invalid!"}), 403
        return f(current_user, *args, **kwargs)

    return decorated


# API Endpoints


@application.route("/")
def home():
    return render_template("index.html")


# Protected route to get all users
@application.route("/users", methods=["GET"])
@token_required
def get_users(current_user):
    logger.debug(f"Fetching users. Current user role: {current_user.role.role_name}")
    if current_user.role.role_name != "Admin":
        logger.warning(f"Unauthorized access attempt by user: {current_user.username}")
        return (
            jsonify({"message": "Unauthorized. Only admins can view all users."}),
            403,
        )

    # Fetch all users along with their roles
    try:
        all_users = User.query.options(joinedload(User.role)).all()
        logger.info(f"Successfully fetched {len(all_users)} users.")
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        return jsonify({"message": "Error fetching users."}), 500
    return users_schema.jsonify(all_users)


# Delete a user
@application.route("/users/<int:user_id>", methods=["DELETE"])
@token_required
def delete_user(current_user, user_id):
    if current_user.role.role_name != "Admin":
        return jsonify({"message": "Unauthorized. Only admins can delete users."}), 403
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found"}), 404
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@application.route("/roles", methods=["GET"])
def get_roles():
    roles = Role.query.all()
    return jsonify(
        [{"role_id": role.role_id, "role_name": role.role_name} for role in roles]
    )


# Delete a shift
@application.route("/shifts/<int:shift_id>", methods=["DELETE"])
def delete_shift(shift_id):
    shift = Shift.query.get(shift_id)
    if shift is None:
        return jsonify({"message": "Shift not found"}), 404
    try:
        db.session.delete(shift)
        db.session.commit()
        return jsonify({"message": "Shift deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


# Delete a shift assignment
@application.route("/shift_assignments/<int:assignment_id>", methods=["DELETE"])
def delete_shift_assignment(assignment_id):
    assignment = ShiftAssignment.query.get(assignment_id)
    if assignment is None:
        return jsonify({"message": "Assignment not found"}), 404
    try:
        db.session.delete(assignment)
        db.session.commit()
        return jsonify({"message": "Assignment deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


# User login
def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        return user
    return None


@application.route("/login", methods=["POST"])
def login():
    # Extract username and password from the JSON body instead of request.authorization
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return make_response(
            "Could not verify",
            401,
            {"WWW-Authenticate": 'Basic realm="Login required!"'},
        )

    username = data["username"]
    password = data["password"]

    try:

        user = authenticate_user(username, password)
        if not user:
            print(f"[DEBUG] User '{username}' not found in database.")
            return make_response(
                "Could not verify",
                401,
                {"WWW-Authenticate": 'Basic realm="Login required!"'},
            )

        token = jwt.encode(
            {
                "user_id": user.user_id,
                "username": user.username,  # Add this line to include the username in the token
                "exp": datetime.utcnow() + timedelta(hours=1),
            },
            token_secret_key,
            algorithm="HS256",
        )
        print(f"[DEBUG] User '{username}' successfully authenticated. Token generated.")
        return jsonify({"token": token})

    except Exception as e:
        print(
            f"[ERROR] An exception occurred during login for user '{username}': {str(e)}"
        )
        return make_response(jsonify({"error": "Internal server error"}), 500)


# Create a new user with admin verification
@application.route("/users", methods=["POST"])
@token_required
def add_user(current_user):
    if current_user.role.role_name != "Admin":
        return (
            jsonify({"message": "Unauthorized. Only admins can create new users."}),
            403,
        )

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
        print("emitting new user")
        socketio.emit("new_user", user_schema.dump(new_user))
        return user_schema.jsonify(new_user), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400


# Get all shifts
@application.route("/shifts", methods=["GET"])
def get_shifts():
    all_shifts = Shift.query.all()
    return shifts_schema.jsonify(all_shifts)


# Create a new shift
@application.route("/shifts", methods=["POST"])
@token_required
def add_shift(current_user):
    if current_user.role.role_name not in ["Admin", "Manager"]:
        return (
            jsonify(
                {"message": "Unauthorized. Only admins and managers can create shifts."}
            ),
            403,
        )

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
        # Emit the new shift data to all connected clients
        print("emitting new shift")
        socketio.emit("new_shift", shift_schema.dump(new_shift))
        return shift_schema.jsonify(new_shift), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400


# Get all shift assignments
@application.route("/shift_assignments", methods=["GET"])
def get_shift_assignments():
    all_assignments = ShiftAssignment.query.all()
    return shift_assignments_schema.jsonify(all_assignments)


# Assign user to a shift
@application.route("/shift_assignments", methods=["POST"])
@token_required
def assign_shift(current_user):
    if current_user.role.role_name not in ["Admin", "Manager"]:
        return (
            jsonify(
                {"message": "Unauthorized. Only admins or managers can assign shifts."}
            ),
            403,
        )

    shift_id = request.json["shift_id"]
    user_id = request.json["user_id"]
    role_id = request.json["role_id"]
    status = request.json.get("status", "Available")  # Default status to 'Available'

    # Check if the user is already assigned to the same shift
    existing_assignment = ShiftAssignment.query.filter_by(
        shift_id=shift_id, user_id=user_id
    ).first()
    if existing_assignment:
        return jsonify({"message": "User is already assigned to this shift."}), 400

    new_assignment = ShiftAssignment(
        shift_id=shift_id, user_id=user_id, role_id=role_id, status=status
    )

    try:
        db.session.add(new_assignment)
        db.session.commit()
        return shift_assignment_schema.jsonify(new_assignment), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@application.route("/shifts/<int:shift_id>/assignments", methods=["GET"])
def get_shift_assignments_for_shift(shift_id):
    assignments = ShiftAssignment.query.filter_by(shift_id=shift_id).all()
    return shift_assignments_schema.jsonify(assignments)


@application.route("/shift_assignments/<int:assignment_id>", methods=["PATCH"])
@token_required
def update_shift_assignment_status(current_user, assignment_id):
    if current_user.role.role_name not in ["Admin", "Manager"]:
        return (
            jsonify(
                {
                    "message": "Unauthorized. Only admins or managers can update assignments."
                }
            ),
            403,
        )

    assignment = ShiftAssignment.query.get(assignment_id)
    if assignment is None:
        return jsonify({"message": "Assignment not found"}), 404

    status = request.json.get("status")
    if not status:
        return jsonify({"message": "Status is required"}), 400

    try:
        assignment.status = status
        db.session.commit()
        return shift_assignment_schema.jsonify(assignment), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400
