from typing import Dict, List

from scrape_app.scrapers.base import Scraper, ScraperParameter
from scrape_app.scrapers.tripadvisor import TripAdvisorScraper
from scrape_app.scrapers.debug import DebugScraper


class ScraperFactory:
    """Scraper factory.

    It defines which scrapers are available through the scrapers dictionary, along with some methods to get
    scraper information and to instantiate a new scraper.
    """
    scrapers: Dict[str, type(Scraper)] = {
        "TripAdvisor": TripAdvisorScraper,
        "Debug": DebugScraper,
    }
    """List of all scrapers that can be used by Django to build the web interface."""

    @classmethod
    def is_scraper_available(cls, scraper_name):
        return scraper_name in cls.scrapers

    @classmethod
    def get_scraper_cls(cls, scraper_name) -> type(Scraper):
        assert cls.is_scraper_available(scraper_name), f"{scraper_name} is not available. Check {cls.scrapers}"
        return cls.scrapers[scraper_name]

    @classmethod
    def get_scraper_params(cls, scraper_name) -> List[ScraperParameter]:
        scraper_cls = cls.get_scraper_cls(scraper_name)
        params = scraper_cls.parameters
        return params

    @classmethod
    def get_scraper_param_by_name(cls, scraper_name, param_name):
        """Gets the scraper called scraper_name and retrieves its parameter with name param_name. Raise errors if
        scraper_name is not available or if it does not have a parameter called param_name"""
        params = cls.get_scraper_params(scraper_name)
        for p in params:
            if p.name == param_name:
                return p
        raise ValueError(f"{scraper_name} does not have a parameter with {param_name}")

    @classmethod
    def get_param_displayed_name(cls, scraper_name, param_name):
        param = cls.get_scraper_param_by_name(scraper_name, param_name)
        return param.displayed_name

    @classmethod
    def get_scraper(cls, scraper_name, url, params_dict):
        scraper_cls = cls.get_scraper_cls(scraper_name)
        return scraper_cls(url, params_dict)
