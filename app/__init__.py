# ✅ Do this first!
import eventlet
eventlet.monkey_patch()

import os
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# ✅ Import blueprints AFTER monkey patching
from app.controllers.login_controllers.landing_page_controller import landing_bp
from app.controllers.login_controllers.admin_controller import admin_bp
from app.controllers.login_controllers.student_login_controller import student_login_bp
from app.controllers.login_controllers.teacher_login_controller import teacher_login_bp
from app.controllers.student_controller import student_bp
from app.controllers.exam_controller import exam_bp
from app.controllers.attendance_controller import attendance_bp
from app.controllers.main_controller import main_bp

# Config imports
from config.cloudinary_config import init_cloudinary
from config.db_config import db_connection
from config.mail_config import mail_connection

# Keep socketio defined at the top
socketio = SocketIO(cors_allowed_origins="*", async_mode="eventlet")

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # Init services
    db_connection()
    init_cloudinary()
    mail_connection(app)

    # Register Blueprints
    app.register_blueprint(landing_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(student_login_bp)
    app.register_blueprint(teacher_login_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(exam_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(main_bp)

    # ✅ IMPORTANT: initialize socketio with app
    socketio.init_app(app)

    return app
