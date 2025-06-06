import os #Access the Environment Variables 
import pymysql #connect to mysqldatabase
from dotenv import load_dotenv #Load variables from the .env file

load_dotenv()  #correct function name is load_dotenv, not load_env

def db_connection():

    #Establish a database connection using pymysql and return the connection object.
    try:
        print("Starting connection...")
        connection = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            cursorclass=pymysql.cursors.DictCursor
            
        )
        print("Successfully connected to MySQL.")
        return connection
    except Exception as e:
        print(f"Error: {e}")
        return None


def insert_student(student):


    #Insert a student record into the students table.

    """student is a dict with keys:
    student_name, student_id, father_name, mother_name,
    student_age, fatherPhone, motherPhone, address, place
    """

    query = """
    INSERT INTO students_information (student_name, student_id, father_name, mother_name,
    student_age, fatherphone, motherphone, address, place
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) """

    connection = db_connection()
    if not connection:
        print("Database connection failed.")
        return 0

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (
                student.get('student_name'),
                student.get('student_id'),
                student.get('father_name'),
                student.get('mother_name'),
                student.get('student_age'),
                student.get('fatherPhone'),
                student.get('motherPhone'),
                student.get('address'),
                student.get('place'),
            ))
        connection.commit()
        print("Student inserted successfully.")
    except Exception as e:
        print(f"Error inserting student: {e}")
    finally:
        connection.close()


def insert_studentDetails(exam):
    query="""INSERT INTO exam_table 
    (exam_name,exam_code,class) VALUES (%s,%s,%s) """

    connection = db_connection()
    if not connection:
        print("Database connection failed.")
        return 

    try:
        with connection.cursor() as cursor:
            cursor.execute(query,(
                exam.get('exam_name'),
                exam.get('exam_code'),
                exam.get('class_name')
            ))
        connection.commit()
        print("Exam Info Details inserted Successfully.")
    except Exception as e:
        print(f"Error inseting info details:{e}")
    finally:
        connection.close()



def publishdetails(exam_details, exam_name, exam_code, class_name):
    connection = db_connection()  # Your function to get MySQL connection
    if connection:
        try:
            with connection.cursor() as cursor:
                # Insert into the main exam_table
                query_exam = """
                    INSERT INTO exam_table (exam_name, exam_code, class_name)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(query_exam, (exam_name, exam_code, class_name))

                # Insert multiple rows into exam_subjects_table
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
            connection.rollback()
        finally:
            connection.close()
