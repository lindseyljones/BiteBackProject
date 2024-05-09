from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Custom Fields", {"fields": ("is_admin",)}),)


# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(Post) 
