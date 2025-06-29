from app.services.student_service import load_all_students_record
from app.services.exam_service import load_all_exams_record
from app.services.attendance_service import load_all_attendance_records
import json

def load_students_record():
    try:
        with open("/sample_record/sample_students_data.json", "r") as file:
            students = json.load(file)
            load_all_students_record(students)
    except Exception as e:
        print(f"Error:{e}")

def load_exams_record():
    try:
        with open("/sample_record/sample_exams_data.json", "r") as file:
            exam_lists = json.load(file)
            load_all_exams_record(exam_lists)
    except Exception as e:
        print(f"Error:{e}")

def attendance_records():
    try:
        with open("/sample_attendance_data.json","r") as file:
            attendance_data = json.load(file)
            load_all_attendance_records(attendance_data)
    except Exception as e:
        print(f"Error : {e}")

def load_all_records():
    load_students_record()
    load_exams_record()
