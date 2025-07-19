from flask import Blueprint,request,render_template,redirect,make_response,url_for,jsonify
from app.services.login_service.teacher_login_service import send_code_for_teacher_login,verify_code_for_teacher_login,get_students_datas_class_wise

teacher_login_bp = Blueprint('teacher_login',__name__)

@teacher_login_bp.route('/teacher_login/send_code',methods=['POST'])
def teacher_login_send_code():
    if request.method == "POST":
        email = request.form.get("user_email")
        token = send_code_for_teacher_login(email)
        response = make_response(render_template('login_page/teacher_verify_code.html'))
        response.set_cookie("teacher_login_token", token, httponly=True, secure=True, samesite='Lax')
        return response
    return render_template("login_page/teacher_login_code.html")

@teacher_login_bp.route('/teacher_login/verify_code',methods=['POST'])
def teacher_login_verify_code():
    if request.method == "POST":
        user_code = request.form.get('user_code')
        token = request.cookies.get('teacher_login_token')
        user_id = verify_code_for_teacher_login(user_code,token)
        if user_id:
            response = make_response(redirect(url_for('admin.dashboard')))
            response.set_cookie("access_token",token,httponly=True, secure=True,samesite='Lax')
            return response
        else:
            return render_template("login_page/teacher_verify_code.html")
    return render_template("login_page/teacher_verify_code.html")

@teacher_login_bp.route('/get_student_datas/<class_name>')
def get_student_datas(class_name):
    students = get_students_datas_class_wise(class_name)  # returns a list of dicts
    print(students)
    return jsonify(students)


