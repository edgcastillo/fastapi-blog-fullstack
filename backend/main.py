from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session

from post.models import Post, PostCreate, PostUpdate
from db.config import get_session
from repositories.post_repository import PostRepository
from db.config import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown events"""
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

# CORS configuration
origins = [
    "http://localhost:5173",
    "https://localhost:5173",
    "http://localhost",
    "https://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoints
@app.get("/ping")
async def ping():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/")
def root():
    return {"status": "healthy", "version": "1.0.0"}

# Post endpoints
@app.get("/posts", response_model=List[Post])
async def get_posts(
    session: Session = Depends(get_session)
):
    repository = PostRepository(session)
    return repository.get_all()

@app.get("/posts/{post_id}", response_model=Post)
async def get_post(
    post_id: int,
    session: Session = Depends(get_session)
):
    repository = PostRepository(session)
    return repository.get_by_id(post_id)

@app.post("/posts", response_model=Post, status_code=201)
async def create_post(
    post: PostCreate,
    session: Session = Depends(get_session)
):
    repository = PostRepository(session)
    return repository.create(post)

@app.patch("/posts/{post_id}", response_model=Post)
async def update_post(
    post_id: int,
    post_update: PostUpdate,
    session: Session = Depends(get_session)
):
    repository = PostRepository(session)
    return repository.update(post_id, post_update)

@app.delete("/posts/{post_id}", status_code=204)
async def delete_post(
    post_id: int,
    session: Session = Depends(get_session)
):
    repository = PostRepository(session)
    repository.delete(post_id)
    return {"message": "Post deleted successfully"}

