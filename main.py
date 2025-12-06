from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from myFastAPI.routers import random_router, items, books

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

app.include_router(random_router.router)
app.include_router(items.router)
app.include_router(books.router)
