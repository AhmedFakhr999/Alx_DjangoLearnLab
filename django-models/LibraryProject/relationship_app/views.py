from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView  # Add TemplateView here
from .models import Book, Library, Author

# Function-based view to list all books
def list_books(request):
    """
    Function-based view that lists all books in the database.
    """
    # Get all books from database
    books = Book.objects.all()
    
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

# Alternative: Class-based home view
class HomeView(TemplateView):
    template_name = 'relationship_app/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_books'] = Book.objects.count()
        context['total_libraries'] = Library.objects.count()
        context['recent_books'] = Book.objects.select_related('author').order_by('-id')[:5]
        return context