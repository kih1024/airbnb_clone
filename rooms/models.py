from django.utils import timezone
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from core import models as core_models
from users import models as user_models
from cal import Calendar


class AbstractItem(core_models.TimeStampedModel):
    """ Abstract Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """ RoomType Model Definition """

    class Meta:
        verbose_name = "Room Type"


class Amenity(AbstractItem):
    """ Amenity Model Definition """

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):
    """ Facility Model Definition """

    class Meta:
        verbose_name_plural = "Facilites"


class HouseRule(AbstractItem):
    """ HouseRule Model Definition """

    class Meta:
        verbose_name = "House Rule"


class Room(core_models.TimeStampedModel):

    """ Room Model Definition"""

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField(help_text="How many people will be staying?")
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        user_models.User, related_name="rooms", on_delete=models.CASCADE
    )  # 일대다 관계. user가 삭제되면 해당 room도 삭제된다. models.PROTECT는 rooms 가 있으면 user는 삭제 못하게 한다.
    room_type = models.ForeignKey(
        RoomType,
        related_name="rooms",
        blank=True,
        on_delete=models.SET_NULL,
        null=True,
    )
    amenities = models.ManyToManyField(
        Amenity, related_name="rooms", blank=True
    )  # 다대다 관계
    facilities = models.ManyToManyField(
        Facility, related_name="rooms", blank=True
    )  # 다대다 관계
    house_rules = models.ManyToManyField(
        HouseRule, related_name="rooms", blank=True
    )  # 다대다 관계

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)  # 첫 글자 대문자로 저장되게 하였다.
        super().save(
            *args, **kwargs
        )  # 모델에서 save를 쓸 경우 어드민,콘솔,뷰 에서건 모델을 저장할수 있다. 하지만 사용자가 어드민에서만 저장하고 싶을때는 admin의 save_model 메소드를 이용

    def get_absolute_url(self):  # django admin 페이지에서 해당 페이지를 바로 볼수 있게 해준다
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0

        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
            return round(((all_ratings) / len(all_reviews)), 2)
        return 0

    def first_photo(self):
        try:
            (photo,) = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None

    def get_next_four_photos(self):
        photos = self.photos.all()[1:5]
        print(photos)
        return photos

    def get_calendars(self):
        now = timezone.now()
        this_year = now.year
        this_month = now.month
        next_month = (this_month + 1) % 12
        next_year = this_year
        if this_month == 12:
            next_year = this_year + 1
        this_month_calendar = Calendar(this_year, this_month)
        next_month_calendar = Calendar(next_year, next_month)
        return [this_month_calendar, next_month_calendar]


class Photo(core_models.TimeStampedModel):
    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey(Room, related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption
