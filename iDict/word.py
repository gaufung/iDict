"""
The class of word using SQLAlchemy orm framework
"""
from sqlalchemy import Column, DateTime, Text, Integer, func, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Word(Base):
    __tablename__ = 'word'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    lookup_on = Column(DateTime, default=func.now())
    priority = Column(Integer, default=1)

    def __str__(self):
        return '{}:{}'.format(self.name, self.priority)


class Explain(Base):
    __tablename__ = 'explain'
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    word_id = Column(Integer, ForeignKey('word.id'))
    word = relationship(
        Word,
        backref=backref('explains',
                        uselist=True,
                        cascade='delete,all')
    )


class Sentence(Base):
    __tablename__ = 'sentence'
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    word_id = Column(Integer, ForeignKey('word.id'))
    word = relationship(
        Word,
        backref=backref('sentences',
                        uselist=True,
                        cascade='delete,all')
    )
