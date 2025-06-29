from flask import Blueprint,render_template,redirect,url_for,jsonify,request
from app.services.student_service import ( getStudentDetails,addStudentDetails,studentInfo,editStudent,deleteStudent,studentImages,fileUpload,getEditStudentDetails,updateEditStudentDetail)

student_bp = Blueprint('student', __name__)

@student_bp.route("/students_reg")
def register_page():
    return render_template("students_registration_page.html")

@student_bp.route("/register", methods=["POST"])
def student_registration():
    student=getStudentDetails()
    addStudentDetails(student)
    return redirect(url_for("student.register_page"))

@student_bp.route("/students_info")
def students_info():
    students,page,total_pages = studentInfo()
    return render_template("students_info.html",students=students,total_pages=total_pages,page=page)

@student_bp.route("/edit_student/<student_id>", methods=["GET"])
def edit_student(student_id):
    # TODO add validation. 
    selected_student=editStudent(student_id)
    return jsonify(selected_student)

@student_bp.route("/delete_student/<student_id>", methods=["POST"])
def delete_student(student_id):
    deleteStudent(student_id)
    return redirect(url_for("student.students_info"))

@student_bp.route("/save_student/<student_id>", methods=["POST"])
def update_student(student_id):
    new_file,old_url=studentImages(student_id)
    image_url = old_url
    if new_file:
       image_url = fileUpload(new_file,old_url=old_url)
    student = getEditStudentDetails(student_id,image_url)
    updateEditStudentDetail(student)
    return jsonify({"success": True})
    