from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import Book, Author, UserProfile

# Get the user model (now points to bookshelf.CustomUser)
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating new CustomUser instances.
    Includes all the custom fields.
    """
    
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text='Select your date of birth'
    )
    
    profile_photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        help_text='Upload a profile photo (optional)'
    )
    
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 
                 'date_of_birth', 'profile_photo')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make email required and add styling
        self.fields['email'].required = True
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your email'})
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Choose a username'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your first name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your last name'})


class CustomUserChangeForm(UserChangeForm):
    """
    Form for updating CustomUser instances.
    """
    
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 
                 'date_of_birth', 'profile_photo')


class ExtendedUserCreationForm(CustomUserCreationForm):
    """
    Extended form with role selection for registration.
    """
    
    ROLE_CHOICES = [
        ('Admin', 'Administrator'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        initial='Member',
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Select your role'
    )
    
    class Meta(CustomUserCreationForm.Meta):
        fields = CustomUserCreationForm.Meta.fields + ('role',)
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        if commit:
            user.save()
            # Create or update the UserProfile with the selected role
            # Note: The signal might have already created the profile
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.role = self.cleaned_data['role']
            profile.save()
        
        return user


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role']