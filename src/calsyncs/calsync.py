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

        events = self.get_events()

        iterations = max(len(events), len(trainings))

        for _ in range(iterations):
            if trainings:
                event = trainings.pop()
            elif events:
                event = events.pop()

            if isinstance(event, dict):  # training
                event_id = (
                    f"{event['trainingSlotId']}-{event['startAt'].replace(':', '')}"
                )
                cal_events = list(
                    filter(lambda x: x.icalendar_component["UID"] == event_id, events)
                )
                if not cal_events:
                    matched.append(
                        (None, event)
                    )  # training without calendar event created
                else:
                    matched.append((cal_events[0], event))  # cal. event + trianing
                    events.remove(cal_events[0])
            else:
                matched.append((event, None))

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
