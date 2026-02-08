from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'relationship_app'

urlpatterns = [
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    
    # Role-based views
    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
    
    # Book views with permission_required decorator
    path('books/', views.list_books, name='book-list'),
    path('books/<int:book_id>/', views.book_detail, name='book-detail'),
    path('books/add/', views.add_book, name='add-book'),          # Uses @permission_required
    path('books/<int:book_id>/edit/', views.edit_book, name='edit-book'),    # Uses @permission_required
    path('books/<int:book_id>/delete/', views.delete_book, name='delete-book'), # Uses @permission_required
    
    # Class-based alternatives
    path('books/class/add/', views.BookCreateView.as_view(), name='add-book-class'),
    path('books/class/<int:pk>/edit/', views.BookUpdateView.as_view(), name='edit-book-class'),
    path('books/class/<int:pk>/delete/', views.BookDeleteView.as_view(), name='delete-book-class'),
    
    # Other URLs
    path('protected/', views.protected_view_example, name='protected'),
    path('libraries/', views.LibraryListView.as_view(), name='library-list'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library-detail'),
]