from flask import Blueprint, request, render_template, redirect, make_response, url_for, jsonify
from app.services.login_service.teacher_login_service import (
    send_code_for_teacher_login,
    verify_code_for_teacher_login,
    get_students_datas_class_wise,
    store_datas_in_students_attendance_table,
    get_students_with_today_attendance,
    get_student_names_with_suitable_class,
    store_students_modified_attendance_data
)
import datetime

teacher_login_bp = Blueprint('teacher_login', __name__)

@teacher_login_bp.route('/teacher_login/send_code', methods=['POST'])
def teacher_login_send_code():
    email = request.form.get("user_email")
    try:
        token = send_code_for_teacher_login(email)
        if not token:
            return jsonify({'error': 'Failed to send code or user not found'}), 400
        
        response = make_response(render_template('login_page/teacher_verify_code.html'))
        response.set_cookie(
            "teacher_login_token",
            token,
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age=600  # 10-minute expiry
        )
        return response
    except Exception as e:
        print(f"Error in teacher_login_send_code: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@teacher_login_bp.route('/teacher_login/verify_code', methods=['POST'])
def teacher_login_verify_code():
    user_code = request.form.get('user_code')
    token = request.cookies.get('teacher_login_token')
    try:
        user_id = verify_code_for_teacher_login(user_code.strip(), token)
        if user_id:
            response = make_response(redirect(url_for('admin.dashboard')))
            response.set_cookie(
                "access_token",
                token,
                httponly=True,
                secure=True,
                samesite='Lax',
                max_age=3600  # 1-hour expiry
            )
            return response
        return render_template(
            "login_page/teacher_verify_code.html",
            error="Invalid code"
        ), 401
    except Exception as e:
        print(f"Error in teacher_login_verify_code: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@teacher_login_bp.route('/get_student_datas/<class_name>')
def get_student_datas(class_name):
    try:
        students = get_students_datas_class_wise(class_name)
        return jsonify(students)
    except Exception as e:
        print(f"Error in get_student_datas: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@teacher_login_bp.route('/get_students_with_attendance/<class_name>')
def get_students_with_attendance(class_name):
    try:
        today = datetime.date.today().isoformat()
        students = get_students_with_today_attendance(class_name, today)
        return jsonify(students)
    except Exception as e:
        print(f"Error in get_students_with_attendance: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    
@teacher_login_bp.route('/get_students_names/<class_name>',methods=['GET'])
def get_students_names(class_name):
    try:
        students = get_student_names_with_suitable_class(class_name)
        print(students)
        return jsonify(students)
    except Exception as e:
        print(f"Error : {e}")
        return jsonify({'sucess':False})

@teacher_login_bp.route('/submit_attendance', methods=['POST'])
def submit_attendance():
    try:
        data = request.get_json()
        print(data)
        store_datas_in_students_attendance_table(data)
        return jsonify({"success": True})
    except Exception as e:
        print("Error:", e)
        return jsonify({"success": False})
    
@teacher_login_bp.route('/submit_modify_attendance',methods=['POST'])
def submit_modified_attendance():
    try:
        data = request.get_json()
        print(data)
        store_students_modified_attendance_data(data)
        return jsonify({'success': True})
    except Exception as e:
        print("Error:", e)
        return jsonify({"success": False})