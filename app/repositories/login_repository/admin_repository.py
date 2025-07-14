from config.db_config import db_connection

def insert_datas_to_db(data):
    try:
        connection = db_connection()
        cursor = connection.cursor()
        query = "INSERT INTO users (user_id,user_name,user_email,user_password,user_role )  VALUES (%s,%s,%s,%s,%s)"
        values = (data['user_id'],data['user_name'],data['user_email'],data['hash_password'],data['user_role'])
        cursor.execute(query,values)
        connection.commit()
        return True
    except Exception as e:
        print(f"Error : {e}")
        return False
    finally:
        connection.close()
        cursor.close()

def get_user_from_db_by_email(user_email):
    try:
        connection = db_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE user_email = %s "
        values = (user_email,)
        cursor.execute(query,values)
        user = cursor.fetchone()
        return user
    except Exception as e:
        print(f"Error : {e}")
        return False
    finally:
        connection.close()
        cursor.close()

def store_user_potp_secret_to_db(user_email, secret):
    try:
        connection = db_connection()
        cursor = connection.cursor()
        query = "UPDATE users SET totp_secret = %s WHERE user_email = %s"
        values = (secret, user_email)
        cursor.execute(query, values)
        connection.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        connection.close()


