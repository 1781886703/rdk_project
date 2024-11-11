from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.utils import timezone
import random  # 模拟温度数据
import json
from .models import DeviceSetting
@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        file_path = 'latest_image.jpg'
        
        if default_storage.exists(file_path):
            default_storage.delete(file_path)
        path = default_storage.save(file_path, ContentFile(image.read()))

        return JsonResponse({'status': 'success'}, status=200)
    return JsonResponse({'status': 'failed'}, status=400)

def display_page(request):
    # 模拟设备信息和设置
    devices = [
        {"id": 1, "name": "设备1", "status": "正常", "temperature": round(random.uniform(20, 30), 1), "image_url": "/media/latest_image.jpg", 
         "settings": {"warmth": 50, "brightness": 60, "contrast": 70}},
        {"id": 2, "name": "设备2", "status": "正常", "temperature": round(random.uniform(20, 30), 1), "image_url": "/media/camera2.jpg",
         "settings": {"warmth": 40, "brightness": 50, "contrast": 60}},
        {"id": 3, "name": "设备3", "status": "异常", "temperature": round(random.uniform(20, 30), 1), "image_url": "/media/camera3.jpg",
         "settings": {"warmth": 30, "brightness": 40, "contrast": 50}},
        {"id": 4, "name": "设备4", "status": "正常", "temperature": round(random.uniform(20, 30), 1), "image_url": "/media/camera4.jpg",
         "settings": {"warmth": 20, "brightness": 30, "contrast": 40}},
    ]
    
    selected_device = devices[0]  # 默认选择设备1，可根据需求动态修改

    statistics = {
        "redLights": 2,
        "greenLights": 10,
        "electricCars": 9,
        "cars": 17,
        "totalTraffic": 21,
        "startTime": "08:00",
        "endTime": "18:00",
    }

    recording_status = {
        "recordedTime": 158,
    }

    recording_settings = {
        "segmentTime": 60,
        "totalTime": 300,
        "location": "深圳大学",
    }

    return render(request, 'display.html', {
        "devices": devices,
        "selected_device": selected_device,
        "statistics": statistics,
        "recording_status": recording_status,
        "recording_settings": recording_settings,
        "timestamp": timezone.now().timestamp()
    })

# 假设这是一个内存字典用于保存设备设置，实际生产中应使用数据库
device_settings = {
    1: {"warmth": 50, "brightness": 60, "contrast": 70},
    2: {"warmth": 40, "brightness": 50, "contrast": 60},
    3: {"warmth": 30, "brightness": 40, "contrast": 50},
    4: {"warmth": 20, "brightness": 30, "contrast": 40},
}

def select_device(request, device_id):
    # 查找设备信息并返回
    devices = {
        1: {"name": "设备1", "settings": {"warmth": 50, "brightness": 60, "contrast": 70}},
        2: {"name": "设备2", "settings": {"warmth": 40, "brightness": 50, "contrast": 60}},
        3: {"name": "设备3", "settings": {"warmth": 30, "brightness": 40, "contrast": 50}},
        4: {"name": "设备4", "settings": {"warmth": 20, "brightness": 30, "contrast": 40}},
    }

    selected_device = devices.get(int(device_id))
    if selected_device:
        return JsonResponse(selected_device)
    else:
        return JsonResponse({"error": "Device not found"}, status=404)