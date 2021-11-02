from django import forms
from django.forms.widgets import Textarea
from .models import *


class PostForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'What is in you mind today?'}))

    required_css_class = "required"
