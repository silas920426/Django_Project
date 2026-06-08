from django.db import models
from django.contrib.auth.models import User
from equipments.models import Equipment

class RepairTicket(models.Model):

    STATUS = [
        ('pending', '待處理'),
        ('assigned', '已派工'),
        ('repairing', '維修中'),
        ('completed', '已完成'),
        ('closed', '已結案'),
    ]

    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField()

    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title