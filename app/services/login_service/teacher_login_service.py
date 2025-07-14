from app.repositories.login_repository.teacher_login_repository import get_datas_from_db_by_email,get_user_from_db_by_user_id
from app.utils.token_utils import generate_token_with_code,decode_token
from app.utils.email_utils import send_code_mail
import random

def send_code_for_teacher_login(email):
    user = get_datas_from_db_by_email(email)
    code = str(random.randint(1000, 9999))
    send_code_mail(user,code)
    token = generate_token_with_code(user,code)
    return token

def verify_code_for_teacher_login(user_code,token):
    decoded = decode_token(token)
    user_id = decoded.get("user_id")
    random_code = decoded.get("random_code")
    if random_code == user_code :
        return user_id
    else:
        return False
    
def get_user_by_user_id(user_id):
    return get_user_from_db_by_user_id(user_id)