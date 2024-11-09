from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from django.shortcuts import redirect
from server_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('display/')),  # 根路径重定向到 display 页面
    path('', include('server_app.urls')),  # 包含 server_app 的路由
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
