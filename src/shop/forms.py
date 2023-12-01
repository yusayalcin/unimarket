from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.db import models


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name")


class UpdateProfileForm(forms.ModelForm):
    bio = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5})
    )
    facebook = forms.CharField(widget=forms.TextInput)
    phone = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = Profile
        fields = ("bio", "facebook", "phone")
