import requests
import time
import random
from contextlib import contextmanager

from .scraper import Scrapper


class DarkSideAPIScraper(Scrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._session = requests.Session()

        self._trainings = []

    @contextmanager
    def login(self):
        print("Getting trainings...")
        data = {
            "email": (None, self._username),
            "password": (None, self._password),
            "remember": (None, 0),
        }
        response = self._session.post(self.compose_url("/api/login"), files=data)
        if response.status_code != requests.codes.ok:
            raise ValueError(f"Could not login, status code: {response.status_code}")

        self._trainings = [
            training for training in response.json()["upcomingTrainings"]
        ] + [training for training in response.json()["pastTrainings"]]

        print(f"Got {len(self._trainings)}")

        yield self

        self.logout()

    def logout(self):
        print("Logging out...")
        time.sleep(random.randint(10, 60))
        self._session.get(self.compose_url("/api/logout"))
        print("Logged out")

    def get_trainings(
        self, filter_func: callable = lambda x: x["status"] == "attending"
    ):
        return list(filter(filter_func, self._trainings))
