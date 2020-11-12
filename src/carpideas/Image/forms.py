from django import forms
from .models import SearchQuery
from .models import ImageURL

class SearchForm(forms.ModelForm):
	search = forms.CharField(widget = forms.Textarea(), max_length = 255)

	class Meta:
		model = SearchQuery
		fields =['userSearchQuery', 'lastSearch','userWhoSearched']