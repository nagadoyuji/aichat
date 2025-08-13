from typing import List
from fastapi import APIRouter, HTTPException
from uuid import UUID

from core.deps import CurrentUser
from model.agent import KnowledgeBaseEntry
from schemas.agent import (
    KnowledgeBaseEntry as KBEntrySchema,
    KnowledgeBaseEntryCreate,
    KnowledgeBaseEntryUpdate
)
from tools.knowledge_base import knowledge_base

router = APIRouter()

@router.get("/knowledge", response_model=List[KBEntrySchema])
async def get_knowledge_entries(
    current_user: CurrentUser
) -> List[KBEntrySchema]:
    """获取当前用户的知识库条目"""
    return await KnowledgeBaseEntry.filter(user=current_user).all()

@router.post("/knowledge", response_model=KBEntrySchema)
async def create_knowledge_entry(
    entry_in: KnowledgeBaseEntryCreate,
    current_user: CurrentUser
) -> KBEntrySchema:
    """创建知识库条目"""
    entry = await KnowledgeBaseEntry.create(
        user=current_user,
        content=entry_in.content,
        title=entry_in.title,
        source=entry_in.source
    )
    
    # 同时添加到向量数据库
    await knowledge_base.add_document(entry)
    
    return entry

@router.get("/knowledge/{entry_id}", response_model=KBEntrySchema)
async def get_knowledge_entry(
    entry_id: UUID,
    current_user: CurrentUser
) -> KBEntrySchema:
    """获取特定知识库条目"""
    try:
        return await KnowledgeBaseEntry.get(id=entry_id, user=current_user)
    except:
        raise HTTPException(status_code=404, detail="Knowledge entry not found")

@router.put("/knowledge/{entry_id}", response_model=KBEntrySchema)
async def update_knowledge_entry(
    entry_id: UUID,
    entry_in: KnowledgeBaseEntryUpdate,
    current_user: CurrentUser
) -> KBEntrySchema:
    """更新知识库条目"""
    try:
        entry = await KnowledgeBaseEntry.get(id=entry_id, user=current_user)
        
        if entry_in.content is not None:
            entry.content = entry_in.content
        if entry_in.title is not None:
            entry.title = entry_in.title
        if entry_in.source is not None:
            entry.source = entry_in.source
            
        await entry.save()
        
        # 更新向量数据库
        await knowledge_base.delete_document(entry_id)
        await knowledge_base.add_document(entry)
        
        return entry
    except:
        raise HTTPException(status_code=404, detail="Knowledge entry not found")

@router.delete("/knowledge/{entry_id}")
async def delete_knowledge_entry(
    entry_id: UUID,
    current_user: CurrentUser
):
    """删除知识库条目"""
    try:
        entry = await KnowledgeBaseEntry.get(id=entry_id, user=current_user)
        await entry.delete()
        
        # 从向量数据库删除
        await knowledge_base.delete_document(entry_id)
        
        return {"detail": "Knowledge entry deleted successfully"}
    except:
        raise HTTPException(status_code=404, detail="Knowledge entry not found")
