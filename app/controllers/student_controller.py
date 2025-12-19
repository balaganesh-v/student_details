from flask import Blueprint,render_template,redirect,url_for,jsonify,request
from app.services.student_service import (
    register_student_details,
    studentInfo,
    editStudent,
    deleteStudent,
    update_edit_student_details,
    validate_student_id
    )



student_bp = Blueprint('student', __name__)

@student_bp.route("/students_reg")
def register_page():
    return render_template("students_registration_page.html")

@student_bp.route("/register", methods=["POST","GET"])
def student_registration():
    if request.method == "POST":
        register_student_details()
    return redirect(url_for("student.register_page"))
    
@student_bp.route("/students_info")
def students_info():
    students,page,total_pages = studentInfo()
    return render_template( "students_info.html",
                            students=students,
                            total_pages=total_pages,
                            page=page
                            )
    
@student_bp.route("/edit_student/<student_id>", methods=["GET"])
def edit_student(student_id):
    valid_student_id = validate_student_id(student_id)
    print(valid_student_id)
    selected_student = editStudent(valid_student_id)
    return jsonify(selected_student)

@student_bp.route("/delete_student/<student_id>", methods=["POST"])
def delete_student(student_id):
    valid_student_id = validate_student_id(student_id)
    deleteStudent(valid_student_id)
    return redirect(url_for("student.students_info"))
    

@student_bp.route("/save_student/<student_id>", methods=["POST"])
def update_student(student_id):
    valid_student_id = validate_student_id(student_id)
    update_edit_student_details(valid_student_id)
    return redirect(url_for("student.students_info"))  

    