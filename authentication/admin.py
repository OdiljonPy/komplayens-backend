from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'username', 'phone_number')
    list_display_links = ('id', 'first_name')
    search_fields = ('first_name', 'last_name', 'username', 'phone_number')
