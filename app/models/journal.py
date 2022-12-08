from datetime import datetime
from uuid import UUID,uuid4
from beanie import Document, Link, Indexed
from pydantic import Field

from app.models.user import User

class Journal(Document):
    title: Indexed(str)
    description: str
    journal_id: UUID = Field(default_factory=uuid4, unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    owner: Link[User]

    class Collection:
        name = "journals"

