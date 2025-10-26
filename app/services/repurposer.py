from __future__ import annotations

from dataclasses import dataclass
from textwrap import shorten
from typing import Callable, Dict, Iterable

from app.schemas.content import RepurposeChannel
from app.services.voice import BrandVoice


@dataclass
class AssetBlueprint:
    channel: RepurposeChannel
    headline_template: str
    body_builder: Callable[[str, BrandVoice, str | None], str]

    def render(self, summary: str, voice: BrandVoice, cta: str | None) -> dict[str, str]:
        headline = self.headline_template.format(summary=shorten(summary, width=70, placeholder="…"))
        body = self.body_builder(summary, voice, cta)
        return {"headline": headline, "body": voice.decorate(body)}


def _tiktok_body(summary: str, voice: BrandVoice, cta: str | None) -> str:
    hooks = summary.split(". ")[:2]
    script = "\n".join(f"{voice.bullet_style} {line.strip()}" for line in hooks if line)
    outro = f"\nCTA: {cta}" if cta else ""
    return f"Hook Script:\n{script}{outro}".strip()


def _thread_body(summary: str, voice: BrandVoice, cta: str | None) -> str:
    bullets = summary.split(". ")[:5]
    thread = "\n\n".join(f"{idx + 1}/ {bullet.strip()}" for idx, bullet in enumerate(bullets) if bullet)
    if cta:
        thread = f"{thread}\n\n{len(bullets) + 1}/ {cta}"
    return thread


def _carousel_body(summary: str, voice: BrandVoice, cta: str | None) -> str:
    segments = summary.split(". ")
    slides = ["Slide 1: Pain ➡️ {pain}".format(pain=segments[0] if segments else summary)]
    if len(segments) > 1:
        slides.append(f"Slide 2: Framework ➡️ {segments[1]}")
    if len(segments) > 2:
        slides.append(f"Slide 3: Proof ➡️ {segments[2]}")
    slides.append(f"Slide {len(slides)+1}: CTA ➡️ {cta or 'DM me for the playbook'}")
    return "\n".join(slides)


def _newsletter_body(summary: str, voice: BrandVoice, cta: str | None) -> str:
    chunks = summary.split(". ")
    intro = chunks[0] if chunks else summary
    bullets = "\n".join(f"{voice.bullet_style} {chunk.strip()}" for chunk in chunks[1:4] if chunk)
    closing = f"\n\nHit reply: {cta}" if cta else ""
    return f"{intro}\n\nKey Takeaways:\n{bullets}{closing}".strip()


def _shorts_body(summary: str, voice: BrandVoice, cta: str | None) -> str:
    beats = summary.split(". ")[:3]
    script_lines = [
        "Beat 1 - Pattern Break:",
        *(f"Beat {idx + 2} - {beat.strip()}" for idx, beat in enumerate(beats) if beat),
    ]
    if cta:
        script_lines.append(f"Final CTA: {cta}")
    return "\n".join(script_lines)


class Repurposer:
    """Turns summaries into channel-ready assets."""

    def __init__(self) -> None:
        self._blueprints: Dict[RepurposeChannel, AssetBlueprint] = {
            RepurposeChannel.TIKTOK: AssetBlueprint(
                channel=RepurposeChannel.TIKTOK,
                headline_template="{summary}",
                body_builder=_tiktok_body,
            ),
            RepurposeChannel.X_THREAD: AssetBlueprint(
                channel=RepurposeChannel.X_THREAD,
                headline_template="{summary}",
                body_builder=_thread_body,
            ),
            RepurposeChannel.LINKEDIN_CAROUSEL: AssetBlueprint(
                channel=RepurposeChannel.LINKEDIN_CAROUSEL,
                headline_template="LinkedIn Carousel: {summary}",
                body_builder=_carousel_body,
            ),
            RepurposeChannel.NEWSLETTER_SUMMARY: AssetBlueprint(
                channel=RepurposeChannel.NEWSLETTER_SUMMARY,
                headline_template="Newsletter TL;DR: {summary}",
                body_builder=_newsletter_body,
            ),
            RepurposeChannel.YOUTUBE_SHORT: AssetBlueprint(
                channel=RepurposeChannel.YOUTUBE_SHORT,
                headline_template="Shorts Hook: {summary}",
                body_builder=_shorts_body,
            ),
        }

    def supported_channels(self) -> Iterable[RepurposeChannel]:
        return self._blueprints.keys()

    def generate(self, summary: str, channels: Iterable[RepurposeChannel], voice: BrandVoice, cta: str | None) -> Dict[RepurposeChannel, dict[str, str]]:
        assets: Dict[RepurposeChannel, dict[str, str]] = {}
        for channel in channels:
            blueprint = self._blueprints.get(channel)
            if not blueprint:
                continue
            assets[channel] = blueprint.render(summary=summary, voice=voice, cta=cta)
        return assets
