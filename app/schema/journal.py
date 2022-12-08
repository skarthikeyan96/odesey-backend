from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class JournalCreate(BaseModel):
    title: str = Field(..., title='Title')
    description: str = Field(..., title='description')
    
    # user can update either title or description of the journal
class JournalUpdate(BaseModel):
    title: Optional[str] 
    description: Optional[str] 

class JournalOutput(BaseModel):
    journal_id: UUID
    title: str
    description: str
    created_at: datetime
    updated_at: datetime
    