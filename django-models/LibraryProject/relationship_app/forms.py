from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

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