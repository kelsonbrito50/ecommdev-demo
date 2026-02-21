"""Custom User model with extended profile fields."""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Extended user model for the e-commerce platform."""

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    cpf = models.CharField(max_length=14, blank=True, help_text='Brazilian CPF')
    date_of_birth = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    # Address fields
    address_street = models.CharField(max_length=255, blank=True)
    address_number = models.CharField(max_length=20, blank=True)
    address_complement = models.CharField(max_length=100, blank=True)
    address_neighborhood = models.CharField(max_length=100, blank=True)
    address_city = models.CharField(max_length=100, blank=True)
    address_state = models.CharField(max_length=2, blank=True)
    address_zipcode = models.CharField(max_length=10, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def __str__(self):
        return self.email

    @property
    def full_address(self):
        parts = filter(None, [
            self.address_street,
            self.address_number,
            self.address_complement,
            self.address_neighborhood,
            self.address_city,
            self.address_state,
            self.address_zipcode,
        ])
        return ', '.join(parts)
