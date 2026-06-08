from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='department_list'),
    path('create/', views.create, name='department_create'),
    path('<int:pk>/update/', views.update, name='department_update'),
    path('<int:pk>/delete/', views.delete, name='department_delete'),
]