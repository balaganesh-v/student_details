from config.db_config import db_connection

def get_datas_from_db_by_email(email):
    try:
        connection = db_connection()
        with connection.cursor() as cursor:
            query = " SELECT * FROM users WHERE  user_email = %s LIMIT 1 ; "
            values = (email,)
            cursor.execute(query, values)
            result = cursor.fetchone()
            return result
    except Exception as e:
        print(f"Database error: {e}")
        return None
    finally:
        if connection:
            connection.close()

def get_user_from_db_by_user_id(user_id):
    try:
        connection = db_connection()
        with connection.cursor() as cursor:
            query = " SELECT * FROM users WHERE  user_id = %s LIMIT 1 ; "
            values = (user_id,)
            cursor.execute(query, values)
            result = cursor.fetchone()
            return result
    except Exception as e:
        print(f"Database error: {e}")
        return None
    finally:
        if connection:
            connection.close()