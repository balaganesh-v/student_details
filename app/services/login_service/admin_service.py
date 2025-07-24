from app.repositories.login_repository.admin_repository import (
    insert_datas_to_db,
    get_user_from_db_by_email,
    store_user_potp_secret_to_db,
    get_user_from_db_by_user_id,
    insert_datas_into_students,
    insert_datas_into_teachers,
    get_student_datas_from_db,
    get_teacher_datas_from_db,
    get_all_teachers_from_db,
    get_all_subjects_from_db,
    get_all_days_from_db
    )
from app.utils.hash_password_utils import check_password,generate_hash_password
from app.utils.token_utils import generate_token_with_stored_secret_key
from app.utils.cloudinary_utils import image_upload_cloudinary_and_get_url
from app.utils.otp_utils import verify_otp
from flask import json,jsonify
import os
import uuid
import pyotp


def insert_datas(data,image_file):
    try:
        data['user_id'] = str(uuid.uuid4())
        password = data['user_password']
        data['hash_password'] = generate_hash_password(password)
        if data['user_role'] == 'Teacher':
            url_link = image_upload_cloudinary_and_get_url(image_file)
            data['image_url']  = url_link
            insert_datas_to_db(data)
            insert_datas_into_teachers(data)
            return ({'success':True})
        elif data['user_role'] == 'Student':
            url_link = image_upload_cloudinary_and_get_url(image_file)
            data['image_url']  = url_link
            insert_datas_to_db(data)
            insert_datas_into_students(data)
            return ({'success':True})
    except Exception as e:
        print("SERVICE ERROR:", e)
        return False


def admin_login_into_web_page(data):
    user= get_user_by_email(data['user_email'])
    stored_hash = user['user_password']
    if user:
        password = data['user_password']
        user_otp = data['user_otp']
        stored_secret_key = user['totp_secret']
        if verify_otp(stored_secret_key,user_otp):
            data['hash_password'] = check_password(password,stored_hash)
            token = generate_token_with_stored_secret_key(user,stored_secret_key)
            return ({ 'success':True , 'token': token })
        else:
            print("OTP are not equal")
    else:
        return ({ 'success':False , 'token': None})

def get_teacher_datas(user_id):
    try:
        return  get_teacher_datas_from_db(user_id)
    except Exception as e:
        print(f"Error : {e}")
        return None
    
def get_student_datas(user_id):
    try:
        return get_student_datas_from_db(user_id)
    except Exception as e:
        print(f"Error : {e}")
        return None

def get_user_by_user_id(user_id):
    try:
        return get_user_from_db_by_user_id(user_id)
    except Exception as e:
        print(f"Error : {e}")
        return None

def get_user_by_email(email):
    try:
        return get_user_from_db_by_email(email)
    except Exception as e:
        print(f"Error : {e}")
        return None

def store_user_potp_secret(user_email, secret_key):
    try:
        return store_user_potp_secret_to_db(user_email, secret_key)
    except Exception as e:
        print(f"Error : {e}")
        return None

def get_all_teachers():
    try:
        return get_all_teachers_from_db()
    except Exception as e:
        print(f"Error : {e}")
        return []

def get_all_subjects():
    try:
        return get_all_subjects_from_db()
    except Exception as e:
        print(f"Error : {e}")
        return []

def get_all_days():
    try:
        return get_all_days_from_db()
    except Exception as e:
        print(f"Error : {e}")
        return []

def insert_datas_into_json_file(data):
    try:
        teacher_id = data.get('teacher_id')
        periods = data.get('periods')

        if not teacher_id or not periods:
            return False, 'Missing teacher ID or periods.'

        file_path = 'app/data/events.json'

        all_data = {}
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                try:
                    content = f.read().strip()
                    all_data = json.loads(content) if content else {}
                except:
                    print("⚠️ Warning: events.json was empty or invalid. Starting with empty dict.")
                    all_data = {}

        all_data[teacher_id] = periods

        with open(file_path, 'w') as f:
            json.dump(all_data, f, indent=2)

        return True, None

    except Exception as e:
        print(f"Error writing to JSON: {e}")
        return False, str(e)

    

def compare_otp(user_otp, stored_secret):
    totp = pyotp.TOTP(stored_secret)
    return totp.verify(user_otp)