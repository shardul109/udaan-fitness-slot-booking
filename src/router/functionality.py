from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy.orm.session import Session

from src.db.models import ClassMasters, ReservationList, WaitingList
from . import get_db

router = APIRouter()


@router.get('/reservation', tags=['functionality'])
def reservation(
        userid: int,
        classid: int,
        db: Session = Depends(get_db)
):
    try:
        class_capacity = db.query(ClassMasters).filter_by(id=classid).one().capacity

        res = db.query(ReservationList).filter_by(class_id=classid).all()
        if len(res) >= class_capacity:
            new_entry = WaitingList(
                class_id=classid,
                user_id=userid
            )
            db.add(new_entry)
            db.commit()
            return {
                'detail': 'reservation full , added in waiting list'
            }

        else:
            new_entry = ReservationList(
                class_id=classid,
                user_id=userid
            )
            db.add(new_entry)
            db.commit()
            return {
                'detail': 'reservation successfull'
            }

    except Exception as e:
        logger.debug(f'{e}')
        raise HTTPException(status_code=400, detail=f'{e}')


@router.get('/cancel_reservation', tags=['functionality'])
def cancel_reservation(
        userid: int,
        classid: int,
        db: Session = Depends(get_db)
):
    try:
        class_start = db.query(ClassMasters).filter_by(id=classid).one().start_time
        if class_start - datetime.now() < timedelta(minutes=30):
            raise HTTPException(status_code=400, detail='cannot cancel , only 30minutes left for the class')

        res = db.query(ReservationList).filter_by(user_id=userid, class_id=classid).one()
        db.delete(res)
        logger.debug('reservation deleted')

        res = db.query(WaitingList).filter_by(class_id=classid).all()
        db.commit()

        if len(res) == 0:
            return {
                'detail': 'successfully cancelled reservation'
            }

        else:
            res = res[0]
            db.delete(res)
            new_entry = ReservationList(class_id=classid, user_id=res.user_id)
            db.add(new_entry)
            logger.debug(f'{res.user_id} reservation confirmed from waiting list')
            db.commit()
            return {
                'detail': 'successfully cancelled reservation'
            }

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.debug(f'{e}')
        raise HTTPException(status_code=400, detail=f'{e}')
