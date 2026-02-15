from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import Book, Author, UserProfile

# Get the custom user model
CustomUser = get_user_model()

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
    
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Tell us about yourself...'}),
        help_text='Tell us about yourself (max 500 characters)'
    )
    
    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
        help_text='Your contact phone number'
    )
    
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 
                 'date_of_birth', 'profile_photo', 'bio', 'phone_number')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make email required and add styling
        self.fields['email'].required = True
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your email'})
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Choose a username'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your first name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your last name'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm password'})


class CustomUserChangeForm(UserChangeForm):
    """
    Form for updating CustomUser instances.
    """
    
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 
                 'date_of_birth', 'profile_photo', 'bio', 'phone_number')


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
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title'
            }),
            'author': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'title': 'Book Title',
            'author': 'Author',
        }


class AuthorForm(forms.ModelForm):
    """Form for adding authors"""
    
    class Meta:
        model = Author
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name'
            }),
        }