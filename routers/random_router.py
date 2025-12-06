import random
from typing import Annotated
from fastapi import APIRouter, HTTPException, Query

router = APIRouter()

@router.get("/", tags=["Random API Practice"])
async def home():
    """Home endpoint returning a welcome message."""
    return {"message": "Welcome the Randomizer API!"}

@router.get("/random/{max_value}", tags=["Random API Practice"])
async def get_random_number(max_value: int):
    """Generate a random number between 1 and max_value."""
    return {
        "max": max_value,
        "random_number": random.randint(1, max_value)
    }
    

@router.get("/random-between", tags=["Random API Practice"])
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
