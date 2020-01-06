from django.db import models
from core import models as core_models


class Conversation(core_models.TimeStampedModel):
    participants = models.ManyToManyField("users.user", blank=True)

    def __str__(self):
        return str(self.created)


# Create your models here.


class Message(core_models.TimeStampedModel):

    message = models.TextField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    conversation = models.ForeignKey("Conversation", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} says: {self.message}"

