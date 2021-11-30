from fastapi import FastAPI, APIRouter, Depends, HTTPException
from src.db.models import get_session, ClassMasters, UserMasters, ReservationList, WaitingList
from pydantic import BaseModel
from . import get_db
from sqlalchemy.orm.session import Session
from loguru import logger
from datetime import datetime
from typing import Optional

router = APIRouter()


class User(BaseModel):
    name: str


@router.post('/create/user', tags=['masters'])
def create_user(
        newuser: User,
        db: Session = Depends(get_db)
):
    try:
        new_entry = UserMasters(name=newuser.name)
        db.add(new_entry)
        db.commit()
        logger.debug('new used added')
        return {
            'detail': 'success'
        }
    except Exception as e:
        logger.debug(f'{e}')
        raise HTTPException(status_code=400, detail=f'{e}')


class ClassSchema(BaseModel):
    type: str
    capacity: int
    start_time: Optional[datetime] = datetime.now().astimezone().replace(microsecond=0)


@router.post('/create/class', tags=['masters'])
def create_class(
        newclass: ClassSchema,
        db: Session = Depends(get_db)
):
    try:
        new_entry = ClassMasters(type=newclass.type,
                                 capacity=newclass.capacity,
                                 start_time=newclass.start_time)
        db.add(new_entry)
        db.commit()
        logger.debug('new class added')
        return {
            'detail': 'success'
        }
    except Exception as e:
        logger.debug(f'{e}')
        raise HTTPException(status_code=400, detail=f'{e}')
