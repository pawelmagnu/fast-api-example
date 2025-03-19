from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, constr
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from datetime import date


DATABASE_URL = "postgresql://user:password@db:5432/library_db"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String(6), unique=True, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    is_borrowed = Column(Boolean, default=False)
    borrowed_by = Column(String(6), nullable=True)
    borrowed_date = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library API", version="1.0.0", description="API for managing library books")

class BookCreate(BaseModel):
    serial_number: constr(min_length=6, max_length=6)
    title: str
    author: str

class BookUpdate(BaseModel):
    is_borrowed: bool
    borrowed_by: constr(min_length=6, max_length=6) = None
    borrowed_date: date = None

@app.post("/books/")
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    with db as session:
        db_book = Book(serial_number=book.serial_number, title=book.title, author=book.author)
        session.add(db_book)
        session.commit()
        session.refresh(db_book)
        return db_book

@app.get("/books/")
def get_books(db: Session = Depends(get_db)):
    with db as session:
        return session.query(Book).all()

@app.delete("/books/{serial_number}")
def delete_book(serial_number: str, db: Session = Depends(get_db)):
    with db as session:
        book = session.query(Book).filter(Book.serial_number == serial_number).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        session.delete(book)
        session.commit()
        return {"message": "Book deleted"}

@app.put("/books/{serial_number}")
def update_book(serial_number: str, update_data: BookUpdate, db: Session = Depends(get_db)):
    with db as session:
        book = session.query(Book).filter(Book.serial_number == serial_number).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        book.is_borrowed = update_data.is_borrowed
        book.borrowed_by = update_data.borrowed_by
        book.borrowed_date = update_data.borrowed_date.isoformat() if update_data.borrowed_date else None
        session.commit()
        return book