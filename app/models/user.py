from uuid import UUID, uuid4

from beanie import Document, Indexed
from pydantic import EmailStr, Field


class User(Document):
    """_summary_

    Args:
        Document (_type_): _description_
    """

    user_id: UUID = Field(default_factory=uuid4)
    email: Indexed(
        EmailStr, unique=True
    )  # EmailStr -> need to understand more about this
    username: Indexed(str, unique=True)
    hashed_password: str
    is_active: bool = True

    # 👇 collection is used at the time of creating the user document in the db
    class Collection:
        """_summary_"""

        name = "users"
