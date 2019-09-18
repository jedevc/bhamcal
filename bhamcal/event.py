from datetime import datetime
from dataclasses import dataclass

@dataclass
class CalendarEvent:
    start: datetime
    end: datetime
    subject: str
    location: str
    description: str
