from django import forms
from .models import Bank


class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['bank_name', 'account_code', 'account_holder','status']
        error_messages = {
            'account_code': {
                'required': 'شماره حساب نمی‌تواند خالی باشد.',
            },
            'bank_name': {
                'required': 'نام بانک نمی‌تواند خالی باشد.',
            }
        }

    
    def clean_account_code(self):
        account_code = self.cleaned_data.get('account_code')
        bank_name = self.cleaned_data.get('bank_name')

        if not account_code:
            raise forms.ValidationError("این فیلد نمی‌تواند خالی باشد.")

        if not account_code.isdigit():
            raise forms.ValidationError("شماره حساب باید فقط عدد باشد.")

        return account_code