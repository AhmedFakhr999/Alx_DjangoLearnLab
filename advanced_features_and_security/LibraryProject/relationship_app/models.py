from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
import os

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
        # Get file extension
        ext = filename.split('.')[-1]
        # Create filename with user ID to avoid conflicts
        filename = f'profile_photos/user_{instance.id}_profile.{ext}'
        return os.path.join('profile_photos/', filename)
    
    profile_photo = models.ImageField(
        _('profile photo'),
        upload_to=profile_photo_upload_path,
        null=True,
        blank=True,
        help_text=_('Upload a profile photo (max 5MB)')
    )
    
    # Additional useful fields
    bio = models.TextField(
        _('biography'),
        max_length=500,
        blank=True,
        help_text=_('Tell us about yourself (max 500 characters)')
    )
    
    phone_number = models.CharField(
        _('phone number'),
        max_length=20,
        blank=True,
        help_text=_('Your contact phone number')
    )
    
    # Track when the user joined
    joined_date = models.DateTimeField(
        _('joined date'),
        auto_now_add=True
    )
    
    # Set email as the USERNAME_FIELD for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    # Use the custom manager
    objects = CustomUserManager()
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-joined_date']
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """Return the full name of the user"""
        full_name = f'{self.first_name} {self.last_name}'.strip()
        return full_name if full_name else self.username
    
    def get_short_name(self):
        """Return the short name for the user"""
        return self.first_name or self.username
    
    @property
    def age(self):
        """Calculate user's age from date of birth"""
        from datetime import date
        if self.date_of_birth:
            today = date.today()
            born = self.date_of_birth
            return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        return None
    
    @property
    def has_profile_photo(self):
        """Check if user has a profile photo"""
        return bool(self.profile_photo and hasattr(self.profile_photo, 'url'))
    
    def clean(self):
        """Custom validation for the user model"""
        from django.core.exceptions import ValidationError
        from datetime import date
        
        super().clean()
        
        # Validate date of birth (must be in the past)
        if self.date_of_birth and self.date_of_birth > date.today():
            raise ValidationError({'date_of_birth': 'Date of birth cannot be in the future.'})


# Keep your existing models but update foreign keys to use CustomUser
class Author(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    
    def __str__(self):
        return f"{self.title} by {self.author.name}"
    
    class Meta:
        permissions = [
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
            ("can_view_book", "Can view book"),
        ]
        ordering = ['title']


class Library(models.Model):
    name = models.CharField(max_length=255)
    books = models.ManyToManyField(Book, related_name='libraries')
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
    
    def get_book_count(self):
        return self.books.count()


class Librarian(models.Model):
    # Update to use CustomUser instead of User
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE,
        related_name='librarian_profile'
    )
    library = models.OneToOneField(
        Library, 
        on_delete=models.CASCADE,
        related_name='librarian'
    )
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.library.name}"
    
    class Meta:
        ordering = ['user__first_name', 'user__last_name']


# UserProfile model for role-based access (using CustomUser)
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Administrator'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    
    # Update to use CustomUser
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='Member'
    )
    
    def __str__(self):
        return f"{self.user.email} - {self.role}"
    
    def is_admin(self):
        return self.role == 'Admin'
    
    def is_librarian(self):
        return self.role == 'Librarian'
    
    def is_member(self):
        return self.role == 'Member'
    
    class Meta:
        permissions = [
            ("can_manage_users", "Can manage users"),
        ]


# Signals to automatically create UserProfile when a new CustomUser is created
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile whenever a new CustomUser is created"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    """Save the UserProfile whenever the CustomUser is saved"""
    if not hasattr(instance, 'profile'):
        UserProfile.objects.create(user=instance)
    instance.profile.save()