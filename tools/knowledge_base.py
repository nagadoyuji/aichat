import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
from uuid import UUID

from core.configs import settings
from model.agent import KnowledgeBaseEntry

class KnowledgeBase:
    def __init__(self):
        self.client = chromadb.Client(
            Settings(
                persist_directory=settings.KB_PERSIST_DIRECTORY,
                anonymized_telemetry=False
            )
        )
        self.collection = self.client.get_or_create_collection(
            name=settings.KB_COLLECTION_NAME
        )

    async def add_document(self, entry: KnowledgeBaseEntry) -> None:
        """添加文档到知识库"""
        self.collection.add(
            documents=[entry.content],
            metadatas=[{
                "title": entry.title,
                "source": entry.source,
                "entry_id": str(entry.id),
                "user_id": str(entry.user_id) if entry.user_id else None
            }],
            ids=[str(entry.id)]
        )
        self.client.persist()

    async def delete_document(self, entry_id: UUID) -> None:
        """从知识库删除文档"""
        self.collection.delete(ids=[str(entry_id)])
        self.client.persist()

    async def search(self, query: str, user_id: Optional[UUID] = None, limit: int = 3) -> List[Dict]:
        """搜索知识库"""
        where = {"user_id": str(user_id)} if user_id else None
        
        results = self.collection.query(
            query_texts=[query],
            n_results=limit,
            where=where
        )
        
        # 格式化结果
        formatted_results = []
        for i in range(len(results["ids"][0])):
            formatted_results.append({
                "id": results["ids"][0][i],
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i]
            })
        
        return formatted_results

# 单例实例
knowledge_base = KnowledgeBase()