from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import AdminChangeForm, AdminCreationForm
from .models import CustomUser


# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = AdminCreationForm
    form = AdminChangeForm
    model = CustomUser
    list_display = ('username', 'get_full_name', 'email')
    fieldsets = ((None, {'fields': ('avatar',)}),)

    @staticmethod
    def full_name(obj):
        return f'{obj.first_name} {obj.last_name}'


admin.site.register(CustomUser, CustomUserAdmin)
