from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm
from .models import *
class PasswordResetRequestForm(PasswordResetForm):
    email = forms.EmailField(label='Email')
    

class PasswordResetConfirmationForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput,
    )
    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput,
    )

class SMSForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}), label='Message')

    def clean(self):
        cleaned_data = super().clean()
        message = cleaned_data.get('message')

        if not message:
            self.add_error('message', 'Please enter a message.')

        return cleaned_data
    

