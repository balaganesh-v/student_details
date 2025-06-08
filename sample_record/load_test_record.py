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
    connection=db_connection()
    if connection:
        try:
            with open('sample_record/sample_exams_data.json','r') as file:
                exam_lists = json.load(file)
            
            with connection.cursor() as cursor:
                # Delete the previous values in the database
                cursor.execute(" TRUNCATE TABLE exam_table;")
                connection.commit()
                #Insert the New values in the Database
                exam_query = """ INSERT INTO exam_table (exam_name, exam_code, class_name) VALUES (%s, %s, %s)"""
                exam_values=[ 
                    (item['exam_name'],item['exam_code'],item['class_name'])
                    for item in exam_lists.get("exam_table",[])
                ]
                cursor.executemany(exam_query,exam_values)
                connection.commit()



                #Delete the Previous values in the Database
                cursor.execute(" TRUNCATE TABLE exam_subjects_table; ")
                connection.commit()

                #Insert the New values in the Database
                exam_subjects_query = """ INSERT INTO exam_subjects_table (exam_code, subject_name, exam_date, exam_time, marks) VALUES (%s, %s, %s, %s, %s) """
                exam_subjects_value = [ 
                    (item['exam_code'],item['subject_name'],item['exam_date'],item['exam_time'],item['marks'])
                    for item in exam_lists.get("exam_subjects_table",[])
                ]
                cursor.executemany(exam_subjects_query,exam_subjects_value)
                connection.commit()
        except Exception as e:
            print(f"Error:{e}")
    pass
# clear exams data
# load exams data from json
# insert exams data to db

def load_all_records():
    load_students_record()
    load_exams_record()




    