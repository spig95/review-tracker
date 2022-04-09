import time

import numpy as np

from scrape_app.utility.date_utils import get_timestamp
from scrape_app.scrapers.base import Scraper, ScraperParameter


class DebugScraper(Scraper):
    """A very simple scraper. This has been used to develop the Django code, and can be used to see a complete example
    of how to implement a Scraper. In particular, how to use ScraperParameter and how to work with ScrapeResults."""
    parameters = [
        ScraperParameter(
            name="seed",
            displayed_name="Random seed",
            param_type="choice",
            options=[1, 42, 1995, 987654321]
        ),
        ScraperParameter(
            name="n_reviews",
            displayed_name="N. Fake Reviews",
            param_type="integer"
        ),
    ]
    freezetime = 0.1
    """Simulate how much time we need to get one review."""

    def __init__(self, url, params_dict):
        super(DebugScraper, self).__init__(url, params_dict)
        self.seed = int(params_dict["seed"])
        self.n_reviews = int(params_dict["n_reviews"])

    def scrape(self, scrape_results):
        """Toy implementation of scrape"""
        np.random.seed(self.seed)

        for i in range(self.n_reviews):
            time.sleep(self.freezetime)  # Simulate some request time
            timestamp, rating = self.get_random_ts_and_rating()
            scrape_results.append_review(timestamp, rating)

        # Very important, finalize results at the end!
        scrape_results.finalize()

    @staticmethod
    def get_random_ts_and_rating():
        """Generate a random timestamp and a random vote between 0 and 5. The vote increases through time with random
        oscillations.
        """
        year = np.random.randint(2013, 2018)
        month = np.random.randint(12) + 1
        day = np.random.randint(28) + 1
        timestamp = get_timestamp(year, month, day)
        avg = 3 + (year + month / 12 - 2013) / 5
        rating = avg + np.random.uniform(1)
        return timestamp, rating
