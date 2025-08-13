from typing import List, Optional
from fastapi import APIRouter, HTTPException
from uuid import UUID

from core.deps import CurrentUser
from model.chat import Conversation, Message
from schemas.chat import (
    Conversation as ConversationSchema,
    ConversationCreate,
    ConversationUpdate,
    Message as MessageSchema,
    MessageCreate,
    ChatRequest,
    ChatResponse
)
from agents.rag_agent import rag_agent

router = APIRouter()

@router.get("/conversations", response_model=List[ConversationSchema])
async def get_conversations(
    current_user: CurrentUser
) -> List[ConversationSchema]:
    """获取当前用户的所有对话"""
    return await Conversation.filter(user=current_user).all().prefetch_related('messages')

@router.post("/conversations", response_model=ConversationSchema)
async def create_conversation(
    conversation_in: ConversationCreate,
    current_user: CurrentUser
) -> ConversationSchema:
    """创建新对话"""
    conversation = await Conversation.create(
        user=current_user,
        title=conversation_in.title
    )
    return await Conversation.get(id=conversation.id).prefetch_related('messages')

@router.get("/conversations/{conversation_id}", response_model=ConversationSchema)
async def get_conversation(
    conversation_id: UUID,
    current_user: CurrentUser
) -> ConversationSchema:
    """获取特定对话详情"""
    try:
        conversation = await Conversation.get(
            id=conversation_id,
            user=current_user
        ).prefetch_related('messages')
        return conversation
    except:
        raise HTTPException(status_code=404, detail="Conversation not found")

@router.put("/conversations/{conversation_id}", response_model=ConversationSchema)
async def update_conversation(
    conversation_id: UUID,
    conversation_in: ConversationUpdate,
    current_user: CurrentUser
) -> ConversationSchema:
    """更新对话"""
    try:
        conversation = await Conversation.get(
            id=conversation_id,
            user=current_user
        )
        if conversation_in.title:
            conversation.title = conversation_in.title
            await conversation.save()
        return await Conversation.get(id=conversation.id).prefetch_related('messages')
    except:
        raise HTTPException(status_code=404, detail="Conversation not found")

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: UUID,
    current_user: CurrentUser
):
    """删除对话"""
    try:
        conversation = await Conversation.get(
            id=conversation_id,
            user=current_user
        )
        await conversation.delete()
        return {"detail": "Conversation deleted successfully"}
    except:
        raise HTTPException(status_code=404, detail="Conversation not found")

@router.post("/message", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    current_user: CurrentUser
) -> ChatResponse:
    """发送消息并获取AI响应"""
    if request.conversation_id:
        try:
            conversation = await Conversation.get(
                id=request.conversation_id,
                user=current_user
            )
        except:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        title = request.message[:50] + "..." if len(request.message) > 50 else request.message
        conversation = await Conversation.create(
            user=current_user,
            title=title
        )

    user_message = await Message.create(
        conversation=conversation,
        content=request.message,
        role=Message.ROLE_USER
    )
    
    messages = await Message.filter(
        conversation=conversation
    ).order_by('created_at').all()
    
    chat_history = [
        {"role": msg.role, "content": msg.content}
        for msg in messages
    ]

    ai_response = await rag_agent.generate_response(
        query=request.message,
        chat_history=chat_history[:-1],  # 排除当前消息
        user_id=current_user.id,
        use_rag=request.use_rag
    )

    ai_message = await Message.create(
        conversation=conversation,
        content=ai_response,
        role=Message.ROLE_ASSISTANT
    )
    
    return {
        "conversation_id": conversation.id,
        "message": ai_message
    }
