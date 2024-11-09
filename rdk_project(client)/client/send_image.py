import requests
import time
import os

# 设置要发送的图片文件夹路径和文件列表
image_folder = os.path.join(os.path.dirname(__file__), "images")
image_files = [os.path.join(image_folder, "frame1.jpg"),
               os.path.join(image_folder, "frame2.jpg"),
               os.path.join(image_folder, "frame3.jpg")]  # 替换为实际图片路径

server_url = "http://192.168.3.35:8001/upload/"  # 将 <center_board_ip> 替换为中心板的实际 IP 地址
      # 替换为服务器的 IP 地址和端口

# 检查图片文件是否存在
for image_path in image_files:
    if not os.path.exists(image_path):
        print(f"Error: {image_path} does not exist. Please check the file paths.")
        exit(1)

print("Starting to send images to the server...")

while True:
    # 循环发送每张图片
    for image_path in image_files:
        with open(image_path, 'rb') as img_file:
            files = {'image': img_file}
            try:
                # 发送 HTTP POST 请求，将图片发送到服务器
                response = requests.post(server_url, files=files)
                if response.status_code == 200:
                    print(f"Image {image_path} sent successfully.")
                else:
                    print(f"Failed to send {image_path}. Server responded with status code {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Error sending {image_path}: {e}")
        
        # 每秒发送一张图片
        time.sleep(1)
