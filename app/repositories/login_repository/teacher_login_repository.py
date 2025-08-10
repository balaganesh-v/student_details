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

def get_all_subjects_from_db():
    try:
        connection = db_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM subjects "
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error : {e}")
        return False
    finally:
        connection.close()
        cursor.close()


def update_teachers_profile_data_into_db(data, user_id):
    connection = None
    try:
        connection = db_connection()
        with connection.cursor() as cursor:
            query = """ 
                UPDATE teachers 
                SET 
                    user_name = %s,
                    age = %s,
                    gender = %s,
                    qualification = %s,
                    account_id = %s,
                    address = %s
                WHERE user_id = %s;
            """
            values = (
                data.get('user_name'),
                data.get('age'),
                data.get('gender'),
                data.get('qualification'),
                data.get('account_id'),
                data.get('address'),
                user_id
            )
            cursor.execute(query, values)
            connection.commit()
            return True
    except Exception as e:
        print("Error updating teacher profile:", e)
        return False
    finally:
        if connection:
            connection.close()



def get_teacher_by_user_id_from_db(user_id):
    try:
        connection = db_connection()
        with connection.cursor() as cursor:
            query = " SELECT * FROM teachers WHERE user_id = %s "
            values = (user_id,)
            cursor.execute(query,values)
            result = cursor.fetchone()
            return result
    except Exception as e:
        print("Error:", e)
        return False

    finally : 
        if connection:
            connection.close()


def publish_details_into_db(exam_details, exam_name, exam_code, class_name):
    try:
        with db_connection() as connection:
            with connection.cursor() as cursor:
                # Check for duplicate exam_code
                cursor.execute("SELECT 1 FROM exam_table WHERE exam_code = %s", (exam_code,))
                if cursor.fetchone():
                    print(f"Error: Exam code {exam_code} already exists")
                    return False
                
                # Insert into exam_table
                cursor.execute(
                    """ 
                    INSERT INTO exam_table 
                    (exam_name, exam_code, class_name) 
                    VALUES (%s, %s, %s) 
                    """,
                    (exam_name, exam_code, class_name)
                )
                # Insert into exam_subjects_table (fixed placeholder count)
                query_subjects = """ 
                    INSERT INTO exam_subjects_table 
                    (exam_code, subject_name, exam_date, start_time, end_time, marks) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                subjects_data = [
                    (
                        exam_code,
                        item["subject_name"],
                        item["exam_date"],
                        item["start_time"],
                        item["end_time"],
                        int(item["marks"]),  # Ensure marks is an integer
                    )
                    for item in exam_details
                ]
                cursor.executemany(query_subjects, subjects_data)
                connection.commit()
                return True
    except Exception as e:
        print(f"Error inserting exam details: {e}")
        connection.rollback()
        return False
    

def store_datas_in_users(data):
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

def store_datas_into_students_db(data):
    try:
        connection = db_connection()
        cursor = connection.cursor()
        query = """ INSERT INTO students 
            (  
                user_id,
                student_name,
                image_url,
                class,
                gender,
                date_of_birth,
                roll_no,
                age,
                father_name,
                mother_name,
                father_mobile_number,
                mother_mobile_number,
                address,
                admission_date
            ) 
            VALUES 
            ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        values = (
                data['user_id'],
                data['user_name'],
                data['image_url'],
                data['student_class'],
                data['gender'],
                data['date_of_birth'],
                data['roll_no'],
                data['age'],
                data['father_name'],
                data['mother_name'],
                data['father_mobile_number'],
                data['mother_mobile_number'],
                data['address'],
                data['admission_date']
            )
        cursor.execute(query,values)
        connection.commit()
    except Exception as e:
        print(f" Error : {e} ")
    finally:
        connection.close()
        cursor.close()