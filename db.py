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
                        student["father_phone"],
                        student["mother_phone"],
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
    return True


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
                cursor.execute("SELECT subject_name FROM subjects_table;")
                result = cursor.fetchall()
                return [row["subject_name"] for row in result]
        except Exception as e:
            print(f"Error fetching subjects: {e}")
        finally:
            connection.close()
    return None



def get_exams():
    try:
        with db_connection() as connection:
            with connection.cursor() as cursor:
                arr=[]
                query=""" SELECT * FROM exam_table ; """
                cursor.execute(query)
                dict_exams=cursor.fetchall()
                print(dict_exams)

                query=""" SELECT * FROM exam_subjects_table;"""
                cursor.execute(query)
                dict_subjects=cursor.fetchall()
                print(dict_subjects)

                return dict_exams,dict_subjects

    except Exception as e:
        print(f"Error : {e}")




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
    if not connection:
        return None
    with connection.cursor() as cursor:
        query = """
          UPDATE students_information
          SET student_name=%s, father_name=%s, mother_name=%s,
              student_age=%s, fatherphone=%s, motherphone=%s,
              place=%s, address=%s, image_url=%s
          WHERE student_id=%s """
        values = (
          student['student_name'],
          student['father_name'],
          student['mother_name'],
          student['student_age'],
          student['father_phone'],
          student['mother_phone'],
          student['place'],
          student['address'],
          student['image_url'],
          student['student_id']
        )
        cursor.execute(query,values)
        connection.commit()
        connection.close()
    return None


def get_old_image(student_id):
    with db_connection() as connection:
        try:
            with connection.cursor() as cursor:
                query = """ SELECT image_url FROM students_information WHERE student_id = %s """
                cursor.execute(query,(student_id,))
                result = cursor.fetchone()
                return result['image_url'] if result else None
        except Exception as e:
            print(f"Error : {e}")
    return None


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
                for row in results:
                    student_id=row['student_id']
                    status=row['attendance_status']
                    attendance_dict[student_id]=status
                    
        except Exception as e:
            print(f"Error:{e}")
        finally:
            connection.close()
            
    return attendance_dict


def working_day(month_input):
    working_day_count = 0
    try:
        with db_connection() as connection:
            with connection.cursor() as cursor:
                query = """SELECT attendance_date FROM attendance WHERE DATE_FORMAT(attendance_date, "%Y-%m") = %s;"""
                cursor.execute(query, (month_input,))
                total_attendance_dates = cursor.fetchall()
                print(total_attendance_dates)
                unique_dates = set([row[0] for row in total_attendance_dates])
                working_day_count = len(unique_dates)
                print(working_day_count)
    except Exception as e:
        print(f"Error: {e}")
        
    return working_day_count


def students_attendance_average(month_input):
    attendance_records = []
    working_day_count = working_day(month_input)
    
    try:
        with db_connection() as connection:
            with connection.cursor() as cursor:
                sql_query = """SELECT student_id FROM students_information"""
                cursor.execute(sql_query)
                results = cursor.fetchall()
                print(results)

                for row in results:
                    student_id = row[0]
                    query = """
                        SELECT ROUND((SUM(CASE WHEN attendance_status = 'Present' THEN 1 ELSE 0 END) * 100 / %s), 2)
                        AS attendance_percentage 
                        FROM attendance
                        WHERE student_id = %s AND DATE_FORMAT(attendance_date, "%Y-%m") = %s
                    """
                    value = (working_day_count, student_id, month_input)
                    cursor.execute(query, value)
                    result = cursor.fetchone()

                    attendance_percentage = result[0] if result[0] is not None else 0.0

                    attendance_records.append({
                        "student_id": student_id,
                        "attendance_percentage": attendance_percentage
                    })

        print(attendance_records)
    except Exception as e:
        print(f"Error: {e}")

        
    return attendance_records
