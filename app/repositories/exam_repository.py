from config.db_config import db_connection

def get_all_exams_from_db():
    try:
        with db_connection() as connection:
            with connection.cursor() as cursor:
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


def get_all_subjects_from_db():
    try:
        with db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT subject_name FROM subjects_table;")
                result = cursor.fetchall()
                return [row["subject_name"] for row in result]
    except Exception as e:
        print(f"Error fetching subjects: {e}")
    return True

def publish_details(exam_details, exam_name, exam_code, class_name):
    try:
        with db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute( """ INSERT INTO exam_table (exam_name, exam_code, class_name) 
                               VALUES (%s, %s, %s) """,(exam_name, exam_code, class_name))
                query_subjects = """ INSERT INTO exam_subjects_table (exam_code, subject_name, exam_date, exam_time, marks) 
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
    return True

def load_all_exams_record_from_db(exam_lists):
    try:
        with db_connection() as connection:
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
    return True