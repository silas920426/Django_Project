# users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import ProfileUpdateForm

# ====================
# 註冊功能
# ====================
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False # 註冊後預設停用，待審核
            user.save()
            messages.success(request, '✅ 帳號註冊成功！請等待管理員開通。')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


# ====================
# 員工通訊錄 CRUD 邏輯
# ====================

# 檢視通訊錄列表
@login_required(login_url='login')
def contact_list(request):
    # 所有人都能看通訊錄 (這裡只列出已經啟用的帳號)
    users = User.objects.filter(is_active=True).order_by('username')
    return render(request, 'users/user_list.html', {'users': users})

# 編輯個人資料
@login_required(login_url='login')
def contact_update(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    
    # 🔥 核心權限檢查：只有「超級管理員」或是「本人」才可以修改
    if not request.user.is_superuser and request.user != user_obj:
        messages.error(request, "❌ 您沒有權限修改其他人的個人資料！")
        return redirect('contact_list')

    if request.method == 'POST':
        # 🔥 建立表單時，傳入 current_user 供 forms.py 判斷是否鎖定部門欄位
        form = ProfileUpdateForm(request.POST, instance=user_obj, current_user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'✨ {user_obj.username} 的個人資料已成功更新！')
            return redirect('contact_list')
    else:
        # 🔥 建立空表單時，一樣要傳入 current_user
        form = ProfileUpdateForm(instance=user_obj, current_user=request.user)
        
    return render(request, 'users/user_form.html', {'form': form, 'user_obj': user_obj})

# 刪除聯絡人
@login_required(login_url='login')
def contact_delete(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    
    # 🔥 只有超級管理員可以刪除帳號
    if not request.user.is_superuser:
        messages.error(request, "❌ 只有超級管理員可以刪除聯絡人！")
        return redirect('contact_list')
        
    # 🔥 管理員不能誤刪自己的帳號
    if request.user == user_obj:
        messages.error(request, "❌ 您無法刪除自己的帳號！")
        return redirect('contact_list')

    user_obj.delete()
    messages.success(request, f"🗑️ 已刪除聯絡人 {user_obj.username}。")
    return redirect('contact_list')