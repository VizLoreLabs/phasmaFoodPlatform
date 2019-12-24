from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from .forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    ordering = ("-date_joined",)
    fieldsets = (
                    ("Authentication Info", {"fields": ("email", "password",)}),
                    ("Personal Info", {"fields": ("first_name", "last_name",)}),
                    ("User Type", {"fields": ("user_type",)}),
                    ("Company", {"fields": ("company",)}),
                    ("Device", {"fields": ("phasma_device",)}),
                    ("Permissions", {"fields": ("is_superuser", "is_staff", "is_active")}),
                    ("Date joined", {"fields": ("date_joined",)}),
                )
    readonly_fields = ("date_joined",)
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2")}
         ),
    )
    list_display = ("email", "first_name", "last_name", "date_joined")
    list_filter = ("is_active",)
    search_fields = ("email",)
    filter_horizontal = ()
