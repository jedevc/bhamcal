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

    @property
    def uid(self):
        return self.subject_code + '/' + self.event_type[:3].upper()
