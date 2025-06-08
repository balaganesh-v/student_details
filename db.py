import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

def db_connection():
    try:
        return pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            cursorclass=pymysql.cursors.DictCursor
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
    return []


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
                cursor.execute(query, (
                    student['student_name'],
                    student['student_id'],
                    student['father_name'],
                    student['mother_name'],
                    student['student_age'],
                    student['fatherPhone'],
                    student['motherPhone'],
                    student['address'],
                    student['place'],
                    student['image_url']
                ))
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
                cursor.execute("DELETE FROM students_information WHERE student_id = %s", (student_id,))
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
                cursor.execute("SELECT * FROM students_information WHERE student_id = %s", (student_id,))
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
                return [row['subject_name'] for row in result]
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
                cursor.execute("""
                    INSERT INTO exam_table (exam_name, exam_code, class_name)
                    VALUES (%s, %s, %s)
                """, (exam_name, exam_code, class_name))

                query_subjects = """
                    INSERT INTO exam_subjects_table (exam_code, subject_name, exam_date, exam_time, marks)
                    VALUES (%s, %s, %s, %s, %s)
                """
                subjects_data = [
                    (exam_code, item['subject_name'], item['exam_date'], item['exam_time'], item['marks'])
                    for item in exam_details
                ]
                cursor.executemany(query_subjects, subjects_data)
                connection.commit()
        except Exception as e:
            print(f"Error inserting exam details: {e}")
        finally:
            connection.close()
