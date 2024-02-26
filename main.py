from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import uuid4, UUID
from fastapi import BackgroundTasks

app = FastAPI()

# Pydantic models
class Book(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    author: str
    publication_year: int

class Review(BaseModel):
    book_id: UUID
    text: str
    rating: int

# In-memory storage
books = []
reviews = []



def send_confirmation_email(review: Review):
    print(f"Sending confirmation email for review: {review.text}")

@app.post("/books/", response_model=Book)
def add_book(book: Book):
    books.append(book)
    return book

# @app.post("/reviews/", response_model=Review)
# def submit_review(review: Review):
#     reviews.append(review)
#     return review

@app.post("/reviews/", response_model=Review)
def submit_review(review: Review, background_tasks: BackgroundTasks):
    reviews.append(review)
    background_tasks.add_task(send_confirmation_email, review)
    return review

@app.get("/books/", response_model=List[Book])
def get_books(author: Optional[str] = None, publication_year: Optional[int] = None):
    if author:
        return [book for book in books if book.author == author]
    if publication_year:
        return [book for book in books if book.publication_year == publication_year]
    return books

@app.get("/reviews/{book_id}", response_model=List[Review])
def get_reviews_for_book(book_id: UUID):
    return [review for review in reviews if review.book_id == book_id]
