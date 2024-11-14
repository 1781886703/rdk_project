from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import cv2
import time
import os
import requests

#192.168.3.35(该板子的罗曦号)(1)

app = Flask(__name__)
CORS(app)  # 启用 CORS

# 不同rdk设备只需要修改这两个
device_id = '1'  #设备号
ip_port = '192.168.3.37:8001'  #确保这是主控板的实际 IP 地址和端口

# 全局变量
recording = False
stop_signal = False
start_time = None  # 用于记录录制开始时间
video_dir_base = "/mnt/usb/videos"
image_folder = "/home/sunrise/Documents/rdk_project(client)/client/images"
image_path = os.path.join(image_folder, "latest_image.jpg")
os.makedirs(image_folder, exist_ok=True)
server_url = f"http://{ip_port}/upload_image{device_id}/"  # 用于发送图片给主控板
current_video_dir = ""  # 当前录制的文件夹路径
send_image_thread = None  # 用于存储图像发送线程
django_url = f"http://{ip_port}/update_recording_status{device_id}/"  # 用于发送运行状态给主控板

# 图像发送线程函数
def send_image():
    print("[INFO] Starting image send thread...")
    while not stop_signal:
        status_code = 1 if recording else 0  # 状态码：1 表示正在录制，0 表示未录制
        if os.path.exists(image_path):
            with open(image_path, 'rb') as img_file:
                files = {'image': img_file}
                data = {'status_code': status_code}  # 发送状态码
                try:
                    response = requests.post(server_url, files=files, data=data)
                    if response.status_code == 200:
                        pass
                        # print(f"[INFO] Image {image_path} sent successfully with status_code={status_code}.")
                    else:
                        print(f"[ERROR] Failed to send image. Status code: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    print(f"[ERROR] Error sending image: {e}")
        else:
            print(f"[WARNING] Image path {image_path} does not exist.")
        
        time.sleep(1)  # 每秒发送一次

# 视频录制函数  主函数
def start_recording(segment_time, total_time, location):
    """开始视频录制并更新图像文件"""
    global recording, stop_signal, start_time, current_video_dir, send_image_thread
    if recording:
        print("[INFO] Recording is already in progress.")
        return

    # 创建新的视频存储目录
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    current_video_dir = os.path.join(video_dir_base, f"{location}_{timestamp}_{segment_time}s_{total_time}s")
    os.makedirs(current_video_dir, exist_ok=True)
    print(f"[INFO] Video files will be saved to: {current_video_dir}")
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
        video_path = os.path.join(current_video_dir, f"video_{timestamp}_{segment_count}.avi")
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
            
            # # 每秒发送一次更新录制状态的请求
            # update_django_recording_status('start', recorded_time=calculate_recorded_time())

        out.release()
        print(f"[INFO] Segment {segment_count} saved to {video_path}")
        
        # 检查是否录制时间已达上限
        if (time.time() - start_time) >= duration:
            stop_signal = True
            print("[INFO] Total recording time reached. Stopping the recording and image sending...")

    stop_signal = True  # 停止 send_image 线程
    update_django_recording_status('stop', recorded_time=calculate_recorded_time())
    cap.release()
    recording = False
    stop_signal = True  
    print("[INFO] Video recording completed.")

# 录制状态更新至 Django 服务器
def update_django_recording_status(command, recorded_time=0):
    """更新录制状态到 Django 服务器"""
    global ip_port,django_url
    # django_url = f"http://{ip_port}/update_recording_status/"
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
    global stop_signal, send_image_thread
    data = request.json
    command = data.get('command')
    segment_time = int(data.get('segment_time', 10))
    total_time = int(data.get('total_time', 60))
    location = data.get('location', 'unknown_location')  # 接收地点信息

    print(f"[INFO] Received command: {command} with segment_time={segment_time}s, total_time={total_time}s, location={location}")

    if command == 'start' and not recording:
        print("[INFO] Starting new recording and image sending...")
        stop_signal = False
        update_django_recording_status('start')
        threading.Thread(target=start_recording, args=(segment_time, total_time, location)).start()
        
        # 启动新的 send_image 线程
        if send_image_thread is None or not send_image_thread.is_alive():
            send_image_thread = threading.Thread(target=send_image, daemon=True)
            send_image_thread.start()
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
