import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI
from http import HTTPStatus

from main import app, get_satisfaction_level
from db import Base, engine, async_session  
from models import Feedback

# Create a test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://user:password@host:port/test_database"

@pytest.fixture(scope="session")
def event_loop():
    """Force event loop to be the main loop."""
    import asyncio

    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def create_test_database():
    """Create a clean test database for each test session."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client(create_test_database):
    """Create an HTTP client for testing."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_get_all_feedback_empty(client: AsyncClient):
    """Test GET /feedback when no feedback exists."""
    response = await client.get("/feedback")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == []

@pytest.mark.asyncio
async def test_create_feedback(client: AsyncClient):
    """Test POST /feedback to create a new feedback entry."""
    data = {"rating": 4, "description": "Good service!"}
    response = await client.post("/feedback", json=data)
    assert response.status_code == HTTPStatus.CREATED
    json_response = response.json()
    assert json_response["rating"] == data["rating"]
    assert json_response["description"] == data["description"]
    assert json_response["satisfaction"] == "Satisfied"
    assert "id" in json_response
    assert "created_at" in json_response

@pytest.mark.asyncio
async def test_get_all_feedback(client: AsyncClient):
    """Test GET /feedback after creating feedback entries."""
    # Create some feedback entries
    await client.post("/feedback", json={"rating": 5, "description": "Excellent!"})
    await client.post("/feedback", json={"rating": 3, "description": "Okay."})
    
    # Get all feedback
    response = await client.get("/feedback")
    assert response.status_code == HTTPStatus.OK
    feedback_entries = response.json()
    assert len(feedback_entries) == 3

@pytest.mark.asyncio
async def test_get_feedback_by_id(client: AsyncClient):
    """Test GET /feedback/{feedback_id} to retrieve a specific entry."""
    # Create a feedback entry
    create_response = await client.post(
        "/feedback", json={"rating": 2, "description": "Not bad."}
    )
    feedback_id = create_response.json()["id"]

    # Get the feedback by ID
    response = await client.get(f"/feedback/{feedback_id}")
    assert response.status_code == HTTPStatus.OK
    json_response = response.json()
    assert json_response["id"] == feedback_id
    assert json_response["rating"] == 2
    assert json_response["description"] == "Not bad."
    assert json_response["satisfaction"] == "Neutral" 

@pytest.mark.asyncio
async def test_get_feedback_not_found(client: AsyncClient):
    """Test GET /feedback/{feedback_id} for a non-existent ID."""
    response = await client.get("/feedback/999999")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Feedback not found"}

@pytest.mark.asyncio
async def test_delete_feedback_by_id(client: AsyncClient):
    """Test DELETE /feedback/{feedback_id} to delete a specific entry."""
    # Create a feedback entry
    create_response = await client.post(
        "/feedback", json={"rating": 1, "description": "Terrible."}
    )
    feedback_id = create_response.json()["id"]

    # Delete the feedback by ID
    response = await client.delete(f"/feedback/{feedback_id}")
    assert response.status_code == HTTPStatus.NO_CONTENT

    # Try to get the deleted feedback
    response = await client.get(f"/feedback/{feedback_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND

@pytest.mark.asyncio
async def test_update_feedback_by_id(client: AsyncClient):
    """Test PUT /feedback/{feedback_id} to update a specific entry."""
    # Create a feedback entry
    create_response = await client.post(
        "/feedback", json={"rating": 3, "description": "It's okay."}
    )
    feedback_id = create_response.json()["id"]

    # Update the feedback
    updated_data = {"rating": 5, "description": "Much better now!"}
    response = await client.put(f"/feedback/{feedback_id}", json=updated_data)
    assert response.status_code == HTTPStatus.OK
    json_response = response.json()
    assert json_response["id"] == feedback_id
    assert json_response["rating"] == 5
    assert json_response["description"] == "Much better now!"
    assert json_response["satisfaction"] == "Very Satisfied" 

@pytest.mark.asyncio
async def test_update_feedback_not_found(client: AsyncClient):
    """Test PUT /feedback/{feedback_id} for a non-existent ID."""
    response = await client.put("/feedback/999999", json={"rating": 5, "description": "Test"})
    assert response.status_code == HTTPStatus.NOT_FOUND

def test_get_satisfaction_level():
    assert get_satisfaction_level(5) == "Very Satisfied"
    assert get_satisfaction_level(4) == "Satisfied"
    assert get_satisfaction_level(3) == "Satisfied"
    assert get_satisfaction_level(2) == "Neutral"
    assert get_satisfaction_level(1) == "Very Dissatisfied"
    with pytest.raises(ValueError):
        get_satisfaction_level(6)  # Invalid rating
