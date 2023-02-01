from django.db import models
from datetime import time

# Create your models here.
class TelegramUser(models.Model):
    telegramChatID = models.IntegerField()
    telegramUserID = models.IntegerField()
    telegramUsername = models.CharField(max_length=255)
    notificationStartTime = models.TimeField(default=time(0, 0, 0))
    notificationEndTime = models.TimeField(default=time(23,59,59))

    def __str__(self) -> str:
        return self.telegramUsername

class Light(models.Model):
    isOn = models.BooleanField(default=False)
    registeredUsers = models.ManyToManyField(TelegramUser)
    motionDetected = models.BooleanField(default=False)
    luxLevel = models.IntegerField(default=0)
    overrideMotionSensor = models.BooleanField(default=False)
    numberOfOkays = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'Light {self.id}'