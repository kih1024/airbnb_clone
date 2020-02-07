from . import models
from django.views.generic import ListView, DetailView
from django.shortcuts import render

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
    city = request.GET.get("city")
    city = str.capitalize(city)
    return render(request, "rooms/search.html", {"city": city})


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
