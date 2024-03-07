from utils import get_event_id

from functools import cache
from abc import abstractmethod


class CalSync:
    EVENT_TEMPLATE = ""  # calendar event ical template

    def __init__(
        self,
        resource_url,
        username,
        password,
        calendar,
        start_date,
        end_date,
        events_filter: callable,
    ):
        self._url = resource_url
        self._username = username
        self._password = password
        self._calendar_name = calendar
        self._start_date = start_date
        self._end_date = end_date
        self.events_filter = events_filter

    @abstractmethod
    @cache
    def get_events(self) -> list:
        pass

    def match_trainings(self, trainings: list[dict]) -> list[tuple]:
        """
        Function matches trainings in a list of dicts to actual calendar events
        (`Event` objects).

        The matching itself is straight-forward, if UID of calendar event `Event`
        is equal to training from list[dict] it's a match. If there is no match at all,
        sentinel value `None` is saved instead (`sync()` depends on such format).

        (Event(...), None) - no matching training found, calendar event should be removed
        (None, {...}) - No matching event in calendar found, new one should be created

        Matches are saved into a list of tuples, where first element is `Event` and
        the second one is actual training (dict).
        """
        matched: list[tuple] = []

        events = {event.icalendar_component["UID"]: event for event in self.get_events()}
        trainings = {get_event_id(training["trainingSlotId"], training["startAt"]): training for training in trainings}

        iterations = max(len(events), len(trainings))

        uuids = [uuid for uuid in events.keys()]
        for uuid in trainings.keys():
            if uuid not in uuids:
                uuids.append(uuid)

        for uuid in uuids:
            matched.append((events.get(uuid, None), trainings.get(uuid, None)))

        return matched

    @abstractmethod
    def create_event(self, training: dict):
        pass

    @abstractmethod
    def remove_event(self, event):
        pass

    def sync(self, trainings: list[dict]):
        """
        Function synchronizes calendar and scrapper. To determine what should be
        added/removed, function `match_trainings()` is used.
        """
        for event, training in self.match_trainings(trainings):
            if None not in (event, training):
                continue

            if event is None:
                self.create_event(training)
            elif training is None:
                self.remove_event(event)
