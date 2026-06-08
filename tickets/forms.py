# tickets/forms.py
from django import forms
from .models import RepairTicket
from equipments.models import Equipment

class RepairTicketForm(forms.ModelForm):
    class Meta:
        model = RepairTicket
        # 讓使用者填寫：故障設備、報修主旨、詳細描述
        fields = ['equipment', 'title', 'description']
        labels = {
            'equipment': '故障設備資產',
            'title': '報修問題主旨',
            'description': '詳細故障狀況描述',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 🔥 防呆防重複：下拉選單只列出目前狀態為「正常 (normal)」的設備
        self.fields['equipment'].queryset = Equipment.objects.filter(status='normal')
        
        # 自動套用 Bootstrap 5 控制項控制樣式
        self.fields['equipment'].widget.attrs.update({'class': 'form-select'})
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': '例如：辦公室影印機卡紙無法取出'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'rows': 4, 'placeholder': '請詳細說明設備目前的故障反應...'})# tickets/forms.py
from django import forms
from .models import RepairTicket
from equipments.models import Equipment

class RepairTicketForm(forms.ModelForm):
    class Meta:
        model = RepairTicket
        # 讓使用者填寫：故障設備、報修主旨、詳細描述
        fields = ['equipment', 'title', 'description']
        labels = {
            'equipment': '故障設備資產',
            'title': '報修問題主旨',
            'description': '詳細故障狀況描述',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 🔥 防呆防重複：下拉選單只列出目前狀態為「正常 (normal)」的設備
        self.fields['equipment'].queryset = Equipment.objects.filter(status='normal')
        
        # 自動套用 Bootstrap 5 控制項控制樣式
        self.fields['equipment'].widget.attrs.update({'class': 'form-select'})
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': '例如：辦公室影印機卡紙無法取出'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'rows': 4, 'placeholder': '請詳細說明設備目前的故障反應...'})