from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated, List
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware


class PostBase(BaseModel):
    # Annotated is used to add validation and metadata to the field
    title: Annotated[str, Field(min_length=1, max_length=50)]
    description: Annotated[str, Field(min_length=1, max_length=100)]
    content: Annotated[str, Field(min_length=1)]

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: Annotated[int, Field(gt=0)]
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "My First Post",
                "description": "A brief description",
                "content": "The full content...",
                "created_at": "2024-02-12T10:00:00"
            }
        }

class PostUpdate(PostBase):
    title: Annotated[str, Field(min_length=1, max_length=50)] | None = None
    description: Annotated[str, Field(min_length=1, max_length=100)] | None = None
    content: Annotated[str, Field(min_length=1)] | None = None


# Create a list of sample posts
posts = [
    Post(
        id=1,
        title="First Post",
        description="This is my first post",
        content="Content of the first post"
    ),
    Post(
        id=2,
        title="Second Post",
        description="This is my second post",
        content="Content of the second post"
    )
]

def generate_new_post_id() -> int:
    if not posts:
        return 1
    return max(p.id for p in posts) + 1

def find_post_by_id(id: int) -> Post | None:
    # generator that will return the first post that matches the id
    return next((post for post in posts if post.id == id), None)

app = FastAPI()

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
)
@app.get("/")
def root():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/posts", response_model=List[Post])
async def get_posts():
    return posts

@app.get("/posts/{post_id}", response_model=Post)
async def get_post(post_id: int):
    post = find_post_by_id(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
    return post

@app.post("/posts", response_model=Post, status_code=201)
async def create_post(post: PostCreate):
    new_id = generate_new_post_id()
    new_post = Post(id=new_id, **post.model_dump())
    posts.append(new_post)
    return new_post

@app.delete("/posts/{post_id}", status_code=204)
async def delete_post(post_id: int):
    post = find_post_by_id(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
    posts.remove(post)
    return {"message": "Post deleted successfully"}

@app.patch("/posts/{post_id}", response_model=Post, description="Update a post by ID with partial data")
async def update_post(post_id: int, post_update: PostUpdate):
    post_to_update = find_post_by_id(post_id)
    if post_to_update is None:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
    try:
        # create a dictionary of the update data
        update_data = post_update.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No update data provided")

        # Create a new post with updated data while preserving the original
        new_post = post_to_update.model_dump()
        new_post.update(update_data)

        # Create Post instance
        updated_post = Post(**new_post)
        
        # Replace the old post with the new one
        posts[posts.index(post_to_update)] = updated_post
        return updated_post
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Error updating post: {e}")

