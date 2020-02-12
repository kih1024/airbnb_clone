from django import forms
from . import models

class SearchForm(forms.Form):

    city = forms.CharField(initial="Anywhere")
    price = forms.IntegerField()
    room_type = forms.ModelChoiceField(queryset=models.RoomType.objects.all())