from flask import render_template,Blueprint,jsonify
from app.services.exam_service  import get_all_subjects,get_all_exams,publish_details
from datetime import date

exam_bp = Blueprint('exam', __name__)

today_date = date.today().strftime("%Y-%m-%d")

@exam_bp.route("/exam")
def exam():
    schedule_exams, schedule_subjects = get_all_exams()
    return render_template("exam.html",schedule_exams=schedule_exams,schedule_subjects=schedule_subjects,today_date=today_date)

@exam_bp.route("/subjects")
def subjects():
    return jsonify(get_all_subjects())

@exam_bp.route("/publish_now")
def publish_now():
    publish_details()
    return render_template("exam.html", schedule_exams=get_all_exams(), schedule_subjects=get_all_subjects(), today_date=date.today())
