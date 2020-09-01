from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django_registration.forms import RegistrationForm
from .models import CustomUser


class CustomUserForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')


class AdminCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')


class AdminChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')
