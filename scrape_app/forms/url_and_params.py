from django import forms

from scrape_app.scrapers.factory import ScraperFactory
from scrape_app.utility.logger import log


class URLAndParamsForm(forms.Form):
    """Form to get the URL of the website to scrape and the parameters specific to a scraper"""
    def __init__(self, *args, **kwargs):
        """
        :param scraper_name: name of the scraper to be used. Check the scraper factory for the list.
            This is not an explicit kwarg, the reason is explained here
            https://stackoverflow.com/questions/14322185/django-form-init-got-multiple-values-for-keyword-argument
        """
        self.scraper_name = kwargs.pop("scraper_name", None)
        log.debug(f"Instantiating URLAndParamsForm for scraper: {self.scraper_name}")
        super(URLAndParamsForm, self).__init__(*args, **kwargs)

        # All the scrapers have URL as parameter
        self.fields["url"] = forms.URLField(label="Restaurant URL")

        log.debug(f"Getting all the scraper-specific parameters")
        self.params_list = ScraperFactory.get_scraper_params(self.scraper_name)
        log.debug(f"This scraper thas the following parameters {[p.name for p in self.params_list]}")

        # Add a field in the form. The fields to be added are defined in the parameters of the scraper.
        # The name of the field is obtained via get_param_displayed_name.
        for param in self.params_list:
            displayed_name = ScraperFactory.get_param_displayed_name(self.scraper_name, param.name)
            if param.django_field_cls == forms.ChoiceField:
                choices_double = [(c, c) for c in param.options_as_str]  # This is what we need for Django
                self.fields[param.name] = param.django_field_cls(label=displayed_name, choices=choices_double)
            else:
                self.fields[param.name] = param.django_field_cls(label=displayed_name)

        # Add class to all fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-field'})

    def get_scraper_name(self):
        return self.scraper_name

    def get_url_to_scrape(self):
        return self.cleaned_data["url"]

    def get_scraper_params_dict(self):
        params_dict = dict()
        for p in self.params_list:
            params_dict[p.name] = self.cleaned_data[p.name]
        return params_dict
