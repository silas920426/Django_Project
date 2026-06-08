# users/models.py
from django.db import models
from django.contrib.auth.models import User
from departments.models import Department

class Profile(models.Model):
    # 變更權限角色
    ROLE_CHOICES = [
        ('employee', '員工'),
        ('supervisor', '主管'),
        ('manager', '經理'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"