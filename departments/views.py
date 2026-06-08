from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Department
from .forms import DepartmentForm

# 所有人都可以看部門清單
def list(request):
    return render(request, 'departments/list.html', {
        'departments': Department.objects.all()
    })

# 權限驗證：必須是超級管理員
def superuser_required(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(superuser_required, login_url='login')
def create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'departments/form.html', {'form': form})

@user_passes_test(superuser_required, login_url='login')
def update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'departments/form.html', {'form': form})

@user_passes_test(superuser_required, login_url='login')
def delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    department.delete()
    return redirect('department_list')