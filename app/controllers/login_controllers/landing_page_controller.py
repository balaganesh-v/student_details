from flask import Blueprint,render_template

landing_bp = Blueprint('landing',__name__)


@landing_bp.route('/student_login_page')
def student_login_page():
    return render_template('login_page/student_login.html')

@landing_bp.route('/teacher_login_page')
def teacher_login_page():
    return render_template('login_page/teacher_login_code.html')

@landing_bp.route('/admin_login_page')
def admin_login_page():
    return render_template("login_page/admin_login.html")
