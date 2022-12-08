from typing import List
from uuid import UUID
from fastapi import APIRouter, status, Request, Depends

from app.models.journal import Journal
from app.schema.journal import JournalCreate, JournalOutput, JournalUpdate
from app.models.user import User
from app.deps.auth_deps import get_current_user

journal_router = APIRouter()


@journal_router.post(
    "/",
    response_description="create a new journal",
    status_code=status.HTTP_201_CREATED,
    response_model=Journal,
)
async def create_journal(
    request: Request,
    data: JournalCreate,
    current_user: User = Depends(get_current_user),
):
    """_summary_

    Args:
        request (Request): _description_
        data (JournalCreate): _description_
        current_user (User, optional): _description_. Defaults to Depends(get_current_user).

    Returns:
        _type_: _description_
    """
    document = Journal(
        **data.dict(), owner=current_user
    )  # https://stackoverflow.com/questions/21809112/what-does-tuple-and-dict-mean-in-python
    result = await Journal.insert(document)
    return result


@journal_router.get(
    "/", response_description="list the journals", response_model=List[JournalOutput]
)
async def view_journal(
    request: Request, current_user: User = Depends(get_current_user)
):
    """_summary_

    Args:
        request (Request): _description_
        current_user (User, optional): _description_. Defaults to Depends(get_current_user).

    Returns:
        _type_: _description_
    """
    journals = await Journal.find(Journal.owner.id == current_user.id).to_list()
    return journals


@journal_router.get("/{journal_id}", response_description="get the journal by id")
async def get_journal_id(
    journal_id: UUID, current_user: User = Depends(get_current_user)
):
    """_summary_

    Args:
        journal_id (UUID): _description_
        current_user (User, optional): _description_. Defaults to Depends(get_current_user).

    Returns:
        _type_: _description_
    """
    journal = await Journal.find_one(
        Journal.journal_id == journal_id, Journal.owner.id == current_user.id
    )
    return journal


@journal_router.patch("/{journal_id}", response_description="update the journal")
async def update_journal(
    journal_id: UUID,
    data: JournalUpdate,
    current_user: User = Depends(get_current_user),
):
    """_summary_

    Args:
        journal_id (UUID): _description_
        data (JournalUpdate): _description_
        current_user (User, optional): _description_. Defaults to Depends(get_current_user).

    Returns:
        _type_: _description_
    """
    journal = await Journal.find_one(
        Journal.journal_id == journal_id, Journal.owner.id == current_user.id
    )

    await journal.update(
        {"$set": data.dict(exclude_unset=True)}
    )  # excludes the value which is not set
    await journal.save()

    return journal


@journal_router.delete("/", response_description="delete the journal")
async def delete_journal(
    journal_id: UUID, current_user: User = Depends(get_current_user)
):
    """_summary_

    Args:
        journal_id (UUID): _description_
        current_user (User, optional): _description_. Defaults to Depends(get_current_user).

    Returns:
        _type_: _description_
    """
    journal = await Journal.find_one(
        Journal.journal_id == journal_id, Journal.owner.id == current_user.id
    )
    if journal:
        await journal.delete()

        return {"message": "success"}
