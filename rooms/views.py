from math import ceil
from . import models
from django.shortcuts import render

# from django.http import HttpResponse


def all_rooms(request):
    # now = datetime.now()
    # hungry = True
    # return HttpResponse(content=f"<h1>{now}</h1>")
    # print(request.GET)
    page = int(request.GET.get("page", 1))
    page = int(page or 1)
    page_size = 10
    limit = page_size * page
    offset = limit - page_size
    all_rooms = models.Room.objects.all()[offset:limit]
    page_count = ceil(models.Room.objects.count() / page_size)
    return render(
        request,
        "rooms/home.html",
        context={
            "rooms": all_rooms,
            "page": page,
            "page_count": page_count,
            "page_range": range(1, page_count + 1),
        },
    )


# Create your views here.
