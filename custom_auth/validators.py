import re
from django import forms
from custom_auth.costants import NAME_SEARCH_PATTERN


def name_validator(value):
    res = re.search(NAME_SEARCH_PATTERN, value)
    if not res:
        raise forms.ValidationError("Invalid format name")
