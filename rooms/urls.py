from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("<int:pk>/", views.RoomDetail.as_view(), name="detail"),
    path("<int:pk>/edit/", views.EditRoomView.as_view(), name="edit"),
    path("<int:pk>/photos/", views.RoomPhotosView.as_view(), name="photos"),
    path("<int:pk>/photos/add/", views.AddPhotoView.as_view(), name="add-photo"),
    path("<int:room_pk>/photos/<int:photo_pk>/delete/", views.delete_photo, name="delete-photo"),
    path("<int:room_pk>/photos/<int:photo_pk>/edit/", views.EditPhotoView.as_view(), name="edit-photo"),
    path("search/", views.SearchView.as_view(), name="search"),
]
# urlpatterns = [path("<int:pk>", views.room_detail, name="detail")]
# detail은 argument(pk) 가 필요하다

# 동작 과정 : urls 등록 -> room_list.html 출력 -> 방 클릭 -> views.room_detail -> detail.html 출력
