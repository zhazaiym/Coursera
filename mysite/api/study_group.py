from mysite.database.models import StudyGroup, User, RoleChoices
from mysite.database.schema import StudyGroupInputSchema, StudyGroupOutSchema
from mysite.database.db import SessionLocal
from mysite.api.auth import get_current_user
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from typing import List

study_group_router = APIRouter(prefix='/study-group', tags=['Study Group'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@study_group_router.post('/', response_model=StudyGroupOutSchema)
async def create_study_group(group:StudyGroupInputSchema, db:Session = Depends(get_db), current_user:User = Depends(get_current_user)):
    if current_user.role != RoleChoices.student:
        raise HTTPException(status_code=403, detail='Создать группу может только студент')
    group_db = StudyGroup(**group.model_dump())
    db.add(group_db)
    db.commit()
    db.refresh(group_db)
    return group_db


@study_group_router.get('/', response_model=List[StudyGroupOutSchema])
async def list_study_group(db: Session = Depends(get_db)):
    return db.query(StudyGroup).all()


@study_group_router.get('/{group_id}/', response_model=StudyGroupOutSchema)
async def detail_study_group(group_id: int, db:Session = Depends(get_db)):
    group = db.query(StudyGroup).filter(StudyGroup.id==group_id).first()
    if not group:
        raise HTTPException(detail='Мындай группа жок', status_code=404)
    return group


@study_group_router.put('/{group_id}/', response_model=dict)
async def update_study_group(group_id: int, group: StudyGroupInputSchema, db: Session = Depends(get_db)):
    group_db = db.query(StudyGroup).filter(StudyGroup.id==group_id).first()
    if not group_db:
        raise HTTPException(detail='Мындай группа жок', status_code=404)
    for group_key, group_value in group.model_dump().items():
        setattr(group_db, group_key, group_value)
    db.commit()
    db.refresh(group_db)
    return {'message': 'Группа озгорулду'}


@study_group_router.delete('/{group_id}/', response_model=dict)
async def delete_study_group(group_id: int, db: Session = Depends(get_db)):
    group_db = db.query(StudyGroup).filter(StudyGroup.id==group_id).first()
    if not group_db:
        raise HTTPException(detail='Мындай группа жок', status_code=404)
    db.delete(group_db)
    db.commit()
    return {'message': 'Группа удалить болду'}
