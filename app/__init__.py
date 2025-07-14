from flask import Flask
from app.controllers.login_controllers.landing_page_controller import landing_bp
from app.controllers.login_controllers.admin_controller import admin_bp
from app.controllers.login_controllers.student_login_controller import student_login_bp
from app.controllers.login_controllers.teacher_login_controller import teacher_login_bp
from app.controllers.student_controller import student_bp
from app.controllers.exam_controller import exam_bp
from app.controllers.attendance_controller import attendance_bp
from app.controllers.main_controller import main_bp
from config.cloudinary_config import init_cloudinary
from config.db_config import db_connection
from config.mail_config import mail_connection
import os
from dotenv import load_dotenv

load_dotenv

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')


    db_connection()
    init_cloudinary()
    mail_connection(app)  
    
    app.register_blueprint(landing_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(student_login_bp)
    app.register_blueprint(teacher_login_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(exam_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(main_bp)

    return app
