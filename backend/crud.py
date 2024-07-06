from models import Feedback  # Import the Feedback model
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)  # Import AsyncSession for asynchronous database operations
from sqlalchemy import (
    select,
    update,
    delete,
)  # Import SQLAlchemy functions for database queries


class CRUD:
    """
    CRUD (Create, Read, Update, Delete) operations for the Feedback model.

    This class provides methods for interacting with the Feedback table in the database.
    """

    async def get_all_feedback(self, session: AsyncSession):
        """
        Retrieves all feedback entries from the database, ordered by creation timestamp.

        Args:
            session (AsyncSession): An asynchronous database session.

        Returns:
            list: A list of Feedback objects representing all feedback entries.
        """
        query = select(Feedback).order_by(
            Feedback.created_at
        )  # Create a SELECT query, ordered by creation timestamp
        result = await session.execute(
            query
        )  # Execute the query using the provided session
        return (
            result.scalars().all()
        )  # Return all results as a list of Feedback objects

    async def add(self, session: AsyncSession, feedback: Feedback):
        """
        Adds a new feedback entry to the database.

        Args:
            session (AsyncSession): An asynchronous database session.
            feedback (Feedback): The Feedback object to be added.

        Returns:
            Feedback: The newly added Feedback object, including the assigned ID.
        """
        session.add(feedback)  # Add the feedback object to the session
        await session.commit()  # Commit the changes to the database
        await session.refresh(
            feedback
        )  # Refresh the feedback object to get the newly assigned ID
        return feedback

    async def get_by_id(self, session: AsyncSession, feedback_id: int):
        """
        Retrieves a feedback entry by its ID.

        Args:
            session (AsyncSession): An asynchronous database session.
            feedback_id (int): The ID of the feedback entry to retrieve.

        Returns:
            Feedback: The Feedback object with the specified ID, or None if not found.
        """
        query = select(Feedback).filter(
            Feedback.id == feedback_id
        )  # Create a SELECT query, filtering by ID
        result = await session.execute(
            query
        )  # Execute the query using the provided session
        return (
            result.scalars().first()
        )  # Return the first result (or None if not found)

    async def delete_by_id(self, session: AsyncSession, feedback_id: int):
        """
        Deletes a feedback entry by its ID.

        Args:
            session (AsyncSession): An asynchronous database session.
            feedback_id (int): The ID of the feedback entry to delete.
        """
        query = delete(Feedback).where(
            Feedback.id == feedback_id
        )  # Create a DELETE query, filtering by ID
        await session.execute(query)  # Execute the query using the provided session
        await session.commit()  # Commit the changes to the database

    async def update_by_id(
        self, session: AsyncSession, feedback_id: int, feedback: Feedback
    ):
        """
        Updates a feedback entry by its ID.

        Args:
            session (AsyncSession): An asynchronous database session.
            feedback_id (int): The ID of the feedback entry to update.
            feedback (Feedback): The updated Feedback object.
        """
        query = (
            update(Feedback)
            .where(
                Feedback.id == feedback_id
            )  # Create an UPDATE query, filtering by ID
            .values(
                rating=feedback.rating,  # Set the new rating value
                description=feedback.description,  # Set the new description value
                satisfaction=feedback.satisfaction,  # Set the new satisfaction value
            )
        )
        await session.execute(query)  # Execute the query using the provided session
        await session.commit()  # Commit the changes to the database
