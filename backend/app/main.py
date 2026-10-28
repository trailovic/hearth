from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.ollama_client import OllamaError, send_message

app = FastAPI(
    title="Hearth API",
    version="0.1.0",
)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=16000)


class ChatResponse(BaseModel):
    response: str
    model: str


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "service": "hearth",
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = await send_message(request.message)
    except OllamaError as exc:
        raise HTTPException(
            status_code=502,
            detail="AI service is currently unavailable",
        ) from exc

    return ChatResponse(
        response=response,
        model="beam:cloud",
    )