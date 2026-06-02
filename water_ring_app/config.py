from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class AppConfig:
    interval_minutes: int = 60
    snooze_minutes: int = 15
    reminder_seconds: int = 10
    auto_start: bool = False
    launch_minimized: bool = True
    cat_style: str = "classic"
    next_reminder: datetime = field(default_factory=lambda: datetime.now() + timedelta(minutes=60))
