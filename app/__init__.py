from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
ma = Marshmallow()
socketio = SocketIO(cors_allowed_origins="*")


def create_app():
    app = Flask(__name__)
    CORS(app)

    db_config = {
        "host": os.getenv("RDS_HOSTNAME"),
        "port": os.getenv("RDS_PORT"),
        "name": os.getenv("RDS_DB_NAME"),
        "user": os.getenv("RDS_USERNAME"),
        "password": os.getenv("RDS_PASSWORD"),
    }

    DATABASE_URL = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['name']}"
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    ma.init_app(app)
    socketio.init_app(app)

    # Register Blueprints
    from app.routes import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app
