from db import Base
from sqlalchemy import Column, Integer, String, Text, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func

class Feedback(Base):
    """Represents feedback data."""

    __tablename__ = "feedback"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    rating: Mapped[int] = mapped_column(nullable=False)

    satisfaction_level = Enum(
        "Very Satisfied",
        "Satisfied",
        "Neutral",
        "Dissatisfied",
        "Very Dissatisfied",
        name="satisfaction_level",
    )

    satisfaction: Mapped[str] = mapped_column(satisfaction_level, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True, default=None)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def __repr__(self):
        """String representation of the Feedback object."""
        return f"<Feedback(id={self.id}, rating={self.rating}, description='{self.description}', satisfaction='{self.satisfaction}', created_at='{self.created_at.isoformat() if self.created_at else None}')>"
