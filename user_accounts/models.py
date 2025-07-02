# user_accounts/models.py

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
import uuid
from django.core.exceptions import ValidationError
from .choices import OrganizationTypes, UserTypes  # Assumed enums defined elsewhere


def user_id_proof_path(instance, filename):
    return f"user_docs/{instance.user_type}/{instance.user_id}/id_proof/{filename}"

def user_address_proof_path(instance, filename):
    return f"user_docs/{instance.user_type}/{instance.user_id}/address_proof/{filename}"


class CustomUserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Please enter an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(email, password, **extra_fields)


class UserAccount(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)

    user_type = models.CharField(max_length=10, choices=UserTypes.choices, default=UserTypes.BUYER)
    organization_type = models.CharField(max_length=50, choices=OrganizationTypes.choices, default='individual')
    company_name = models.CharField(max_length=255, blank=True, null=True)
    gstin = models.CharField(max_length=20, blank=True, null=True)

    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.TextField()
    postal_code = models.CharField(max_length=15)

    id_proof = models.FileField(upload_to=user_id_proof_path)
    address_proof = models.FileField(upload_to=user_address_proof_path)

    is_verified_by_admin = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)

    objects = CustomUserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'full_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.full_name}   -  {self.user_type}"

    def clean(self):
       if self.organization_type != 'individual' and not self.company_name:
            raise ValidationError("Company name is required for non-individual organizations.")
    
    def save(self, *args, **kwargs):
        if self.pk:
            original = UserAccount.objects.get(pk=self.pk)
            if original.user_type != self.user_type:
                raise ValidationError("Cannot change user_type once registered.")
        super().save(*args, **kwargs)
        
