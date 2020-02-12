from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django_countries import countries
from . import models, forms

# from django.http import Http404
# from django.shortcuts import render

# from django.shortcuts import render, redirect
# from django.core.paginator import Paginator, EmptyPage

# from django.http import HttpResponse

# https://ccbv.co.uk/projects/Django/3.0/django.views.generic.list/ListView/  참고
class HomeView(ListView):

    """ HomeView Definiton """

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"


class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Room


def search(request):

    form = forms.SearchForm()

    return render(request, "rooms/search.html", {"form": form})



