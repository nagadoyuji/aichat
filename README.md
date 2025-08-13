# ai聊天后端
## 1.功能介绍
### 1.1 login
---  

/api/v1/login：注册用户  

### 1.2 user
---  

/api/v1/users/：获取用户列表；  
/api/v1/users/：创建用户；  
/api/v1/users/me:获取当前用户信息；  
/api/v1/users/me:更新用户信息  

### 1.3 chat
---  

/api/v1/chat/conversations:获取当前用户的所有对话；  
/api/v1/chat/conversations:创建新对话；  
/api/v1/chat/conversations/{conversation_id}:获取特定对话详情；  
/api/v1/chat/conversations/{conversation_id}:更新对话；  
/api/v1/chat/conversations/{conversation_id}:删除对话；  
/api/v1/chat/message:发送消息并获取AI响应；  

### 1.4 service
<!-- knowledgebase构建 -->  
---  

/api/v1/knowledge:获取当前用户的知识库条目;  
/api/v1/knowledge:创建知识库条目;  
/api/v1/knowledge{entry_id}:更新知识库条目;  
/api/v1/knowledge{entry_id}:删除知识库条目  

## 2.技术框架

fatspai,postgresql,langchain,langgraph  
