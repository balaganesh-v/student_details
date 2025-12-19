from flask import render_template,request,Blueprint,redirect,url_for,make_response
from app.services.login_service.student_login_service import login_into_website_using_data,send_password_reset_link,reset_password_to_login

student_login_bp = Blueprint('student_login',__name__)

@student_login_bp.route('/student_login',methods = ['POST'] )
def student_login():
    data = request.form.to_dict()
    result = login_into_website_using_data(data)
    print(result)
    print(result.get("success"))
    if result.get("success") == True:
        response = make_response(redirect(url_for('admin.dashboard')))
        response.set_cookie("access_token", result["token"], httponly=True, secure=True,samesite='Lax')
        return response    
    return render_template("login_page/login.html")

@student_login_bp.route('/student_forgot_password')
def student_forgot_password_page():
    return render_template("login_page/forgot_password.html")

@student_login_bp.route('/forgot_password',methods=['POST','GET'])
def forgot_password():
    if request.method == "POST":
        email = request.form.get('email')
        token = send_password_reset_link(email)
        response = make_response(render_template("login_page/student_login.html"))
        response.set_cookie("access_token",token,httponly=True, secure=True,samesite='Lax')
        return response
    return render_template('login_page/forgot_password.html')

@student_login_bp.route("/reset_password/<token>", methods=["POST","GET"])
def reset_password(token):
    if request.method == "POST":
        data = request.form.to_dict()
        reset_password_to_login(data, token)
        return redirect(url_for('landing.student_login_page'))
    return render_template('login_page/reset_password.html',token = token)

@student_login_bp.route('/logout', methods=['POST'])
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