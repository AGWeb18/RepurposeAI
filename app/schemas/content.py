from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class SourceType(str, Enum):
    PODCAST = "podcast"
    VIDEO = "video"
    BLOG = "blog"
    NEWSLETTER = "newsletter"


class ContentIngestRequest(BaseModel):
    title: str = Field(..., description="Human-friendly title for the source content")
    body: str = Field(..., description="Full transcript or article body")
    source_type: SourceType = Field(..., description="Type of the original content")
    duration_minutes: Optional[int] = Field(
        default=None,
        ge=1,
        description="Approximate duration or reading time to help with pacing",
    )
    tags: List[str] = Field(default_factory=list, description="Topic tags to improve routing")
    brand_voice_id: Optional[str] = Field(
        default=None,
        description="Brand voice profile to apply on ingest",
    )


class ContentIngestResponse(BaseModel):
    content_id: str
    stored_at: datetime


class RepurposeChannel(str, Enum):
    TIKTOK = "tiktok"
    YOUTUBE_SHORT = "youtube_short"
    X_THREAD = "x_thread"
    LINKEDIN_CAROUSEL = "linkedin_carousel"
    NEWSLETTER_SUMMARY = "newsletter_summary"


class RepurposeRequest(BaseModel):
    content_id: str
    channels: List[RepurposeChannel]
    brand_voice_id: Optional[str] = Field(
        default=None, description="Override the voice profile used for asset generation"
    )
    primary_cta: Optional[str] = Field(
        default=None,
        description="Call to action appended to outbound posts for conversion tracking",
    )
    cadence_days: int = Field(
        default=3,
        ge=1,
        description="Spacing between scheduled posts in the evergreen queue",
    )


class RepurposedAsset(BaseModel):
    channel: RepurposeChannel
    headline: str
    body: str
    scheduled_for: datetime
    brand_voice_id: str


class RepurposeResponse(BaseModel):
    content_id: str
    assets: List[RepurposedAsset]
