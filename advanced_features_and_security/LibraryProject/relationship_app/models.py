from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

# Get the user model - this will now point to bookshelf.CustomUser
User = get_user_model()

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
    # Use string reference to the user model
    user = models.OneToOneField(
        User, 
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


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Administrator'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    
    # Use string reference to the user model
    user = models.OneToOneField(
        User, 
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


# Signals to automatically create UserProfile when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile whenever a new User is created"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the UserProfile whenever the User is saved"""
    if not hasattr(instance, 'profile'):
        UserProfile.objects.create(user=instance)
    instance.profile.save()