from django.db import models
from django_countries.fields import CountryField
from core import models as core_models
from users import models as user_models


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
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        user_models.User, on_delete=models.CASCADE
    )  # 일대다 관계. user가 삭제되면 해당 room도 삭제된다. models.PROTECT는 rooms 가 있으면 user는 삭제 못하게 한다.
    room_type = models.ForeignKey(
        RoomType, blank=True, on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField(Amenity, blank=True)  # 다대다 관계
    facilities = models.ManyToManyField(Facility, blank=True)  # 다대다 관계
    house_rules = models.ManyToManyField(HouseRule, blank=True)  # 다대다 관계

    def __str__(self):
        return self.name


class Photo(AbstractItem):
    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return self.caption
