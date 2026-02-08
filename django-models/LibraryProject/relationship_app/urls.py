from django.urls import path
from . import views

app_name = 'relationship_app'

urlpatterns = [
    # Authentication URLs using function-based views
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    
    # Protected example URLs
    path('protected/', views.protected_view_example, name='protected'),
    path('protected-books/', views.ProtectedListView.as_view(), name='protected-books'),
    
    # Original URLs
    path('books/', views.list_books, name='book-list'),
    path('libraries/', views.LibraryListView.as_view(), name='library-list'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library-detail'),
    path('library-fn/<int:library_id>/', views.library_detail_function, name='library-detail-fn'),
]