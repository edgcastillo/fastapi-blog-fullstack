from datetime import datetime
from sqlmodel import Session, select
from post.models import Post
from sqlalchemy import select

def seed_posts(session: Session) -> None:
    """
    Seeds the database with initial posts if they don't exist.
    """
    # Check if we already have posts
    if session.exec(select(Post)).first():
        return

    # Create sample posts
    sample_posts = [
        Post(
            title="Welcome to FastAPI",
            description="Getting started with FastAPI and SQLModel",
            content="""FastAPI is a modern web framework for building APIs with Python. It's known for its high performance, 
            automatic API documentation, and type checking. Combined with SQLModel, you get a powerful toolkit for building 
            robust web applications. This framework is built on top of Starlette and Pydantic, providing excellent 
            performance and data validation out of the box. Whether you're building a small API or a large-scale 
            application, FastAPI's intuitive design and comprehensive features make it an excellent choice.""",
            created_at=datetime(2024, 1, 1, 12, 0)
        ),
        Post(
            title="Repository Pattern",
            description="Understanding the Repository Design Pattern",
            content="""The repository pattern is a design pattern that isolates the data layer from the rest of the app. 
            It acts as an abstraction layer between business logic and data access logic. This separation of concerns makes 
            your code more maintainable and testable. The pattern provides a more object-oriented view of the persistence 
            layer, encapsulating the data access logic and allowing the business logic to be agnostic of the underlying 
            data source. This makes it easier to modify the data persistence implementation without affecting the business 
            logic.""",
            created_at=datetime(2024, 1, 2, 14, 30)
        ),
        Post(
            title="Database Management",
            description="Best practices for database management",
            content="""When working with databases, it's important to consider several key aspects: performance, security, 
            and maintainability. Always use connection pooling to manage database connections efficiently. Implement proper 
            indexing strategies to optimize query performance. Regular backups and monitoring are crucial for data safety. 
            Use migrations to manage database schema changes, and always validate data before it reaches your database. 
            Consider implementing caching strategies for frequently accessed data, and ensure your database queries are 
            optimized for performance.""",
            created_at=datetime(2024, 1, 3, 9, 45)
        )
    ]

    # Add posts to database
    for post in sample_posts:
        session.add(post)
    
    session.commit() 