from flask import Blueprint,render_template,request,redirect,make_response,url_for,jsonify
from app.services.login_service.admin_service import (
    insert_datas,
    admin_login_into_web_page,
    store_user_potp_secret,
    get_user_by_email,
    get_user_by_user_id,
    get_student_datas,
    get_teacher_datas,
    get_all_teachers,
    get_all_subjects,
    insert_datas_into_json_file,
    get_all_days
    )
from app.utils.email_utils import send_login_email
from app.utils.otp_utils import generate_qr_url,generate_secret
from app.utils.token_utils import decode_token

admin_bp = Blueprint('admin',__name__)


@admin_bp.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        data = request.form.to_dict()
        user = get_user_by_email(data['user_email'])

        if not user:
            return render_template("login_page/admin_login.html")
        
        if not user.get("totp_secret"):
            secret_key = generate_secret()
            store_user_potp_secret(user["user_email"], secret_key)
            qr_url = generate_qr_url(user["user_email"], secret_key)
            return render_template("login_page/setup_2fa.html", qr_url=qr_url)
        
        result = admin_login_into_web_page(data)
        if result :
            token = result.get('token')
            response = make_response(redirect(url_for('admin.dashboard')))
            response.set_cookie("access_token", token, httponly=True, secure=True, samesite='Lax')
            return response
        
    return render_template("login_page/admin_login.html")

@admin_bp.route("/dashboard")
def dashboard():
    token = request.cookies.get('access_token')
    decoded = decode_token(token)
    user_id = decoded.get("user_id")
    user = get_user_by_user_id(user_id)
    if user["user_role"] == "Principal":
        return render_template("login_page/admin_dashboard.html",user = user)
    if user["user_role"] == "Teacher":
        teacher = get_teacher_datas(user_id)
        return render_template("login_page/teacher_dashboard.html",user = user,teacher = teacher)
    if user["user_role"] == "Student":
        student = get_student_datas(user_id)
        return render_template("login_page/student_dashboard.html",user = user)    

@admin_bp.route('/add_student',methods=['POST'])
def add_student():
    data=request.form.to_dict()
    print(data)
    image_file = request.files.get('image_file')
    result = insert_datas(data,image_file)
    if result.get('success'):
        send_login_email(data)
        print("Student added and login email sent successfully.")
    else:
        print("Failed to add student. Email not sent.")
    return render_template('login_page/admin_dashboard.html')   

@admin_bp.route('/add_teacher',methods=['POST'])
def add_teacher():
    data=request.form.to_dict()
    image_file = request.files.get('image_file')
    result = insert_datas(data,image_file)
    if result.get('success'):
        send_login_email(data)
        print("Student added and login email sent successfully.")
    else:
        print("Failed to add student. Email not sent.")
    return render_template('login_page/admin_dashboard.html')  

@admin_bp.route('/subjects',methods = ['GET'])
def get_subjects():
    try:
        subjects = get_all_subjects()
        return jsonify(subjects)
    except Exception as e:
        print(f"Error in Get Subjects: {e}")
        return jsonify({'Error': 'Internal server error'}), 500
    
@admin_bp.route('/teachers',methods = ['GET'])
def get_teachers():
    try:
        teachers = get_all_teachers()
        return jsonify(teachers)
    except Exception as e:
        print(f"Error in Get Subjects: {e}")
        return jsonify({'Error': 'Internal server error'}), 500


@admin_bp.route('/days',methods = ['GET'])
def get_days():
    try:
        days = get_all_days()
        return jsonify(days)
    except Exception as e:
        print(f"Error in Get Subjects: {e}")
        return jsonify({'Error': 'Internal server error'}), 500


@admin_bp.route('/save_periods', methods=['POST'])
def save_periods():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'Invalid or missing JSON'}), 400
        
        success, error = insert_datas_into_json_file(data)
        
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': error}), 400
    except Exception as e:
        print(f"Error in save_periods route: {e}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500


@admin_bp.route('/update_teacher',methods=['get'])
def update_teacher():
    pass
    
@admin_bp.route('/view_students',methods = ['POST'])
def view_students():
    return redirect('student.students_info')

@admin_bp.route('/view_teachers',methods = ['POST'])
def view_teachers():
    return True

@admin_bp.route('/view_classes',methods = ['POST'])
def view_classes():
    return True


