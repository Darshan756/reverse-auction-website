# user_accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import UserAccount


@admin.register(UserAccount)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'full_name','user_type','is_active', 'is_staff', )
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
        ('User Type & Organization', {'fields': ('user_type', 'organization_type', 'company_name', 'gstin')}),
        ('Address', {'fields': ('country', 'state', 'city', 'street', 'postal_code')}),
        ('Documents', {'fields': ('id_proof', 'address_proof')}),
        ('Verification', {'fields': ('is_verified_by_admin', 'verification_date')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'phone_number', 'password1', 'password2', 'user_type', 'is_staff', 'is_active')}
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        """
        Make 'user_type' read-only after the object is created.
        """
        if obj:  # editing existing user
            return self.readonly_fields + ('user_type',)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        """
        Catch validation errors from model.save and show friendly admin message.
        """
        try:
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            self.message_user(request, str(e), level=messages.ERROR)
    
    @admin.display(description='ID Proof')
    def id_proof_link(self, obj):
        if obj.id_proof:
            return format_html('<a href="{}" target="_blank">View</a>', obj.id_proof.url)
        return "No file"
  
    @admin.display(description='Address Proof')
    def address_proof_link(self, obj):
        if obj.address_proof:
            return format_html('<a href="{}" target="_blank">View</a>', obj.address_proof.url)
        return "No file"

