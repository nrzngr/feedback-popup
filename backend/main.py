from fastapi import FastAPI, HTTPException
from sqlalchemy.ext.asyncio import async_sessionmaker
from db import engine
from crud import CRUD
from schemas import FeedbackModel, FeedbackCreateModel
from typing import List
from models import Feedback
from http import HTTPStatus
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Feedback API", description="Simple feedback form API", docs_url="/"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Allow requests from frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

async_session = async_sessionmaker(
    bind=engine, expire_on_commit=False
)

db = CRUD()


@app.get("/feedback", response_model=List[FeedbackModel])
async def get_all_feedback():
    """Retrieves all feedback entries."""
    async with async_session() as session:
        feedbacks = await db.get_all_feedback(session)
    return feedbacks


@app.post("/feedback", status_code=HTTPStatus.CREATED, response_model=FeedbackModel)
async def create_feedback(feedback_data: FeedbackCreateModel):
    """Creates a new feedback entry."""
    async with async_session() as session:
        new_feedback = Feedback(
            rating=feedback_data.rating,
            description=feedback_data.description,
            satisfaction=get_satisfaction_level(feedback_data.rating),
        )
        feedback = await db.add(session, new_feedback)
    return feedback


@app.get("/feedback/{feedback_id}", response_model=FeedbackModel)
async def get_feedback_by_id(feedback_id: int):
    """Retrieves a feedback entry by ID."""
    async with async_session() as session:
        feedback = await db.get_by_id(session, feedback_id)
        if not feedback:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Feedback not found"
            )
    return feedback


@app.delete("/feedback/{feedback_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_feedback_by_id(feedback_id: int):
    """Deletes a feedback entry by ID."""
    async with async_session() as session:
        await db.delete_by_id(session, feedback_id)


@app.put("/feedback/{feedback_id}", response_model=FeedbackModel)
async def update_feedback_by_id(feedback_id: int, feedback_data: FeedbackCreateModel):
    """Updates a feedback entry by ID."""
    async with async_session() as session:
        feedback = await db.get_by_id(session, feedback_id)
        if not feedback:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Feedback not found"
            )
        feedback.rating = feedback_data.rating
        feedback.description = feedback_data.description
        feedback.satisfaction = get_satisfaction_level(feedback_data.rating)
        await db.update_by_id(session, feedback_id, feedback)
    return feedback


def get_satisfaction_level(rating: int) -> str:
    """Maps a rating to a satisfaction level."""
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
