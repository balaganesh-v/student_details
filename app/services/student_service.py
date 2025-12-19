from flask import request,jsonify
from app.repositories.student_repository import (
    insert_student,
    pagination,
    get_student_information,
    delete_detail,get_old_image_url,
    update_student_details,
    load_all_students_record_from_db
    )
from app.validators.student_validator import StudentRegistrationSchema,StudentIdSchema
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
        
def datas_with_image_url(data):
    image_url=getUrlOfImage()
    data["image_url"] = image_url
    return data
    
def validate_datas(datas):
    validated_data=StudentRegistrationSchema(**datas).dict()
    return validated_data

def validate_student_id(studentId):
    datas = {"studentId": studentId}
    student_id_datas = StudentIdSchema(**datas).dict()
    return student_id_datas["studentId"]

    
def register_student_details():
    data=request.form.to_dict()
    datas=datas_with_image_url(data)
    validated_data=validate_datas(datas)
    addStudentDetails(validated_data)
    return True

def addStudentDetails(validated_data):
    insert_student(validated_data)
    return True

def studentInfo():
    page = get_current_page()
    offset = calculate_offset(page)
    return pagination(per_page=10, offset=offset, page=page)

def get_current_page():
    return request.args.get("page", 1, type=int)

def calculate_offset(page, per_page=10):
    return (page - 1) * per_page


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
    
def update_edit_student_details(valid_student_id):
    data = request.form.to_dict()
    image_url = studentPhotoUrl(valid_student_id)
    data["student_id"] = valid_student_id
    data["image_url"] = image_url
    updateEditStudentDetail(data)
    

def updateEditStudentDetail(data):
    update_student_details(data)
    

def load_all_students_record(students_data):
    return load_all_students_record_from_db(students_data)
    