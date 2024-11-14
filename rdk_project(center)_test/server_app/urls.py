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
    path('get_recording_status1/', views.get_recording_status1, name='get_recording_status1'),
    path('get_recording_status2/', views.get_recording_status2, name='get_recording_status2'),
    path('get_recording_status3/', views.get_recording_status3, name='get_recording_status3'),
    path('get_recording_status4/', views.get_recording_status4, name='get_recording_status4'),
    path('update_recording_status1/', views.update_recording_status1, name='update_recording_status1'),
    path('update_recording_status2/', views.update_recording_status2, name='update_recording_status2'),
    path('update_recording_status3/', views.update_recording_status3, name='update_recording_status3'),
    path('update_recording_status4/', views.update_recording_status4, name='update_recording_status4'),
    path('save_the_record_time/', views.save_the_record_time, name='save_the_record_time'),
    path('get_the_record_time/', views.get_the_record_time, name='get_the_record_time'),
]