import jwt
from flask import current_app
from datetime import datetime,timedelta
def generate_token(current_user):
    if current_user:
        payload = {
            'user_id': current_user['user_id']
            }
        token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        print(" No user ")
        return None

def generate_token_with_stored_secret_key(user,stored_secret_key):
    if user:
        payload = {
            'user_id': user['user_id'],
            'secret_key':stored_secret_key,
            'exp': datetime.utcnow() + timedelta(minutes=15)  
        }
        token = jwt.encode(payload,current_app.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        print(" No user ")
        return None



def generate_token_with_expiry_time(user):
    if user:
        payload = {
            'user_id': user['user_id'],
            'exp': datetime.utcnow() + timedelta(minutes=15)  
        }
        token = jwt.encode(payload,current_app.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        print(" No user ")
        return None


def decode_token(token):
    try:
        decoded = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
    
def generate_token_with_code(user,code):
    if user:
        payload = {
            'user_id': user['user_id'],
            'random_code':code,
            'exp': datetime.utcnow() + timedelta(minutes=5)  
        }
        token = jwt.encode(payload,current_app.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        print(" No user ")
        return None