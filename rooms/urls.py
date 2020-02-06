from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [path("<int:pk>", views.room_detail, name="detail")]
# detail은 argument(pk) 가 필요하다

# 동작 과정 : urls 등록 -> room_list.html 출력 -> 방 클릭 -> views.room_detail -> detail.html 출력
