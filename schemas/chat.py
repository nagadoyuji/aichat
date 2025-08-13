from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class MessageBase(BaseModel):
    content: str
    role: str

class MessageCreate(MessageBase):
    pass

class MessageUpdate(BaseModel):
    content: Optional[str] = None

class MessageInDBBase(MessageBase):
    id: UUID
    conversation_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class Message(MessageInDBBase):
    pass

class ConversationBase(BaseModel):
    title: str

class ConversationCreate(ConversationBase):
    pass

class ConversationUpdate(BaseModel):
    title: Optional[str] = None

class ConversationInDBBase(ConversationBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Conversation(ConversationInDBBase):
    messages: List[Message] = []

class ChatRequest(BaseModel):
    conversation_id: Optional[UUID] = None
    message: str
    use_rag: bool = False

class ChatResponse(BaseModel):
    conversation_id: UUID
    message: Message