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

def get_students_datas_class_wise_from_db(class_name):
    try:
        connection = db_connection()
        cursor = connection.cursor()
        query = """ SELECT * FROM students WHERE class = %s """
        values = (class_name,)
        cursor.execute(query,values)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error : {e}")
    finally:
        if connection:
            connection.close()
            cursor.close()


def insert_students_attendance_datas_into_db(datas):
    try:
        connection=db_connection()
        cursor = connection.cursor()
        query = " UPDATE  students_attendance SET attendance_status = %s WHERE user_id = %s "
        values = [
            (data['attendance']['status'],data['attendance']['user_id'],)
            for data in datas 
            ]
        cursor.executemany(query,values)
        connection.commit()
        return True
    except Exception as e:
        print(f"Error : {e}")
        return None
    finally:
        if connection:
            connection.close()
            cursor.close()