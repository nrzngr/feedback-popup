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
    """CRUD operations for the Feedback model."""

    async def get_all_feedback(self, session: AsyncSession):
        """Retrieves all feedback entries, ordered by creation timestamp."""
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
        """Adds a new feedback entry to the database."""
        session.add(feedback)  # Add the feedback object to the session
        await session.commit()  # Commit the changes to the database
        await session.refresh(
            feedback
        )  # Refresh the feedback object to get the newly assigned ID
        return feedback

    async def get_by_id(self, session: AsyncSession, feedback_id: int):
        """Retrieves a feedback entry by its ID."""
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
        """Deletes a feedback entry by its ID."""
        query = delete(Feedback).where(
            Feedback.id == feedback_id
        )  # Create a DELETE query, filtering by ID
        # Execute the query using the provided session
        await session.execute(query)
        await session.commit()  # Commit the changes to the database

    async def update_by_id(
        self, session: AsyncSession, feedback_id: int, feedback: Feedback
    ):
        """Updates a feedback entry by its ID."""
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
        # Execute the query using the provided session
        await session.execute(query)
        await session.commit()  # Commit the changes to the database
