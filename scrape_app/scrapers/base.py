from abc import ABC
from typing import List

from scrape_app.scrapers.scraper_parameter.scraper_parameter import ScraperParameter
from scrape_app.utility.scrape_results import ScrapeResults


class Scraper(ABC):
    """Base class that serves as an interface for all scrapers.  Here there are some important steps on how you can
    generate a new scraper.

    1) Define the scraper parameters

    A scraper can have parameters that will be displayed by the front-end to the user. These parameters are implemented
    by the ScraperParameter class. In particular, to create a new scraper called MyCoolScraper with a choice
    parameter, you can do as follows:

    >>> class MyCoolScraper(Scraper):
    >>>        parameters = [
    >>>             ScraperParameter(
    >>>                 name="my_param_key",
    >>>                 displayed_name="Parameter",
    >>>                 param_type="choice",
    >>>                 options=['option 1', 'option 2']
    >>>             )]

    .. note:: you can make sure if you have setup the parameters correctly by running the tests in TestScraperParameters

    2) Use scraper parameters

    The scraper parameters values can be accessed in the init method. In particular, when the scraper is initialized,
    params_dict contains the parameters with the values selected by the user in the front-end.

    >>> # Inside MyCoolScraper, init method
    >>>     def __init__(self, url, params_dict):
    >>>         super(Scraper, self).__init__(url, params_dict)
    >>>         self.my_param = params_dict["my_param_key"]

    3) Implement scrape() method

    Your custom scraper must implement the scrape() method, see the documentation of Scraper.scrape() for more details.

    4) Add the scraper to the front-end

    Adding the scraper to the front-end is really simple. You just need to add an entry in ScraperFactory.scrapers with
    a nice name for your scraper. After this, the Django view that renders the main page will start using your scraper,
    giving it as an option to the user.
    """

    parameters: List[ScraperParameter] = list()
    """List of parameters that the user can choose from. When you extent this list, the parameter name must be present
    in params_dict (see Scraper init method)."""

    def __init__(self, url, params_dict=None):
        """Init method.

        :param url: url from which one wants to scrape the reviews
        :param params_dict: dictionary with parameter values. The keys must correspond to the names of the
            self.parameters. The parameters values are chosen by the user in the web interface.
            When implementing a new scraper, you can add a new parameter appending it to self.parameters, and then you
            can fetch its value in the init by accessing the associated key in params_dict.
            That is: params_dict[param.name]. A complete example is given in DebugScraper.
        """
        self.initial_url = url  # Child classes should validate the url
        self.validate_params_dict(params_dict)
        self.params_dict = params_dict

    def scrape(self, scrape_results: ScrapeResults):
        """Use this method to get reviews and ratings.

        This method must update scrape_results and does not have to return anything. Read the documentation of
        ScrapeResults to get to know how to update scrape_results, or have a look at DebugScraper for an example.

        :param scrape_results: use this class to store the results of the scraping
        """
        raise NotImplementedError("Base class does not implement this method.")

    @classmethod
    def get_param_names(cls):
        return [p.name for p in cls.parameters]

    @classmethod
    def get_param_by_name(cls, param_name):
        for param in cls.parameters:
            if param_name == param.name:
                return param
        raise ValueError(f"Found no parameter with name {param_name} in {cls.get_param_names()}")

    @classmethod
    def validate_params_dict(cls, params_dict):
        """Params_dict is valid when all keys correspond with parameter names. For each key in params_dict, there must
        be a parameter with the key name, and viceversa.
        """
        if params_dict is None and cls.parameters:
            raise ValueError(f"Empty params_dict, specify the value of the following scraper parameters: "
                             f"{sorted(cls.get_param_names())}")

        if not sorted(params_dict.keys()) == sorted(cls.get_param_names()):
            raise ValueError(f"Make sure params_dict matches with the list of parameters. "
                             f"{sorted(params_dict.keys())} != {sorted(cls.get_param_names())}")

        for param_name, param_value in params_dict.items():
            param = cls.get_param_by_name(param_name)
            param.validate_value(param_value)
