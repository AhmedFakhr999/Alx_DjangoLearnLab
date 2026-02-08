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
    
    # Protected example URLs
    path('protected/', views.protected_view_example, name='protected'),
    path('protected-books/', views.ProtectedListView.as_view(), name='protected-books'),
    
    # Original URLs
    path('books/', views.list_books, name='book-list'),
    path('libraries/', views.LibraryListView.as_view(), name='library-list'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library-detail'),
    path('library-fn/<int:library_id>/', views.library_detail_function, name='library-detail-fn'),
]