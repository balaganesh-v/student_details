from flask import Flask,flash, render_template, request, redirect, url_for
from db import db_connection, insert_student

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
            print(students)
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



@app.route('/student_info')
def student_info():
    connection = db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM students_information")
                students = cursor.fetchall()
            print(students)
        except Exception as e:
            print(f"Error fetching students: {e}")
        finally:
            connection.close()
    return render_template('student_info.html', students=students)



if __name__ == '__main__':
    app.run(debug=True)
