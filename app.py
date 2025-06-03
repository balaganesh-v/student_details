from flask import Flask, render_template, request, redirect, url_for
from db import db_connection, insert_student

app = Flask(__name__)

@app.route('/')
def index():

    return render_template("index.html")

students=[]
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print(request.form)
        # breakpoint()
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
        print(student)
        students.append(student)
        insert_student(student)
        return redirect(url_for('/register'))
    return render_template('register.html')

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
