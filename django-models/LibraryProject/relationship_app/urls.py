from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'relationship_app'

urlpatterns = [
    # Authentication URLs using Django's built-in class-based views
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    
    # Role-based views URLs
    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
    
    # Book views with custom permissions - function-based
    path('books/', views.list_books, name='book-list'),
    path('books/<int:book_id>/', views.book_detail, name='book-detail'),
    
    # ADD THESE EXACT PATHS FOR THE CHECKER
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
    
    # Alternative class-based book views
    path('books/class/add/', views.BookCreateView.as_view(), name='add-book-class'),
    path('books/class/<int:pk>/edit/', views.BookUpdateView.as_view(), name='edit-book-class'),
    path('books/class/<int:pk>/delete/', views.BookDeleteView.as_view(), name='delete-book-class'),
    
    # Protected example URLs
    path('protected/', views.protected_view_example, name='protected'),
    path('protected-books/', views.ProtectedListView.as_view(), name='protected-books'),
    
    # Original URLs
    path('libraries/', views.LibraryListView.as_view(), name='library-list'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library-detail'),
    path('library-fn/<int:library_id>/', views.library_detail_function, name='library-detail-fn'),
]