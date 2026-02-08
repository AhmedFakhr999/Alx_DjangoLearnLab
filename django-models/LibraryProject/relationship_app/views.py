from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate  # Add these imports
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from .models import Book, Library, Author

# Function-based view to list all books
def list_books(request):
    books = Book.objects.select_related('author').all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view to display all libraries
class LibraryListView(ListView):
    model = Library
    template_name = 'relationship_app/library_list.html'
    context_object_name = 'libraries'
    
    def get_queryset(self):
        return Library.objects.prefetch_related('books').all()

# Class-based view for library detail
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Library.objects.prefetch_related('books__author'), pk=pk)

# Function-based view for library detail
def library_detail_function(request, library_id):
    library = get_object_or_404(Library.objects.prefetch_related('books__author'), id=library_id)
    return render(request, 'relationship_app/library_detail.html', {'library': library})

# Home page view
def home(request):
    total_books = Book.objects.count()
    total_libraries = Library.objects.count()
    recent_books = Book.objects.select_related('author').order_by('-id')[:5]
    
    return render(request, 'relationship_app/home.html', {
        'total_books': total_books,
        'total_libraries': total_libraries,
        'recent_books': recent_books,
    })

# FUNCTION-BASED LOGIN VIEW (to use django.contrib.auth.login)
def user_login(request):
    """Function-based login view using django.contrib.auth.login"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # Use django.contrib.auth.login
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    
    return render(request, 'relationship_app/login.html', {'form': form})

# FUNCTION-BASED LOGOUT VIEW
def user_logout(request):
    """Function-based logout view"""
    from django.contrib.auth import logout
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

# FUNCTION-BASED REGISTER VIEW
def register(request):
    """Function-based registration view using django.contrib.auth.forms"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Auto-login after registration
            login(request, user)  # Use django.contrib.auth.login
            messages.success(request, f'Account created for {user.username}! You are now logged in.')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'relationship_app/register.html', {'form': form})

# Protected views
@login_required
def protected_view_example(request):
    return render(request, 'relationship_app/protected.html', {'user': request.user})

class ProtectedListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'relationship_app/protected_books.html'
    context_object_name = 'books'
    login_url = 'relationship_app:login'
    
    def get_queryset(self):
        return Book.objects.select_related('author').all()