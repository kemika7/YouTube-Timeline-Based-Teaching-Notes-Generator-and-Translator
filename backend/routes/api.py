import logging
import traceback

from fastapi import APIRouter, HTTPException

from models.schemas import (
    NotesRequest,
    NotesResponse,
    TranscriptRequest,
    TranscriptResponse,
    TranslateRequest,
    TranslateResponse,
)
from services.history_service import history
from services.notes_service import NotesError, generate_notes
from services.transcript_service import TranscriptError, fetch_transcript
from services.translation_service import TranslationError, translate_text
from utils.youtube_utils import extract_video_id

log = logging.getLogger("uvicorn.error")

router = APIRouter()


def _log_unexpected(where: str, exc: Exception) -> str:
    tb = traceback.format_exc()
    log.error("[%s] %s\n%s", where, exc, tb)
    return f"{type(exc).__name__}: {exc}"

LANGUAGE_NAMES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "hi": "Hindi",
    "zh-CN": "Chinese (Simplified)",
    "ja": "Japanese",
    "ar": "Arabic",
    "pt": "Portuguese",
    "ru": "Russian",
}


@router.get("/languages")
def languages():
    return {"languages": [{"code": code, "name": name} for code, name in LANGUAGE_NAMES.items()]}


@router.post("/extract-transcript", response_model=TranscriptResponse)
def extract_transcript(req: TranscriptRequest):
    try:
        result = fetch_transcript(req.url, req.language or "en")
        return TranscriptResponse(**result)
    except TranscriptError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=_log_unexpected("api", e))


@router.post("/translate", response_model=TranslateResponse)
def translate(req: TranslateRequest):
    try:
        translated = translate_text(req.text, req.target_language, req.source_language or "auto")
        return TranslateResponse(translated_text=translated, target_language=req.target_language)
    except TranslationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=_log_unexpected("api", e))


@router.post("/generate-notes", response_model=NotesResponse)
def generate_notes_endpoint(req: NotesRequest):
    try:
        transcript = req.transcript
        video_id: str | None = extract_video_id(req.url) if req.url else None

        if not transcript:
            if not req.url:
                raise HTTPException(status_code=400, detail="Provide a YouTube URL or transcript.")
            data = fetch_transcript(req.url, "en")
            transcript = data["transcript"]
            video_id = data["video_id"]
            if req.language and req.language != "en":
                transcript = translate_text(transcript, req.language)

        language_name = LANGUAGE_NAMES.get(req.language, req.language)
        notes = generate_notes(transcript, format=req.format, language=language_name)

        history.add(
            {
                "video_id": video_id or "",
                "url": req.url or "",
                "format": req.format,
                "language": req.language,
                "notes": notes,
            }
        )

        return NotesResponse(
            video_id=video_id,
            notes=notes,
            format=req.format,
            language=req.language,
        )
    except (TranscriptError, TranslationError, NotesError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=_log_unexpected("api", e))


@router.get("/history")
def get_history(limit: int = 50):
    return {"items": history.list(limit=limit)}


@router.delete("/history")
def clear_history():
    history.clear()
    return {"status": "cleared"}
