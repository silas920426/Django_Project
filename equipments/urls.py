from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='equipment_list'),
    path('create/', views.create, name='equipment_create'),
    path('<int:pk>/update/', views.update, name='equipment_update'),
    path('<int:pk>/delete/', views.delete, name='equipment_delete'),
]