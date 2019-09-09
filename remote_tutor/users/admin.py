from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from remote_tutor.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("full_name",)}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "full_name", "is_superuser"]
    search_fields = ["full_name"]
