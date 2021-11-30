from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, Date, DateTime, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

cdb = None
DBSession: sessionmaker = None
Base = declarative_base()


def init_db():
    global cdb, DBSession
    config_path = f'src/db'
    cdb = create_engine(
        f'sqlite:///{config_path}/config.db', connect_args={'check_same_thread': False})
    Base.metadata.create_all(cdb)
    Base.metadata.bind = cdb
    DBSession = sessionmaker(bind=cdb)


def get_session():
    if DBSession is not None:
        session = DBSession()
        return session
    else:
        return None


class ClassMasters(Base):
    __tablename__ = 'class_masters'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    capacity = Column(Integer)
    start_time = Column(DateTime)


class UserMasters(Base):
    __tablename__ = "user_masters"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class ReservationList(Base):
    __tablename__ = "reservation_list"
    id = Column(Integer, primary_key=True)
    class_id = Column(Integer)
    user_id = Column(Integer)


class WaitingList(Base):
    __tablename__ = "waiting_list"
    id = Column(Integer, primary_key=True)
    class_id = Column(Integer)
    user_id = Column(Integer)
