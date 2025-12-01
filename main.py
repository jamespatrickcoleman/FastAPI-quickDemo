import random

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, Annotated

app = FastAPI()

books = [
    {"id": 1, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
    {"id": 3, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"}, 
]

items_db = []

class Book(BaseModel):
    title: str
    author: str

class Item(BaseModel):
    name: str = Field(
        ..., 
        title="Item Name", 
        description="The name of the item",
        min_length=1,    
        max_length=100
    )
    description: Optional[str] = Field(None, title="Item Description", description="A brief description of the item")

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

@app.get("/items")
def get_randomized_items():
    """Retrieve a randomized list of items."""
    randomized_items = items_db.copy()
    random.shuffle(randomized_items)
    return {
        "original_items": items_db,
        "items": randomized_items,
        "count": len(items_db)
    }

@app.post("/items")
def add_item(body: dict):
    """Create a new item with a name and optional description."""
    # item_name = body.get("name")
    # if not item_name:
    #     raise HTTPException(status_code=400, detail="Item 'name' is required")

    if item_name in items_db:
        raise HTTPException(status_code=400, detail="Item already exists")

    items_db.append(item_name)
    return {'message': f"Item '{item_name}' added successfully."}

@app.put("/items/{update_item_name}")
def update_item(update_item_name: str, item: Item):
    """Update an existing item's name."""
    if update_item_name not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    # new_name = body.get("name")
    # if not new_name:
    #     raise HTTPException(status_code=400, detail="New item 'name' is required")
    if item.name in items_db:
        raise HTTPException(status_code=400, detail="An item with the new name already exists")

    index = items_db.index(update_item_name)
    items_db[index] = item.name
    return {'message': f"Item '{update_item_name}' updated to '{item.name}' successfully."}

@app.delete("/items/{delete_item_name}")
def delete_item(delete_item_name: str):
    """Delete an item by its name."""
    if delete_item_name not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    items_db.remove(delete_item_name)
    return {'message': f"Item '{delete_item_name}' deleted successfully."}

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