from django.contrib import admin
from .models import User, Employee
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'username', 'phone_number')
    list_display_links = ('id', 'full_name')
    search_fields = ('full_name', 'username', 'phone_number')




@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name')