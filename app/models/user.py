from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from backend.db import Base


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'keep_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    slag = Column(String, unique=True)
    tasks = relationship('Task', back_populates='user')


# from sqlalchemy.schema import CreateTable
#
# print(CreateTable(User.__table__))
