import json
import uuid
from datetime import datetime
from pathlib import Path

from config import HISTORY_FILE


class HistoryStore:
    """Append-only JSON history of generated notes."""

    MAX_ITEMS = 200

    def __init__(self, path: str = HISTORY_FILE):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def _read(self) -> list:
        try:
            return json.loads(self.path.read_text(encoding="utf-8") or "[]")
        except (OSError, json.JSONDecodeError):
            return []

    def _write(self, items: list) -> None:
        self.path.write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8")

    def list(self, limit: int = 50) -> list:
        items = self._read()
        return items[-limit:][::-1]

    def add(self, item: dict) -> dict:
        items = self._read()
        record = {
            "id": str(uuid.uuid4()),
            "created_at": datetime.utcnow().isoformat() + "Z",
            **item,
        }
        items.append(record)
        items = items[-self.MAX_ITEMS :]
        self._write(items)
        return record

    def clear(self) -> None:
        self._write([])


history = HistoryStore()
