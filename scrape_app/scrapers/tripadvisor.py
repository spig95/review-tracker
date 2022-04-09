import random

import dateparser
import numpy as np
import urllib.parse

from scrape_app.scrapers.base import Scraper, ScraperParameter
from scrape_app.utility.date_utils import get_timestamp
from scrape_app.utility.headers import tripadvisor_headers
from scrape_app.utility.logger import log
from scrape_app.utility.scrape_results import ScrapeResults
from scrape_app.utility.web_utils import get_soup


class TripAdvisorScraper(Scraper):
    """Scraper for TripAdvisor restaurants"""
    parameters = [
        ScraperParameter(
            name="lang",
            displayed_name="Consider only reviews in language:",
            param_type="choice",
            options=["all", "english", "italian", "portuguese", "spanish", "french", "german"],
        )
    ]

    # One extension for each "known" language (lang options)
    known_extensions = {
        "english": ".com",
        "italian": ".it",
        "portuguese": ".com.br",
        "spanish": ".es",
        "french": ".fr",
        "german": ".de"
    }

    def __init__(self, url, params_dict):
        super(TripAdvisorScraper, self).__init__(url, params_dict)
        self.lang = params_dict["lang"]

        o = urllib.parse.urlsplit(url)
        if "tripadvisor" not in o.netloc:
            raise ValueError(f"The url does not correspond to a restaurant on Tripadvisor. Got {url}")

        self.base_url = f"{o.scheme}://{o.netloc}"
        """Starting part of the url. For instance: https://www.tripadvisor.com."""

        self.restaurant_path = o.path
        """Restaurant path, to be added to self.base_url to get the restaurant."""

    def scrape(self, scrape_results):
        extension = "." + self.base_url.split(".")[-1]
        no_extension_url = self.base_url[:-len(extension)]

        if self.lang == "all":
            desired_lang_extensions = self.known_extensions.values()
        elif self.lang in self.known_extensions:
            desired_lang_extensions = [self.known_extensions[self.lang]]
        else:
            raise KeyError(f"Unexpected value of {self.lang}. Not in {self.known_extensions}")

        # Each of these corresponds to a different languages
        for e in desired_lang_extensions:
            specific_language_url = no_extension_url + e
            self.scrape_all_pages(specific_language_url, self.restaurant_path, scrape_results)

        # Very important: finalize scrape_results!
        scrape_results.finalize()

    @staticmethod
    def scrape_all_pages(base_url, restaurant_path, scrape_results: ScrapeResults):
        """Scrape all the reviews looking for all the page numbers. base_url specifies the language of the reviews.

        :param base_url: url of Tripadvisor, ending with a specific language extension
        :param restaurant_path: path of the restaurant. To get the restaurant, do base_url + restaurant_path
        :param scrape_results: structure to store results
        """
        restaurant_url = base_url + restaurant_path
        soup = get_soup(restaurant_url, TripAdvisorScraper.get_headers())

        # Loop until we do not finish the pages
        last_num = 1
        page_num = 1
        while page_num <= last_num:
            soup = TripAdvisorScraper.get_soup_from_page_num(base_url, soup, page_num)
            if soup is None:
                # Not able to find the next soup
                break
            TripAdvisorScraper.scrape_single_page(soup, scrape_results)
            if page_num == last_num:
                # Update page num if we find more pages
                last_num = TripAdvisorScraper.get_last_page_num(soup)
            page_num += 1  # Update page to scrape

    @staticmethod
    def scrape_single_page(soup, scrape_results) -> (np.array, np.array):
        """Given a html page with reviews, return the scraped reviews

        :return timestamps, ratings: array of timestamps (seconds), ratings are floats
        :rtype: (np.array, np.array)
        """
        # Get divs with reviews
        review_containers = soup.findAll("div", {"class": "review-container"})

        for rev in review_containers:
            rating = rev.find("span", {"class": "ui_bubble_rating"})
            date = rev.find("span", {"class": "ratingDate"})
            rating = TripAdvisorScraper.process_rating(rating)
            ts = TripAdvisorScraper.process_date(date)
            scrape_results.append_review(ts, rating)

        return scrape_results.get_reviews()

    @staticmethod
    def get_last_page_num(soup):
        """Not all the pages have class_='pageNum last', so we use this function """
        page_num_elems = soup.findAll("a", class_="pageNum")
        # Normally are 1, 2, 3, ..., N
        visible_page_numbers = [int(elem["data-page-number"]) for elem in page_num_elems]
        if visible_page_numbers:
            return max(visible_page_numbers)  # Last page is always included
        else:
            return 1

    @staticmethod
    def get_soup_from_page_num(base_url, this_page_soup, page_num):
        """Get the link of page_num and return corresponding soup. We return None if no soup relative to page_num is
        found
        """
        pages_soup = this_page_soup.find("div", class_="pageNumbers")
        if pages_soup is None:
            return None

        if page_num == "first" or page_num == "last":
            # This works since we pass only one keyword as a class and we don't need anything else
            # Warning: not all tripadvisor webpages have "last" elem
            next_page_elem = pages_soup.find("a", class_=page_num)
        elif type(page_num) == int:
            next_page_elem = pages_soup.find("a", {"data-page-number": str(page_num)})
        else:
            raise ValueError(f"Got unexpected '{page_num}'.")

        if next_page_elem is None:
            raise RuntimeError(f"Cannot find next page with '{page_num}'.")
        next_page_href = next_page_elem["href"]
        next_page_url = f"{base_url}/{next_page_href}"
        return get_soup(next_page_url, TripAdvisorScraper.get_headers())

    @staticmethod
    def process_rating(rating) -> float:
        """Get rating, considering that Tripadvisor rating has the following form:
            <span class="ui_bubble_rating bubble_10"></span>
        """
        log.debug(rating)
        class_list = rating["class"]
        bubble_class = [c for c in class_list if c.startswith("bubble_")]
        try:
            assert len(bubble_class) == 1, class_list
            bubble_str = bubble_class[0]
            rating = bubble_str[7:]
            return float(rating) / 10
        except Exception as e:
            raise e

    @staticmethod
    def process_date(date) -> float:
        """Returns datetime. Tripadvisor format is 'month day, year'. We return timestamp. See get_timestamp()."""
        log.debug(date)
        date_str = date["title"]
        datetime = dateparser.parse(date_str)
        return get_timestamp(datetime.year, datetime.month, datetime.day)

    @staticmethod
    def get_headers():
        return random.choice(tripadvisor_headers.headers_list)
