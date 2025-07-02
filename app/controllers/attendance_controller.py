from flask import render_template,Blueprint,redirect,request,url_for
from app.services.attendance_service import (
    get_student_name_id,
    get_today_attendance,
    get_students_attendance,
    register_students_attendance,
    students_attendance_average
    )

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route("/attendance")
def attendance_page():
    students = get_student_name_id()
    attendance = get_today_attendance() or {}
    return render_template("attendance.html", students=students, attendance = attendance)

@attendance_bp.route("/register_attendance", methods=["POST", "GET"])
def register_attendance():
    if request.method == "POST":
        data = request.form.to_dict()
        arr = []
        for key, value in data.items():
            arr = get_students_attendance(key,value,arr)
        register_students_attendance(arr)
        return redirect(url_for("attendance.attendance_page"))
    return redirect(url_for("attendance.attendance_page"))


@attendance_bp.route("/attendance_result")
def attendance_result():
    return render_template("attendance_result.html")

@attendance_bp.route("/attendance_report", methods=["POST","GET"])
def attendance_report():
    if request.method =="POST":
        month_input = request.form.get("month")
        attendance_records = students_attendance_average(month_input)
        return render_template("attendance_result.html",attendance_records=attendance_records)
    return redirect(url_for("attendance.attendance_result"))

