from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from mysite.database.models import(RoleChoices, UserStatusChoices, CourseStatusChoices,
                                   CourseLevelChoices, StudyGroupStatusChoices, ApplicationStatusChoices,
                                   EnrollmentStatusChoices)

class UserInputSchema(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: RoleChoices
    user_status: UserStatusChoices
    is_active: bool

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: EmailStr
    role: RoleChoices
    user_status: UserStatusChoices
    is_active: bool

class CurrentUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: EmailStr
    role: RoleChoices
    user_status: UserStatusChoices


class CategoryInputSchema(BaseModel):
    category_name: str


class CategoryOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category_name: str


class CourseInputSchema(BaseModel):
    title: str
    category: str
    description: str
    level: CourseLevelChoices
    price: int
    duration_weeks: int
    is_active: bool
    status: CourseStatusChoices


class CourseOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    category: str
    description: str
    level: CourseLevelChoices
    price: int
    duration_weeks: int
    is_active: bool
    status: CourseStatusChoices


class StudyGroupInputSchema(BaseModel):
    name: str
    course_id: int
    teacher_id: int
    starts_on: datetime
    ends_on: datetime
    status: StudyGroupStatusChoices


class StudyGroupOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    course_id: int
    teacher_id: int
    starts_on: datetime
    ends_on: datetime
    status: StudyGroupStatusChoices


class ApplicationInputSchema(BaseModel):
    course_id: int
    comment: str


class ApplicationOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    course_id: int
    manager_id: int | None = None
    comment: Optional[str]
    status: ApplicationStatusChoices

class ApplicationUpdateSchema(BaseModel):
    manager_id: int | None = None
    status: ApplicationStatusChoices


class EnrollmentInputSchema(BaseModel):
    student_id: int
    group_id: int
    status: EnrollmentStatusChoices


class EnrollmentOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    group_id: int
    status: EnrollmentStatusChoices

class ChainInputSchema(BaseModel):
    text: str


class ChainOutSchema(BaseModel):
    answer: str

