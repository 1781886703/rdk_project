# send_image.py
import requests
import time
import os

# 设置要发送的图片路径
image_path = "/home/sunrise/Documents/rdk_project(client)/client/images/latest_image.jpg"
server_url = "http://10.5.5.1:8001/upload_image1/"  # 替换为服务器的实际 IP 地址和端口

print("Starting to send images to the server...")

while True:
    # 检查图片文件是否存在
    if os.path.exists(image_path):
        with open(image_path, 'rb') as img_file:
            files = {'image': img_file}
            try:
                # 发送 HTTP POST 请求，将图片发送到服务器
                response = requests.post(server_url, files=files)
                if response.status_code == 200:
                    print(f"Image {image_path} sent successfully.")
                else:
                    print(f"Failed to send image. Server responded with status code {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Error sending image: {e}")
    else:
        print(f"Error: {image_path} does not exist. Please check the file path.")
    
    # 每秒发送一次
    time.sleep(1)
