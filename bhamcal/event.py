from datetime import datetime
from dataclasses import dataclass

@dataclass
class CalendarEvent:
    start: datetime
    end: datetime
    subject: str
    subject_code: str
    event_type: str
    location: str
    description: str
