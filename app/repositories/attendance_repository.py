from config.db_config import db_connection

def get_student_name_id_from_db():
    try:
        with db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT student_name,student_id FROM students_information")
                return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching students: {e}")
    return True

def get_today_attendance_from_db(today_date):
    connection=db_connection()
    attendance_dict={}
    try:
        with db_connection() as connection:
            with connection.cursor() as cursor:
                query=""" SELECT student_id,attendance_status FROM attendance WHERE attendance_date = %s """
                cursor.execute(query,(today_date,))
                results=cursor.fetchall()
                for row in results:
                    student_id=row['student_id']
                    status=row['attendance_status']
                    attendance_dict[student_id]=status
            return attendance_dict
    except Exception as e:
        print(f"Error:{e}")
    return True

def register_students_attendance_to_db(arr):
    try:
        with db_connection() as connection:
            with connection.cursor() as cursor:
                query = """ INSERT INTO attendance ( student_id , attendance_date , attendance_status )
                VALUES (%s , %s ,%s );"""
                cursor.executemany(query,arr)
                connection.commit()
                print("Successfully Values are Updated")

    except Exception as e:
        print(f"Error:{e}")
        

def students_attendance_average_from_db(month_input):
    attendance_records = []
    working_day_count = working_day(month_input)
    
    try:
        with db_connection() as connection:
            with connection.cursor() as cursor:
                sql_query = """SELECT student_id FROM students_information"""
                cursor.execute(sql_query)
                results = cursor.fetchall()
                
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

# def load_all_attendance_records_from_db(attendance_data):
    