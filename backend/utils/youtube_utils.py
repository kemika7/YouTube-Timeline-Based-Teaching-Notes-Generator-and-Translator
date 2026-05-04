import re
from urllib.parse import urlparse, parse_qs
from typing import Optional

YOUTUBE_REGEX = re.compile(
    r"(?:youtube\.com/(?:[^/\n\s]+/\S+/|(?:v|e(?:mbed)?)/|\S*?[?&]v=)|youtu\.be/)([a-zA-Z0-9_-]{11})"
)


def extract_video_id(url: str) -> Optional[str]:
    if not url:
        return None
    match = YOUTUBE_REGEX.search(url)
    if match:
        return match.group(1)
    parsed = urlparse(url)
    if parsed.hostname == "youtu.be":
        candidate = parsed.path.lstrip("/")[:11]
        return candidate or None
    if parsed.hostname and "youtube.com" in parsed.hostname:
        qs = parse_qs(parsed.query)
        if "v" in qs and qs["v"]:
            return qs["v"][0]
    return None
