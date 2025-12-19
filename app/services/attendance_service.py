from app.repositories.attendance_repository import (get_student_name_id_from_db,
                                                    get_today_attendance_from_db,
                                                    register_students_attendance_to_db,
                                                    students_attendance_average_from_db,
                                                    load_all_attendance_records_from_db)
from datetime import date

today_date = date.today().strftime("%Y-%m-%d")

def get_student_name_id():
    return get_student_name_id_from_db()

def get_today_attendance():
    return get_today_attendance_from_db(today_date)

def get_students_attendance(key,value,arr):
    try:
        if key.startswith("attendance_"):
            student_id = int(key.replace("attendance_", ""))
            attendance_status = value
            today_date = date.today().strftime("%Y-%m-%d")
            arr.append((student_id, today_date, attendance_status))
            return arr
    except Exception as e:
        print(f"Error : {e}")
    return arr

def register_students_attendance(arr):
    return  register_students_attendance_to_db(arr)

def students_attendance_average(month_input):
    return students_attendance_average_from_db(month_input)

def load_all_attendance_records(attendance_data):
    return load_all_attendance_records_from_db(attendance_data)