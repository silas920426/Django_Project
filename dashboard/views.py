from django.shortcuts import render
from tickets.models import RepairTicket
from equipments.models import Equipment

def dashboard(request):
    context = {
        "equipment_count": Equipment.objects.count(),
        "pending": RepairTicket.objects.filter(status='pending').count(),
        "repairing": RepairTicket.objects.filter(status='repairing').count(),
        "completed": RepairTicket.objects.filter(status='completed').count(),
    }
    return render(request, "dashboard/index.html", context)