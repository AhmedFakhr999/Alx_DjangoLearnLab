from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Book, Author

class ExtendedUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('Admin', 'Administrator'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        initial='Member',
        help_text='Select your role'
    )
    
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'role']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Create or update the UserProfile with the selected role
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.role = self.cleaned_data['role']
            profile.save()
        
        return user

class BookForm(forms.ModelForm):
    """Form for adding and editing books"""
    class Meta:
        model = Book
        fields = ['title', 'author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book title'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Book Title',
            'author': 'Author',
        }
        help_texts = {
            'title': 'Enter the full title of the book',
            'author': 'Select the author from the list or create a new one',
        }

class AuthorForm(forms.ModelForm):
    """Form for adding authors (for completeness)"""
    class Meta:
        model = Author
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter author name'}),
        }