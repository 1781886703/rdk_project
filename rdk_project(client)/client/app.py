from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import cv2
import time
import os
import requests
import logging

app = Flask(__name__)
CORS(app)  # 启用 CORS

# 配置 logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log")
    ]
)

# 不同 rdk 设备只需要修改这两个
device_id = '1'  # 设备号
ip_port = '192.168.3.37:8001'  # 主控板的实际 IP 地址和端口（这个是您的电脑 IP）
# ip_port = '10.5.5.1:8001' 

# 全局变量
video_dir_base = "/mnt/usb/videos"
image_folder = "/home/sunrise/Documents/rdk_project(client)/client/images"
image_path = os.path.join(image_folder, "latest_image.jpg")
os.makedirs(image_folder, exist_ok=True)
server_url = f"http://{ip_port}/upload_image{device_id}/"  # 用于发送图片给主控板
django_url = f"http://{ip_port}/update_recording_status{device_id}/"  # 用于发送运行状态给主控板

# 线程控制事件
stop_event = threading.Event()
recording_event = threading.Event()

# 图像发送线程函数
def send_image():
    logging.info("启动图像发送线程...")
    while not stop_event.is_set():
        status_code = 1 if recording_event.is_set() else 0  # 状态码：1 表示正在录制，0 表示未录制
        if os.path.exists(image_path):
            try:
                with open(image_path, 'rb') as img_file:
                    files = {'image': img_file}
                    data = {'status_code': status_code}  # 发送状态码
                    response = requests.post(server_url, files=files, data=data, timeout=5)
                    if response.status_code != 200:
                        logging.error(f"发送图像失败。状态码: {response.status_code}")
            except requests.exceptions.RequestException as e:
                logging.error(f"发送图像时出错: {e}")
        else:
            logging.warning(f"图像路径 {image_path} 不存在。")
        
        stop_event.wait(1)  # 每秒发送一次，支持通过 stop_event 及时停止

    logging.info("图像发送线程已停止。")

# 录制状态更新至 Django 服务器
def update_django_recording_status(command, recorded_time=0):
    """更新录制状态到 Django 服务器"""
    data = {
        'command': command,
        'recordedTime': recorded_time
    }
    try:
        response = requests.post(django_url, json=data, timeout=5)
        if response.status_code == 200:
            logging.info(f"Django 服务器录制状态更新成功: {response.json()}")
        else:
            logging.error(f"Django 服务器录制状态更新失败。状态码: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"更新 Django 录制状态时出错: {e}")

# 计算已录制时长
def calculate_recorded_time(start_time):
    """返回已录制的总时长（单位：秒）"""
    if start_time:
        return int(time.time() - start_time)
    return 0

# 停止录制和相关线程的函数
def stop_all_operations(start_time):
    if recording_event.is_set():
        logging.info("检测到停止信号，正在停止所有操作...")
        stop_event.set()  # 触发停止事件
        update_django_recording_status('stop', recorded_time=calculate_recorded_time(start_time))
        recording_event.clear()  # 清除录制标志
    else:
        logging.info("系统未在录制中，无需停止。")

# 视频录制函数
def start_recording(segment_time, total_time, location):
    """开始视频录制并更新图像文件"""
    logging.info("开始视频录制线程...")
    start_time = time.time()  # 记录开始时间

    # 创建新的视频存储目录
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    current_video_dir = os.path.join(video_dir_base, f"{location}_{timestamp}_{segment_time}s_{total_time}s")
    os.makedirs(current_video_dir, exist_ok=True)
    logging.info(f"视频文件将保存到: {current_video_dir}")
    logging.info(f"开始录制视频，segment_time={segment_time}s, total_time={total_time}s")

    # 检查 U盘是否存在
    if not os.path.exists("/mnt/usb"):
        logging.error("/mnt/usb 不存在。无法开始录制。")
        stop_all_operations(start_time)
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logging.error("无法打开摄像头。停止录制。")
        stop_all_operations(start_time)
        return

    # 设置摄像头参数
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    recording_event.set()  # 设置录制标志

    try:
        segment_count = 0
        last_image_update_time = time.time()  # 用于控制图像更新的时间间隔

        while (time.time() - start_time) < total_time and not stop_event.is_set():
            segment_count += 1
            video_path = os.path.join(current_video_dir, f"video_{timestamp}_{segment_count}.avi")
            out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'XVID'), 30, (640, 480))

            logging.info(f"开始录制第 {segment_count} 段视频: {video_path}，segment_time={segment_time}s")
            segment_start_time = time.time()

            while (time.time() - segment_start_time) < segment_time and not stop_event.is_set():
                ret, frame = cap.read()
                if not ret:
                    logging.error("从摄像头读取帧失败。停止录制。")
                    stop_all_operations(start_time)
                    break

                out.write(frame)

                # 每秒更新一次图像
                current_time = time.time()
                if current_time - last_image_update_time >= 1:
                    cv2.imwrite(image_path, frame)  # 将当前帧保存为 latest_image.jpg
                    last_image_update_time = current_time
                    logging.info(f"图像已更新: {image_path}")

                # 检查 U盘是否存在
                if not os.path.exists("/mnt/usb"):
                    logging.error("/mnt/usb 已不可用。停止录制。")
                    stop_all_operations(start_time)
                    break

            out.release()
            logging.info(f"第 {segment_count} 段视频已保存到: {video_path}")

        if (time.time() - start_time) >= total_time:
            logging.info("达到总录制时间上限。停止录制和图像发送...")
            stop_all_operations(start_time)

    except Exception as e:
        logging.error(f"录制过程中发生异常: {e}")
        stop_all_operations(start_time)

    finally:
        cap.release()
        recording_event.clear()
        stop_event.set()  # 确保发送图像线程停止
        logging.info("视频录制线程已完成。")

# 控制视频录制和图像发送的路由
@app.route('/handle_recording_command/', methods=['POST'])
def handle_recording_command():
    logging.info("进入 handle_recording_command 路由")
    data = request.json
    command = data.get('command')
    segment_time = int(data.get('segment_time', 10))
    total_time = int(data.get('total_time', 60))
    location = data.get('location', 'unknown_location')  # 接收地点信息

    logging.info(f"接收到命令: {command}，segment_time={segment_time}s, total_time={total_time}s, location={location}")

    if command == 'start' and not recording_event.is_set():
        logging.info("启动新的录制和图像发送线程...")
        stop_event.clear()  # 确保停止事件被清除
        update_django_recording_status('start')
        threading.Thread(target=start_recording, args=(segment_time, total_time, location), daemon=True).start()
        
        # 启动图像发送线程
        threading.Thread(target=send_image, daemon=True).start()
        return jsonify({'status': 'recording started'})

    elif command == 'stop' and recording_event.is_set():
        logging.info("接收到停止命令。停止录制和图像发送...")
        stop_all_operations(start_time=None)  # 传递 start_time 可以根据需要调整
        return jsonify({'status': 'recording stopped'})

    logging.error("接收到无效命令。")
    return jsonify({'status': 'invalid command'})

if __name__ == '__main__':
    logging.info("Flask 应用正在 http://0.0.0.0:8001 启动...")
    app.run(host='0.0.0.0', port=8001)
