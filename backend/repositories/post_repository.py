from sqlmodel import Session, select
from post.models import Post, PostCreate, PostUpdate
from fastapi import HTTPException

"""
Repository Pattern Implementation for Post Entity

The Repository pattern is an abstraction layer between the business logic and data storage.
Key benefits:
- Separates data access logic from business logic
- Makes the code more maintainable and testable
- Provides a consistent interface for data operations
- Encapsulates the data access implementation details
"""
class PostRepository:
    def __init__(self, session: Session):
        """Initialize repository with a database session"""
        self.session = session

    # Each method represents an atomic operation on the Post entity
    def get_all(self) -> list[Post]:
        """Retrieves all posts from the database"""
        statement = select(Post)
        return self.session.exec(statement).all()

    def get_by_id(self, post_id: int) -> Post:
        """Retrieves a single post by its ID, raising 404 if not found"""
        statement = select(Post).where(Post.id == post_id)
        post = self.session.exec(statement).first()
        if not post:
            raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
        return post

    def create(self, post_create: PostCreate) -> Post:
        """Creates a new post in the database"""
        post = Post.model_validate(post_create)
        self.session.add(post)
        self.session.commit()
        self.session.refresh(post)
        return post

    def update(self, post_id: int, post_update: PostUpdate) -> Post:
        """Updates an existing post with partial data"""
        post = self.get_by_id(post_id)
        
        update_data = post_update.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No update data provided")

        for key, value in update_data.items():
            setattr(post, key, value)

        self.session.add(post)
        self.session.commit()
        self.session.refresh(post)
        return post

    def delete(self, post_id: int) -> None:
        """Deletes a post from the database"""
        post = self.get_by_id(post_id)
        self.session.delete(post)
        self.session.commit() 