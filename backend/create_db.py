from db import Base, engine  # Import the Base class and engine from the 'db' module
import asyncio  # Import asyncio for asynchronous operations


async def create_db():
    """
    Creates the database tables if they don't exist.

    This function drops all existing tables and then creates the tables defined in the models.
    It uses the SQLAlchemy engine to connect to the database and execute the necessary SQL commands.
    """
    async with engine.begin() as conn:  # Create a connection context manager to ensure proper connection handling
        from models import (
            Feedback,
        )  # Import the Feedback model from the 'models' module

        await conn.run_sync(Base.metadata.drop_all)  # Drop all existing tables (if any)
        await conn.run_sync(
            Base.metadata.create_all
        )  # Create all tables defined in the models

    await engine.dispose()  # Dispose of the engine to release resources


asyncio.run(create_db())  # Run the create_db function asynchronously
