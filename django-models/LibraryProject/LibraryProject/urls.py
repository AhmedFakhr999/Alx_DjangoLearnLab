from django.contrib import admin
from django.urls import path, include
from relationship_app.views import home  # Import the home view

urlpatterns = [
    # Root URL - use function-based view
    path('', home, name='home'),
    
    # Or use the class-based view (uncomment if you want this instead):
    # from relationship_app.views import HomeView
    # path('', HomeView.as_view(), name='home'),
    
    # Admin URL
    path('admin/', admin.site.urls),
    
    # Relationship app URLs
    path('relationship/', include('relationship_app.urls')),
]