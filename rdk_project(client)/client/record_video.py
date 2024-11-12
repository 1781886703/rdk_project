# record_video.py
import cv2
import time
from datetime import datetime
import os

# 设置视频保存路径
video_dir = "/mnt/usb/videos"  # 确保该文件夹存在于U盘目录中
fps = 30  # 每秒帧数
duration = 10  # 录制总时长，单位为秒

# 自动生成视频文件名，包含时间戳
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
video_path = f"{video_dir}/video_{timestamp}.avi"

# 设置每秒提取图片保存路径
image_folder = "/home/sunrise/Documents/rdk_project(client)/client/images"
os.makedirs(image_folder, exist_ok=True)  # 创建目录（若不存在）
image_path = os.path.join(image_folder, "latest_image.jpg")

# 初始化摄像头
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, fps)  # 设置FPS
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # 设置帧宽度
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # 设置帧高度

# 视频编码设置
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(video_path, fourcc, fps, (640, 480))

# 开始时间
start_time = time.time()
last_frame_time = start_time  # 用于记录上次提取帧的时间

print("Starting video recording...")

while (time.time() - start_time) < duration:
    ret, frame = cap.read()
    if ret:
        out.write(frame)  # 写入视频文件
        
        # 每秒提取一帧
        current_time = time.time()
        if current_time - last_frame_time >= 1:  # 每秒保存一张图片
            cv2.imwrite(image_path, frame)  # 保存为latest_image.jpg
            last_frame_time = current_time  # 更新上次提取时间
            print(f"Frame saved as {image_path}")
    else:
        print("Error: Failed to capture video frame.")
        break

# 释放资源
cap.release()
out.release()
print(f"视频录制完成，已存储到: {video_path}")
