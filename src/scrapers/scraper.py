from typing import Self

from requests.compat import urljoin
from abc import abstractmethod
from contextlib import contextmanager


class Scrapper:
    def __init__(self, url, username, password):
        self._url = url
        self._username = username
        self._password = password

    def compose_url(self, endpoint):
        return urljoin(self._url, endpoint)

    @abstractmethod
    @contextmanager
    def login(self) -> Self:
        yield

    @abstractmethod
    def logout(self):
        pass

    @abstractmethod
    def get_trainings(self, filter_func: callable) -> list[dict]:
        """
        Should return list of dictionaries that represents individual training
        sessions.
        """
        pass
