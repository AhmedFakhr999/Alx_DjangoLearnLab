from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView, CustomLogoutView, RegisterView  # Import the views

app_name = 'relationship_app'

urlpatterns = [
    # Home page (moved to main urls.py)
    # path('', views.home, name='home'),  # Remove this if home is in main urls.py
    
    # Authentication URLs
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    
    # Protected example URLs (require login)
    path('protected/', views.protected_view_example, name='protected'),
    path('protected-books/', views.ProtectedListView.as_view(), name='protected-books'),
    
    # Original URLs
    path('books/', views.list_books, name='book-list'),
    path('libraries/', views.LibraryListView.as_view(), name='library-list'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library-detail'),
    path('library-fn/<int:library_id>/', views.library_detail_function, name='library-detail-fn'),
]