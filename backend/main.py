from fastapi import FastAPI, HTTPException
from sqlalchemy.ext.asyncio import async_sessionmaker
from db import engine  # Import the database engine from the 'db' module
from crud import CRUD  # Import the CRUD class from the 'crud' module
from schemas import (
    FeedbackModel,
    FeedbackCreateModel,
)  # Import Pydantic models for data validation and serialization
from typing import List  # Import List for type hinting
from models import Feedback  # Import the Feedback model
from http import HTTPStatus  # Import HTTPStatus for status codes

app = FastAPI(
    title="Feedback API", description="This is a simple feedback form API", docs_url="/"
)

async_session = async_sessionmaker(
    bind=engine,  # Bind the session to the database engine
    expire_on_commit=False,  # Disable automatic expiration of objects after commit
)

db = CRUD()  # Create an instance of the CRUD class


@app.get("/feedback", response_model=List[FeedbackModel])
async def get_all_feedback():
    """
    Retrieves all feedback entries from the database.

    This endpoint returns a list of all feedback entries, ordered by creation timestamp.

    Returns:
        List[FeedbackModel]: A list of FeedbackModel objects representing all feedback entries.
    """
    async with async_session() as session:  # Create a session context manager for database operations
        feedbacks = await db.get_all_feedback(
            session
        )  # Call the get_all_feedback method from the CRUD class
    return feedbacks


@app.post("/feedback", status_code=HTTPStatus.CREATED, response_model=FeedbackModel)
async def create_feedback(feedback_data: FeedbackCreateModel):
    """
    Creates a new feedback entry in the database.

    This endpoint receives feedback data from the client, validates it, maps the rating to a satisfaction level,
    and then adds the new feedback entry to the database.

    Args:
        feedback_data (FeedbackCreateModel): The feedback data received from the client.

    Returns:
        FeedbackModel: The newly created feedback entry, including its ID and other details.
    """
    async with async_session() as session:  # Create a session context manager for database operations
        new_feedback = Feedback(
            rating=feedback_data.rating,  # Set the rating from the received data
            description=feedback_data.description,  # Set the description from the received data
            satisfaction=get_satisfaction_level(
                feedback_data.rating
            ),  # Map the rating to a satisfaction level
        )
        feedback = await db.add(
            session, new_feedback
        )  # Add the new feedback entry to the database using the CRUD class
    return feedback


@app.get("/feedback/{feedback_id}", response_model=FeedbackModel)
async def get_feedback_by_id(feedback_id: int):
    """
    Retrieves a feedback entry by its ID.

    This endpoint fetches a specific feedback entry from the database based on the provided ID.

    Args:
        feedback_id (int): The ID of the feedback entry to retrieve.

    Returns:
        FeedbackModel: The feedback entry with the specified ID, or raises a 404 Not Found error if not found.
    """
    async with async_session() as session:  # Create a session context manager for database operations
        feedback = await db.get_by_id(
            session, feedback_id
        )  # Retrieve the feedback entry using the CRUD class
        if not feedback:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Feedback not found"
            )  # Raise a 404 Not Found error if the feedback is not found
    return feedback


@app.delete("/feedback/{feedback_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_feedback_by_id(feedback_id: int):
    """
    Deletes a feedback entry by its ID.

    This endpoint removes a feedback entry from the database based on the provided ID.

    Args:
        feedback_id (int): The ID of the feedback entry to delete.
    """
    async with async_session() as session:  # Create a session context manager for database operations
        await db.delete_by_id(
            session, feedback_id
        )  # Delete the feedback entry using the CRUD class


@app.put("/feedback/{feedback_id}", response_model=FeedbackModel)
async def update_feedback_by_id(feedback_id: int, feedback_data: FeedbackCreateModel):
    """
    Updates a feedback entry by its ID.

    This endpoint updates an existing feedback entry in the database based on the provided ID and new data.

    Args:
        feedback_id (int): The ID of the feedback entry to update.
        feedback_data (FeedbackCreateModel): The updated feedback data.

    Returns:
        FeedbackModel: The updated feedback entry.
    """
    async with async_session() as session:  # Create a session context manager for database operations
        feedback = await db.get_by_id(
            session, feedback_id
        )  # Retrieve the feedback entry using the CRUD class
        if not feedback:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Feedback not found"
            )  # Raise a 404 Not Found error if the feedback is not found
        feedback.rating = feedback_data.rating  # Update the rating
        feedback.description = feedback_data.description  # Update the description
        feedback.satisfaction = get_satisfaction_level(
            feedback_data.rating
        )  # Update the satisfaction level
        await db.update_by_id(
            session, feedback_id, feedback
        )  # Update the feedback entry in the database using the CRUD class
    return feedback


def get_satisfaction_level(rating: int) -> str:
    """
    Maps a rating to a satisfaction level.

    This function takes a rating value and returns the corresponding satisfaction level based on the defined mapping.

    Args:
        rating (int): The rating value.

    Returns:
        str: The satisfaction level corresponding to the rating.

    Raises:
        ValueError: If the rating is invalid (not between 1 and 5).
    """
    if rating == 5:
        return "Very Satisfied"
    elif rating in (4, 3):
        return "Satisfied"
    elif rating == 2:
        return "Neutral"
    elif rating == 1:
        return "Very Dissatisfied"
    else:
        raise ValueError("Invalid rating")
