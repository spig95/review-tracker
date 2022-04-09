import threading

import numpy as np

from scrape_app.utility.date_utils import order_by_time
from scrape_app.utility.plot import get_html_plot


class ScrapeResults:
    """A thread-safe class to store timestamps and ratings. Provides get methods and info strings."""
    def __init__(self):
        self._ratings = []
        self._timestamps = []
        self._done = False
        self._custom_info_str = None
        self._lock = threading.Lock()

    def append_review(self, ts, rating):
        with self._lock:
            self._timestamps.append(round(ts, 3))
            self._ratings.append(round(rating, 2))

    def finalize(self):
        with self._lock:
            self._done = True

    def is_empty(self):
        with self._lock:
            return not self._ratings or not self._timestamps

    def get_are_results_complete(self):
        with self._lock:
            return self._done

    def set_info_str(self, s):
        with self._lock:
            self._custom_info_str = s

    def get_info_str(self):
        with self._lock:
            if self._custom_info_str is not None:
                return self._custom_info_str
        if self._done:
            return f"Scraping finished! Got a total of {len(self._ratings)}!"
        else:
            return f"Scraping in progress... got {len(self._ratings)} so far."

    def get_reviews(self) -> (list, list):
        """Return two lists, one for timestamps and one for ratings"""
        with self._lock:
            timestamps, ratings = self._timestamps.copy(), self._ratings.copy()
        timestamps, ratings = order_by_time(timestamps, ratings)
        return timestamps, ratings
