from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from uuid import uuid4, UUID
import sqlite3

Base = declarative_base()
engine = create_engine('sqlite:///./test.db', echo=True)
SessionLocal = sessionmaker(bind=engine)

class BookDB(Base):
    __tablename__ = 'books'
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    title = Column(String)
    author = Column(String)
    publication_year = Column(Integer)
    reviews = relationship("ReviewDB", back_populates="book")

class ReviewDB(Base):
    __tablename__ = 'reviews'
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    book_id = Column(String, ForeignKey('books.id'))
    text = Column(String)
    rating = Column(Integer)
    book = relationship("BookDB", back_populates="reviews")

Base.metadata.create_all(bind=engine)
