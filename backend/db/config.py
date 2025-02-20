from sqlmodel import create_engine, Session, SQLModel
from .seed import seed_posts

SQLITE_FILE_NAME = "database.db"
SQLITE_URL = f"sqlite:///{SQLITE_FILE_NAME}"

engine = create_engine(SQLITE_URL, echo=True)

def init_db():
    """Creates all database tables based on SQLModel definitions and seeds initial data"""
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        seed_posts(session)

def get_session():
    """
    Creates a new database session for each request and closes it afterwards.
    This dependency will handle the lifecycle of the database session,
    ensuring proper cleanup of resources.
    Yields:
        Session: SQLModel database session
    """
    with Session(engine) as session:
        yield session 