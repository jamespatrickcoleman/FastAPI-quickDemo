import random
from fastapi import APIRouter, HTTPException
from myFastAPI.models import Item, ItemResponse, ItemListResponse, ItemUpdateResponse, ItemDeleteResponse
from myFastAPI.database import items_db

router = APIRouter()

@router.get("/items", response_model=ItemListResponse, tags=['Books API'])
async def get_randomized_items():
    """Retrieve a randomized list of items."""
    randomized_items = items_db.copy()
    random.shuffle(randomized_items)
    return ItemListResponse(
        original_items=items_db,
        randomized_items=randomized_items,
        count=len(items_db)
    )

@router.post("/items", response_model=ItemResponse, tags=['Books API'])
async def add_item(item: Item):
    """Create a new item with a name and optional description."""
    if item.name in items_db:
        raise HTTPException(status_code=400, detail="Item already exists")

    items_db.append(item.name)
    return ItemResponse(
        message="Item added successfully.",
        item=item.name
    )

@router.put("/items/{update_item_name}", response_model=ItemUpdateResponse, tags=['Books API'])
async def update_item(update_item_name: str, item: Item):
    """Update an existing item's name."""
    if update_item_name not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    if item.name in items_db:
        raise HTTPException(status_code=400, detail="An item with the new name already exists")

    index = items_db.index(update_item_name)
    items_db[index] = item.name
    return ItemUpdateResponse(
        message="Item updated successfully.",
        old_name=update_item_name,
        new_name=item.name
    )

@router.delete("/items/{delete_item_name}", response_model=ItemDeleteResponse, tags=['Books API'])
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
