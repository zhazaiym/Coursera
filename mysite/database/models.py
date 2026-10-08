from mysite.database.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text, Boolean, DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from enum import Enum as PyEnum
from datetime import datetime


class RoleChoices(str, PyEnum):
    student = 'student'
    teacher = 'teacher'
    manager = 'manager'
    admin = 'admin'


class UserStatusChoices(str, PyEnum):
    free = 'free'
    pro = 'pro'


class CourseLevelChoices(str, PyEnum):
    beginner = 'beginner'
    intermediate = 'intermediate'
    advanced = 'advanced'


class CourseStatusChoices(str, PyEnum):
    free = 'free'
    plus = 'plus'


class StudyGroupStatusChoices(str, PyEnum):
    recruiting = 'recruiting'
    active = 'active'
    completed = 'completed'
    cancelled = 'cancelled'


class ApplicationStatusChoices(str, PyEnum):
    new = 'new'
    in_progress = 'in_progress'
    accepted = 'accepted'
    rejected = 'rejected'
    cancelled = 'cancelled'


class EnrollmentStatusChoices(str, PyEnum):
    active = 'active'
    completed = 'completed'
    cancelled = 'cancelled'


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    role: Mapped[RoleChoices] = mapped_column(SQLAlchemyEnum(RoleChoices))
    user_status: Mapped[UserStatusChoices] = mapped_column(SQLAlchemyEnum(UserStatusChoices))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String)


class Course(Base):
    __tablename__ = "course"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    level: Mapped[CourseLevelChoices] = mapped_column(SQLAlchemyEnum(CourseLevelChoices))
    price: Mapped[int] = mapped_column(Integer)
    duration_weeks: Mapped[int] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    status: Mapped[CourseStatusChoices] = mapped_column(SQLAlchemyEnum(CourseStatusChoices))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())


class StudyGroup(Base):
    __tablename__ = "study_group"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    course_id: Mapped[int] = mapped_column(Integer)
    teacher_id: Mapped[int] = mapped_column(Integer)
    starts_on: Mapped[datetime] = mapped_column(DateTime)
    ends_on: Mapped[datetime] = mapped_column(DateTime)
    capacity: Mapped[int] = mapped_column(Integer)
    status: Mapped[StudyGroupStatusChoices] = mapped_column(SQLAlchemyEnum(StudyGroupStatusChoices))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())



class Application(Base):
    __tablename__ = "application"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    student_id: Mapped[int] = mapped_column(Integer)

    course_id: Mapped[int] = mapped_column(Integer)

    manager_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    comment: Mapped[str] = mapped_column(Text)

    status: Mapped[ApplicationStatusChoices] = mapped_column(
        SQLAlchemyEnum(ApplicationStatusChoices),
        default=ApplicationStatusChoices.new
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )


class Enrollment(Base):
    __tablename__ = "enrollment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(Integer)
    group_id: Mapped[int] = mapped_column(Integer)
    status: Mapped[EnrollmentStatusChoices] = mapped_column(SQLAlchemyEnum(EnrollmentStatusChoices))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
