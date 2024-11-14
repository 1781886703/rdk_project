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
from datetime import timedelta
from .models import Recording
from datetime import datetime
# 上传图像的通用函数
@csrf_exempt
def upload_image2(request):
    return upload_image_generic(request, device_id=2)
@csrf_exempt
def upload_image1(request):
    return upload_image_generic(request, device_id=1)

@csrf_exempt
def upload_image3(request):
    return upload_image_generic(request, device_id=3)

@csrf_exempt
def upload_image4(request):
    return upload_image_generic(request, device_id=4)

def upload_image_generic(request, device_id):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        file_path = f'latest_image{device_id}.jpg'
        
        if default_storage.exists(file_path):
            default_storage.delete(file_path)
        path = default_storage.save(file_path, ContentFile(image.read()))

        return JsonResponse({'status': 'success', 'device_id': device_id}, status=200)
    return JsonResponse({'status': 'failed', 'device_id': device_id}, status=400)

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
# 新增更新录制状态函数，每个函数对应一个设备
@csrf_exempt
def update_recording_status1(request):
    return update_recording_status_generic(request, device_id=1)

@csrf_exempt
def update_recording_status2(request):
    return update_recording_status_generic(request, device_id=2)

@csrf_exempt
def update_recording_status3(request):
    return update_recording_status_generic(request, device_id=3)

@csrf_exempt
def update_recording_status4(request):
    return update_recording_status_generic(request, device_id=4)

@csrf_exempt
def update_recording_status_generic(request, device_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        command = data.get('command')
        total_time = data.get('total_time', 0)  # 录制总时长，用于计算预计结束时间

        # 获取或创建对应设备的 RecordingStatus 记录
        status, created = RecordingStatus.objects.get_or_create(device_id=device_id)

        if command == 'start':
            status.is_recording = True
            status.start_time = timezone.now()  # 记录开始时间
            status.total_time = total_time  # 将总时长存储
        elif command == 'stop':
            status.is_recording = False
            status.start_time = None  # 停止时清空开始时间
            status.total_time = 0  # 清除总时长

        status.save()
        return JsonResponse({
            'status': 'updated',
            'isRecording': status.is_recording,
        })

    return JsonResponse({'status': 'failed'}, status=400)
# 新增获取录制状态函数，每个函数对应一个设备
def get_recording_status1(request):
    return get_recording_status_generic(request, device_id=1)

def get_recording_status2(request):
    return get_recording_status_generic(request, device_id=2)

def get_recording_status3(request):
    return get_recording_status_generic(request, device_id=3)

def get_recording_status4(request):
    return get_recording_status_generic(request, device_id=4)

def get_recording_status_generic(request, device_id):
    status, created = RecordingStatus.objects.get_or_create(device_id=device_id)
    return JsonResponse({
        'isRecording': status.is_recording, 
    })

#视图来处理保存录制信息的逻辑
@csrf_exempt
def save_the_record_time(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        start_time = data.get('start_time')
        total_time = data.get('total_time')
        
        # Save to database
        recording = Recording(start_time=datetime.fromisoformat(start_time), total_time=int(total_time))
        recording.save()
        return JsonResponse({'status': 'success'})

def get_the_record_time(request):
    # Retrieve the latest recording (you can change logic if needed)
    latest_recording = Recording.objects.latest('start_time')
    return JsonResponse({'start_time': latest_recording.start_time.isoformat(),'total_time': latest_recording.total_time})