from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام گروه را وارد کنید'
            })
        }
        labels = {
            'name': 'نام گروه'
        }

User = get_user_model()

class UserForm(forms.ModelForm):
    password1 = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput,
        required=False
    )
    password2 = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput,
        required=False
    )

    group = forms.ModelChoiceField(
        queryset=Group.objects.all().order_by('name'),
        required=False,
        label='گروه'
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # اگر ساخت کاربر جدید است
        if not self.instance.pk:
            self.fields['password1'].required = True
            self.fields['password2'].required = True
        else:
            # در حالت ویرایش، گروه فعلی کاربر نمایش داده شود
            current_group = self.instance.groups.first()
            if current_group:
                self.fields['group'].initial = current_group

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        # حالت ساخت
        if not self.instance.pk:
            if not password1 or not password2:
                raise forms.ValidationError('رمز عبور و تکرار آن الزامی است.')

        # اگر یکی از رمزها وارد شده، باید هر دو وارد شوند و برابر باشند
        if password1 or password2:
            if password1 != password2:
                self.add_error('password2', 'تکرار کلمه عبور با رمز عبور یکسان نیست.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        
        password1 = self.cleaned_data.get('password1')

        if password1:
            user.set_password(password1)

        group = self.cleaned_data.get('group')

        if commit:
            user.save()
            if group:
                user.groups.set([group])
            else:
                user.groups.clear()

        return user