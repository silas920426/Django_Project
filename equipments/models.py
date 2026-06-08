from django.db import models
from departments.models import Department

class Equipment(models.Model):

    STATUS = [
        ('normal', '正常'),
        ('repair', '維修中'),
        ('scrap', '報廢'),
    ]

    name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS, default='normal')

    def __str__(self):
        return self.name