# users/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Profile
from departments.models import Department

class ProfileUpdateForm(forms.ModelForm):
    # 來自 User 模型的基本資料
    last_name = forms.CharField(label='姓氏', max_length=30, required=False)
    first_name = forms.CharField(label='名字', max_length=30, required=False)
    email = forms.EmailField(label='電子郵件', required=False)
    
    # 來自 Profile 模型的聯絡資料
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False, label='所屬部門')
    phone = forms.CharField(label='聯絡電話', max_length=20, required=False)

    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'email']

    def __init__(self, *args, **kwargs):
        # 🔥 從參數中將當前登入的使用者抽出來 (沒有的話預設為 None)
        current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)
        
        # 如果使用者已經有 profile，把資料預填進表單
        if hasattr(self.instance, 'profile'):
            self.fields['department'].initial = self.instance.profile.department
            self.fields['phone'].initial = self.instance.profile.phone
            
        # 🔥 核心權限邏輯：如果當前修改資料的人「不是」超級管理員，就鎖定部門欄位
        if current_user and not current_user.is_superuser:
            self.fields['department'].disabled = True  # 變成唯讀鎖定狀態
            self.fields['department'].help_text = "⚠️ 只有超級管理員可以變更您的所屬部門。"

        # 自動套用 Bootstrap 5 外觀樣式
        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        # 先儲存 User 內建資料
        user = super().save(commit=commit)
        
        # 同步更新或建立對應的 Profile 資料
        profile, created = Profile.objects.get_or_create(user=user)
        
        # 即使前端 disabled，後端依然會拿原本的資料存回去，防止變成空白
        profile.department = self.cleaned_data['department']
        profile.phone = self.cleaned_data['phone']
        
        if commit:
            profile.save()
        return user