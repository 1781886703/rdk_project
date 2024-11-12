#!/bin/bash

# 定义项目路径
PROJECT_DIR="/home/sunrise/Documents/rdk_project(client)/client"

# 切换到项目目录
cd "$PROJECT_DIR" || exit

# 运行 record_video.py 并在后台运行
echo "Starting video recording..."
nohup python3 record_video.py > record_video.log 2>&1 &

# 运行 send_image.py 并在后台运行
echo "Starting image sending..."
nohup python3 send_image.py > send_image.log 2>&1 &

echo "Both scripts are now running in the background."
echo "Check record_video.log and send_image.log for output logs."

