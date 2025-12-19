from flask import render_template,Blueprint,jsonify,request,redirect,url_for
from app.services.exam_service  import get_all_subjects,get_paginated_exams,publish_details
from datetime import date
from builtins import zip

exam_bp = Blueprint('exam', __name__)

today_date = date.today().strftime("%Y-%m-%d")

@exam_bp.route("/exam")
def exam_page():
    exams,grouped_subjects,page,total_pages = get_paginated_exams()
    return render_template(
        "exam.html",
        schedule_exams=exams,
        grouped_subjects=grouped_subjects,
        page=page,
        total_pages=total_pages,
        today_date=today_date,
        zip = zip
    )


@exam_bp.route("/subjects")
def subjects():
    return jsonify(get_all_subjects())

@exam_bp.route("/publish_now")
def publish_now():
    publish_details()
    return redirect(url_for("exam.exam_page"))