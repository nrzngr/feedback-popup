from sqlalchemy.ext.asyncio import (
    create_async_engine,
)  # Import create_async_engine for creating an asynchronous database engine
from sqlalchemy.orm import (
    DeclarativeBase,
)  # Import DeclarativeBase for defining SQLAlchemy models
from dotenv import (
    load_dotenv,
)  # Import load_dotenv for loading environment variables from a .env file
import os  # Import os for interacting with the operating system

load_dotenv()  # Load environment variables from a .env file (if present)

# Get the database URL from the environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Create an asynchronous database engine using the provided URL
engine = create_async_engine(
    url=DATABASE_URL, echo=True
)  # Echo=True enables logging of SQL statements


# Define a base class for SQLAlchemy models
class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.

    This class provides a foundation for defining database tables using SQLAlchemy's declarative approach.
    It inherits from DeclarativeBase, which provides the necessary functionality for mapping Python classes
    to database tables.
    """

    pass
