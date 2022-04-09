from django import forms

param_types_mapping = {
    "generic": forms.Field,
    "char": forms.CharField,
    "integer": forms.IntegerField,
    "boolean": forms.BooleanField,
    "choice": forms.ChoiceField,
}
"""A mapping from a string to the Django form type that will be rendered in the web-page. This does not cover
all the possible form fields, but one can easily add the required field to this dictionary."""