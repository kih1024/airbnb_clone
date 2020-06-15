from django.db import models
from . import managers

# Create your models here.
class TimeStampedModel(models.Model):
    """ Time Stamped Model"""

    created = models.DateTimeField(auto_now_add=True)
    # 모델을 디비에 적용할때 현재 시간 날짜 저장
    updated = models.DateTimeField(auto_now=True)
    # 저장 할때마다 updated 모델에 현재 date 그리고 시간 저장
    # 모델 이지만 데이터베이스에 나타나지 않는 모델
    
    objects = managers.CustomModelManager()

    class Meta:
        abstract = True
