from django import forms

from scrape_app.scrapers.factory import ScraperFactory


class ScraperForm(forms.Form):
    """Form to get the scraper name. List of scrapers is defined in the factory."""
    choices = tuple([(name, name) for name in ScraperFactory.scrapers])
    scraper_name = forms.ChoiceField(label="Select from where do you want to get the reviews", choices=choices)
