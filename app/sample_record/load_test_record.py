from pathlib import Path
from app.services.student_service import load_all_students_record
from app.services.exam_service import load_all_exams_record
from app.services.attendance_service import load_all_attendance_records
import json

students_file = Path("app")/"sample_record" / "sample_students_data.json"
exams_file = Path("app")/"sample_record"/"sample_exams_data.json"
attendance_file = Path("app")/"sample_record"/"sample_attendance_data.json"

def load_students_record():
    try:
        with students_file.open('r') as file:
            students_data = json.load(file)
            load_all_students_record(students_data)
    except Exception as e:
        print(f"Error:{e}")

def load_exams_record():
    try:
        with exams_file.open("r") as file:
            exams_data = json.load(file)
            load_all_exams_record(exams_data)
    except Exception as e:
        print(f"Error:{e}")

def load_attendance_records():
    try:
        with attendance_file.open("r") as file:
            attendance_data = json.load(file)
            load_all_attendance_records(attendance_data)
    except Exception as e:
        print(f"Error : {e}")

def load_all_records():
    load_students_record()
    load_exams_record()
    load_attendance_records()
