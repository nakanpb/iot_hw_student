from unicodedata import name
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship

from database import Base

class student(Base):
    __tablename__ = 'students'

    name = Column(String, index=True)
    sername = Column(String, index=True)
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, index=True)
    gender = Column(String, index=True)

