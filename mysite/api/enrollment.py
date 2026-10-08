from mysite.database.models import Enrollment, User, RoleChoices
from mysite.database.schema import EnrollmentInputSchema, EnrollmentOutSchema
from mysite.database.db import SessionLocal
from mysite.api.auth import get_current_user
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from typing import List

enrollment_router = APIRouter(prefix='/enrollment', tags=['Enrollment'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@enrollment_router.post('/', response_model=EnrollmentOutSchema)
async def create_enrollment(enrollment:EnrollmentInputSchema, db:Session = Depends(get_db)):
    enrollment_db = Enrollment(**enrollment.model_dump())
    db.add(enrollment_db)
    db.commit()
    db.refresh(enrollment_db)
    return enrollment_db


@enrollment_router.get('/', response_model=List[EnrollmentOutSchema])
async def list_enrollment(db: Session = Depends(get_db), current_user:User = Depends(get_current_user)):
    if current_user.role == RoleChoices.student:
        return db.query(Enrollment).filter(Enrollment.student_id==current_user.id).all()
    return db.query(Enrollment).all()


@enrollment_router.get('/{enrollment_id}/', response_model=EnrollmentOutSchema)
async def detail_enrollment(enrollment_id: int, db:Session = Depends(get_db), current_user:User = Depends(get_current_user)):
    enrollment = db.query(Enrollment).filter(Enrollment.id==enrollment_id).first()
    if not enrollment:
        raise HTTPException(detail='Мындай запись жок', status_code=404)
    if current_user.role == RoleChoices.student and enrollment.student_id != current_user.id:
        raise HTTPException(status_code=403, detail='Бул запись сиздики эмес')
    return enrollment


@enrollment_router.put('/{enrollment_id}/', response_model=dict)
async def update_enrollment(enrollment_id: int, enrollment: EnrollmentInputSchema, db: Session = Depends(get_db)):
    enrollment_db = db.query(Enrollment).filter(Enrollment.id==enrollment_id).first()
    if not enrollment_db:
        raise HTTPException(detail='Мындай запись жок', status_code=404)
    for enrollment_key, enrollment_value in enrollment.model_dump().items():
        setattr(enrollment_db, enrollment_key, enrollment_value)
    db.commit()
    db.refresh(enrollment_db)
    return {'message': 'Запись озгорулду'}


@enrollment_router.delete('/{enrollment_id}/', response_model=dict)
async def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment_db = db.query(Enrollment).filter(Enrollment.id==enrollment_id).first()
    if not enrollment_db:
        raise HTTPException(detail='Мындай запись жок', status_code=404)
    db.delete(enrollment_db)
    db.commit()
    return {'message': 'Запись удалить болду'}
