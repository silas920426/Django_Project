"""
URL configuration for Django_Project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # 👈 新增引入這行

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 🔥 1. 將預設根目錄直接綁定為登入頁面
    # redirect_authenticated_user=True 代表如果已經登入過，會自動跳轉，不用再登入一次
    path('', auth_views.LoginView.as_view(template_name='users/login.html', redirect_authenticated_user=True), name='login'),
    
    # 🔥 2. 將原本的首頁 (Dashboard) 移到獨立的路徑
    path('dashboard/', include('dashboard.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('departments/', include('departments.urls')),
    path('equipments/', include('equipments.urls')),
    path('tickets/', include('tickets.urls')),
    path('users/', include('users.urls')),
]