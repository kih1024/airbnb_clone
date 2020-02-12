from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django_countries import countries
from . import models

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

    # context를 추가 하고 싶다면 다음과 같은 function을 사용
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     now = timezone.now()
    #     context["now"] = now
    #     return context

    # context_object_name = "rooms"


class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Room


def search(request):
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")
    instant = bool(request.GET.get("instant", False))
    superhost = bool(request.GET.get("superhost", False))

    form = {
        "city": city,
        "s_room_type": room_type,
        "s_country": country,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "instant": instant,
        "superhost": superhost,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()
    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
    }

    filter_args = {}

    if city != "Anywhere":
        filter_args["city__startswith"] = city

    filter_args["country"] = country

    # print(filter_args)

    if room_type != 0:
        filter_args["room_type__pk"] = room_type

    if price != 0:
        filter_args["price__lte"] = price
    if guests != 0:
        filter_args["guests__gte"] = guests
    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms
    if beds != 0:
        filter_args["beds__gte"] = beds
    if baths != 0:
        filter_args["baths__gte"] = baths
    if instant is True:
        filter_args["instant_book"] = True
    if superhost is True:
        filter_args["host__superhost"] = True

    rooms = models.Room.objects.filter(**filter_args)

    if len(s_amenities) > 0:
        for s_amenity in s_amenities:
            rooms = rooms.filter(amenities__pk=int(s_amenity))

    if len(s_facilities) > 0:
        for s_facility in s_facilities:
            rooms = rooms.filter(facilities__pk=int(s_facility))

    return render(request, "rooms/search.html", {**form, **choices, "rooms": rooms})


# def room_detail(request, pk):
#     try:
#         room = models.Room.objects.get(pk=pk)
#         return render(request, "rooms/detail.html", {"room": room})
#     except models.Room.DoesNotExist:
#         raise Http404()
#         # return redirect(reverse("core:home"))


# def all_rooms(request):
#     page = request.GET.get("page",1)
#     room_list = (
#         models.Room.objects.all()
#     )  # 이렇게 하면 쿼리셋만 만드는거지 데이터베이스에서 불러오는게 아님. 호출할때 그때서야 디비에서 값들을 불러옴. 매우 게으름..
#     paginator = Paginator(room_list, 10, orphans=5)
#     try:
#         rooms = paginator.page(int(page))
#         return render(request, "rooms/home.html", {"page": rooms})
#     except EmptyPage:
#         return redirect("/")
#     # print(rooms)
#     print(vars(rooms))

# 위에 것들을 반복 하고 싶지 않다 -> class based view

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
