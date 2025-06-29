# app/__init__.py
from flask import Flask
from app.controllers.student_controller import student_bp
from app.controllers.exam_controller import exam_bp
from app.controllers.attendance_controller import attendance_bp
from app.controllers.main_controller import main_bp
from config.cloudinary_config import init_cloudinary
from config.db_config import db_connection

def create_app():
    app = Flask(__name__)
    app.secret_key = "your-secret-key"

    db_connection()
    init_cloudinary()

    app.register_blueprint(student_bp)
    app.register_blueprint(exam_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(main_bp)

    return app