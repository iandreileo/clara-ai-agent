from app.services.chat_service import ChatService
from app.api.v1.models import ChatRequest, ChatResponse, ChatHistory
from fastapi import Depends, APIRouter, HTTPException
from app.core.security import verify_token

router = APIRouter()
chat_service = ChatService()

# FastAPI endpoints
@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest, user_token: str = Depends(verify_token)):
    """Process a chat message"""
    return await chat_service.process_message(
        message=request.message,
        user_token=user_token,
        conversation_id=request.conversation_id
    )
