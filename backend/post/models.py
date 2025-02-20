from sqlmodel import Field, SQLModel
from typing import Annotated
from datetime import datetime

class PostBase(SQLModel):
    # Annotated is used to add validation and metadata to the field
    title: Annotated[str, Field(min_length=1, max_length=50)]
    description: Annotated[str, Field(min_length=1, max_length=100)]
    content: Annotated[str, Field(min_length=1)]

class PostCreate(PostBase):
    pass

class Post(PostBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
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