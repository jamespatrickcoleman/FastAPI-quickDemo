from fastapi import FastAPI
from pydantic import BaseModel 
from typing import Optional

app = FastAPI()

books = [
    {"id": 1, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
    {"id": 3, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"}, 
]

class Book(BaseModel):
    title: str
    author: str
    

@app.get("/books")
def get_books(limit: Optional[int] = None):
    """Retrieve a list of books, optionally limited by the 'limit' query parameter."""
    if limit:
        return {"books": books[:limit]}
    return {"books": books}


@app.get("/books/{book_id}")
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