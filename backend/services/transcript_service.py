import json
import re
from typing import Optional
from urllib.request import Request, urlopen

import yt_dlp

from services.cache_service import cache
from utils.youtube_utils import extract_video_id


class TranscriptError(Exception):
    pass


_VTT_TIMING = re.compile(r"\d{2}:\d{2}:\d{2}\.\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}\.\d{3}")
_VTT_TAG = re.compile(r"<[^>]+>")


def _vtt_to_text(vtt: str) -> str:
    out = []
    last = None
    for raw in vtt.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("WEBVTT") or line.startswith("NOTE") or line.startswith("Kind:") or line.startswith("Language:"):
            continue
        if _VTT_TIMING.search(line):
            continue
        if line.isdigit():
            continue
        cleaned = _VTT_TAG.sub("", line).strip()
        if cleaned and cleaned != last:
            out.append(cleaned)
            last = cleaned
    return " ".join(out).strip()


def _track_text(tracks: list) -> Optional[str]:
    if not tracks:
        return None
    preferred = sorted(
        tracks,
        key=lambda t: 0 if t.get("ext") == "json3" else 1 if t.get("ext") == "vtt" else 2,
    )
    for track in preferred:
        url = track.get("url")
        if not url:
            continue
        try:
            req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(req, timeout=30) as resp:
                content = resp.read().decode("utf-8", errors="replace")
        except Exception:
            continue

        ext = track.get("ext")
        if ext == "json3":
            try:
                data = json.loads(content)
                text = " ".join(
                    seg.get("utf8", "")
                    for event in data.get("events", [])
                    for seg in (event.get("segs") or [])
                ).strip()
                if text:
                    return text
            except json.JSONDecodeError:
                continue
        elif ext in ("vtt", "srv3", "srv2", "srv1", "ttml"):
            text = _vtt_to_text(content)
            if text:
                return text
        else:
            if content.strip():
                return content.strip()
    return None


def _candidate_languages(language: str, subs: dict, auto: dict) -> list[str]:
    seen = []
    for lang in [language, "en"]:
        if lang and lang not in seen:
            seen.append(lang)
    for lang in list(subs.keys()) + list(auto.keys()):
        if lang and lang not in seen:
            seen.append(lang)
    return seen


def fetch_transcript(url: str, language: str = "en") -> dict:
    video_id = extract_video_id(url)
    if not video_id:
        raise TranscriptError("Invalid YouTube URL")

    cache_key = f"{video_id}_{language}"
    cached = cache.get(cache_key)
    if cached:
        return {**cached, "cached": True}

    yt_url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        "skip_download": True,
        "quiet": True,
        "no_warnings": True,
        "writeautomaticsub": True,
        "writesubtitles": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(yt_url, download=False)
    except yt_dlp.utils.DownloadError as e:
        msg = str(e).lower()
        if "unavailable" in msg:
            raise TranscriptError("This video is unavailable.")
        if "private" in msg:
            raise TranscriptError("This video is private.")
        if "sign in" in msg or "age" in msg:
            raise TranscriptError("This video requires sign-in (age-restricted).")
        raise TranscriptError(f"Failed to fetch video: {e}")
    except Exception as e:
        raise TranscriptError(f"Failed to fetch video: {e}")

    subs = info.get("subtitles") or {}
    auto = info.get("automatic_captions") or {}
    if not subs and not auto:
        raise TranscriptError("No transcript or captions found for this video.")

    transcript_text: Optional[str] = None
    used_language: Optional[str] = None

    for lang in _candidate_languages(language, subs, auto):
        text = _track_text(subs.get(lang, []))
        if text:
            transcript_text = text
            used_language = lang
            break
    if not transcript_text:
        for lang in _candidate_languages(language, subs, auto):
            text = _track_text(auto.get(lang, []))
            if text:
                transcript_text = text
                used_language = lang
                break

    if not transcript_text:
        raise TranscriptError("Could not download captions for this video.")

    payload = {
        "video_id": video_id,
        "transcript": transcript_text,
        "language": used_language or "auto",
    }
    cache.set(cache_key, payload)
    return {**payload, "cached": False}
