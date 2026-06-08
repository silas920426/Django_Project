from django import forms
from .models import Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']
        labels = {
            'name': '部門名稱',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 自動為所有欄位加上 Bootstrap 5 的 class
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': '例如：資訊部'})