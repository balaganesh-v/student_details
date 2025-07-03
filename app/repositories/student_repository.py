from config.db_config import db_connection

def insert_student(data,image_url):
    try:
        with db_connection() as connection:
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
                        data.get("studentName"),
                        data.get("studentId"),
                        data.get("fatherName"),
                        data.get("motherName"),
                        data.get("studentAge"),
                        data.get("fatherPhone"),
                        data.get("motherPhone"),
                        data.get("studentAddress"),
                        data.get("studentPlace"),
                        image_url,
                    ),
                )
                connection.commit()
    except Exception as e:
        print(f"Error inserting student: {e}")
    return True


def pagination(per_page,offset,page):
    try:
        with db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(" SELECT COUNT(*) AS total FROM students_information ;")
                result = cursor.fetchone()
                total_students = result['total']
                total_pages = (total_students + per_page - 1) // per_page
                cursor.execute(" SELECT * FROM students_information LIMIT %s OFFSET %s",(per_page,offset))
                students=cursor.fetchall() 
                return (students,page,total_pages)
    except Exception as e:
        print(f"Error : {e}")
    
def get_student_information(student_id):
    try:
        connection = db_connection()  # call the function to get a connection object
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students_information WHERE student_id = %s", (student_id,))
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(f"Error fetching student: {e}")
        return None  # return None instead of True on failure
    finally:
        cursor.close()
        connection.close()


def delete_detail(student_id):
    try:
        with db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM students_information WHERE student_id = %s",(student_id,),)
                connection.commit()
    except Exception as e:
        print(f"Error deleting student: {e}")
    return True

def get_old_image_url(student_id):
    try:
        with db_connection() as connection:
            with connection.cursor() as cursor:
                query = """ SELECT image_url FROM students_information WHERE student_id = %s """
                cursor.execute(query,(student_id,))
                result = cursor.fetchone()
                return result['image_url']
    except Exception as e:
        print(f"Error : {e}")
    return True

def update_student_details(data,student_id,image_url):
    try:
        connection = db_connection()  # Call the function to get a connection
        cursor = connection.cursor()
        query = """
            UPDATE students_information
            SET student_name=%s, father_name=%s, mother_name=%s,
                student_age=%s, fatherphone=%s, motherphone=%s,
                place=%s, address=%s, image_url=%s
            WHERE student_id=%s
        """
        values = (
            data.get('studentName'),
            data.get('fatherName'),
            data.get('motherName'),
            data.get('studentAge'),
            data.get('fatherPhone'),
            data.get('motherPhone'),
            data.get('StudentPlace'),
            data.get('studentAddress'),
            image_url,
            data.get('student_id')
        )
        cursor.execute(query, values)
        connection.commit()
        return True
    except Exception as e:
        print(f"Error updating student: {e}")
        return False
    finally:
        cursor.close()
        connection.close()


def load_all_students_record_from_db(students_data):
    try:
        with db_connection() as connection:
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
                    for student in students_data
                ]
                cursor.executemany(query, values)
                connection.commit()
    except Exception as e:
        print(f"Error:{e}")
    return True