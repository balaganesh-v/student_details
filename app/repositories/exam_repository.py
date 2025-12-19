
from config.db_config import db_connection



def get_pagination_exams_from_db(per_page,offset):
    try:
        connection = db_connection()
        cursor = connection.cursor()

        # Calculating the total
        cursor.execute(""" SELECT  COUNT(DISTINCT exam_code) AS total 
                       FROM exam_table;""")
        result = cursor.fetchone()
        total_students = result['total']

        
        total_pages = (total_students + per_page - 1) // per_page
        cursor.execute( """
                       SELECT exam_name, exam_code, class_name 
                       FROM exam_table 
                       LIMIT %s OFFSET %s;
                    """, (per_page, offset))
        exams = cursor.fetchall()

        exam_codes = [exam['exam_code'] for exam in exams]
        subjects_grouped = [[] for _ in exams] 
        if exam_codes:
            placeholders = ','.join(['%s'] * len(exam_codes))
            cursor.execute(f"""
                           SELECT exam_code, subject_name, exam_date
                           FROM exam_subjects_table
                           WHERE exam_code IN ({placeholders})
                           ORDER BY exam_code;
                        """, tuple(exam_codes))
            all_subjects = cursor.fetchall()
            
             # Group subjects by exam (same order as exams list)
            for subject in all_subjects:
                for i, exam in enumerate(exams):
                    if subject['exam_code'] == exam['exam_code']:
                        subjects_grouped[i].append(subject)
                        break
        
        

        return exams, subjects_grouped, total_pages

    except Exception as e:
        print(f"Error : {e}")
        return [], [], 0




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
