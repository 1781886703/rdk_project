# models.py
from django.db import models

class DeviceSetting(models.Model):
    device_id = models.IntegerField(unique=True)
    warmth = models.IntegerField(default=50)
    brightness = models.IntegerField(default=50)
    contrast = models.IntegerField(default=50)

    def __str__(self):
        return f"Device {self.device_id} Settings"

class RecordingStatus(models.Model):
    device_id = models.IntegerField(unique=True)  # 设备 ID
    is_recording = models.BooleanField(default=False)
    # start_time = models.DateTimeField(null=True, blank=True)  # 记录开始时间

    def __str__(self):
        return f"Device {self.device_id} - Recording: {self.is_recording}"
    
class Recording(models.Model):
    start_time = models.DateTimeField()
    total_time = models.IntegerField()  # Total time in seconds

    def __str__(self):
        return f"Recording started at {self.start_time}, total time: {self.total_time} seconds"