from flask import Flask,flash, render_template, request, redirect, url_for, jsonify,render_template_string
from db import db_connection, insert_student,insert_studentDetails,publishdetails


app = Flask(__name__)
app.secret_key='your-secret-key'


@app.route('/')
def index():
    connection = db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM students_information")
                students = cursor.fetchall()
        except Exception as e:
            print(f"Error fetching students: {e}")
        finally:
            connection.close()
    return render_template("index.html",students=students)


students = []
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        student = {
            'student_name': request.form.get('studentName'),
            'student_id': request.form.get('studentId'),
            'father_name': request.form.get('fatherName'),
            'mother_name': request.form.get('motherName'),
            'student_age': request.form.get('age'),
            'fatherPhone': request.form.get('fatherPhone'),
            'motherPhone': request.form.get('motherPhone'),
            'address': request.form.get('address'),
            'place': request.form.get('place'),
        }
        insert_student(student)  # Assuming this saves student in DB or storage
        students.append(student)  # Local list update if needed
        flash('Registration successful!', 'success')
        return redirect(url_for('index'))
    else:
        flash('Invalid request method.', 'warning')
        return redirect(url_for('index'))
    
# @app.route('/student_info')
# def student_info():
#     connection = db_connection()
#     if connection:
#         try:
#             with connection.cursor() as cursor:
#                 cursor.execute("SELECT * FROM students_information")
#                 students = cursor.fetchall()
#             print(students)
#         except Exception as e:
#             print(f"Error fetching students: {e}")
#         finally:
#             connection.close()
#     return render_template('student_info.html', students=students)

@app.route('/delete_student/<student_id>', methods=['POST'])
def delete_student(student_id):
    connection = db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM students_information WHERE student_id = %s"
                cursor.execute(sql, (student_id,))
                connection.commit()
        except Exception as e:
            print("Error:", e)
        finally:
            connection.close()
    return redirect(url_for('index'))


@app.route('/edit_student/<student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    connection = db_connection()
    selected_student = None
    if connection:
        try:
            with connection.cursor() as cursor:
                # Fetch selected student by ID
                cursor.execute("SELECT * FROM students_information WHERE student_id = %s", (student_id,))
                selected_student = cursor.fetchone()
                print(selected_student)

        except Exception as e:
            print(f"Error fetching students: {e}")
        finally:
            connection.close()
        print(selected_student)
    if selected_student:
        return jsonify(selected_student)
    else:
        return jsonify({'error': 'Student not found'}), 404



@app.route('/exam')
def exam():
    return render_template("exam.html",exam_details=exam_details)


@app.route('/subjects')
def getSubjects():
    subjects=[]
    connection=db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT subject_name FROM subjects_table ")
                result=cursor.fetchall()
                subjects = [row['subject_name'] for row in result]
        except Exception as e:
            print(f"Error fetching students: {e}")
        finally:
            connection.close()
    return jsonify(subjects)





# add route will call from the AJAX
exam_details=[]
@app.route('/add', methods=['POST'])
def add_exam():
    data = request.get_json()
    if data:
        exam_details.append({
            'subject_name': data['subject_name'],
            'exam_date': data['exam_date'],
            'exam_time': data['exam_time'],
            'marks': data['marks']
        })
        return jsonify(data)  # Echo back to client for immediate update
    return jsonify({'error': 'Invalid data'}), 400



@app.route('/publish_now', methods=['POST'])
def publish():
    global exam_details
    exam_name = request.form.get('examName')
    exam_code = request.form.get('examCode')
    class_name = request.form.get('className')

    # Process and store the published exam (you can save to DB or a file)
    publishdetails(exam_details, exam_name, exam_code, class_name)

    # Clear after publishing
    exam_details.clear()
    return render_template("exam.html", exam_details=[])


    



if __name__ == '__main__':
    app.run(debug=True)

