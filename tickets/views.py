# tickets/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import RepairTicket
from .forms import RepairTicketForm
from equipments.models import Equipment

# 🔥 權限判斷小工具：檢查是否為「超級管理員」或所屬部門為「維修部」
def is_repair_staff(user):
    if user.is_superuser:
        return True
    if hasattr(user, 'profile') and user.profile.department:
        return user.profile.department.name == '維修部'
    return False

# 檢視報修清單
@login_required(login_url='login')
def list(request):
    # 🔥 關鍵修改：將原本的 request.user.is_superuser 改成 is_repair_staff()
    # 這樣超級管理員和「維修部」的人員，都能看到全公司所有的報修單
    if is_repair_staff(request.user):
        tickets = RepairTicket.objects.all().order_by('-created_at')
    else:
        # 其他一般部門的員工，就只能看到自己送出的單子
        tickets = RepairTicket.objects.filter(reporter=request.user).order_by('-created_at')
        
    return render(request, 'tickets/list.html', {'tickets': tickets})

# 創建報修單
@login_required(login_url='login')
def create(request):
    if request.method == 'POST':
        form = RepairTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.reporter = request.user
            ticket.status = 'pending'
            ticket.save()
            
            equipment = ticket.equipment
            equipment.status = 'repair'
            equipment.save()
            
            return redirect('ticket_list')
    else:
        form = RepairTicketForm()
    return render(request, 'tickets/form.html', {'form': form})

# 查看維修單詳細內容（唯讀模式 + 處理功能）
@login_required(login_url='login')
def detail(request, pk):
    # 核心防護：如果不是報修部或管理員，直接踢回列表頁
    if not is_repair_staff(request.user):
        messages.error(request, '❌ 權限不足：只有「維修部」人員與超級管理員可以查看報修單詳細內容。')
        return redirect('ticket_list')

    ticket = get_object_or_404(RepairTicket, pk=pk)
    form = RepairTicketForm(instance=ticket)
    
    if request.method == 'POST' and 'mark_processed' in request.POST:
        ticket.status = 'completed'
        ticket.save()
        
        equipment = ticket.equipment
        equipment.status = 'normal'
        equipment.save()
        
        return redirect('ticket_list')
        
    return render(request, 'tickets/detail.html', {
        'ticket': ticket,
        'form': form
    })

# 編輯報修單
@login_required(login_url='login')
def update(request, pk):
    ticket = get_object_or_404(RepairTicket, pk=pk)
    if request.method == 'POST':
        form = RepairTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('ticket_list')
    else:
        form = RepairTicketForm(instance=ticket)
    return render(request, 'tickets/form.html', {'form': form})

# 刪除報修單
@login_required(login_url='login')
def delete(request, pk):
    # 核心防護：如果不是報修部或管理員，直接踢回列表頁
    if not is_repair_staff(request.user):
        messages.error(request, '❌ 權限不足：只有「報修部」人員與超級管理員可以刪除報修單。')
        return redirect('ticket_list')

    ticket = get_object_or_404(RepairTicket, pk=pk)
    
    if ticket.status == 'pending' or ticket.status == 'repairing':
        equipment = ticket.equipment
        equipment.status = 'normal'
        equipment.save()
        
    ticket.delete()
    return redirect('ticket_list')