from db import students_record,exams_record
import json


def load_students_record():
    try:
        with open("sample_record/sample_students_data.json", "r") as file:
            students = json.load(file)
            students_record(students)
    except Exception as e:
        print(f"Error:{e}")


def load_exams_record():
    try:
        with open("sample_record/sample_exams_data.json", "r") as file:
            exam_lists = json.load(file)
            exams_record(exam_lists)
    except Exception as e:
        print(f"Error:{e}")



def load_all_records():
    load_students_record()
    load_exams_record()
