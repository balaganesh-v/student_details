from flask import Blueprint,render_template,request,redirect,make_response
from app.services.login_service.admin_service import insert_datas,admin_login_into_web_page,store_user_potp_secret,get_user_by_email
from app.utils.email_utils import send_login_email
from app.utils.otp_utils import generate_qr_url,generate_secret

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
            response = make_response(render_template("login_page/admin_dashboard.html", user=user))
            response.set_cookie("access_token", token, httponly=True, secure=True, samesite='Lax')
            return response
        
    return render_template("login_page/admin_login.html")

    

@admin_bp.route('/add_student',methods=['POST'])
def add_student():
    data=request.form.to_dict()
    success = insert_datas(data)
    if success :
        send_login_email(data)
        print("Student added and login email sent successfully.")
    else:
        print("Failed to add student. Email not sent.")
    return render_template('login_page/admin_dashboard.html')   

@admin_bp.route('/add_teacher',methods=['POST'])
def add_teacher():
    data=request.form.to_dict()
    success = insert_datas(data)
    if success :
        send_login_email(data)
        print("Student added and login email sent successfully.")
    else:
        print("Failed to add student. Email not sent.")
    return render_template('login_page/admin_dashboard.html')  

@admin_bp.route('/view_students',methods = ['POST'])
def view_students():
    return redirect('student.students_info')

@admin_bp.route('/view_teachers',methods = ['POST'])
def view_teachers():
    return True

@admin_bp.route('/view_classes',methods = ['POST'])
def view_classes():
    return True