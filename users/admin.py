from django.contrib import admin
from .models import User, UserType, UserLog
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Register your models here.

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    # form = UserAdminChangeForm
    # add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.

    list_display = ("email", "admin", "last_login")
    list_filter = ("admin",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "date_of_birth",
                    "gender",
                    "contact_number",
                    "sms_notification_active",
                    "email_notification_active",
                    "user_image",
                )
            },
        ),
        ("Login info", {"fields": ("last_login",)}),
        (
            "Permissions",
            {
                "fields": (
                    "admin",
                    "staff",
                    "is_active",
                )
            },
        ),
    )
    readonly_fields = ("last_login",)
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(UserType)
admin.site.register(UserLog)
