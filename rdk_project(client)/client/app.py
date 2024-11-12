from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import cv2
import time
import os
import requests

app = Flask(__name__)
CORS(app)  # 启用 CORS

# 全局变量
recording = False
stop_signal = False
start_time = None  # 用于记录录制开始时间
video_dir = "/mnt/usb/videos"
image_folder = "/home/sunrise/Documents/rdk_project(client)/client/images"
image_path = os.path.join(image_folder, "latest_image.jpg")
os.makedirs(image_folder, exist_ok=True)
server_url = "http://192.168.3.37:8001/upload_image1/"  # 确保这是主控板的实际 IP 地址和端口

# 图像发送线程函数
def send_image():
    print("[INFO] Starting image send thread...")
    while not stop_signal:
        if os.path.exists(image_path):
            with open(image_path, 'rb') as img_file:
                files = {'image': img_file}
                try:
                    response = requests.post(server_url, files=files)
                    if response.status_code == 200:
                        print(f"[INFO] Image {image_path} sent successfully.")
                    else:
                        print(f"[ERROR] Failed to send image. Status code: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    print(f"[ERROR] Error sending image: {e}")
        else:
            print(f"[WARNING] Image path {image_path} does not exist.")
        
        time.sleep(1)  # 每秒发送一次

# 视频录制函数
def start_recording(segment_time, total_time):
    """开始视频录制并更新图像文件"""
    global recording, stop_signal, start_time
    if recording:
        print("[INFO] Recording is already in progress.")
        return

    print(f"[INFO] Starting video recording with segment_time={segment_time}s, total_time={total_time}s")
    recording = True
    stop_signal = False
    start_time = time.time()  # 记录开始时间
    duration = total_time
    segment_count = 0
    last_image_update_time = time.time()  # 用于控制图像更新的时间间隔

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    while (time.time() - start_time) < duration and not stop_signal:
        segment_count += 1
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        video_path = f"{video_dir}/video_{timestamp}_{segment_count}.avi"
        out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'XVID'), 30, (640, 480))
        
        print(f"[INFO] Recording segment {segment_count}: {video_path} with segment_time={segment_time}s")
        segment_start_time = time.time()
        while (time.time() - segment_start_time) < segment_time:
            ret, frame = cap.read()
            if not ret or stop_signal:
                print("[WARNING] Stopping segment recording early due to stop signal or capture error.")
                break
            out.write(frame)
            
            # 每秒更新一次图像
            current_time = time.time()
            if current_time - last_image_update_time >= 1:
                cv2.imwrite(image_path, frame)  # 将当前帧保存为 latest_image.jpg
                last_image_update_time = current_time
                print(f"[INFO] Image updated at {image_path}")

        out.release()
        print(f"[INFO] Segment {segment_count} saved to {video_path}")
        if stop_signal:
            print("[INFO] Recording stopped by stop signal.")
            break

    cap.release()
    recording = False
    print("[INFO] Video recording completed.")

# 录制状态更新至 Django 服务器
def update_django_recording_status(command, recorded_time=0):
    """更新录制状态到 Django 服务器"""
    django_url = "http://192.168.3.37:8001/update_recording_status/"
    data = {
        'command': command,
        'recordedTime': recorded_time
    }
    try:
        response = requests.post(django_url, json=data)
        if response.status_code == 200:
            print(f"[INFO] Updated Django recording status: {response.json()}")
        else:
            print(f"[ERROR] Failed to update recording status. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Error updating recording status: {e}")

# 计算已录制时长
def calculate_recorded_time():
    """返回已录制的总时长（单位：秒）"""
    if start_time:
        return int(time.time() - start_time)
    return 0

# 控制视频录制和图像发送的路由
@app.route('/handle_recording_command/', methods=['POST'])
def handle_recording_command():
    print("[INFO] Entered handle_recording_command route")
    global stop_signal
    data = request.json
    command = data.get('command')
    segment_time = int(data.get('segment_time', 10))
    total_time = int(data.get('total_time', 60))

    print(f"[INFO] Received command: {command} with segment_time={segment_time}s, total_time={total_time}s")  # 调试输出

    if command == 'start' and not recording:
        print("[INFO] Starting new recording and image sending...")
        stop_signal = False
        update_django_recording_status('start')
        threading.Thread(target=start_recording, args=(segment_time, total_time)).start()
        threading.Thread(target=send_image, daemon=True).start()
        return jsonify({'status': 'recording started'})

    elif command == 'stop':
        stop_signal = True
        update_django_recording_status('stop', recorded_time=calculate_recorded_time())
        print("[INFO] Stop command received. Stopping recording and image sending...")
        return jsonify({'status': 'recording stopped'})

    print("[ERROR] Invalid command received.")
    return jsonify({'status': 'invalid command'})

if __name__ == '__main__':
    print("[INFO] Flask app is starting on http://0.0.0.0:8001...")
    app.run(host='0.0.0.0', port=8001)
