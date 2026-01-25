from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.contrib.auth.views import LoginView, LogoutView  # Add this import
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Book, Library, Author

# Function-based view to list all books
def list_books(request):
    """
    Function-based view that lists all books in the database.
    """
    # Get all books from database
    books = Book.objects.select_related('author').all()
    
    # Render the template with books data
    return render(request, 'relationship_app/list_books.html', {
        'books': books
    })

# Class-based view to display all libraries
class LibraryListView(ListView):
    """
    Class-based view that lists all libraries.
    """
    model = Library
    template_name = 'relationship_app/library_list.html'
    context_object_name = 'libraries'
    
    def get_queryset(self):
        """Override to prefetch related books and librarian."""
        return Library.objects.prefetch_related('books').all()

# Class-based view to display details of a specific library
class LibraryDetailView(DetailView):
    """
    Class-based view that displays details for a specific library.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_object(self, queryset=None):
        """Get the library object or return 404 if not found."""
        pk = self.kwargs.get('pk')
        return get_object_or_404(Library.objects.prefetch_related('books__author'), pk=pk)

# Additional function-based view for library detail (alternative to class-based)
def library_detail_function(request, library_id):
    """
    Alternative function-based view for library details.
    """
    library = get_object_or_404(Library.objects.prefetch_related('books__author'), id=library_id)
    return render(request, 'relationship_app/library_detail.html', {
        'library': library
    })

# Home page view - function based
def home(request):
    """Home page view showing basic statistics and links"""
    total_books = Book.objects.count()
    total_libraries = Library.objects.count()
    recent_books = Book.objects.select_related('author').order_by('-id')[:5]
    
    return render(request, 'relationship_app/home.html', {
        'total_books': total_books,
        'total_libraries': total_libraries,
        'recent_books': recent_books,
    })

# Authentication Views

class CustomLoginView(LoginView):
    """Custom login view"""
    template_name = 'relationship_app/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        messages.success(self.request, 'Login successful!')
        return reverse_lazy('home')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return super().form_invalid(form)

class CustomLogoutView(LogoutView):
    """Custom logout view"""
    next_page = 'home'
    
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'You have been logged out.')
        return super().dispatch(request, *args, **kwargs)

class RegisterView(CreateView):
    """User registration view"""
    form_class = UserCreationForm
    template_name = 'relationship_app/register.html'
    success_url = reverse_lazy('relationship_app:login')  # Changed to app-specific login
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Registration successful! Please log in.')
        return response
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'You are already logged in.')
            return redirect('home')
        return super().get(request, *args, **kwargs)

# Protected views (require login)
@login_required
def protected_view_example(request):
    """Example of a protected view using decorator"""
    return render(request, 'relationship_app/protected.html', {
        'user': request.user
    })

class ProtectedListView(LoginRequiredMixin, ListView):
    """Example of a protected class-based view"""
    model = Book
    template_name = 'relationship_app/protected_books.html'
    context_object_name = 'books'
    login_url = 'relationship_app:login'  # Changed to app-specific login
    
    def get_queryset(self):
        return Book.objects.select_related('author').all()