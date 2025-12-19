from config.db_config import db_connection

def get_datas_from_db_by_email(email):
    try:
        connection = db_connection()
        with connection.cursor() as cursor:
            query = """
                SELECT * FROM users 
                WHERE  user_email = %s
                LIMIT 1;
            """
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

def insert_password_into_db(hashed_password,current_user_id):
    try:
        connection = db_connection()
        with connection.cursor() as cursor:
            query = "UPDATE users SET user_password=%s WHERE user_id=%s" 
            values = (hashed_password,current_user_id)
            cursor.execute(query,values)
            connection.commit()
            return True
    except Exception as e:
        print(f" Error : {e} ")
        return False
    finally:
        if connection:
            connection.close()


def using_id_to_get_datas_from_db(current_user_id):
    try:
        connection = db_connection()
        with connection.cursor() as cursor:
            query = """SELECT * FROM users 
            WHERE user_id = %s"""
            cursor.execute(query,(current_user_id,))
            result = cursor.fetchone()
            return result
    except Exception as e:
        print(f" Error : {e} ")
        return None
    finally:
        if connection:
            connection.close()
