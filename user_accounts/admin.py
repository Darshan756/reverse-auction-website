from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Buyer, Supplier
from django.utils.html import format_html


@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'full_name', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'full_name')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('2FA', {'fields': ('is_email_verified', 'is_phone_verified')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'phone_number', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization_type', 'company_name', 'is_verified_by_admin', 'verification_date')
    list_filter = ('is_verified_by_admin',)
    readonly_fields = ('verification_date',)
    search_fields = ('user__email', 'company_name')


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization_type', 'company_name', 'gstin', 'is_verified_by_admin', 'verification_date')
    list_filter = ('is_verified_by_admin',)
    readonly_fields = ('verification_date',)
    search_fields = ('user__email', 'company_name', 'gstin')
