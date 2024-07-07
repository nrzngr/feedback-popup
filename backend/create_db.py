from db import Base, engine
import asyncio

async def create_db():
    """Creates database tables if they don't exist."""
    async with engine.begin() as conn:
        from models import Feedback
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()

asyncio.run(create_db())
