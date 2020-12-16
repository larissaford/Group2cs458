from django import forms
from .models import SearchQuery
from .models import ImageURL


class searchForm(forms.Form):

    search = forms.CharField(max_length=100)
    class Meta:
        model =SearchQuery

        fields=['userSearchQuery','lastSearched']