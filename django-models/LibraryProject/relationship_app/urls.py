from django.urls import path
from . import views
from .views import list_books

app_name = 'relationship_app'  # Add this namespace

urlpatterns = [
    # Function-based view for listing all books
    path('books/', views.list_books, name='book-list'),
    
    # Class-based view for listing all libraries
    path('libraries/', views.LibraryListView.as_view(), name='library-list'),
    
    # Class-based view for library detail
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library-detail'),
    
    # Alternative function-based view for library detail
    path('library-fn/<int:library_id>/', views.library_detail_function, name='library-detail-fn'),
]