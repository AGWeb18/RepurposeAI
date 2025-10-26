from __future__ import annotations

from typing import Dict

from fastapi import FastAPI, HTTPException

from app.schemas.content import (
    ContentIngestRequest,
    ContentIngestResponse,
    RepurposeChannel,
    RepurposeRequest,
    RepurposeResponse,
    RepurposedAsset,
)
from app.services.calendar import EvergreenCalendar
from app.services.content_store import ContentStore
from app.services.repurposer import Repurposer
from app.services.voice import BrandVoice, BrandVoiceRegistry, DEFAULT_VOICE


app = FastAPI(
    title="RepurposeAI",
    description="Turn one long-form asset into dozens of sticky, channel-ready posts.",
    version="0.1.0",
)


voice_registry = BrandVoiceRegistry()
voice_registry.upsert(DEFAULT_VOICE)
content_store = ContentStore()
calendar = EvergreenCalendar()
repurposer = Repurposer()


@app.post("/ingest", response_model=ContentIngestResponse)
def ingest_content(payload: ContentIngestRequest) -> ContentIngestResponse:
    voice = _resolve_voice(payload.brand_voice_id)
    stored = content_store.ingest(payload, voice)
    return ContentIngestResponse(content_id=stored.content_id, stored_at=stored.stored_at)


@app.post("/repurpose", response_model=RepurposeResponse)
def repurpose_content(payload: RepurposeRequest) -> RepurposeResponse:
    stored = content_store.get(payload.content_id)
    if not stored:
        raise HTTPException(status_code=404, detail="Content not found")
    voice = _resolve_voice(payload.brand_voice_id or stored.brand_voice_id)
    assets = repurposer.generate(
        summary=stored.summary,
        channels=payload.channels,
        voice=voice,
        cta=payload.primary_cta,
    )
    scheduled_assets = [
        _hydrate_asset(
            channel=channel,
            blueprint=asset,
            cadence_days=payload.cadence_days,
            voice_id=voice.voice_id,
        )
        for channel, asset in assets.items()
    ]
    return RepurposeResponse(content_id=payload.content_id, assets=scheduled_assets)


@app.get("/voices")
def list_voices() -> Dict[str, dict]:
    return {voice.voice_id: voice.model_dump() for voice in voice_registry.list()}


def _resolve_voice(voice_id: str | None) -> BrandVoice:
    if voice_id is None:
        return DEFAULT_VOICE
    voice = voice_registry.get(voice_id)
    if not voice:
        raise HTTPException(status_code=404, detail="Brand voice not found")
    return voice


def _hydrate_asset(
    channel: RepurposeChannel,
    blueprint: Dict[str, str],
    cadence_days: int,
    voice_id: str,
) -> RepurposedAsset:
    scheduled_for = calendar.next_slot(channel, cadence_days=cadence_days)
    return RepurposedAsset(
        channel=channel,
        headline=blueprint["headline"],
        body=blueprint["body"],
        scheduled_for=scheduled_for,
        brand_voice_id=voice_id,
    )


@app.post("/voices/{voice_id}")
def upsert_voice(voice_id: str, voice: BrandVoice) -> BrandVoice:
    if voice.voice_id != voice_id:
        raise HTTPException(status_code=400, detail="Voice ID mismatch")
    return voice_registry.upsert(voice)


@app.post("/calendars/reset")
def reset_calendar() -> Dict[str, str]:
    calendar.reset()
    return {"status": "reset"}
