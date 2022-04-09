import datetime
import unittest
import matplotlib.pyplot as plt

from scrape_app.scrapers.debug import DebugScraper
from scrape_app.scrapers.tripadvisor import TripAdvisorScraper
from scrape_app.utility.helpers import moving_avg_timebased
from scrape_app.utility.plot import get_html_plot
from scrape_app.utility.scrape_results import ScrapeResults
from test import SKIP_DEV_TESTS


class TestTripAdvisorScraper(unittest.TestCase):
    def setUp(self):
        self.valid_urls = [
            "https://www.tripadvisor.it/Restaurant_Review-g194883-d1858834-Reviews-Ristorante_Lago_D_oro-Riva_Del_Garda_Province_of_Trento_Trentino_Alto_Adige.html",
            "https://www.tripadvisor.com.br/Restaurant_Review-g194883-d1858834-Reviews-Ristorante_Lago_D_oro-Riva_Del_Garda_Province_of_Trento_Trentino_Alto_Adige.html",
            "https://www.tripadvisor.ca/Restaurant_Review-g194883-d1858834-Reviews-Ristorante_Lago_D_oro-Riva_Del_Garda_Province_of_Trento_Trentino_Alto_Adige.html"
        ]
        self.wrong_urls = [
            "https://restaurantguru.com/Ristorante-Lago-Doro-Riva-del-Garda"
        ]

    def test_is_valid_url(self):
        for url in self.wrong_urls:
            self.assertRaises(ValueError, TripAdvisorScraper, url, params_dict={"lang": "all"})

    @unittest.skipIf(condition=SKIP_DEV_TESTS, reason="for development")
    def test_scrape(self):
        urls = [
            "https://www.tripadvisor.com/Restaurant_Review-g187849-d3650443-Reviews-Ristorante_Pizzeria_Da_Marco-Milan_Lombardy.html"
        ]
        scrape_results = ScrapeResults()
        for url in urls:
            ts = DebugScraper(url=url, params_dict={"seed": "42", "n_reviews": 10})
            ts.scrape(scrape_results)
            timestamps, ratings = scrape_results.get_reviews()
            get_html_plot(timestamps, ratings)
            delta_days = 60
            a, _, _ = moving_avg_timebased(timestamps, ratings, delta_days)
            plt.title(f"Reviews moving average over {delta_days} days")
            datetimes = [datetime.datetime.fromtimestamp(ts) for ts in timestamps]
            plt.plot(datetimes, ratings, 'o-', lw=0.75)
            plt.plot(datetimes, a)
            plt.show()
            plt.close()
