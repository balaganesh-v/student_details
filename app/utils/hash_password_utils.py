import bcrypt

def generate_hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password

def check_password(password: str, stored_hash: str) -> bool:
    if isinstance(stored_hash, str):
        stored_hash = stored_hash.encode('utf-8')  # convert string hash to bytes
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
