# rdk_project

## 项目背景：无

## 项目简介
rdk_project 是基于 RDK X 系列开发板的嵌入式项目，旨在实现多功能应用，如视频传输、红绿灯识别和传感器数据采集等。该项目基于 Linux 系统，利用了多种硬件模块和通信接口。
这也是一个实现多个rdk_x5之间通讯，收集、处理传感器数据（尤其是视频数据），并提供了人机交互平台+数据可视化网页（基于django）的项目。

## 功能特点
- 视频存储和图片传输
- 实时视频抽帧
- 多设备之间的网络通信
- 各种传感器数据的采集与处理
- 使用django框架搭建人机交互平台与数据可视化显示

## 安装
1. 克隆项目到本地：
    ```bash
    git clone https://github.com/1781886703/rdk_project.git
    cd rdk_project
    ```
2. 安装依赖：
    - 确保开发环境支持 Linux。
    - 安装必要的库（如 OpenCV、Django、requests等）。

3. 配置 RDK X 系列开发板，参照文档对设备进行设置。

## 使用方法
（有两个文件夹：分别是client端和center端的，分别部署到两个不同的板子上）
center端：
1. 根据rdk文档，打开soft ap模式
2. 启动主程序：
    ```bash
    python manager.py runserver 0.0.0.0:8001
    ```
client端：
1.启动主程序
python3 send_images.py
