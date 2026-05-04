import json
from pathlib import Path
from typing import Any, Optional

from config import CACHE_DIR


class TranscriptCache:
    """Simple two-tier (memory + JSON file) cache for transcripts."""

    def __init__(self, cache_dir: str = CACHE_DIR):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._memory: dict[str, Any] = {}

    def _path(self, key: str) -> Path:
        safe = key.replace("/", "_").replace("\\", "_")
        return self.cache_dir / f"transcript_{safe}.json"

    def get(self, key: str) -> Optional[dict]:
        if key in self._memory:
            return self._memory[key]
        p = self._path(key)
        if p.exists():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                self._memory[key] = data
                return data
            except (OSError, json.JSONDecodeError):
                return None
        return None

    def set(self, key: str, value: dict) -> None:
        self._memory[key] = value
        try:
            self._path(key).write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
        except OSError:
            pass


cache = TranscriptCache()
