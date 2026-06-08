from django.shortcuts import render
from tickets.models import RepairTicket
from equipments.models import Equipment
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def dashboard(request):
    context = {
        "equipment_count": Equipment.objects.count(),
        "pending": RepairTicket.objects.filter(status='pending').count(),
        "repairing": RepairTicket.objects.filter(status='repairing').count(),
        "completed": RepairTicket.objects.filter(status='completed').count(),
    }
    return render(request, "dashboard/index.html", context)

def dashboard(request):
    context = {
        "equipment_count": Equipment.objects.count(),
        "pending": RepairTicket.objects.filter(status='pending').count(),
        "repairing": RepairTicket.objects.filter(status='repairing').count(),
        "completed": RepairTicket.objects.filter(status='completed').count(),
    }
    return render(request, "dashboard/index.html", context)