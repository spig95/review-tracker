import time
import threading

from review_tracker import celery_app
from scrape_app.scrapers.factory import ScraperFactory
from scrape_app.utility.scrape_results import ScrapeResults


def aggregate_results(sr: ScrapeResults):
    timestamps, ratings = sr.get_reviews()
    aggregated_results = {
        'info_str': sr.get_info_str(),
        'timestamps': timestamps,
        'ratings': ratings,
        'done': sr.get_are_results_complete()
    }
    return aggregated_results


@celery_app.task(bind=True)
def scrape_task(self, scraper_name, url, params_dict):
    """A task to start a scraping process. This is a task with a state that allows to retrieve the results while the
    task is running.
    """
    s = ScraperFactory.get_scraper(scraper_name, url, params_dict)
    sr = ScrapeResults()
    t = threading.Thread(target=s.scrape, args=(sr,))
    t.start()

    while not sr.get_are_results_complete():
        self.update_state(
            state='PROGRESS',
            meta=aggregate_results(sr)
        )
        time.sleep(1)

    return aggregate_results(sr)
