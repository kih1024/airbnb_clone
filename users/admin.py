from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    # 클래스는 모델을 조정 할 수 있다
    """Custom User Admin """

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                )
            },
        ),
    )

    list_filter = UserAdmin.list_filter + ("superhost",)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "email_verified",
        "email_secret",
    )
    # list_filter = ("superhost","gender","currency",)
