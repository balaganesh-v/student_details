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

def insert_datas_into_teachers(data):
    try:
        connection = db_connection()
        cursor = connection.cursor()
        query = """
            INSERT INTO teachers 
            (user_id,user_name,image_url,gender,qualification,age,year_of_experience,subject_specialization,salary_package,mobile_number,address,account_id,class_ids)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        values = (
            data['user_id'],
            data['user_name'],
            data['image_url'],
            data['gender'],
            data['qualification'],
            data['age'],
            data['year_of_experience'],
            data['subject_specialization'],
            data['salary_package'],
            data['mobile_number'],
            data['address'],
            data['account_number'],
            data['specified_class']
            )
        cursor.execute(query,values)
        connection.commit()
        return True
    except Exception as e:
        print(f"Error : {e}")
        return False
    finally:
        connection.close()
        cursor.close()


def insert_datas_into_students(data):
    try:
        connection = db_connection()
        cursor = connection.cursor()
        query = """ INSERT INTO students 
                (user_id,student_name,image_url,class,gender,date_of_birth,roll_no,age,father_name,
                mother_name,father_mobile_number,mother_mobile_number,address,admission_date) VALUES 
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
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

def insert_students_into_attendance_db(data):
    try:
        connection = db_connection()
        cursor = connection.cursor()
        query = "INSERT INTO students_attendance (user_id,student_name) VALUES (%s,%s) " 
        values = (data ['user_id'],data['user_name'],)
        cursor.execute(query,values)
        connection.commit()
    except Exception as e:
        print(f"Error : {e}")
        return None


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



def get_user_from_db_by_user_id(user_id):
    try:
        connection = db_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE user_id = %s "
        values = (user_id,)
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

def get_teacher_datas_from_db(user_id):
    try:
        connection = db_connection()
        cursor = connection.cursor()
        query = """ SELECT * FROM teachers WHERE user_id = %s """
        values = (user_id,)
        cursor.execute(query,values)
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(f"Error : {e}")
        return False
    finally:
        connection.close()
        cursor.close()

def get_student_datas_from_db(user_id):
    try:
        connection = db_connection()
        cursor = connection.cursor()
        query = """ SELECT * FROM students WHERE user_id = %s """
        values = (user_id,)
        cursor.execute(query,values)
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(f"Error : {e}")
        return False
    finally:
        connection.close()
        cursor.close()
    
def get_all_teachers_from_db():
    try:
        connection = db_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM teachers "
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error : {e}")
        return False
    finally:
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

def get_all_days_from_db():
    try:
        connection = db_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM days "
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error : {e}")
        return False
    finally:
        connection.close()
        cursor.close()
