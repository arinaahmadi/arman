from django import forms
from .models import Bank


class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['bank_name', 'account_code', 'account_holder']
