"""Admin configuration for authentication app."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_staff', 'created_at']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'address_state']
    search_fields = ['email', 'username', 'first_name', 'last_name', 'cpf']
    ordering = ['-created_at']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile', {'fields': ('phone', 'cpf', 'date_of_birth', 'avatar')}),
        ('Address', {'fields': (
            'address_street', 'address_number', 'address_complement',
            'address_neighborhood', 'address_city', 'address_state', 'address_zipcode',
        )}),
    )
