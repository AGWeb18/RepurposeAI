from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict

from app.schemas.content import RepurposeChannel


class EvergreenCalendar:
    """Simple cadence-based scheduler for evergreen queues."""

    def __init__(self) -> None:
        self._next_slots: Dict[RepurposeChannel, datetime] = defaultdict(datetime.utcnow)

    def next_slot(self, channel: RepurposeChannel, cadence_days: int) -> datetime:
        scheduled_at = self._next_slots[channel]
        now = datetime.utcnow()
        if scheduled_at <= now:
            scheduled_at = now + timedelta(minutes=5)
        self._next_slots[channel] = scheduled_at + timedelta(days=cadence_days)
        return scheduled_at

    def reset(self) -> None:
        self._next_slots.clear()
