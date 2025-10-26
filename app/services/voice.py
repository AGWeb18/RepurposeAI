from __future__ import annotations

from typing import Dict, Iterable, Optional, Tuple

from pydantic import BaseModel, Field


class BrandVoice(BaseModel):
    """Represents how a creator wants content to sound."""

    voice_id: str = Field(..., description="Stable identifier for the profile")
    label: str = Field(..., description="Human-friendly voice name")
    tagline: str = Field(default="", description="Short primer injected as an intro")
    bullet_style: str = Field(default="•", description="Prefix used for bullet lists")
    adjectives: Tuple[str, ...] = Field(default_factory=tuple, description="Tone descriptors")

    def decorate(self, text: str) -> str:
        prefix = f"{self.tagline}\n" if self.tagline else ""
        suffix = ""
        if self.adjectives:
            suffix = f"\n\nTone cues: {', '.join(self.adjectives)}"
        return f"{prefix}{text}{suffix}".strip()


class BrandVoiceRegistry:
    """In-memory voice registry. Sticky feature: creators can save many voices."""

    def __init__(self) -> None:
        self._voices: Dict[str, BrandVoice] = {}

    def upsert(self, voice: BrandVoice) -> BrandVoice:
        self._voices[voice.voice_id] = voice
        return voice

    def get(self, voice_id: Optional[str]) -> Optional[BrandVoice]:
        if voice_id is None:
            return None
        return self._voices.get(voice_id)

    def list(self) -> Iterable[BrandVoice]:
        return self._voices.values()


DEFAULT_VOICE = BrandVoice(
    voice_id="default",
    label="Default Energetic",
    tagline="Let's repurpose brilliance!",
    adjectives=("energetic", "actionable", "friendly"),
)
