from django.db import models

class DeviceSetting(models.Model):
    device_id = models.IntegerField(unique=True)
    warmth = models.IntegerField(default=50)
    brightness = models.IntegerField(default=50)
    contrast = models.IntegerField(default=50)

    def __str__(self):
        return f"Device {self.device_id} Settings"
