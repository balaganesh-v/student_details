from pydantic import BaseModel, validator, HttpUrl
import re

class StudentRegistrationSchema(BaseModel):
    studentName: str
    studentId: int
    fatherName: str
    motherName: str
    studentAge: int 
    studentPlace: str
    fatherPhone: str
    motherPhone: str
    studentAddress: str
    image_url: HttpUrl  # Validates that it's a proper URL

    @validator("studentName", "fatherName", "motherName", "studentPlace")
    def validate_names(cls, value, field):
        if not re.match(r"^[A-Za-z.\s]+$", value):
            raise ValueError(f"{field.name} must contain only letters and spaces")
        return value

    @validator("studentId")
    def validate_student_id(cls, value):
        if value < 0:
            raise ValueError("Student ID must be a positive integer")
        return value

    @validator("studentAge")
    def validate_age(cls, value):
        if value < 3 or value > 100:
            raise ValueError("Student age must be between 3 and 100")
        return value

    @validator("fatherPhone", "motherPhone")
    def validate_phone(cls, value, field):
        if not re.match(r"^\d{10}$", value):
            raise ValueError(f"{field.name} must be a valid 10-digit number")
        return value

    @validator("studentAddress")
    def validate_address(cls, value):
        if len(value.strip()) < 5:
            raise ValueError("Student address must be at least 5 characters long")
        return value


class StudentIdSchema(BaseModel):
    studentId : int

    @validator("studentId")
    def validate_student_id(cls, value):
        if value < 0:
            raise ValueError("Student ID must be a positive integer")
        return value