from typing import Optional
from pydantic import BaseModel


class TranscriptRequest(BaseModel):
    url: str
    language: Optional[str] = "en"


class TranscriptResponse(BaseModel):
    video_id: str
    transcript: str
    language: str
    cached: bool = False


class TranslateRequest(BaseModel):
    text: str
    target_language: str
    source_language: Optional[str] = "auto"


class TranslateResponse(BaseModel):
    translated_text: str
    target_language: str


class NotesRequest(BaseModel):
    url: Optional[str] = None
    transcript: Optional[str] = None
    language: str = "en"
    format: str = "detailed"


class NotesResponse(BaseModel):
    video_id: Optional[str] = None
    notes: str
    format: str
    language: str
