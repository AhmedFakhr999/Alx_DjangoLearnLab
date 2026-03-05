from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import UserProfile, Book, Author

# Get the custom user model
CustomUser = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """Form for creating new users with custom fields"""
    
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text='YYYY-MM-DD format'
    )
    
    profile_photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        help_text='Upload a profile photo'
    )
    
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'maxlength': '500'}),
        help_text='Tell us about yourself (max 500 characters)'
    )
    
    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Your contact phone number'
    )
    
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'date_of_birth', 
                  'profile_photo', 'bio', 'phone_number', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make email required
        self.fields['email'].required = True

class CustomUserChangeForm(UserChangeForm):
    """Form for updating existing users"""
    
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'date_of_birth', 
                  'profile_photo', 'bio', 'phone_number', 'is_active', 'is_staff', 'is_superuser')

class ExtendedUserCreationForm(CustomUserCreationForm):
    """Extended form with role selection"""
    
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
    """Form for adding authors"""
    class Meta:
        model = Author
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter author name'}),
        }