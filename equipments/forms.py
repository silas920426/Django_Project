from django import forms
from .models import Equipment

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'serial_number', 'department', 'location', 'status']
        labels = {
            'name': '設備名稱',
            'serial_number': '設備序號/資產編號',
            'department': '所屬部門',
            'location': '放置位置',
            'status': '設備狀態',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 自動為所有欄位加上 Bootstrap 5 的 class
        for field_name, field in self.fields.items():
            if field_name == 'department' or field_name == 'status':
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})