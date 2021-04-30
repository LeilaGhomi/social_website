from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import models

from apps.account.models import User


class AccountCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'reg_type')

    # def _clean_form(self):
    #     if self.reg_type == 'email' and self.email is None:
    #         messages.error('Enter your email address')
    #     elif self.reg_type == 'sms' and self.phone_number is None:
    #         messages.error('Enter your phone number')
    #     else:
    #         return HttpResponseRedirect(reverse('register'))


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'gender', 'phone_number', 'bio', 'website', 'pro_pic')

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        del self.fields['password']
