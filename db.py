import os
import pymysql
from dotenv import load_dotenv
from datetime import date

load_dotenv()


def db_connection():
    try:
        return pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            cursorclass=pymysql.cursors.DictCursor,
        )
    except Exception as e:
        print(f"Error connecting to DB: {e}")
        return None


def students_information():
    connection = db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM students_information")
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching students: {e}")
        finally:
            connection.close()
    


def insert_student(student):
    connection = db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO students_information (
                        student_name, student_id, father_name, mother_name,
                        student_age, fatherphone, motherphone, address, place, image_url )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(
                    query,
                    (
                        student["student_name"],
                        student["student_id"],
                        student["father_name"],
                        student["mother_name"],
                        student["student_age"],
                        student["fatherPhone"],
                        student["motherPhone"],
                        student["address"],
                        student["place"],
                        student["image_url"],
                    ),
                )
                connection.commit()
        except Exception as e:
            print(f"Error inserting student: {e}")
        finally:
            connection.close()


def delete_detail(student_id):
    connection = db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM students_information WHERE student_id = %s",
                    (student_id,),
                )
                connection.commit()
        except Exception as e:
            print(f"Error deleting student: {e}")
        finally:
            connection.close()


def select_student(student_id):
    connection = db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM students_information WHERE student_id = %s",
                    (student_id,),
                )
                return cursor.fetchone()
        except Exception as e:
            print(f"Error fetching student: {e}")
        finally:
            connection.close()
    return None


def get_subjects():
    connection = db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT subject_name FROM subjects_table")
                result = cursor.fetchall()
                return [row["subject_name"] for row in result]
        except Exception as e:
            print(f"Error fetching subjects: {e}")
        finally:
            connection.close()
    return []


def publishdetails(exam_details, exam_name, exam_code, class_name):
    connection = db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO exam_table (exam_name, exam_code, class_name)
                    VALUES (%s, %s, %s)
                """,
                    (exam_name, exam_code, class_name),
                )

                query_subjects = """
                    INSERT INTO exam_subjects_table (exam_code, subject_name, exam_date, exam_time, marks)
                    VALUES (%s, %s, %s, %s, %s)
                """
                subjects_data = [
                    (
                        exam_code,
                        item["subject_name"],
                        item["exam_date"],
                        item["exam_time"],
                        item["marks"],
                    )
                    for item in exam_details
                ]
                cursor.executemany(query_subjects, subjects_data)
                connection.commit()
        except Exception as e:
            print(f"Error inserting exam details: {e}")
        finally:
            connection.close()


# clear students data
# load students data from json
# insert students data to db

def students_record(students):
    connection = db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM students_information")
                connection.commit()
                query = """
                INSERT INTO students_information (student_name, student_id, father_name, mother_name,
                student_age, fatherphone, motherphone, address, place, image_url )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                values = [
                    (
                        student["student_name"],
                        student["student_id"],
                        student["father_name"],
                        student["mother_name"],
                        student["student_age"],
                        student["fatherphone"],
                        student["motherphone"],
                        student["address"],
                        student["place"],
                        student["image_url"],
                    )
                    for student in students
                ]
                cursor.executemany(query, values)
                connection.commit()
        except Exception as e:
            print(f"Error:{e}")
        finally:
            connection.close()

# clear exams data
# load exams data from json
# insert exams data to db

def exams_record(exam_lists):
    connection = db_connection()
    if connection:
        try:
            with connection.cursor() as cursor: 
                #Delete the previous values in the database
                cursor.execute(" DELETE FROM exam_table;")
                connection.commit()
                # Insert the New values in the Database
                exam_query = """ INSERT INTO exam_table (exam_name, exam_code, class_name) VALUES (%s, %s, %s)"""
                exam_values = [
                    (item["exam_name"], item["exam_code"], item["class_name"])
                    for item in exam_lists.get("exam_table", [])
                ]
                cursor.executemany(exam_query, exam_values)
                connection.commit()

                # Delete the Previous values in the Database
                cursor.execute(" TRUNCATE TABLE exam_subjects_table; ")
                connection.commit()

                # Insert the New values in the Database
                exam_subjects_query = """ INSERT INTO exam_subjects_table (exam_code, subject_name, exam_date, exam_time, marks) VALUES (%s, %s, %s, %s, %s) """
                exam_subjects_value = [
                    (
                        item["exam_code"],
                        item["subject_name"],
                        item["exam_date"],
                        item["exam_time"],
                        item["marks"],
                    )
                    for item in exam_lists.get("exam_subjects_table", [])
                ]
                cursor.executemany(exam_subjects_query, exam_subjects_value)
                connection.commit()
        except Exception as e:
            print(f"Error:{e}")
        finally:
            connection.close()


def update(student):
    connection = db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:

                query = """ UPDATE students_information
                SET 
                    student_name=%s,
                    father_name=%s,
                    mother_name=%s,
                    student_age=%s,
                    fatherphone=%s,
                    motherphone=%s,
                    place=%s,
                    address=%s
                    
                    WHERE student_id=%s  """

                values=(
                    student['student_name'],
                    student['father_name'],
                    student['mother_name'],
                    student['student_age'],
                    student['father_phone'],
                    student['mother_phone'],
                    student['place'],
                    student['address'],
                    student['student_id']
                    )
                
                cursor.execute(query,values)
                connection.commit()
                print("Successfully Values are Updated")

        except Exception as e:
            print(f"Error : {e}")
        finally:
            connection.close()


def reg_attendance(arr):
    connection=db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                query = """ INSERT INTO attendance ( student_id , attendance_date , attendance_status )
                VALUES (%s , %s ,%s );"""
                cursor.executemany(query,arr)
                connection.commit()
                print("Successfully Values are Updated")

        except Exception as e:
            print(f"Error:{e}")
        finally:
            connection.close()

def get_today_attendance():
    connection=db_connection()
    attendance_dict={}
    if connection:
        try:
            with connection.cursor() as cursor:
                query=""" SELECT student_id , attendance_status FROM attendance WHERE attendance_date = %s """
                today_date=date.today().strftime('%Y-%m-%d')
                cursor.execute(query,(today_date,))
                results=cursor.fetchall()
                print(results)
                for row in results:
                    student_id=row['student_id']
                    status=row['attendance_status']
                    attendance_dict[student_id]=status

                print(attendance_dict)

        except Exception as e:
            print(f"Error:{e}")
        finally:
            connection.close()
            
    return attendance_dict
