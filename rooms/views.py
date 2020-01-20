from . import models
from django.shortcuts import render

# from django.http import HttpResponse


def all_rooms(request):
    # now = datetime.now()
    # hungry = True
    # return HttpResponse(content=f"<h1>{now}</h1>")
    all_rooms = models.Room.objects.all()
    return render(request, "rooms/home.html", context={"rooms": all_rooms})


# Create your views here.
