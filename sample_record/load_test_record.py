from db import db_connection
import json


def load_students_record():
    connection=db_connection()
    if connection:
        try:
            with open("sample_record/sample_students_data.json", 'r') as file:
                students = json.load(file)

            with connection.cursor() as cursor:
                cursor.execute("TRUNCATE TABLE students_information")
                connection.commit()
                query="""INSERT INTO students_information (
                        student_name, student_id, father_name, mother_name,
                        student_age, fatherphone, motherphone, address, place, image_url )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                values=[
                    (student['student_name'],student['student_id'],student['father_name'],
                    student['mother_name'],student['student_age'],student['fatherphone'],
                    student['motherphone'],student['address'],student['place'],student['image_url']) 
                    for student in students
                    ]
                cursor.executemany(query, values)
                connection.commit()
        except Exception as e:
            print(f"Error:{e}")
# clear students data
# load students data from json
# insert students data to db


def load_exams_record():
    pass
# clear exams data
# load exams data from json
# insert exams data to db

def load_all_records():
    load_students_record()
    load_exams_record()




    