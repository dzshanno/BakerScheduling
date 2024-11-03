from app import db


class Role(db.Model):
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), unique=True, nullable=False)


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.role_id"))
    role = db.relationship("Role", backref=db.backref("users", lazy=True))
    date_joined = db.Column(db.DateTime, default=db.func.current_timestamp())


class Shift(db.Model):
    shift_id = db.Column(db.Integer, primary_key=True)
    shift_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    num_trainee_needed = db.Column(db.Integer, default=0)
    num_trained_needed = db.Column(db.Integer, default=0)
    num_trainer_needed = db.Column(db.Integer, default=0)


class ShiftAssignment(db.Model):
    assignment_id = db.Column(db.Integer, primary_key=True)
    shift_id = db.Column(db.Integer, db.ForeignKey("shift.shift_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    role_id = db.Column(db.Integer, db.ForeignKey("role.role_id"))
    status = db.Column(db.String(50), nullable=False, default="Available")
    shift = db.relationship("Shift", backref=db.backref("assignments", lazy=True))
    user = db.relationship("User", backref=db.backref("assignments", lazy=True))
    role = db.relationship("Role")
