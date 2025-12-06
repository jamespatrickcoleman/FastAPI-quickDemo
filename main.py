import random

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Annotated

tags_metadata = [
    {
        "name": "Random API Practice",
        "description": "APIs for practic creating python REST APIs.",
    },
    {
        "name": "Books API",
        "description": "APIs for managing a collection of books.",
    }
]

app = FastAPI(
    title="Randomi API",
    description="An API to generate random numbers and manage a collection of items and books.",
    version="1.0.0",
    openapi_tags=tags_metadata
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

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

class ItemResponse(BaseModel):
    message: str
    item: str

class ItemListResponse(BaseModel):
    original_items: list[str]
    randomized_items: list[str]
    count: int

class ItemUpdateResponse(BaseModel):
    message: str
    old_name: str
    new_name: str

class ItemDeleteResponse(BaseModel):
    message: str
    deleted_item: str
    remaining_count: int

@app.get("/", tags=["Random API Practice"])
async def home():
    """Home endpoint returning a welcome message."""
    return {"message": "Welcome the Randomizer API!"}

@app.get("/random/{max_value}", tags=["Random API Practice"])
async def get_random_number(max_value: int):
    """Generate a random number between 1 and max_value."""
    return {
        "max": max_value,
        "random_number": random.randint(1, max_value)
    }
    

@app.get("/random-between", tags=["Random API Practice"])
async def get_random_number_between(
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

@app.get("/items", response_model=ItemListResponse, tags=['Books API'])
async def get_randomized_items():
    """Retrieve a randomized list of items."""
    randomized_items = items_db.copy()
    random.shuffle(randomized_items)
    return ItemListResponse(
        original_items=items_db,
        randomized_items=randomized_items,
        count=len(items_db)
    )


@app.post("/items", response_model=ItemResponse, tags=['Books API'])
async def add_item(item: Item):
    """Create a new item with a name and optional description."""
    if item_name in items_db:
        raise HTTPException(status_code=400, detail="Item already exists")

    items_db.append(item_name)
    return ItemResponse(
        message="Item added successfully.",
        item=item.name
    )

@app.put("/items/{update_item_name}", response_model=ItemUpdateResponse, tags=['Books API'])
async def update_item(update_item_name: str, item: Item):
    """Update an existing item's name."""
    if update_item_name not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    if item.name in items_db:
        raise HTTPException(status_code=400, detail="An item with the new name already exists")

    index = items_db.index(update_item_name)
    items_db[index] = item.name
    return 

@app.delete("/items/{delete_item_name}", response_model=ItemDeleteResponse, tags=['Books API'])
async def delete_item(delete_item_name: str):
    """Delete an item by its name."""
    if delete_item_name not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    items_db.remove(delete_item_name)
    return ItemDeleteResponse(
        message="Item deleted successfully.",
        deleted_item=delete_item_name,
        remaining_count=len(items_db)   
    )

@app.get("/books", tags=["Books API"])
async def get_books(limit: Optional[int] = None):
    """Retrieve a list of books, optionally limited by the 'limit' query parameter."""
    if limit:
        return {"books": books[:limit]}
    return {"books": books}


@app.get("/book/{book_id}", tags=["Books API"])
async def get_book(book_id: int):
    """Retrieve a book by its ID."""
    for book in books:
        if book["id"] == book_id:
            return book 
    return {"error": 'Book not found'}, 404

@app.post("/books", tags=["Books API"])
async def create_book(book: Book):
    """Add a new book to the collection."""
    new_book = {"id": len(books) + 1, "title": book.title, "author": book.author}
    books.append(new_book)
    return new_book