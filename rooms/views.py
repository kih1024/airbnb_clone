from math import ceil
from . import models
from django.shortcuts import render
from django.core.paginator import Paginator

# from django.http import HttpResponse


def all_rooms(request):
    page = request.GET.get("page")
    room_list = (
        models.Room.objects.all()
    )  # 이렇게 하면 쿼리셋만 만드는거지 데이터베이스에서 불러오는게 아님. 호출할때 그때서야 디비에서 값들을 불러옴. 매우 게으름..
    paginator = Paginator(room_list, 10)
    rooms = paginator.get_page(page)
    # print(rooms)
    print(vars(rooms))
    return render(request, "rooms/home.html", {"rooms": rooms})

    # print(vars(rooms.paginator))
    # page = int(page or 1)
    # page_size = 10
    # limit = page_size * page
    # offset = limit - page_size
    # all_rooms = models.Room.objects.all()[offset:limit]
    # page_count = ceil(models.Room.objects.count() / page_size)
    # context={
    #     "rooms": all_rooms,
    #     "page": page,
    #     "page_count": page_count,
    #     "page_range": range(1, page_count + 1),
    # },


# Create your views here.
