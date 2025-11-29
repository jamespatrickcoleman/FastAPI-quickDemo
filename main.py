import random

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel 
from typing import Optional, Annotated

app = FastAPI()

books = [
    {"id": 1, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
    {"id": 3, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"}, 
]

class Book(BaseModel):
    title: str
    author: str


@app.get("/")
def home():
    """Home endpoint returning a welcome message."""
    return {"message": "Welcome the Randomizer API!"}

@app.get("/random/{max_value}")
def get_random_number(max_value: int):
    """Generate a random number between 1 and max_value."""
    return {
        "max": max_value,
        "random_number": random.randint(1, max_value)
    }
    

@app.get("/random-between")
def get_random_number_between(
    max_value: Annotated[int, Query(
        title="Maximum Value",
        description="The upper limit for the random number generation",
        ge=1,
        le=1000
    )]= 99,
    min_value: Annotated[int, Query(
        title="Minimum Value",
        description="The lower limit for the random number generation",
        ge=1,
        le=1000
    )]= 1):
    """Generate a random number between min_value and max_value."""
    if min_value >= max_value:
        raise HTTPException(status_code=400, detail="min_value must be less than max_value")
    return {
        "min": min_value,
        "max": max_value,
        "random_number": random.randint(min_value, max_value)
    }


@app.get("/books")
def get_books(limit: Optional[int] = None):
    """Retrieve a list of books, optionally limited by the 'limit' query parameter."""
    if limit:
        return {"books": books[:limit]}
    return {"books": books}


@app.get("/book/{book_id}")
def get_book(book_id: int):
    """Retrieve a book by its ID."""
    for book in books:
        if book["id"] == book_id:
            return book 
    return {"error": 'Book not found'}, 404

@app.post("/books")
def create_book(book: Book):
    """Add a new book to the collection."""
    new_book = {"id": len(books) + 1, "title": book.title, "author": book.author}
    books.append(new_book)
    return new_book