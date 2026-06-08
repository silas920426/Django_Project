# tickets/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='ticket_list'),
    path('create/', views.create, name='ticket_create'),
    path('<int:pk>/', views.detail, name='ticket_detail'), # 👈 新增這行：查看詳細
    path('<int:pk>/update/', views.update, name='ticket_update'),
    path('<int:pk>/delete/', views.delete, name='ticket_delete'),
]