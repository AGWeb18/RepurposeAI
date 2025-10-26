from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional

from app.schemas.content import ContentIngestRequest, SourceType
from app.services.voice import BrandVoice


@dataclass
class StoredContent:
    content_id: str
    request: ContentIngestRequest
    stored_at: datetime
    summary: str
    brand_voice_id: str


class ContentStore:
    """Minimal content bank that powers reuse and highlights the sticky archive feature."""

    def __init__(self) -> None:
        self._storage: Dict[str, StoredContent] = {}
        self._counter = 0

    def _make_id(self) -> str:
        self._counter += 1
        return f"content-{self._counter:04d}"

    def ingest(self, payload: ContentIngestRequest, voice: BrandVoice) -> StoredContent:
        content_id = self._make_id()
        summary = self._summarize(payload)
        stored = StoredContent(
            content_id=content_id,
            request=payload,
            stored_at=datetime.utcnow(),
            summary=voice.decorate(summary),
            brand_voice_id=voice.voice_id,
        )
        self._storage[content_id] = stored
        return stored

    def get(self, content_id: str) -> Optional[StoredContent]:
        return self._storage.get(content_id)

    def _summarize(self, payload: ContentIngestRequest) -> str:
        """Lightweight heuristic summary until LLM integration lands."""
        text = payload.body.strip()
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if not lines:
            return payload.title
        first = lines[0]
        middle = lines[len(lines) // 2] if len(lines) > 1 else ""
        closing = lines[-1] if len(lines) > 2 else ""
        parts = [first]
        if middle:
            parts.append(middle)
        if closing:
            parts.append(closing)
        modifiers = {
            SourceType.PODCAST: "Podcast highlight:",
            SourceType.VIDEO: "Video takeaway:",
            SourceType.BLOG: "Article insight:",
            SourceType.NEWSLETTER: "Newsletter recap:",
        }
        prefix = modifiers.get(payload.source_type, "Content insight:")
        return f"{prefix} {' '.join(parts)}"
