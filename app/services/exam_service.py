from app.repositories.exam_repository import(
    get_all_subjects_from_db,
    publish_details,
    load_all_exams_record_from_db,
    get_pagination_exams_from_db
    )
from flask import request


def get_paginated_exams():
    page = int(request.args.get("page", 1))
    per_page = 5
    offset = (page-1)*per_page
    exams, grouped_subjects ,total_pages  = get_pagination_exams_from_db(per_page,offset)
    return  exams,grouped_subjects,page,total_pages 
    
    
def get_all_subjects():
    return get_all_subjects_from_db()

def publish_details():
    exam_name,exam_code,class_name,exam_details = get_exam_details()
    publish_details(exam_details, exam_name, exam_code, class_name)

def get_exam_details():
    data = request.get_json()
    exam_name = data.get("exam_name")
    exam_code = data.get("exam_code")
    class_name = data.get("class_name")
    exam_details = data.get("exam_details", [])
    return exam_name,exam_code,class_name,exam_details

def load_all_exams_record(exams_list):
    return load_all_exams_record_from_db(exams_list)