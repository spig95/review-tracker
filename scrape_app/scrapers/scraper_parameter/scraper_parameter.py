from typing import List, Union

from scrape_app.scrapers.scraper_parameter.param_types_mapping import param_types_mapping


class ScraperParameter:
    """Class that represents a parameter for a Scraper. It allows the user to specify new parameters that can be used
    in a Scraper.

    See the documentation of Scraper to see how one can add a parameter to a scraper. If you add it in the correct way,
    the Django application will add a form to allow the user to select the parameter value.
    """
    def __init__(self,
                 name,
                 displayed_name,
                 param_type="generic",
                 options: Union[List, None] = None
                 ):
        """Init.

        :param name: name of the parameter. Things to consider:
            - the name is used by the backend as a unique identifier of the parameter, a Scraper cannot have two
              parameters with the same name
            - this is the name that will be used by Django in params_dict (the argument of Scraper.__init__)
        :param displayed_name: the name that the end-user will see on the front-end
        :param param_type (optional): defines the type and the Django field that will be displayed to the user. Choose
            among the ones in param_types_mapping
        :param options: (optional) if the parameter type is 'choice', you should use this list to list all the options
        """
        if param_type not in param_types_mapping:
            raise ValueError(f"{param_type} not known. Error during parameter {name} initialization.")

        if param_type != "choice" and options:
            raise ValueError(f"Error during {name} initialization. Don't put a list of options if "
                             f"param_type != 'choice'. Got {param_type}, {options}")

        self.name = name
        self.displayed_name = displayed_name
        self.param_type = param_type
        self.django_field_cls = param_types_mapping[param_type]
        self.options_as_str = [str(o) for o in options] if options else []

    def validate_value(self, value):
        # TODO: automatically validate also for the other available types
        if self.param_type == "choice" and value not in self.options_as_str:
            raise ValueError(
                f"Got {value}. Not a valid option for parameter '{self.name}'. Options: ({self.options_as_str})")
