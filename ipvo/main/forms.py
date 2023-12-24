from django import forms
from .models import *

class BookFilterForm(forms.Form):
    author = forms.ModelChoiceField(queryset=Author.objects.all(), required=False, empty_label="All Authors")
    publisher = forms.ModelChoiceField(queryset=Publisher.objects.all(), required=False, empty_label="All Publishers")
    
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'abstract', 'author', 'publisher','publication_date']
