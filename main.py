from fastapi import FastAPI
from api import init_api

app = FastAPI(
    title="AI Chat Backend",
    description="A simple AI chat backend with FastAPI, PostgreSQL and Gemini",
    version="1.0.0",
)

# 初始化API
init_api(app)

@app.get("/")
async def root():
    return {"message": "Welcome to AI Chat Backend. Visit /docs for API documentation."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
