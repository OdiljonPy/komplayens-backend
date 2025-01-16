from django.contrib import admin
from .models import User, Customer


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone_number')
    list_display_links = ('id', 'first_name')
    search_fields = ('first_name', 'last_name', 'phone_number')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip_address', 'user_agent')
    list_display_links = ('id', 'ip_address')
