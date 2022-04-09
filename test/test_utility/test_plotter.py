import unittest

from scrape_app.scrapers.debug import DebugScraper
from scrape_app.utility.plot import get_html_plot
from scrape_app.utility.scrape_results import ScrapeResults
from test import SKIP_DEV_TESTS


class TestPlotter(unittest.TestCase):

    @unittest.skipIf(condition=SKIP_DEV_TESTS, reason="for development")
    def test_scrape(self):
        scrape_results = ScrapeResults()
        ts = DebugScraper(url="", params_dict={"seed": "42", "n_reviews": 500})
        ts.freezetime = 0  # Fasssst
        ts.scrape(scrape_results)
        timestamps, ratings = scrape_results.get_reviews()
        html = get_html_plot(timestamps, ratings)
        with open("plot.html", 'w') as p:
            p.write(html)  # Open this file with a browser to see the plot
