from db import Base  # Import the Base class from the 'db' module
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Enum,
    DateTime,
)  # Import SQLAlchemy data types
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)  # Import Mapped and mapped_column for SQLAlchemy declarative mappings
from sqlalchemy import func  # Import func for using database functions like 'now()'


class Feedback(Base):
    """
    SQLAlchemy model representing feedback data.

    This class defines the structure of the 'feedback' table in the database.
    It maps Python attributes to database columns and provides a string representation
    for the Feedback object.
    """

    __tablename__ = "feedback"  # Define the table name in the database
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )  # Define the primary key column (integer, auto-incrementing)
    rating: Mapped[int] = mapped_column(
        nullable=False
    )  # Define the rating column (integer, not nullable)

    # Define the satisfaction level enum
    satisfaction_level = Enum(
        "Very Satisfied",
        "Satisfied",
        "Neutral",
        "Dissatisfied",
        "Very Dissatisfied",
        name="satisfaction_level",  # Give the enum a name for use in the database
    )

    # Add the satisfaction level column
    satisfaction: Mapped[str] = mapped_column(
        satisfaction_level, nullable=False
    )  # Define the satisfaction column (enum type, not nullable)
    description: Mapped[str] = mapped_column(
        Text, nullable=True
    )  # Define the description column (text, nullable)

    # Add datetime column
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),  # Define the creation timestamp column (datetime with timezone, default to current timestamp)
    )

    def __repr__(self):
        """
        String representation of the Feedback object.

        Returns:
            str: A string representation of the Feedback object, including its attributes.
        """
        return f"<Feedback(id={self.id}, rating={self.rating}, description='{self.description}', satisfaction='{self.satisfaction}', created_at='{self.created_at.isoformat() if self.created_at else None}')>"
