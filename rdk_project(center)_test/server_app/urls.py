# django_server/server_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload_image1/', views.upload_image1, name='upload_image1'),
    path('upload_image2/', views.upload_image2, name='upload_image2'),
    path('upload_image3/', views.upload_image3, name='upload_image3'),
    path('upload_image4/', views.upload_image4, name='upload_image4'),
    path('display/', views.display_page, name='display_page'),
    path('select_device/<int:device_id>/', views.select_device, name='select_device'),
    path('get_recording_status/', views.get_recording_status, name='get_recording_status'),
    path('update_recording_status/', views.update_recording_status, name='update_recording_status'),
]
