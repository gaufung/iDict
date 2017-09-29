"""
The class of word using SQLAlchemy orm framework
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Text

Base = declarative_base()


class Word(Base):
    __tablename__ = 'word'

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    chinese = Column(String, nullable=False)
    sentence = Column(String)

