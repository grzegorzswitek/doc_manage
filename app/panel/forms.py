from django import forms
from django.contrib.auth.forms import UserCreationForm

from dokumentacja.models import User


class ZarejestrujForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', )