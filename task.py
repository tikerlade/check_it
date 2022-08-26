from datetime import datetime
import re
import requests

from pprint import pprint


class Task:
    """
    Class to represent task object from .yaml file.
    """
    url: str
    request_int: int
    symbols_diff: int = None
    str_to_find: str = None
    completed: bool = False
    old_version: str
    new_version: str
    last_update_time: datetime = datetime.now()
    must_have = {'url', 'request_int'}

    def __new__(cls, *args, **kwargs):
        """
        Checks that provided arguments don't conflict with each other.
        """

        # Check must have fields
        if not cls.must_have.issubset(kwargs.keys()):
            return None

        # Check that either symbols_diff or request_int define, not both, both some
        request_int_defined = kwargs.get('symbols_diff', 0) > 0
        str_to_find_defined = kwargs.get('str_to_find', '') != ''

        if not (request_int_defined ^ str_to_find_defined):
            return None

        return super(Task, cls).__new__(cls)

    def __init__(self, **params):
        """
        Initializes task as Python object.
        """
        self.__dict__.update(params)
        self.old_version = self.request_url()

    def __lt__(self, other):
        return self.last_update_time < other.last_update_time

    def completed_repr(self):
        return "[green]:heavy_check_mark:" if self.completed else "[red]:cross_mark:"

    def check(self) -> bool:
        """
        Checks weather task is completed or no.
        :return: None
        """
        s1 = self.old_version
        s2 = self.request_url()

        self.last_update_time = datetime.now()
        if self.symbols_diff is not None:
            diff = sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))
            if diff > self.symbols_diff:
                self.completed = True
                return True
        elif self.str_to_find is not None:
            p = re.compile(self.str_to_find)

            if bool(re.search(p, s2)):
                self.completed = True
                return True
        return False

    def request_url(self):
        return requests.get(self.url).text
