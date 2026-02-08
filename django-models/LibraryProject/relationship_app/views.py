from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from .models import Book, Library, Author, UserProfile

# Custom test functions for role-based access
def is_admin(user):
    """Check if user has Admin role"""
    if user.is_authenticated:
        return hasattr(user, 'profile') and user.profile.role == 'Admin'
    return False

def is_librarian(user):
    """Check if user has Librarian role"""
    if user.is_authenticated:
        return hasattr(user, 'profile') and user.profile.role == 'Librarian'
    return False

def is_member(user):
    """Check if user has Member role"""
    if user.is_authenticated:
        return hasattr(user, 'profile') and user.profile.role == 'Member'
    return False

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

# REGISTRATION VIEW WITH ROLE SELECTION
def register(request):
    """Enhanced registration view with role selection"""
    from .forms import ExtendedUserCreationForm  # We'll create this form
    
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Auto-login after registration
            login(request, user)
            messages.success(request, f'Account created for {user.username}! You are now logged in as a {user.profile.role}.')
            return redirect('home')
    else:
        form = ExtendedUserCreationForm()
    
    return render(request, 'relationship_app/register.html', {'form': form})

# ROLE-BASED VIEWS

@login_required
@user_passes_test(is_admin)
def admin_view(request):
    """View accessible only to Admin users"""
    user_count = User.objects.count()
    book_count = Book.objects.count()
    library_count = Library.objects.count()
    
    return render(request, 'relationship_app/admin_view.html', {
        'user_count': user_count,
        'book_count': book_count,
        'library_count': library_count,
        'current_user': request.user,
    })

@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    """View accessible only to Librarian users"""
    # Librarians can see all books and libraries
    books = Book.objects.select_related('author').all()
    libraries = Library.objects.all()
    
    return render(request, 'relationship_app/librarian_view.html', {
        'books': books,
        'libraries': libraries,
        'current_user': request.user,
    })

@login_required
@user_passes_test(is_member)
def member_view(request):
    """View accessible only to Member users"""
    # Members can see books and basic library info
    recent_books = Book.objects.select_related('author').order_by('-id')[:10]
    libraries = Library.objects.all()
    
    return render(request, 'relationship_app/member_view.html', {
        'recent_books': recent_books,
        'libraries': libraries,
        'current_user': request.user,
    })

# Protected views (existing)
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