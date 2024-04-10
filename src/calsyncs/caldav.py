import pytz
import random
import caldav

from functools import cache
from dateutil import parser
from icalendar import Event
from datetime import datetime, timedelta

from .calsync import CalSync
from utils import get_event_id, EVENTID_CALSYNC_PREFIX

class CalDav(CalSync):
    EVENT_TEMPLATE = """
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Sabre//Sabre VObject 4.4.2//EN
CALSCALE:GREGORIAN
BEGIN:VEVENT
SUMMARY:{title}
DTSTART;TZID={tz}:{event_start}
DTEND;TZID={tz}:{event_end}
DTEND:{event_end}
UID:{uid}
SEQUENCE:0
CREATED:{created}
LAST-MODIFIED:{created}
LOCATION:Böhmova 11\nBrno\, Czechia
TRANSP:OPAQUE
URL;VALUE=URI:
X-TITLE=Böhmova 11:
X-APPLE-TRAVEL-DURATION;VALUE=DURATION:PT15M
END:VEVENT
END:VCALENDAR
"""

    def __init__(
        self,
        *args,
        events_filter: callable = lambda x: EVENTID_CALSYNC_PREFIX in x.data,
        **kwargs,
    ):
        super().__init__(*args, events_filter=events_filter, **kwargs)

        client = caldav.DAVClient(
            url=self._url, username=self._username, password=self._password
        )
        principal = client.principal()

        calendars = principal.calendars()
        for calendar in calendars:
            if calendar.name == self._calendar_name:
                self._calendar = calendar
                break
        else:
            raise KeyError(f"Could not get calendar: {self._calendar_name}")

        self._fmt = "%Y%m%dT%H%M%SZ"
        self.tz = pytz.timezone("Europe/Prague")

    @cache
    def get_events(self):
        raw_events = self._calendar.date_search(self._start_date, self._end_date)
        return list(filter(self.events_filter, raw_events))

    def _get_date_from_training(self, raw_date: str):
        """
        Transforms ISO datetime to string in format: "%Y%m%dT%H%M%SZ"
        """

        parsed = parser.parse(raw_date)

        return parsed.strftime(self._fmt)

    def create_event(self, training):
        if training["startAt"] < datetime.now().isoformat():
            return

        print("Creating event ", training)

        event_start_str = self._get_date_from_training(training["startAt"])
        event_end_str = self._get_date_from_training(training["endAt"])

        created = datetime.now().strftime(self._fmt)

        self._calendar.save_event(
            self.EVENT_TEMPLATE.format(
                title=training["name"],
                uid=get_event_id(training["trainingSlotId"], training["startAt"]),
                event_start=event_start_str,
                event_end=event_end_str,
                tz=self.tz.zone,
                created=created,
            )
        )

    def remove_event(self, event):
        print("Removing event: ")
        print(event.data)
        try:
            event.delete()
        except:
            print(f"Could not remove {event.data}")
            raise
