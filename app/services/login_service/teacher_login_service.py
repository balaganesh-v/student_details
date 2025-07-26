from app.repositories.login_repository.teacher_login_repository import (
    get_datas_from_db_by_email,
    get_user_from_db_by_user_id,
    get_students_datas_class_wise_from_db,
    get_students_with_attendance_from_db,
    store_datas_in_students_attendance_table_db,
    get_students_with_attendance_from_db,
    get_student_names_with_suitable_class_from_db,
    store_students_modified_attendance_data_into_db,
    update_teachers_profile_data_into_db,
    get_teacher_by_user_id_from_db
)
from app.utils.token_utils import generate_token_with_code, decode_token
from app.utils.email_utils import send_code_mail
from flask import jsonify,json
import random
import os

def send_code_for_teacher_login(email):
    try:
        user = get_datas_from_db_by_email(email)
        if not user:
            print(f"No user found for email: {email}")
            return None
        
        code = str(random.randint(1000, 9999))
        if not send_code_mail(user, code):
            print(f"Failed to send email to: {email}")
            return None
            
        return generate_token_with_code(user, code)
    except Exception as e:
        print(f"Error in send_code_for_teacher_login: {e}")
        return None

def get_periods_from_stored_json_file(token):
    try:
        decoded = decode_token(token)
        teacher_id = decoded.get('user_id')

        if teacher_id:
            json_path = os.path.join('app','data','periods.json')
            if  os.path.exists(json_path):
                with open(json_path, 'r') as file:
                    data = json.load(file)
                    periods = data.get(teacher_id, [])
                    return periods
            else:
                return jsonify({'error': 'Periods file not found'}), 404
        else:
            return jsonify({'error': 'Teacher ID not found'}), 404
    except Exception as e:
        print(f"Error in Get periods from JSON file: {e}")
        return False
    

def verify_code_for_teacher_login(user_code, token):
    try:
        decoded = decode_token(token)
        if decoded.get("random_code") == user_code:
            return decoded.get("user_id")
        return False
    except Exception as e:
        print(f"Error in verify_code_for_teacher_login: {e}")
        return False

def get_user_by_user_id(user_id):
    try:
        return get_user_from_db_by_user_id(user_id)
    except Exception as e:
        print(f"Error in get_user_by_user_id: {e}")
        return None

def get_students_datas_class_wise(class_name):
    try:
        return get_students_datas_class_wise_from_db(class_name)
    except Exception as e:
        print(f"Error in get_students_datas_class_wise: {e}")
        return []
    
def get_students_with_today_attendance(class_name, date):
    try:
        return get_students_with_attendance_from_db(class_name, date)
    except Exception as e:
        print(f"Error in get_students_with_today_attendance: {e}")
        return []

def get_student_names_with_suitable_class(class_name):
    try:
        return get_student_names_with_suitable_class_from_db(class_name)
    except Exception as e:
        print(f"Error in get_students_with_today_attendance: {e}")
        return []

def store_datas_in_students_attendance_table(data):
    try: 
        return store_datas_in_students_attendance_table_db(data)
    except Exception as e:
        print(f"Error store_datas_in_students_attendance_table : {e}")
        return []

def store_students_modified_attendance_data(data):
    try: 
        return store_students_modified_attendance_data_into_db(data)
    except Exception as e:
        print(f"Error store_datas_in_students_attendance_table : {e}")
        return []
    
def get_teacher_by_user_id(user_id):
    try:
        return get_teacher_by_user_id_from_db(user_id)
    except Exception as e:
        print(f"Error store_datas_in_students_attendance_table : {e}")
        return []
    
def update_teacher_profile_datas(data,user_id):
    try: 
        return update_teachers_profile_data_into_db(data,user_id)
    except Exception as e:
        print(f"Error store_datas_in_students_attendance_table : {e}")
        return []
    

def add_assignments_into_json_file(data):
    try:
        file_path = 'app/data/assignments.json'

        # Load existing assignments if file exists, otherwise use empty list
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                try:
                    assignments = json.load(f)
                except json.JSONDecodeError:
                    assignments = []
        else:
            assignments = []

        # Append new assignment
        assignments.append(data['assignment'])

        # Save updated list back to file
        with open(file_path, 'w') as f:
            json.dump(assignments, f, indent=2)

        return True, None
    except Exception as e:
        print(f"Error writing to JSON: {e}")
        return False, str(e)
        
def get_assignments_from_json_file():
    try:
        with open('app/data/assignments.json', 'r') as file:
            assignments = json.load(file)
            print(assignments)
            return assignments
    except Exception as e:
        print(f"Error Getting to JSON: {e}")
        return False, str(e)

def delete_selected_assignment_by_index_in_json_file(index):
    try:
        file_name = "app/data/assignments.json"
        with open( file_name  ,'r') as file:
            assignments = json.load(file)
            assignments.pop(index)
            with open( file_name , 'w') as f:
                json.dump(assignments, f, indent=2)
                return jsonify({"message": "Assignment deleted."}), 200
            
    except Exception as e:
        print(f"Error in Deleting the data in assignments JSON: {e}")
        return False, str(e)