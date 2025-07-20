from config.db_config import db_connection

def get_datas_from_db_by_email(email):
    connection = None
    try:
        connection = db_connection()
        with connection.cursor() as cursor:
            query = "SELECT user_id, user_email, user_name FROM users WHERE user_email = %s LIMIT 1"
            cursor.execute(query, (email,))
            return cursor.fetchone()
    except Exception as e:
        print(f"DB Error in get_datas_from_db_by_email: {e}")
        return None
    finally:
        if connection:
            connection.close()

def get_user_from_db_by_user_id(user_id):
    connection = None
    try:
        connection = db_connection()
        with connection.cursor() as cursor:
            query = "SELECT user_id, user_email, user_name FROM users WHERE user_id = %s LIMIT 1"
            cursor.execute(query, (user_id,))
            return cursor.fetchone()
    except Exception as e:
        print(f"DB Error in get_user_from_db_by_user_id: {e}")
        return None
    finally:
        if connection:
            connection.close()

def get_students_datas_class_wise_from_db(class_name):
    connection = None
    try:
        connection = db_connection()
        with connection.cursor() as cursor:
            query = "SELECT user_id, student_name, class FROM students WHERE class = %s"
            cursor.execute(query, (class_name,))
            return cursor.fetchall()
    except Exception as e:
        print(f"DB Error in get_students_datas_class_wise_from_db: {e}")
        return []
    finally:
        if connection:
            connection.close()
        

def get_students_with_attendance_from_db(class_name, date):
    connection = None
    try:
        connection = db_connection()
        with connection.cursor() as cursor:
            query = """
                SELECT s.user_id, s.student_name, s.class, a.attendance_status
                FROM students s
                LEFT JOIN students_attendance a
                    ON s.user_id = a.user_id AND a.attendance_date = %s
                WHERE s.class = %s
            """
            cursor.execute(query, (date, class_name))
            return cursor.fetchall()
    except Exception as e:
        print(f"DB Error in get_students_with_attendance_from_db: {e}")
        return []
    finally:
        if connection:
            connection.close()

def get_student_names_with_suitable_class_from_db(class_name):
    try:
        connection = db_connection()
        with connection.cursor() as cursor:
            query = "SELECT * FROM students WHERE class = %s "
            values = (class_name,)
            cursor.execute(query,values)
            students = cursor.fetchall()
            return students
    except Exception as e:
        print(f" Error : {e} ")
        return []
    finally:
        if connection:
            connection.close()


def store_datas_in_students_attendance_table_db(data):
    try:

        class_name = data['class_name']
        attendance_date = data['date']
        attendance_list = data['attendance']  # List of {user_id, user_name, status}

        connection = db_connection()
        cursor = connection.cursor()

        for student in attendance_list:
            user_id = student['user_id']
            student_name = student['user_name']
            status = student['status']

            cursor.execute("""
                INSERT INTO students_attendance (user_id, student_name, attendance_date, attendance_status)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE attendance_status = VALUES(attendance_status)
            """, (user_id, student_name, attendance_date, status))

        connection.commit()      
        return True
    
    except Exception as e:
        print("Error:", e)
        return False
    
    finally : 
        if connection:
            connection.close()
            cursor.close()


def store_students_modified_attendance_data_into_db(data):
    try:

        attendance_date = data['date']
        attendance_list = data['attendance']  # List of {user_id, user_name, status}

        connection = db_connection()
        cursor = connection.cursor()

        for student in attendance_list:
            user_id = student['user_id']
            status = student['status']
            
            query = "UPDATE students_attendance SET attendance_status = %s  WHERE user_id = %s AND attendance_date = %s "
            values = (status,user_id,attendance_date,)
            cursor.execute(query,values)
        connection.commit()      
        return True
    
    except Exception as e:
        print("Error:", e)
        return False

    finally : 
        if connection:
            connection.close()
            cursor.close()