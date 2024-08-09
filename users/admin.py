from django.contrib import admin
from .models import Note
from users.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserModelAdmin(BaseUserAdmin):
    
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ["id", "email", "name", "tc", "is_admin", "level"]
    list_filter = ["is_admin"]
    fieldsets = [
        ('User Credentials', {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name", "tc"]}),
        ("Game Level", {"fields": ['level']}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "tc", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email", "id"]
    ordering = ["email"]
    filter_horizontal = []



# Register your models here.
admin.site.register(Note)
admin.site.register(User, UserModelAdmin)
