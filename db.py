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
        return

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
