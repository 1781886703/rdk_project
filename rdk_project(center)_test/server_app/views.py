from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.utils import timezone
import random  # 模拟温度数据
import json
import requests
from .models import DeviceSetting
from .models import RecordingStatus
@csrf_exempt
def upload_image1(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        file_path = 'latest_image1.jpg'
        
        if default_storage.exists(file_path):
            default_storage.delete(file_path)
        path = default_storage.save(file_path, ContentFile(image.read()))

        return JsonResponse({'status': 'success'}, status=200)
    return JsonResponse({'status': 'failed'}, status=400)

def upload_image2(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        file_path = 'latest_image2.jpg'
        
        if default_storage.exists(file_path):
            default_storage.delete(file_path)
        path = default_storage.save(file_path, ContentFile(image.read()))

        return JsonResponse({'status': 'success'}, status=200)
    return JsonResponse({'status': 'failed'}, status=400)

def upload_image3(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        file_path = 'latest_image3.jpg'
        
        if default_storage.exists(file_path):
            default_storage.delete(file_path)
        path = default_storage.save(file_path, ContentFile(image.read()))

        return JsonResponse({'status': 'success'}, status=200)
    return JsonResponse({'status': 'failed'}, status=400)

def upload_image4(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        file_path = 'latest_image4.jpg'
        
        if default_storage.exists(file_path):
            default_storage.delete(file_path)
        path = default_storage.save(file_path, ContentFile(image.read()))

        return JsonResponse({'status': 'success'}, status=200)
    return JsonResponse({'status': 'failed'}, status=400)
def display_page(request):
    # 模拟设备信息和设置
    devices = [
        {"id": 1, "name": "设备1", "status": "正常", "temperature": round(random.uniform(20, 30), 1), "image_url": "/media/latest_image1.jpg", 
         "settings": {"warmth": 50, "brightness": 60, "contrast": 70}},
        {"id": 2, "name": "设备2", "status": "正常", "temperature": round(random.uniform(20, 30), 1), "image_url": "/media/latest_image2.jpg",
         "settings": {"warmth": 40, "brightness": 50, "contrast": 60}},
        {"id": 3, "name": "设备3", "status": "异常", "temperature": round(random.uniform(20, 30), 1), "image_url": "/media/latest_image3.jpg",
         "settings": {"warmth": 30, "brightness": 40, "contrast": 50}},
        {"id": 4, "name": "设备4", "status": "正常", "temperature": round(random.uniform(20, 30), 1), "image_url": "/media/latest_image4.jpg",
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
        "segmentTime": 10,
        "totalTime": 20,
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
    
#更新录制状态，比如在开始录制时设为“录制中”，在停止录制时更新状态和时长
@csrf_exempt
def update_recording_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        command = data.get('command')
        recorded_time = data.get('recordedTime', 0)

        # 获取或创建唯一的 RecordingStatus 记录
        status, created = RecordingStatus.objects.get_or_create(id=1)

        if command == 'start':
            status.is_recording = True
            status.recorded_time = 0  # 重置录制时长
            status.start_time = timezone.now()  # 设置开始时间为当前时间
        elif command == 'stop':
            status.is_recording = False
            status.recorded_time = recorded_time  # 更新已录制时长
            status.start_time = None  # 停止时清空开始时间

        status.save()
        return JsonResponse({
            'status': 'updated', 
            'isRecording': status.is_recording, 
            'recordedTime': status.recorded_time, 
            'statusCode': status.status_code,
            'startTime': status.start_time
        })
    
    return JsonResponse({'status': 'failed'}, status=400)

# 获取当前录制状态
def get_recording_status(request):
    status, created = RecordingStatus.objects.get_or_create(id=1)
    return JsonResponse({
        'isRecording': status.is_recording, 
        'recordedTime': status.recorded_time,
        'startTime': status.start_time,
    })

