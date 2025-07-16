from app.repositories.login_repository.admin_repository import (
    insert_datas_to_db,
    get_user_from_db_by_email,
    store_user_potp_secret_to_db,
    get_user_from_db_by_user_id,
    insert_datas_into_students,
    insert_datas_into_teachers
    )
from app.utils.hash_password_utils import check_password,generate_hash_password
from app.utils.token_utils import generate_token_with_stored_secret_key
from app.utils.cloudinary_utils import image_upload_cloudinary_and_get_url
from app.utils.otp_utils import verify_otp
import uuid
import pyotp


def insert_datas(data,image_file):
    try:
        data['user_id'] = str(uuid.uuid4())
        password = data['user_password']
        data['hash_password'] = generate_hash_password(password)
        insert_datas_to_db(data)
        if data['user_role'] == 'Teacher':
            url_link = image_upload_cloudinary_and_get_url(image_file)
            data['image_url']  = url_link
            return insert_datas_into_teachers(data)
        elif data['user_role'] == 'Student':
            return insert_datas_into_students(data)
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

def get_user_by_user_id(user_id):
    return get_user_from_db_by_user_id(user_id)

def get_user_by_email(email):
    return get_user_from_db_by_email(email)

def store_user_potp_secret(user_email, secret_key):
   return store_user_potp_secret_to_db(user_email, secret_key)

def compare_otp(user_otp, stored_secret):
    totp = pyotp.TOTP(stored_secret)
    return totp.verify(user_otp)