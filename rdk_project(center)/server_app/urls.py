# django_server/server_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload_image/', views.upload_image, name='upload_image'),
    path('display/', views.display_page, name='display_page'),
    path('select_device/<int:device_id>/', views.select_device, name='select_device'),
]
