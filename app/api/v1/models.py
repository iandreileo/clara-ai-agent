from typing import List
from pydantic import BaseModel
from typing import List, Dict, Optional
from langgraph.prebuilt.chat_agent_executor import AgentState

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str

class ChatHistory(BaseModel):
    messages: List[Dict[str, str]]

class UserState(BaseModel):
    """User-specific state information"""
    user_token: str
    language: str = "en"  # Default to English

class ChatAppState(AgentState):
    conversation_id: str
    user_token: str

class PersonalInfo(BaseModel):
    name: str
    email: str
    phone: str
    summary: str
    country: str

class WorkExperience(BaseModel):
    company: str
    title: str
    location: str
    start_date: str
    end_date: str


class Education(BaseModel):
    school: str
    degree: str
    start_date: str
    end_date: str

