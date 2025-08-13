from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class KnowledgeBaseEntryBase(BaseModel):
    content: str
    title: str
    source: Optional[str] = None

class KnowledgeBaseEntryCreate(KnowledgeBaseEntryBase):
    pass

class KnowledgeBaseEntryUpdate(BaseModel):
    content: Optional[str] = None
    title: Optional[str] = None
    source: Optional[str] = None

class KnowledgeBaseEntryInDBBase(KnowledgeBaseEntryBase):
    id: UUID
    user_id: Optional[UUID]
    created_at: datetime

    class Config:
        from_attributes = True

class KnowledgeBaseEntry(KnowledgeBaseEntryInDBBase):
    pass