from config.db_config import db_connection
from datetime import datetime
from calendar import monthrange

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

    if working_day_count == 0:
        print("Warning: Working day count is 0 for month:", month_input)
        return []  # avoid division by zero

    try:
        connection = db_connection()
        cursor = connection.cursor()

        query = "SELECT student_id FROM attendance GROUP BY student_id "
        cursor.execute(query)
        results = cursor.fetchall()

        for row in results:
            student_id = row['student_id']
        
            query = """
            SELECT ROUND((SUM(CASE WHEN attendance_status = 'Present' THEN 1 ELSE 0 END) * 100.0 / %s), 2)
            AS attendance_percentage
            FROM attendance
            WHERE student_id = %s AND DATE_FORMAT(attendance_date, '%%Y-%%m') = %s
            """
            values = (working_day_count, student_id, month_input)
            cursor.execute(query, values)
            result = cursor.fetchone()
            attendance_percentage = result['attendance_percentage'] 
            attendance_records.append({
                "student_id": student_id,
                "attendance_percentage": attendance_percentage
            })

    except Exception as e:
        print(f"Error: students_attendance_average {e}")
        return 0
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return attendance_records


def working_day(month_input):
    try:
        dt = datetime.strptime(month_input, "%Y-%m")
        start = dt.replace(day=1).strftime('%Y-%m-%d')
        end = dt.replace(day=monthrange(dt.year, dt.month)[1]).strftime('%Y-%m-%d')
        with db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""SELECT COUNT(DISTINCT attendance_date) AS total FROM attendance WHERE attendance_date BETWEEN %s AND %s""", (start, end))
                result = cursor.fetchone()
                count = result['total']
                print(result['total'])

                if count == 0:
                    print(f" No attendance records found for {month_input}")

        return count

    except Exception as e:
        print(f"Error in working_day: {e}")
        return 0


def load_all_attendance_records_from_db(attendance_data):
    try:
        connection = db_connection()
        cursor = connection.cursor() 
        query = ''' DELETE FROM attendance ; '''
        cursor.execute(query)
        connection.commit()
        query1='''INSERT INTO attendance (student_id,attendance_date,attendance_status) VALUES ( %s,%s,%s )'''
        values1 = [
            (
                student_attendance_record['student_id'],
                student_attendance_record['attendance_date'],
                student_attendance_record['attendance_status']
            )
            for student_attendance_record in attendance_data
            ]
        cursor.executemany(query1,values1)
        connection.commit()
    except Exception as e:
        print(f"Error : {e}")
    finally:
        cursor.close()
        connection.close()