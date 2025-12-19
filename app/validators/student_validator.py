from pydantic import BaseModel, HttpUrl, field_validator
from pydantic_core.core_schema import FieldValidationInfo
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
    image_url: HttpUrl

    @field_validator("studentName", "fatherName", "motherName", "studentPlace")
    @classmethod
    def validate_names(cls, value: str, info: FieldValidationInfo) -> str:
        if not re.match(r"^[A-Za-z.\s]+$", value):
            raise ValueError(f"{info.field_name} must contain only letters and spaces")
        return value

    @field_validator("studentId")
    @classmethod
    def validate_student_id(cls, value: int) -> int:
        if value < 0:
            raise ValueError("Student ID must be a positive integer")
        return value

    @field_validator("studentAge")
    @classmethod
    def validate_age(cls, value: int) -> int:
        if value < 3 or value > 100:
            raise ValueError("Student age must be between 3 and 100")
        return value

    @field_validator("fatherPhone", "motherPhone")
    @classmethod
    def validate_phone(cls, value: str, info: FieldValidationInfo) -> str:
        if not re.match(r"^\d{10}$", value):
            raise ValueError(f"{info.field_name} must be a valid 10-digit number")
        return value

    @field_validator("studentAddress")
    @classmethod
    def validate_address(cls, value: str) -> str:
        if len(value.strip()) < 5:
            raise ValueError("Student address must be at least 5 characters long")
        return value


class StudentIdSchema(BaseModel):
    studentId: int

    @field_validator("studentId")
    @classmethod
    def validate_student_id(cls, value: int) -> int:
        if value < 0:
            raise ValueError("Student ID must be a positive integer")
        return value
