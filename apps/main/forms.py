from django import forms
from django.forms import widgets


class FilterForm(forms.Form):
    """
    This form will be rendered in the invoice list page to receive from_date and to_date from the frontend to filter
    the records
    """
    from_date = forms.DateField(widget=widgets.DateInput(attrs={'type': 'date'}), )
    to_date = forms.DateField(widget=widgets.DateInput(attrs={'type': 'date'}), )
