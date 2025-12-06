from pydantic import BaseModel, Field
from typing import Optional

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
