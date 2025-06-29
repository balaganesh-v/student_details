from flask import request
from app.repositories.student_repository import insert_student,pagination,get_student_information,delete_detail,get_old_image_url,update_student_details,load_all_students_record_from_db
import cloudinary.uploader
import os

def getStudentDetails():
    image = request.files.get("studentPhoto")
    image_url = None
    if image:
        try:
            upload_result = cloudinary.uploader.upload(image)
            image_url = upload_result.get("secure_url")
        except Exception as e:
            print(f"Image upload failed: {e}")
            image_url = None
    student = {
        "student_name": request.form.get("studentName"),
        "student_id": request.form.get("studentId"),
        "father_name": request.form.get("fatherName"),
        "mother_name": request.form.get("motherName"),
        "student_age": request.form.get("age"),
        "father_phone": request.form.get("fatherPhone"),
        "mother_phone": request.form.get("motherPhone"),
        "address": request.form.get("address"),
        "place": request.form.get("place"),
        "image_url": image_url,
    }
    return student

def addStudentDetails(student):
    insert_student(student)
    return True

def studentInfo():
    page = request.args.get('page',1,type=int)
    per_page = 10
    offset = (page-1)*per_page
    students,page,total_page= pagination(per_page,offset,page)
    return students,page,total_page

def editStudent(student_id):
    selected_students_info = get_student_information(student_id)
    return selected_students_info

def deleteStudent(student_id):
    return delete_detail(student_id)

def studentImages(student_id):
    new_file = request.files.get('image')
    old_url = get_old_image_url(student_id)
    return new_file,old_url

def fileUpload(new_file,old_url):
    if new_file and new_file.filename:
        try:
            if old_url:
                pid = os.path.splitext(os.path.basename(old_url))[0]
                cloudinary.uploader.destroy(pid)
            result = cloudinary.uploader.upload(new_file)
            image_url = result.get("secure_url")
        except Exception as e:
            print(f"Error : {e}")
        return image_url
    
def getEditStudentDetails(student_id,image_url):
    data = request.form
    student = {
        "student_name": data.get("student_name"),
        "student_id": student_id,
        "father_name": data.get("father_name"),
        "mother_name": data.get("mother_name"),
        "student_age": data.get("student_age"),
        "fatherphone": data.get("fatherphone"),
        "motherphone": data.get("motherphone"),
        "place": data.get("place"),
        "address": data.get("address"),
        "image_url": image_url
    }
    return student

def updateEditStudentDetail(student):
    return update_student_details(student)

def load_all_students_record(students):
    return load_all_students_record_from_db(students)
    