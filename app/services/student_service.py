from flask import request
from app.repositories.student_repository import (
    insert_student,
    pagination,
    get_student_information,
    delete_detail,get_old_image_url,
    update_student_details,
    load_all_students_record_from_db
    )
import cloudinary.uploader
import os

def getUrlOfImage():
    image = request.files.get("studentPhoto")
    image_url = None
    if image:
        try:
            upload_result = cloudinary.uploader.upload(image)
            image_url = upload_result.get("secure_url")
            return image_url
        except Exception as e:
            print(f"Image upload failed: {e}")
            image_url = None
            return image_url

def addStudentDetails(data,student):
    insert_student(data,student)
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

def studentPhotoUrl(student_id):
    new_file,old_url=studentImages(student_id)
    image_url = old_url
    if new_file:
       image_url = fileUpload(new_file,old_url=old_url)
       return image_url
    return image_url

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
    


def updateEditStudentDetail(data,student_id,image_url):
    return update_student_details(data,student_id,image_url)

def load_all_students_record(students_data):
    return load_all_students_record_from_db(students_data)
    