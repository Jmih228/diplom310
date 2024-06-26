from django.contrib import admin
from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone_number', 'city', 'invite_code')
    list_filter = ('id', 'email', 'phone_number', 'city', 'invite_code')
    search_fields = ('id', 'email', 'phone_number', 'city', 'invite_code')
