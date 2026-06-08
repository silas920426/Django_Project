# equipments/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Equipment
from .forms import EquipmentForm

# 所有人都可以看設備清單
def list(request):
    return render(request, 'equipments/list.html', {
        'equipments': Equipment.objects.all()
    })

# 以下操作必須是超級管理員 (Superuser) 才能執行
def superuser_required(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(superuser_required, login_url='login')
def create(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid(): # 注意：這裡本來也有一個小筆誤 is_value_valid()，已經幫你修正為 is_valid()
            form.save()
            return redirect('equipment_list')
    else:
        form = EquipmentForm()
    return render(request, 'equipments/form.html', {'form': form})

@user_passes_test(superuser_required, login_url='login')
def update(request, pk):
    # 使用 get_object_or_404，如果找不到該設備就回傳 404 錯誤頁面
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            return redirect('equipment_list')
    else:
        form = EquipmentForm(instance=equipment)
    return render(request, 'equipments/form.html', {'form': form})

@user_passes_test(superuser_required, login_url='login')
def delete(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    equipment.delete()
    return redirect('equipment_list')
# equipments/views.py 裡面的 create 函式

@user_passes_test(superuser_required, login_url='login')
def create(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('equipment_list')
    else:
        form = EquipmentForm()
        
    # 👇 請確保這裡寫的是 'equipments/create.html'
    return render(request, 'equipments/create.html', {'form': form})