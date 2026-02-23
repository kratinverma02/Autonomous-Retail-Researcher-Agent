from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime


# ---------------- CHAT MESSAGE ----------------
class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


# ---------------- REQUEST MODEL ----------------
class ResearchRequest(BaseModel):
    query: str
    chat_history: Optional[List[ChatMessage]] = Field(default_factory=list)


# ---------------- SOURCE MODEL ----------------
class Source(BaseModel):
    title: str
    url: str


# ---------------- REPORT MODEL ----------------
class Report(BaseModel):
    query: str
    executive_summary: str
    trends: str
    insights: str
    recommendations: str
    sources: List[Source]
    timestamp: datetime
