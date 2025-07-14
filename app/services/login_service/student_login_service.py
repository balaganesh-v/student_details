from app.repositories.login_repository.student_login_repository import get_datas_from_db_by_email,insert_password_into_db,using_id_to_get_datas_from_db
from app.utils.hash_password_utils import check_password,generate_hash_password
from app.utils.token_utils import generate_token,generate_token_with_expiry_time,decode_token
from app.utils.email_utils import send_reset_email,send_new_password_to_email


def login_into_website_using_data(data):
    current_user = get_datas_from_db_by_email(data['user_email'])
    password = data.get('user_password')
    stored_hash = current_user['user_password'].encode('utf-8')
    is_valid = check_password(password,stored_hash)
    if is_valid:
        token = generate_token(current_user)
        return {'success': True, 'token': token , 'user': current_user}
    else:
        return {'success': False, 'message': 'Incorrect password.'}
    
def send_password_reset_link(email):
    user = get_datas_from_db_by_email(email)
    if user:
        token = generate_token_with_expiry_time(user)
        to_name = user['user_name']
        to_email = user['user_email']
        send_reset_email(to_name,to_email,token)
        return token
    else:
        return None

def reset_password_to_login(data,token):
    try:
        decoded = decode_token(token)
        current_user_id = decoded.get('user_id')
        current_user = using_id_to_get_datas_from_db(current_user_id)
        to_name = current_user['user_name']
        to_email = current_user['user_email']
        return update_password_for_current_user(data,current_user_id,to_name,to_email)
    except Exception as e: 
        print(f" Error : {e} ")
        return None
    
def update_password_for_current_user(data,current_user_id,to_name,to_email):
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')
    if new_password == confirm_password:
        hashed_password = generate_hash_password(new_password)
        insert_password_into_db(hashed_password,current_user_id)
        send_new_password_to_email(to_name,to_email,new_password)
        return True
    else :
        print("Passwords do not match")
        return False