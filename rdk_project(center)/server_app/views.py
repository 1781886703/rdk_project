from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.utils import timezone
import random  # 模拟温度数据

@csrf_exempt  # 禁用 CSRF 验证
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        # 文件名路径为 "media/latest_image.jpg"
        file_path = 'latest_image.jpg'
        
        # 覆盖保存文件
        if default_storage.exists(file_path):
            default_storage.delete(file_path)  # 删除已有文件
        path = default_storage.save(file_path, ContentFile(image.read()))  # 重新保存为最新文件

        return JsonResponse({'status': 'success'}, status=200)
    return JsonResponse({'status': 'failed'}, status=400)

def display_page(request):
    # 模拟设备信息
    devices = [
        {"id": 1, "name": "Camera 1", "status": "running", "temperature": random.uniform(35, 45), "image_url": "/media/latest_image.jpg"},
        {"id": 2, "name": "Camera 2", "status": "not running", "temperature": random.uniform(35, 45), "image_url": "/media/camera2.jpg"},
        {"id": 3, "name": "Camera 3", "status": "error", "temperature": random.uniform(35, 45), "image_url": "/media/camera3.jpg"},
        {"id": 4, "name": "Camera 4", "status": "running", "temperature": random.uniform(35, 45), "image_url": "/media/camera4.jpg"},
    ]
    return render(request, 'display.html', {
        "devices": devices,
        "timestamp": timezone.now().timestamp()
    })
