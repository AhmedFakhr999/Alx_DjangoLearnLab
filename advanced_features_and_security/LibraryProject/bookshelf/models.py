from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
import os

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    class Meta:
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]

    def __str__(self):
        return self.title

class CustomUserManager(BaseUserManager):
    """
    Custom manager for CustomUser model.
    Handles user creation with email as the unique identifier.
    """
    
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular user with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom User model extending AbstractUser with additional fields.
    Uses email as the unique identifier for authentication.
    """
    
    # Make email required and unique
    email = models.EmailField(
        _('email address'),
        unique=True,
        help_text=_('Required. Provide a valid email address.')
    )
    
    # Add custom fields as required by the task
    date_of_birth = models.DateField(
        _('date of birth'),
        null=True,
        blank=True,
        help_text=_('Your date of birth (YYYY-MM-DD)')
    )
    
    def profile_photo_upload_path(instance, filename):
        """Generate upload path for profile photos"""
        ext = filename.split('.')[-1]
        filename = f'profile_photos/user_{instance.id}_profile.{ext}'
        return os.path.join('profile_photos/', filename)
    
    profile_photo = models.ImageField(
        _('profile photo'),
        upload_to=profile_photo_upload_path,
        null=True,
        blank=True,
        help_text=_('Upload a profile photo (max 5MB)')
    )
    
    # Set email as the USERNAME_FIELD for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    # Use the custom manager
    objects = CustomUserManager()
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        return self.email