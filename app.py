from flask import Flask, render_template, request, redirect, url_for, jsonify
from db import (
    students_information,
    delete_detail,
    select_student,
    get_exams,
    get_subjects,
    insert_student,
    publishdetails,
    update,
    reg_attendance,
    get_today_attendance,
    students_attendance_average,
    get_old_image
)
from sample_record.load_test_record import load_all_records
import cloudinary, cloudinary.uploader
from datetime import date
import os 

app = Flask(__name__)
app.secret_key = "your-secret-key"

exam_details = []  # ✅ Move this to the top before use


def cloudinary_config():
    cloudinary.config(
        cloud_name=os.getenv("CLOUD_NAME"),
        api_key=os.getenv("API_KEY"),
        api_secret=os.getenv("API_SECRET"),
    )


cloudinary_config()


def pagination(students):
    page = request.args.get("page", 1, type=int)
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(students) + per_page - 1) // per_page
    paginated_students = students[start:end]

    return paginated_students, total_pages, page


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/students_info")
def students_info():
    students=students_information()
    paginated_students, total_pages, page = pagination(students)
    return render_template("students_info.html",students=paginated_students,total_pages=total_pages,page=page)


@app.route("/students_reg")
def students_reg():
    return render_template("students_registration_page.html")


@app.route("/register", methods=["POST"])
def register():
    image = request.files.get("studentPhoto")
    image_url = None
    if image:
        try:
            upload_result = cloudinary.uploader.upload(image)
            image_url = upload_result.get("secure_url")
        except Exception as e:
            print(f"Image upload failed: {e}")
            image_url = None

    student = {
        "student_name": request.form.get("studentName"),
        "student_id": request.form.get("studentId"),
        "father_name": request.form.get("fatherName"),
        "mother_name": request.form.get("motherName"),
        "student_age": request.form.get("age"),
        "father_phone": request.form.get("fatherPhone"),
        "mother_phone": request.form.get("motherPhone"),
        "address": request.form.get("address"),
        "place": request.form.get("place"),
        "image_url": image_url,
    }
    insert_student(student)
    return redirect(url_for("index"))


@app.route("/delete_student/<student_id>", methods=["POST"])
def delete_student(student_id):
    delete_detail(student_id)
    return redirect(url_for("index"))


@app.route("/edit_student/<student_id>", methods=["GET"])
def edit_student(student_id):
    selected_student = select_student(student_id)
    if selected_student:
        return jsonify(selected_student)
    return jsonify({"error": "Student not found"}), 404


@app.route("/exam")
def exam():
    result_exams, result_subjects = get_exams()
    today_date = date.today().strftime("%Y-%m-%d")
    return render_template(
        "exam.html",
        exam_details=exam_details,
        schedule_exams=result_exams,
        schedule_subjects=result_subjects,
        today_date=today_date
    )


@app.route("/subjects")
def subjects():
    return jsonify(get_subjects())


@app.route("/add", methods=["POST"])
def add_exam():
    data = request.get_json()
    if data:
        exam_details.append(
            {
                "subject_name": data["subject_name"],
                "exam_date": data["exam_date"],
                "exam_time": data["exam_time"],
                "marks": data["marks"],
            }
        )
        return jsonify(data)
    return jsonify({"error": "Invalid data"}), 400


@app.route("/publish_now", methods=["POST"])
def publish():
    exam_name = request.form.get("examName")
    exam_code = request.form.get("examCode")
    class_name = request.form.get("className")
    publishdetails(exam_details, exam_name, exam_code, class_name)
    exam_details.clear()
    return render_template("exam.html", exam_details=[])


@app.route("/save_student/<student_id>", methods=["POST"])
def update_student(student_id):
    new_image = request.files.get('image')
    old_url = get_old_image(student_id)
    image_url = old_url

    if new_image and new_image.filename:
        try:
            if old_url:
                pid = os.path.splitext(os.path.basename(old_url))[0]
                cloudinary.uploader.destroy(pid)
            res = cloudinary.uploader.upload(new_image)
            image_url = res.get("secure_url")
        except Exception as e:
            return jsonify({"error": f"Image upload failed: {e}"})

    data = request.form
    student = {
        "student_name": data.get("student_name"),
        "student_id": student_id,
        "father_name": data.get("father_name"),
        "mother_name": data.get("mother_name"),
        "student_age": data.get("student_age"),
        "father_phone": data.get("fatherphone"),
        "mother_phone": data.get("motherphone"),
        "place": data.get("place"),
        "address": data.get("address"),
        "image_url": image_url
    }

    try:
        update(student)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)})



@app.route("/attendance")
def attendance():
    students = students_information()
    paginated_students, total_pages, page = pagination(students)
    attendance = get_today_attendance() or {}
    return render_template("attendance.html", students=paginated_students, attendance=attendance,_pages=total_pages,page=page)


@app.route("/register_attendance", methods=["POST", "GET"])
def register_attendance():
    if request.method == "POST":
        try:
            data = request.form.to_dict()
            arr = []
            for key, value in data.items():
                if key.startswith("attendance_"):
                    student_id = int(key.replace("attendance_", ""))
                    attendance_status = value
                    today_date = date.today().strftime("%Y-%m-%d")
                    arr.append((student_id, today_date, attendance_status))
            reg_attendance(arr)
            return redirect(url_for("attendance"))

        except Exception as e:
            print("Error:", e)
            return "Something went wrong", 500

    # For GET request
    return redirect(url_for("attendance"))


@app.route("/attendance_result")
def attendance_result():
    return render_template("attendance_result.html")


@app.route("/attendance_report", methods=["POST"])
def attendance_report():
    if request.method == "POST":
        month_input = request.form.get("month")
        attendance_records = students_attendance_average(month_input)
        return render_template("attendance_result.html",attendance_records=attendance_records)
    
    return redirect(url_for("attendance_result"))


if __name__ == "__main__":
    load_all_records()
    app.run(debug=True)
