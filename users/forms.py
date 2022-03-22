from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

# used to update django forms to use them the way i need to


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email"]


class ProfileUpdateForm(forms.ModelForm):
    firstName = forms.CharField(label="First Name", max_length=50)
    lastName = forms.CharField(label="Last Name", max_length=50)

    class Meta:
        model = Profile
        fields = ["firstName", "lastName"]
