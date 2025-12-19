from flask import Blueprint, request, render_template, redirect, make_response, url_for, jsonify
from app.services.login_service.teacher_login_service import (
    send_code_for_teacher_login,
    verify_code_for_teacher_login,
    get_students_datas_class_wise,
    store_datas_in_students_attendance_table,
    get_students_with_today_attendance,
    get_student_names_with_suitable_class,
    store_students_modified_attendance_data,
    get_teacher_by_user_id,
    update_teacher_profile_datas,
    get_periods_from_stored_json_file,
    add_assignments_into_json_file,
    get_assignments_from_json_file,
    delete_selected_assignment_by_index_in_json_file,
    update_changes_in_assignment,
    get_all_subjects,
    publish_details,
    store_student_datas,
    get_student_by_user_id
)
from app.utils.email_utils import send_login_email
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
            "access_token",
            token,
            httponly=True,
            secure=True,
            samesite='Lax',
        )
        return response
    except Exception as e:
        print(f"Error in teacher_login_send_code: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@teacher_login_bp.route('/teacher_login/verify_code', methods=['POST'])
def teacher_login_verify_code():
    user_code = request.form.get('user_code')
    token = request.cookies.get('access_token')
    try:
        user_id = verify_code_for_teacher_login(user_code.strip(), token)
        if user_id:
            response = make_response(redirect(url_for('admin.dashboard')))
            response.set_cookie(
                "access_token",
                token,
                httponly=True,
                secure=True,
                samesite='Lax'
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
        return jsonify(students)
    except Exception as e:
        print(f"Error : {e}")
        return jsonify({'sucess':False})

@teacher_login_bp.route('/submit_attendance', methods=['POST'])
def submit_attendance():
    try:
        data = request.get_json()
        store_datas_in_students_attendance_table(data)
        return jsonify({"success": True})
    except Exception as e:
        print("Error:", e)
        return jsonify({"success": False})
    
@teacher_login_bp.route('/submit_modify_attendance',methods=['POST'])
def submit_modified_attendance():
    try:
        data = request.get_json()
        store_students_modified_attendance_data(data)
        return jsonify({'success': True})
    except Exception as e:
        print("Error:", e)
        return jsonify({"success": False})
    
@teacher_login_bp.route('/get_user_by_user_id/<user_id>',methods=['GET'])
def get_user_by_user_id(user_id):
    try:
        teacher = get_teacher_by_user_id(user_id)
        return jsonify(teacher)
    except Exception as e:
        print("Error:", e)
        return jsonify({"success": False})

@teacher_login_bp.route('/update_teacher/<user_id>', methods=['POST'])
def update_teacher_profile(user_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data received'}), 400

        success = update_teacher_profile_datas(data,user_id)
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Failed to update teacher profile'}), 500

    except Exception as e:
        print("Error in route update_teacher_profile:", e)
        return jsonify({'success': False, 'error': str(e)}), 500
    
@teacher_login_bp.route('/teacher/calendar/events', methods=['GET'])
def get_teacher_events():
    try:
        token = request.cookies.get('access_token')
        periods = get_periods_from_stored_json_file(token)
        return jsonify(periods)
    except Exception as e:
        return jsonify({'error': f'Failed to fetch events: {str(e)}'}), 500

@teacher_login_bp.route('/add_assignment',methods = ['POST'] )
def add_assignment():
    try:
        data = request.get_json()
        print(data)
        if not data:
            return jsonify({'success': False, 'error': 'Invalid or missing JSON'}), 400
        success, error = add_assignments_into_json_file(data)
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': error}), 400
    except Exception as e:
        print(f"Error in Create the Assignments route: {e}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

@teacher_login_bp.route('/get_assignments',methods = ['GET'] )
def get_assignments():
    try:
        assignments = get_assignments_from_json_file()
        return jsonify(assignments)
    except Exception as e:
        print(f"Error in Get Assignments route: {e}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500
  
@teacher_login_bp.route('/delete_assignment/<int:index>', methods=['DELETE'])
def delete_assignment(index):
    try:
        delete_selected_assignment_by_index_in_json_file(index)
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error in Delete the selected Assignments route: {e}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500
    
@teacher_login_bp.route('/update_assignment/<int:index>',methods = ['POST'])
def update_assignment(index):
    try:
        updated_data = request.get_json()
        update_changes_in_assignment(index,updated_data)
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error in Update the modify changes in the Assignment : {e}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

@teacher_login_bp.route('/subjects',methods = ['GET'])
def get_subjects():
    try:
        subjects = get_all_subjects()
        return jsonify(subjects)
    except Exception as e:
        print(f"Error in Get Subjects: {e}")
        return jsonify({'Error': 'Internal server error'}), 500
    
@teacher_login_bp.route('/logout', methods=['POST'])
def logout():
    token = request.cookies.get('access_token')
    print("Logging out token:", token)  # Optional for debug/logging

    response = make_response(redirect('/'))  # Redirect to landing page
    response.set_cookie(
        key='access_token',
        value='',
        expires=0,                  # Expire immediately
        httponly=True,
        secure=True,
        samesite='Lax'
    )
    return response


@teacher_login_bp.route("/subjects")
def subjects():
    return jsonify(get_all_subjects())

@teacher_login_bp.route("/publish_now", methods=['POST'])
def publish_now():
    success = publish_details()
    if not success:
        return jsonify({"error": "Failed to publish exam schedule"}), 500
    return jsonify({"status": "success", "redirect": url_for("admin.dashboard")}), 200

@teacher_login_bp.route('/add_student',methods = ['POST'])
def add_student():
    data=request.form.to_dict()
    image_file = request.files.get('image_file')
    result = store_student_datas(data,image_file)
    if result.get('success'):
        send_login_email(data)
        print("Student added and login email sent successfully.")
        return render_template('login_page/teacher_dashboard.html')
    else:
        print("Failed to add student. Email not sent.")
        return render_template('login_page/teacher_dashboard.html')  

@teacher_login_bp.route('/teacher_login/get_user_by_user_id/<user_id>', methods=['GET'])
def get_student_user_by_user_id(user_id):
    try:
        print(user_id)
        student = get_student_by_user_id(user_id)
        print(student)
        return jsonify(student)
    except Exception as e:
        print("Error:", e)
        return jsonify({"success": False, "error": str(e)})