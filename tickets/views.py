# tickets/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import RepairTicket
from .forms import RepairTicketForm
from equipments.models import Equipment

# 檢視報修清單（加上登入保護）
@login_required(login_url='login')
def list(request):
    # 如果是管理員，可以看到全公司的報修單；一般員工只能看到自己送出的單子
    if request.user.is_superuser:
        tickets = RepairTicket.objects.all().order_by('-created_at')
    else:
        tickets = RepairTicket.objects.filter(reporter=request.user).order_by('-created_at')
        
    return render(request, 'tickets/list.html', {'tickets': tickets})

# 創建報修單 + 自動變更設備狀態為「維修中」
@login_required(login_url='login')
def create(request):
    if request.method == 'POST':
        form = RepairTicketForm(request.POST)
        if form.is_valid():
            # commit=False 代表先產生資料庫物件，但先不急著寫入（因為要補上報修人欄位）
            ticket = form.save(commit=False)
            ticket.reporter = request.user
            ticket.status = 'pending'  # 初始狀態設為待處理
            ticket.save()              # 正式寫入資料庫，產生報修單
            
            # 🔥【核心業務邏輯】同步更新設備狀態
            equipment = ticket.equipment
            equipment.status = 'repair'  # 將該台設備變更為「維修中」
            equipment.save()             # 儲存設備的狀態更新
            
            return redirect('ticket_list')
    else:
        form = RepairTicketForm()
    return render(request, 'tickets/form.html', {'form': form})

# 🔥【新增】查看維修單詳細內容（唯讀模式 + 處理功能）
@login_required(login_url='login')
def detail(request, pk):
    # 取得特定的報修單
    ticket = get_object_or_404(RepairTicket, pk=pk)
    
    # 使用原本的表單，HTML 中會把它變成 disabled (唯讀)
    form = RepairTicketForm(instance=ticket)
    
    # 當按下「已處理」按鈕時（送出 POST 請求）
    if request.method == 'POST' and 'mark_processed' in request.POST:
        # 1. 將報修單狀態改為已完成
        ticket.status = 'completed'
        ticket.save()
        
        # 2. 連動：將對應的設備狀態改回「正常」
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

# 🔥【更新】刪除報修單（包含狀態恢復防呆機制）
@login_required(login_url='login')
def delete(request, pk):
    ticket = get_object_or_404(RepairTicket, pk=pk)
    
    # 如果報修單在還沒處理前就被刪除了，把設備狀態恢復成正常
    if ticket.status == 'pending' or ticket.status == 'repairing':
        equipment = ticket.equipment
        equipment.status = 'normal'
        equipment.save()
        
    ticket.delete()
    return redirect('ticket_list')