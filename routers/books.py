from typing import Optional
from fastapi import APIRouter
from myFastAPI.models import Book
from myFastAPI.database import books

router = APIRouter()

@router.get("/books", tags=["Books API"])
async def get_books(limit: Optional[int] = None):
    """Retrieve a list of books, optionally limited by the 'limit' query parameter."""
    if limit:
        return {"books": books[:limit]}
    return {"books": books}

@router.get("/book/{book_id}", tags=["Books API"])
async def get_book(book_id: int):
    """Retrieve a book by its ID."""
    for book in books:
        if book["id"] == book_id:
            return book 
    return {"error": 'Book not found'}, 404

@router.post("/books", tags=["Books API"])
async def create_book(book: Book):
    """Add a new book to the collection."""
    new_book = {"id": len(books) + 1, "title": book.title, "author": book.author}
    books.append(new_book)
    return new_book
