import unittest

from scrape_app.scrapers.base import Scraper
from scrape_app.scrapers.debug import DebugScraper
from scrape_app.scrapers.factory import ScraperFactory


class TestScraperParameters(unittest.TestCase):
    def test_unknown_param(self):
        params_dict = {"a": 1}
        self.assertRaises(ValueError, Scraper, url="www.google.com", params_dict=params_dict)
        self.assertRaises(ValueError, DebugScraper, url="www.google.com", params_dict=params_dict)
        self.assertRaises(
            ValueError, DebugScraper, url="www.google.com", params_dict={"seed": "wrong", "n_reviews": 10})

    def test_correct_params_dict(self):
        dbg_scraper = DebugScraper(url="www.google.com", params_dict={"n_reviews": 1000, "seed": "42"})
        self.assertEqual(dbg_scraper.n_reviews, 1000)
        self.assertEqual(dbg_scraper.seed, 42)

    def test_scraper_parameter_consistency(self):
        """Automated test for scraper in the factory. Checks that when the parameters are consistent"""
        for scraper_name, scraper_cls in ScraperFactory.scrapers.items():
            params_dict = {}
            for param in ScraperFactory.get_scraper_params(scraper_name):
                if param.param_type == "choice":
                    value = param.options_as_str[0]
                else:
                    value = "dummy"
                params_dict[param.name] = value
            scraper_cls.validate_params_dict(params_dict)

            # Add a parameter that should raise an exception because it does not exist
            params_dict["TEST_PARAMETER_KEY_12345_THIS_SHOULD_NOT_EXIST"] = "dummy"
            self.assertRaises(ValueError, scraper_cls.validate_params_dict, params_dict)

    def test_scraper_parameters_are_unique(self):
        """Automated test for all scrapers in the factory. Checks that when the parameters have unique names"""
        for scraper_name, scraper_cls in ScraperFactory.scrapers.items():
            params_names = [p.name for p in scraper_cls.parameters]
            self.assertEqual(
                len(params_names),
                len(set(params_names)),
                f"{params_names} contains duplicates. Please fix {scraper_name} scraper!"
            )
