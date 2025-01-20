from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from backend.db import Base
from models import *


class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = {'keep_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    priority = Column(Integer)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    slug = Column(String, unique=True, index=True)
    user = relationship('User', back_populates='tasks')


# from sqlalchemy.schema import CreateTable
#
# print(CreateTable(Task.__table__))
