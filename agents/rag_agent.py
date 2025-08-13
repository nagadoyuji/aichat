import google.generativeai as genai
from typing import List, Dict, Optional
from uuid import UUID

from core.configs import settings
from tools.knowledge_base import knowledge_base

# 配置Gemini
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)
else:
    raise ValueError("GEMINI_API_KEY is not set in environment variables")

class RAGAgent:
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.model = genai.GenerativeModel(model_name)
    
    async def generate_response(
        self, 
        query: str, 
        chat_history: List[Dict[str, str]] = None,
        user_id: Optional[UUID] = None,
        use_rag: bool = False
    ) -> str:
        """生成响应，可选地使用RAG"""
        chat_history = chat_history or []
        
        # 如果使用RAG，先搜索知识库
        context = ""
        if use_rag:
            search_results = await knowledge_base.search(query, user_id)
            if search_results:
                context = "Here is some context that might help you answer the question:\n"
                for result in search_results:
                    context += f"- {result['content']}\n\n"
        
        # 构建提示
        prompt = f"Answer the following question. {context if context else ''}"
        
        # 添加对话历史
        messages = []
        for msg in chat_history[-5:]:  # 只取最近5条历史
            messages.append({
                "role": msg["role"],
                "parts": [msg["content"]]
            })
        
        # 添加当前查询
        messages.append({
            "role": "user",
            "parts": [f"{prompt}\nQuestion: {query}"]
        })
        
        # 生成响应
        response = self.model.generate_content(messages)
        return response.text

# 单例实例
rag_agent = RAGAgent()