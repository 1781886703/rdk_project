from django.db import models

class DeviceSetting(models.Model):
    device_id = models.IntegerField(unique=True)
    warmth = models.IntegerField(default=50)
    brightness = models.IntegerField(default=50)
    contrast = models.IntegerField(default=50)

    def __str__(self):
        return f"Device {self.device_id} Settings"

class RecordingStatus(models.Model):
    is_recording = models.BooleanField(default=False)
    recorded_time = models.IntegerField(default=0)  # 存储已录制时长，单位为秒
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Recording: {self.is_recording}, Time: {self.recorded_time}s"
